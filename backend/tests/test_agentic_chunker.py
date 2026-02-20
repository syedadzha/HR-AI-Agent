from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from ingest import AgenticChunker


def test_agentic_chunker_deduplication():
    # Mock LLM (not used if we mock methods)
    mock_llm = MagicMock()
    chunker = AgenticChunker(mock_llm)

    # Mock the internal methods to avoid chain logic
    def mock_get_propositions(text):
        if "Chunk 1" in text:
            return ["Proposition A", "Proposition B", "Proposition C"]
        else:
            return ["Proposition B", "Proposition C", "Proposition D"]

    chunker._get_propositions = MagicMock(side_effect=mock_get_propositions)
    chunker._get_title = MagicMock(return_value="Summary Title")

    with patch("ingest.RecursiveCharacterTextSplitter") as mock_splitter:
        mock_instance = mock_splitter.return_value
        # Simulate two overlapping chunks from the splitter
        mock_instance.split_documents.return_value = [
            Document(page_content="Chunk 1 content", metadata={"source": "test"}),
            Document(page_content="Chunk 2 content", metadata={"source": "test"}),
        ]

        doc = Document(page_content="Full content", metadata={"source": "test"})
        chunks = chunker.split_documents([doc])

        # Verify deduplication
        assert len(chunks) == 1
        content = chunks[0].page_content
        assert "Proposition A" in content
        assert "Proposition B" in content
        assert "Proposition C" in content
        assert "Proposition D" in content

        # Count occurrences to ensure deduplication worked
        # Since they are joined by spaces, we check for "Proposition B " or similar
        assert content.count("Proposition B") == 1
        assert content.count("Proposition C") == 1

        # Verify metadata preservation
        assert chunks[0].metadata["source"] == "test"
        assert chunks[0].metadata["section_title"] == "Summary Title"


def test_agentic_chunker_grouping():
    mock_llm = MagicMock()
    chunker = AgenticChunker(mock_llm)

    # 10 propositions of 200 chars each = 2000 chars total.
    # Should result in 2 chunks (1200 limit)
    propositions = [f"Proposition {i} " + "x" * 180 for i in range(10)]

    chunker._get_propositions = MagicMock(return_value=propositions)
    chunker._get_title = MagicMock(return_value="Group Title")

    with patch("ingest.RecursiveCharacterTextSplitter") as mock_splitter:
        mock_instance = mock_splitter.return_value
        mock_instance.split_documents.return_value = [
            Document(page_content="Initial Chunk", metadata={})
        ]

        doc = Document(page_content="Full content", metadata={})
        chunks = chunker.split_documents([doc])

        # Each proposition is ~200 chars.
        # 1200 / 200 = 6 props per chunk.
        # 10 props total -> 2 chunks.
        assert len(chunks) == 2
        assert chunks[0].metadata["section_title"] == "Group Title"
        assert chunks[1].metadata["section_title"] == "Group Title"
