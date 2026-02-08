# Project: HR Policy Assistance (RAG System)

## Overview
A RAG-based application allowing users to upload HR documents (PDF/DOCX), store chunks in Qdrant, and chat with them via a Vue/Nuxt interface.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI (Python), Conda Env: `hr-policy-rag`
- **Vector Database:** Qdrant (Self-hosted via Docker)
- **RAG Framework:** LangChain (preferred)
- **Parsing:** Unstructured.io (handles PDF and Word best)
- **Embeddings:** [use local ollama]

## Core Requirements
1. **Ingestion:** - Parse documents into chunks (~1000 tokens, 10% overlap).
   - Metadata MUST include `file_id`, `filename`, and `upload_date`.
2. **File Management:** - Users must be able to list uploaded files.
   - Deletion must use Qdrant's `delete` method with a filter on `file_id`.
3. **Chat:** - Context-aware retrieval with chat history management.

## Project Structure (Crucial)
This is a monorepo. Please respect this layout:
- `/frontend`: Nuxt 3 application code.
- `/backend`: FastAPI service and RAG logic.
- `/data`: (Local only) temporary storage for uploads before processing.

## Coding Standards
- Use **pnpm** for frontend.
- Use **type hints** in Python.
- Store sensitive keys in `.env` (never hardcode).