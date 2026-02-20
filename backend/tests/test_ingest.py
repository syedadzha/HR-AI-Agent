from unittest.mock import MagicMock, patch

import pytest

from ingest import ensure_collection_exists, process_and_index_file


@pytest.fixture
def mock_langchain():
    with (
        patch("ingest.MarkItDown") as mock_markitdown,
        patch("ingest.AgenticChunker") as mock_chunker,
        patch("ingest.QdrantVectorStore") as mock_qdrant,
        patch("ingest.client") as mock_client,
    ):
        # Mock MarkItDown
        mock_result = MagicMock()
        mock_result.text_content = "This is a test document content."
        mock_markitdown.return_value.convert.return_value = mock_result

        # Mock Chunker
        mock_chunk = MagicMock()
        mock_chunk.page_content = "This is a test document content."
        mock_chunk.metadata = {}
        mock_chunker.return_value.split_documents.return_value = [mock_chunk]

        # Mock Qdrant Vector Store
        mock_vector_store = MagicMock()
        mock_qdrant.return_value = mock_vector_store

        yield {
            "markitdown": mock_markitdown,
            "chunker": mock_chunker,
            "qdrant": mock_qdrant,
            "client": mock_client,
            "vector_store": mock_vector_store,
            "chunk": mock_chunk,
        }


def test_process_and_index_file_logic(mock_langchain):
    mocks = mock_langchain

    file_path = "dummy.pdf"
    filename = "test.pdf"

    file_id = process_and_index_file(file_path, filename)

    # Check if collection exists check was called
    mocks["client"].collection_exists.assert_called()

    # Check if MarkItDown was used
    mocks["markitdown"].return_value.convert.assert_called_once_with(file_path)

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
