# Code Review Checklist

## Security
- [ ] **Secrets:** Are there any hardcoded API keys, tokens, or passwords?
- [ ] **Input Validation:** Are all external inputs (API params, file uploads) properly validated (e.g., Pydantic models)?
- [ ] **Injection:** Is there any risk of SQL, command, or prompt injection?
- [ ] **Authentication:** Are sensitive endpoints protected by `X-API-Key` or proper auth headers?
- [ ] **CORS:** Is the CORS policy restrictive and correct?

## RAG & Vector Search (Specific)
- [ ] **Metadata:** Does the ingestion process store necessary metadata (file_id, filename, section_title)?
- [ ] **Retrieval:** Is `top_k` dynamically adjusted to avoid context window overflow?
- [ ] **Sanitization:** Is chat history sanitized before being sent to the LLM?
- [ ] **Chunking:** Does the chunking logic match the agentic chunking requirements?

## Python (FastAPI)
- [ ] **Types:** Are all function signatures fully typed with Python type hints?
- [ ] **Logging:** Are `print` and `traceback` calls replaced with structured logger calls (`logger_config.py`)?
- [ ] **Dependencies:** Is dependency injection used for database connections and services?
- [ ] **Error Handling:** Are exceptions caught and logged with appropriate context?
- [ ] **Models:** Are Pydantic models used for all request and response schemas?

## Frontend (Nuxt 3)
- [ ] **Composition API:** Does it use `<script setup>` and the Composition API?
- [ ] **State Management:** Are Pinia stores used for global state (auth, file list, chat)?
- [ ] **Tailwind:** Are Tailwind CSS classes used consistently for styling?
- [ ] **Types:** Are TypeScript types and interfaces used for all props and data?
- [ ] **API Calls:** Are `$fetch` or `useFetch` used correctly with error handling?

## General Quality
- [ ] **Readability:** Is the code easy to read and follow?
- [ ] **DRY:** Is there any significant code duplication that should be refactored?
- [ ] **Performance:** Are there any obvious performance bottlenecks (e.g., N+1 queries)?
- [ ] **Tests:** Are there unit or integration tests covering the new logic?
- [ ] **Documentation:** Are complex logic blocks explained with clear comments?
