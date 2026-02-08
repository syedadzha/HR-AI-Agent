# HR Policy RAG System

A RAG-based application for chatting with HR documents.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI, LangChain
- **Database:** Qdrant (Docker)
- **Embeddings/Chat:** Ollama (Local)

## Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+ (and pnpm)
- [Ollama](https://ollama.com/) installed and running

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
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
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
3. Wait for "Uploading..." to finish (this includes parsing and indexing).
4. Start asking questions in the chat window.
