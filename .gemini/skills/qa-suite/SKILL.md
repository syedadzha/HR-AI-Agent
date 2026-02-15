---
name: qa-suite
description: Quality Assurance suite. Use for running backend tests, checking API endpoints, and verifying system stability.
---

# QA Suite

This skill ensures the stability and quality of the HR Policy RAG system.

## Capabilities

### 1. Run Backend Tests
Execute the pytest suite for the FastAPI backend.
```powershell
./skills/qa-suite/qa-suite/scripts/run_backend_tests.ps1
```

### 2. API Verification
- Check `backend/main.py` for endpoint definitions.
- Use `curl` or similar to manually test endpoints if tests fail.
- Key endpoints:
  - `POST /upload`: Upload PDF/DOCX.
  - `POST /chat`: RAG chat interface.
  - `GET /files`: List uploaded documents.

### 3. Frontend Testing (Manual)
- Currently, automated frontend tests are not configured.
- Verify `frontend/components/ChatInterface.vue` loads correctly.
- Ensure file uploads trigger the backend endpoint.