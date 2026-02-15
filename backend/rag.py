import os
from typing import List, Tuple
from langchain_ollama import ChatOllama
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from ingest import get_vector_store

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3")

llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=CHAT_MODEL,
    temperature=0
)

def get_rag_chain():
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever()
    
    # 1. Contextualize and Enrich question based on history
    contextualize_q_system_prompt = """You are an HR Search Query Optimizer. Given a chat history and the latest user question, \
    perform the following:
    1. Reformulate the question into a standalone version if it references previous turns.
    2. Enrich the question with relevant HR terminology, keywords, and synonyms (e.g., if the user asks about 'leaving', \
    include terms like 'resignation', 'notice period', 'termination').
    3. Ensure the optimized query is designed to match formal policy documentation and section titles.
    4. Keep the output as a single, concise search-optimized string. Do NOT answer the question."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    
    # 2. Answer question
    qa_system_prompt = """
    
    You are a knowledgeable and approachable HR Specialist. Your goal is to provide clear, accurate guidance to employees based only on the provided policy context.

    Operational Guidelines:

    Conversational Authority: Speak naturally. Instead of "The policy states X," try "You’re eligible for X" or "Our current guidelines for X are..."

    No Meta-References: Never mention "the provided documents," "the context," or "the database." The user should feel they are talking to a person, not a file-reader.

    Structure for Speed: Use bolding for key terms (e.g., 30 days, Manager approval) and bullet points for multi-step processes.

    The "I Don't Know" Protocol: If the context doesn't cover the query, say: "I don't have the specific details on [Topic] in my current records. It’s best to reach out to the HR Operations team directly for clarification."

    Conciseness: Provide the answer in 3 sentences or fewer unless the topic is a complex multi-step process.

    Context:
    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def chat_with_doc(question: str, history: List[Tuple[str, str]]):
    """
    history: List of (role, content) tuples or similar.
    We need to convert them to LangChain Message objects.
    """
    chat_history = []
    for role, content in history:
        if role == "user":
            chat_history.append(HumanMessage(content=content))
        elif role == "assistant":
            chat_history.append(AIMessage(content=content))
            
    chain = get_rag_chain()
    
    response = chain.invoke({"input": question, "chat_history": chat_history})
    return response["answer"]

def stream_chat_with_doc(question: str, history: List[Tuple[str, str]]):
    """
    Generator that yields chunks of the response.
    """
    chat_history = []
    for role, content in history:
        if role == "user":
            chat_history.append(HumanMessage(content=content))
        elif role == "assistant":
            chat_history.append(AIMessage(content=content))
            
    chain = get_rag_chain()
    
    for chunk in chain.stream({"input": question, "chat_history": chat_history}):
        # langchain_core.runnables.base.create_retrieval_chain returns dicts
        # we want the 'answer' part
        if "answer" in chunk:
            yield chunk["answer"]
