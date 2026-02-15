import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys

# Add backend directory to path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

@pytest.fixture
def mock_metadata():
    with patch("main.get_files_metadata") as mock_get, \
         patch("main.save_files_metadata") as mock_save:
        mock_get.return_value = []
        mock_save.return_value = None
        yield mock_get, mock_save

@pytest.fixture
def mock_ingest():
    with patch("main.process_and_index_file") as mock_process, \
         patch("main.delete_file_from_index") as mock_delete:
        mock_process.return_value = "test-file-id"
        mock_delete.return_value = None
        yield mock_process, mock_delete

@pytest.fixture
def mock_rag():
    with patch("main.stream_chat_with_doc") as mock_stream:
        # Mock stream_chat_with_doc to yield a few chunks
        def yield_chunks(q, h):
            yield "This is a "
            yield "mock answer."
        mock_stream.side_effect = yield_chunks
        yield mock_stream

def test_list_files_empty(mock_metadata):
    mock_get, _ = mock_metadata
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_file(mock_metadata, mock_ingest):
    mock_get, mock_save = mock_metadata
    mock_process, _ = mock_ingest
    
    # Mock shutil.copyfileobj and open to avoid writing to disk
    with patch("builtins.open", new_callable=MagicMock), \
         patch("shutil.copyfileobj"), \
         patch("os.remove"):
        
        files = {'file': ('test.txt', b"test content", 'text/plain')}
        response = client.post("/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["file_id"] == "test-file-id"
        assert "upload_date" in data
        
        mock_process.assert_called_once()
        mock_save.assert_called_once()

def test_delete_file(mock_metadata, mock_ingest):
    mock_get, mock_save = mock_metadata
    mock_process, mock_delete = mock_ingest
    
    # Setup initial state
    mock_get.return_value = [{"file_id": "test-id", "filename": "test.txt", "upload_date": "2023-01-01"}]
    
    response = client.delete("/files/test-id")
    
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "File deleted"}
    
    mock_delete.assert_called_with("test-id")
    # Verify save was called with empty list (since we filtered out the file)
    mock_save.assert_called_with([])

def test_chat(mock_rag):
    mock_stream = mock_rag
    
    payload = {
        "question": "Hello?",
        "history": []
    }
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    # StreamingResponse content is in response.text or response.content
    assert response.text == "This is a mock answer."
    
    mock_stream.assert_called_once()

def test_chat_with_history(mock_rag):
    mock_stream = mock_rag
    
    payload = {
        "question": "Follow up",
        "history": [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]
    }
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    assert response.text == "This is a mock answer."
    
    # Verify the history was converted correctly to tuples
    mock_stream.assert_called_with("Follow up", [("user", "Hi"), ("assistant", "Hello")])
