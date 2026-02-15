# HR Policy RAG System

A RAG-based application for chatting with HR documents, featuring advanced parsing and agentic chunking.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI, LangChain, **MarkItDown**
- **Database:** Qdrant (Docker)
- **Embeddings/Chat:** Ollama (Local)

## Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+ (and pnpm)
- [Ollama](https://ollama.com/) installed and running

## Advanced Pipeline Features
This system implements a sophisticated ingestion pipeline:
1.  **Parsing:** Uses Microsoft's **MarkItDown** for robust conversion of various file types (PDF, DOCX, etc.) to high-quality Markdown.
2.  **Initial Chunking:** Large-scale splitting (4000 characters) with a 10% overlap to preserve context across boundaries.
3.  **Agentic Extraction:** Uses an LLM to decompose text into standalone, factual propositions.
4.  **Deduplication:** Automatically removes redundant propositions caused by chunk overlaps.
5.  **Semantic Grouping:** Groups propositions into coherent chunks (~1200 characters) with LLM-generated titles for better retrieval accuracy.

## Setup Instructions

### 1. Database (Qdrant)
Start the vector database:
```bash
docker-compose up -d
```

### 2. Ollama Models
Ensure you have the embedding and chat models pulled:
```bash
ollama pull nomic-embed-text
ollama pull llama3
```
*Note: If you want to use different models, update `backend/.env`.*

### 3. Backend
Navigate to `backend` folder:
```bash
cd backend
# Create environment from yml
conda env create -f environment.yml
# Activate
conda activate hr-policy-rag

python main.py
```
Backend will run at `http://localhost:8000`.

### 4. Frontend
Navigate to `frontend` folder (in a new terminal):
```bash
cd frontend
pnpm install
pnpm dev
```
Frontend will run at `http://localhost:3000`.

## Usage
1. Open `http://localhost:3000`.
2. Upload PDF or DOCX files via the sidebar.
3. Wait for "Uploading..." to finish (this includes MarkItDown parsing and Agentic Chunking).
4. Start asking questions in the chat window.

## Testing
Run the backend test suite:
```bash
$env:PYTHONPATH = "backend"
pytest backend/tests -v
```