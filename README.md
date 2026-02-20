# HR Policy RAG System

A RAG-based application for chatting with HR documents, featuring advanced parsing and agentic chunking.

## Tech Stack
- **Frontend:** Nuxt 3, Tailwind CSS, Pinia
- **Backend:** FastAPI, LangChain, **MarkItDown**
- **Database:** Qdrant (Docker)
- **Embeddings/Chat:** Ollama (Local)

## Prerequisites
- Docker & Docker Compose
- **Python 3.11**
- Node.js 18+ (and pnpm)
- [Ollama](https://ollama.com/) (Optional, if not using Docker for Ollama)

## Setup Instructions

### 1. Database & Models (Docker)
The `docker-compose.yml` file is configured to start both Qdrant and Ollama, and it will automatically pull the required models (`llama3` and `nomic-embed-text`) on startup.

```bash
docker-compose up -d
```
*Note: The initial pull might take a few minutes depending on your internet speed.*

### 2. Backend
Navigate to the `backend` folder and set up your environment.

**Option A: Using Conda (Recommended)**
```bash
cd backend
conda env create -f environment.yml
conda activate hr-policy-rag
```

**Option B: Using Pip**
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file from the example:
```bash
cp .env.example .env
```
*(On Windows PowerShell: `copy .env.example .env`)*

#### Run Backend
```bash
python main.py
```
Backend will run at `http://localhost:8000`.

### 3. Frontend
Navigate to `frontend` folder (in a new terminal):
```bash
cd frontend
pnpm install
pnpm dev
```
Frontend will run at `http://localhost:3000`.

## Code Quality & Formatting

To maintain high standards and consistency, we use a specialized toolset for both the frontend and backend.

### **Frontend (Nuxt 3)**
We use **ESLint** (v10 Flat Config) for code analysis, **Prettier** for formatting, and **Tailwind CSS Linter** to enforce utility class ordering.

- **Check for issues:**
  ```bash
  cd frontend
  pnpm lint
  ```
- **Auto-fix issues:**
  ```bash
  pnpm lint:fix
  ```
- **Format code:**
  ```bash
  pnpm format
  ```

### **Backend (FastAPI)**
We use **Ruff** for lightning-fast linting and formatting, and **MyPy** for strict static type checking.

- **Lint and Auto-fix:**
  ```bash
  cd backend
  conda activate hr-policy-rag
  ruff check . --fix
  ```
- **Format code:**
  ```bash
  ruff format .
  ```
- **Type Check:**
  ```bash
  mypy . --config-file pyproject.toml
  ```

### **Automated Pre-commit Hooks**
We use **Husky** and **lint-staged**. On every `git commit`, the system automatically:
1. Lints and formats changed frontend files.
2. Lints, formats, and checks types for changed backend files.
*The commit will fail if errors are found, ensuring the codebase stays clean.*

## Testing
Run the backend test suite:

**PowerShell (Windows):**
```powershell
$env:PYTHONPATH = "backend"; pytest backend/tests -v
```

**Bash (Linux/macOS):**
```bash
PYTHONPATH=backend pytest backend/tests -v
```