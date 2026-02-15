---
name: rag-ops
description: RAG pipeline operations. Use for inspecting Qdrant collections, debugging ingestion, and optimizing retrieval parameters.
---

# RAG Operations Specialist

This skill assists with the management and optimization of the RAG (Retrieval-Augmented Generation) pipeline.

## Capabilities

### 1. Inspect Vector Database
Use the bundled script to check the status of your Qdrant collection and peek at indexed documents.

```bash
python skills/rag-ops/rag-ops/scripts/inspect_collection.py
```

### 2. Ingestion Debugging
When files fail to process or retrieval is poor:
- Check `backend/ingest.py` for `chunk_size` and `chunk_overlap`.
- Standard recommendation: Start with 1000/100. If answers are missing context, increase overlap to 200.
- Verify `backend/data/files.json` aligns with Qdrant contents.

### 3. Retrieval Tuning
To improve chat quality:
- Adjust `k` (number of retrieved docs) in `backend/rag.py`.
- Current model: `nomic-embed-text` (via Ollama).
- If irrelevant context is retrieved, consider re-ranking or stricter similarity thresholds.