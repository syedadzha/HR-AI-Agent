# Project: HR Policy Assistance (RAG System)

## Overview
A RAG-based application allowing users to upload HR documents (PDF/DOCX), store chunks in Qdrant, and chat with them via a Vue/Nuxt interface. The backend features a service-oriented architecture, centralized logging, and API key authentication.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI (Python), Conda Env: `hr-policy-rag`
- **Vector Database:** Qdrant (Self-hosted via Docker)
- **Metadata Store:** SQLite
- **RAG Framework:** LangChain (preferred)
- **Parsing:** MarkItDown (for PDF/DOCX to Markdown conversion)
- **Embeddings:** [use local ollama]

## Backend Architecture
The backend follows a service-oriented architecture to separate concerns:
- **`main.py`:** The main FastAPI application file, responsible for routing, security, and dependency injection. It acts as a thin wrapper around the service layer.
- **`services/`:** Contains the business logic.
    - **`file_service.py`:** Handles the logic for file uploading, processing, and deletion.
    - **`chat_service.py`:** Manages the RAG chat logic, including history processing and retrieval.
- **`database.py`:** Manages the connection and CRUD operations for the SQLite metadata store.
- **`logger_config.py`:** Configures the application-wide logging system.

## Core Requirements
1. **Ingestion:**
   - Parse documents to Markdown using MarkItDown.
   - **Agentic Chunking:** Initial split (4000 chars, 10% overlap) -> Proposition extraction -> Deduplication -> Semantic grouping (~1200 chars) with titles.
   - Metadata (`file_id`, `filename`, `upload_date`, `section_title`) MUST be stored and indexed.
2. **File Management:**
   - Users must be able to list uploaded files. Metadata is stored in a SQLite database.
   - Deletion must remove entries from both the metadata store and the Qdrant vector index, using a filter on `file_id`.
3. **Chat:**
   - Context-aware retrieval with dynamic `top_k` adjustment to prevent context window overflow.
   - Chat history is sanitized to mitigate prompt injection risks.

## Security
- **API Key Authentication:** The `/upload` and `/files/{file_id}` endpoints are protected. A valid API key must be provided in the `X-API-Key` header for all requests to these endpoints.
- **CORS Policy:** The Cross-Origin Resource Sharing (CORS) policy is configured to only allow requests from the specific frontend URL defined in the `backend/.env` file.

## Logging
- A centralized logging system is implemented using Python's `logging` module.
- Logs are configured in `backend/logger_config.py`.
- Logs are sent to both the console and a rotating file located at `logs/backend.log`.
- All `print` and `traceback` calls have been replaced with structured logger calls.

## Specialized Agents (Skills)
The project now includes specialized skills in `.gemini/skills/`:
- **`rag-ops`**: RAG pipeline operations and Qdrant inspection.
- **`qa-suite`**: Quality Assurance and backend testing.
- **`doc-keeper`**: Documentation maintenance.

## Development & Testing
- **Setup Environment**:
  1. Create and activate the Conda environment:
     ```bash
     conda create -n hr-policy-rag python=3.11 -y
     conda activate hr-policy-rag
     ```
  2. Install Python dependencies:
     ```bash
     pip install -r backend/requirements.txt
     ```
  3. Create a `.env` file in the `backend` directory with `SECRET_KEY` and `FRONTEND_URL` values.

## Project Structure (Crucial)
This is a monorepo. Please respect this layout:
- `/frontend`: Nuxt 3 application code.
- `/backend`: FastAPI service and RAG logic.
  - `/services`: Contains business logic (e.g., `file_service.py`, `chat_service.py`).
  - `database.py`: SQLite database management.
  - `logger_config.py`: Logging configuration.
  - `main.py`, `ingest.py`, `rag.py`
- `/data`: (Local only) temporary storage for uploads and the SQLite DB.
- `/logs`: Contains backend log files.

## Coding Standards
- Use **pnpm** for frontend.
- Use **type hints** in Python.
- Store sensitive keys and configuration in `backend/.env` (never hardcode).