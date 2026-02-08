import os
import uuid
from typing import List
from datetime import datetime
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
COLLECTION_NAME = "hr_docs"

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL)
embeddings = OllamaEmbeddings(
    base_url=OLLAMA_BASE_URL,
    model=EMBEDDING_MODEL
)

def get_vector_store():
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

def ensure_collection_exists():
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE), # Adjust size based on model
        )

def process_and_index_file(file_path: str, filename: str) -> str:
    """
    Parses a file, chunks it, and indexes it into Qdrant.
    Returns the file_id.
    """
    ensure_collection_exists()
    
    file_id = str(uuid.uuid4())
    upload_date = datetime.now().isoformat()
    
    # 1. Parse
    loader = UnstructuredLoader(file_path)
    docs = loader.load()
    
    # 2. Chunk
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    
    # 3. Add Metadata
    for chunk in chunks:
        chunk.metadata["file_id"] = file_id
        chunk.metadata["filename"] = filename
        chunk.metadata["upload_date"] = upload_date
        
    # 4. Index
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    
    return file_id

def delete_file_from_index(file_id: str):
    """
    Deletes all vectors associated with a specific file_id.
    """
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.file_id",
                        match=models.MatchValue(value=file_id),
                    )
                ]
            )
        ),
    )
