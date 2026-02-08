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
    
    # 1. Contextualize question based on history
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    
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
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Respond in Markdown format. Use bullet points, bold text, or tables if they help make the information clearer.
    Keep the answer concise (maximum 4-5 sentences unless detail is required).

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
