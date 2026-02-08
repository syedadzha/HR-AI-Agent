import os
import pytest
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings, ChatOllama
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3")

def test_qdrant_connectivity():
    """Test if Qdrant is reachable."""
    client = QdrantClient(url=QDRANT_URL)
    try:
        collections = client.get_collections()
        assert collections is not None
    except Exception as e:
        pytest.fail(f"Failed to connect to Qdrant: {e}")

def test_ollama_embeddings():
    """Test if Ollama embeddings are working."""
    embeddings = OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=EMBEDDING_MODEL
    )
    try:
        vector = embeddings.embed_query("This is a test.")
        assert len(vector) > 0
        assert isinstance(vector[0], float)
    except Exception as e:
        pytest.fail(f"Failed to get embeddings from Ollama: {e}")

def test_ollama_chat():
    """Test if Ollama chat model is working."""
    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=CHAT_MODEL,
        temperature=0
    )
    try:
        response = llm.invoke("Say 'ready'")
        assert "ready" in response.content.lower()
    except Exception as e:
        pytest.fail(f"Failed to get response from Ollama chat: {e}")

def test_qdrant_collection_lifecycle():
    """Test creating, checking, and deleting a test collection in Qdrant."""
    client = QdrantClient(url=QDRANT_URL)
    test_collection = "test_connectivity_collection"
    
    # Cleanup if exists
    if client.collection_exists(test_collection):
        client.delete_collection(test_collection)
        
    # Create
    from qdrant_client.http import models
    client.create_collection(
        collection_name=test_collection,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    
    assert client.collection_exists(test_collection)
    
    # Delete
    client.delete_collection(test_collection)
    assert not client.collection_exists(test_collection)
