import os
import pytest
from unittest.mock import patch, MagicMock
from ingest import process_and_index_file, ensure_collection_exists

@pytest.fixture
def mock_langchain():
    with patch("ingest.UnstructuredLoader") as mock_loader, \
         patch("ingest.RecursiveCharacterTextSplitter") as mock_splitter, \
         patch("ingest.QdrantVectorStore") as mock_qdrant, \
         patch("ingest.client") as mock_client:
        
        # Mock Loader
        mock_doc = MagicMock()
        mock_doc.page_content = "This is a test document content."
        mock_doc.metadata = {}
        mock_loader.return_value.load.return_value = [mock_doc]
        
        # Mock Splitter
        mock_chunk = MagicMock()
        mock_chunk.page_content = "This is a test document content."
        mock_chunk.metadata = {}
        mock_splitter.return_value.split_documents.return_value = [mock_chunk]
        
        # Mock Qdrant Vector Store
        mock_vector_store = MagicMock()
        mock_qdrant.return_value = mock_vector_store
        
        yield {
            "loader": mock_loader,
            "splitter": mock_splitter,
            "qdrant": mock_qdrant,
            "client": mock_client,
            "vector_store": mock_vector_store,
            "chunk": mock_chunk
        }

def test_process_and_index_file_logic(mock_langchain):
    mocks = mock_langchain
    
    file_path = "dummy.pdf"
    filename = "test.pdf"
    
    file_id = process_and_index_file(file_path, filename)
    
    # Check if collection exists check was called
    mocks["client"].collection_exists.assert_called()
    
    # Check if loader was initialized with correct path
    mocks["loader"].assert_called_once_with(file_path)
    
    # Check if chunks got metadata
    assert mocks["chunk"].metadata["file_id"] == file_id
    assert mocks["chunk"].metadata["filename"] == filename
    assert "upload_date" in mocks["chunk"].metadata
    
    # Check if documents were added to vector store
    mocks["vector_store"].add_documents.assert_called_once_with([mocks["chunk"]])
    
    assert isinstance(file_id, str)
    assert len(file_id) > 0

def test_ensure_collection_exists_creation(mock_langchain):
    mocks = mock_langchain
    mocks["client"].collection_exists.return_value = False
    
    ensure_collection_exists()
    
    mocks["client"].create_collection.assert_called_once()

def test_ensure_collection_exists_skips_if_exists(mock_langchain):
    mocks = mock_langchain
    mocks["client"].collection_exists.return_value = True
    
    ensure_collection_exists()
    
    mocks["client"].create_collection.assert_not_called()
