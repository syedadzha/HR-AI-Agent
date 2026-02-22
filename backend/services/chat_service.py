from typing import List, Tuple, AsyncGenerator
from rag import stream_chat_with_doc, chat_with_doc


async def handle_streaming_chat(question: str, history: List[Tuple[str, str]]) -> AsyncGenerator[str, None]:
    """
    Handles a streaming chat request by consuming the sync generator from RAG
    and yielding chunks asynchronously.
    """
    for chunk in stream_chat_with_doc(question, history):
        yield chunk


def handle_blocking_chat(question: str, history: List[Tuple[str, str]]):
    """Handles a blocking chat request."""
    return chat_with_doc(question, history)
