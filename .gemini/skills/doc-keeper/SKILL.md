---
name: doc-keeper
description: Documentation maintainer. Use for updating GEMINI.md, generating API docs, and ensuring project structure matches documentation.
---

# Documentation Keeper

This skill is responsible for maintaining the project's knowledge base, primarily `GEMINI.md`.

## Capabilities

### 1. Sync GEMINI.md
Whenever a new feature is added or a tech stack choice is changed, update `GEMINI.md`.
- **Project Structure**: Update the file tree representation if files are moved/added.
- **Tech Stack**: Update version numbers or library choices.
- **Core Requirements**: Mark completed requirements or add new constraints.

### 2. API Documentation
Ensure `backend/main.py` routes are reflected in any API docs or `GEMINI.md` descriptions.
- Check `backend/ingest.py` for new parameters.
- Check `backend/rag.py` for logic changes.

### 3. Setup Verification
Ensure `README.md` or `GEMINI.md` contains correct setup instructions:
- Python environment (`conda` or `venv`).
- Frontend dependencies (`pnpm install`).
- Environment variables (`.env.example`).