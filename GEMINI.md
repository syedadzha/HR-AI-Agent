# Project: HR Policy Assistance (RAG System)

## Overview
A RAG-based application allowing users to upload HR documents (PDF/DOCX), store chunks in Qdrant, and chat with them via a Vue/Nuxt interface.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI (Python), Conda Env: `hr-policy-rag`
- **Vector Database:** Qdrant (Self-hosted via Docker)
- **RAG Framework:** LangChain (preferred)
- **Parsing:** MarkItDown (for PDF/DOCX to Markdown conversion)
- **Embeddings:** [use local ollama]

## Core Requirements
1. **Ingestion:** 
   - Parse documents to Markdown using MarkItDown.
   - **Agentic Chunking:** Initial split (4000 chars, 10% overlap) -> Proposition extraction -> Deduplication -> Semantic grouping (~1200 chars) with titles.
   - Metadata MUST include `file_id`, `filename`, `upload_date`, and `section_title`.
2. **File Management:** - Users must be able to list uploaded files.
   - Deletion must use Qdrant's `delete` method with a filter on `file_id`.
3. **Chat:** - Context-aware retrieval with chat history management.

## Specialized Agents (Skills)
The project now includes specialized skills in `.gemini/skills/`:
- **`rag-ops`**: RAG pipeline operations and Qdrant inspection.
- **`qa-suite`**: Quality Assurance and backend testing.
- **`doc-keeper`**: Documentation maintenance.

## Development & Testing
- **Setup Environment**:
  `conda create -n hr-policy-rag python=3.11 -y; conda activate hr-policy-rag; pip install -r backend/requirements.txt`
- **Backend Tests**: Run via `qa-suite` or manually:
  `$env:PYTHONPATH = "backend"; conda activate hr-policy-rag; pytest backend/tests -v`
- **DB Inspection**: Use `rag-ops` script:
  `python .gemini/skills/rag-ops/scripts/inspect_collection.py`

## Project Structure (Crucial)
This is a monorepo. Please respect this layout:
- `/frontend`: Nuxt 3 application code.
- `/backend`: FastAPI service and RAG logic.
- `/data`: (Local only) temporary storage for uploads before processing.

## Coding Standards
- Use **pnpm** for frontend.
- Use **type hints** in Python.
- Store sensitive keys in `.env` (never hardcode).