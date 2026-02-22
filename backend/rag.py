import os
import re
from typing import Any, Generator, List

from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

from ingest import get_vector_store

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3")

llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=CHAT_MODEL, temperature=0)


def _estimate_tokens(text: str) -> int:
    """A very rough approximation of token count."""
    return len(text) // 4


def sanitize_chat_history(history: List[BaseMessage]) -> List[BaseMessage]:
    """
    Sanitizes chat history to remove potential prompt injection instructions.
    """
    sanitized_history = []
    # This regex looks for common instruction-like keywords at the start of a line.
    instruction_pattern = re.compile(
        r"^\s*(ignore|disregard|forget|override|instead|system|instruction:).*",
        re.IGNORECASE | re.MULTILINE,
    )

    for message in history:
        if isinstance(message.content, str):
            sanitized_content = instruction_pattern.sub("", message.content).strip()
            # If sanitization results in an empty message, skip it.
            if not sanitized_content:
                continue

            if isinstance(message, HumanMessage):
                sanitized_history.append(HumanMessage(content=sanitized_content))
            elif isinstance(message, AIMessage):
                sanitized_history.append(AIMessage(content=sanitized_content))
            else:
                sanitized_history.append(message)  # Keep other message types
        else:
            sanitized_history.append(message)

    return sanitized_history


def get_rag_chain(k_value: int = 4) -> Runnable:
    """Creates the RAG chain with a configurable 'k' for the retriever."""
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k_value})

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
    qa_system_prompt = """You are a knowledgeable and approachable HR Specialist. Your goal is to provide clear, accurate guidance to employees based only on the provided policy context.

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


def _prepare_chat_inputs(history: list[tuple[str, str]]):
    """
    Sanitizes history, estimates token count, and determines 'k' for retrieval.
    """
    chat_history: list[BaseMessage] = []
    for role, content in history:
        if role == "user":
            chat_history.append(HumanMessage(content=content))
        elif role == "assistant":
            chat_history.append(AIMessage(content=content))

    sanitized_history = sanitize_chat_history(chat_history)
    history_text = " ".join(
        [str(msg.content) for msg in sanitized_history]
    )
    history_tokens = _estimate_tokens(history_text)

    # Agentic chunks are ~1800 chars (~450 tokens). Context window is ~8k.
    # Reserve ~4k for answer/prompt, leaving ~4k for history+docs.
    k = 2 if history_tokens > 2000 else 4
    return sanitized_history, k


def chat_with_doc(question: str, history: list[tuple[str, str]]) -> str:
    """
    Handles a blocking chat request with dynamic 'k' adjustment.
    """
    sanitized_history, k = _prepare_chat_inputs(history)
    chain = get_rag_chain(k_value=k)
    response = chain.invoke({"input": question, "chat_history": sanitized_history})
    return str(response.get("answer", "I could not find an answer."))


def stream_chat_with_doc(
    question: str, history: list[tuple[str, str]]
) -> Generator[str, None, None]:
    """
    Handles a streaming chat request with dynamic 'k' adjustment.
    """
    sanitized_history, k = _prepare_chat_inputs(history)
    chain = get_rag_chain(k_value=k)
    for chunk in chain.stream({"input": question, "chat_history": sanitized_history}):
        if "answer" in chunk:
            yield str(chunk["answer"])
