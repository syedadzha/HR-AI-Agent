import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add backend directory to path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)
API_KEY = "default-secret-key"
HEADERS = {"X-API-Key": API_KEY}


@pytest.fixture
def mock_db():
    with patch("main.get_all_files_metadata") as mock_get:
        yield mock_get


@pytest.fixture
def mock_file_service():
    with (
        patch("main.handle_upload_file") as mock_upload,
        patch("main.handle_delete_file") as mock_delete,
    ):
        mock_upload.return_value = {
            "file_id": "test-file-id",
            "filename": "test.txt",
            "upload_date": "2023-01-01T00:00:00",
        }
        mock_delete.return_value = None
        yield mock_upload, mock_delete


@pytest.fixture
def mock_chat_service():
    with (
        patch("main.handle_streaming_chat") as mock_stream,
        patch("main.handle_blocking_chat") as mock_blocking,
    ):
        # Mock streaming chat
        async def yield_chunks(q, h):
            yield "This is a "
            yield "mock answer."

        mock_stream.side_effect = yield_chunks
        mock_blocking.return_value = "This is a mock answer."
        yield mock_stream, mock_blocking


def test_list_files_empty(mock_db):
    mock_db.return_value = []
    response = client.get("/files", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == []


def test_list_files_unauthorized():
    response = client.get("/files")
    assert response.status_code == 403


def test_upload_file(mock_file_service):
    mock_upload, _ = mock_file_service

    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/upload", files=files, headers=HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["file_id"] == "test-file-id"
    assert "upload_date" in data

    mock_upload.assert_called_once()


def test_upload_file_unauthorized():
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 403


def test_delete_file(mock_file_service):
    _, mock_delete = mock_file_service

    response = client.delete("/files/test-id", headers=HEADERS)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "File deleted"}

    mock_delete.assert_called_with("test-id")


def test_delete_file_unauthorized():
    response = client.delete("/files/test-id")
    assert response.status_code == 403


def test_chat(mock_chat_service):
    mock_stream, _ = mock_chat_service

    payload = {"question": "Hello?", "history": []}
    response = client.post("/chat", json=payload, headers=HEADERS)

    assert response.status_code == 200
    assert response.text == "This is a mock answer."

    mock_stream.assert_called_once()


def test_chat_blocking(mock_chat_service):
    _, mock_blocking = mock_chat_service

    payload = {"question": "Hello?", "history": []}
    response = client.post("/chat/blocking", json=payload, headers=HEADERS)

    assert response.status_code == 200
    assert response.json() == {"answer": "This is a mock answer."}

    mock_blocking.assert_called_once()


def test_chat_with_history(mock_chat_service):
    mock_stream, _ = mock_chat_service

    payload = {
        "question": "Follow up",
        "history": [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"},
        ],
    }
    response = client.post("/chat", json=payload, headers=HEADERS)

    assert response.status_code == 200
    assert response.text == "This is a mock answer."

    # Verify the history was converted correctly to tuples
    mock_stream.assert_called_with(
        "Follow up", [("user", "Hi"), ("assistant", "Hello")]
    )


def test_chat_unauthorized():
    payload = {"question": "Hello?", "history": []}
    response = client.post("/chat", json=payload)
    assert response.status_code == 403
