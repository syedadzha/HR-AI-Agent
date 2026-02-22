import os
import logging
from dotenv import load_dotenv
from typing import Annotated

from fastapi import Depends, FastAPI, File, HTTPException, Security, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from database import get_all_files_metadata, initialize_db
from logger_config import setup_logging
from services.chat_service import handle_blocking_chat, handle_streaming_chat
from services.file_service import handle_delete_file, handle_upload_file

# --- Setup ---
setup_logging()
logger = logging.getLogger("hr_policy_rag")
load_dotenv()

app = FastAPI(title="HR Policy RAG")

# --- CORS ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database ---
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
initialize_db()

# --- Security ---
API_KEY = os.getenv("SECRET_KEY", "default-secret-key")
if API_KEY == "your_secret_key_here" or API_KEY == "default-secret-key":
    logger.warning(
        "Using default or placeholder secret key. "
        "Please set a strong SECRET_KEY in your .env file."
    )

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Could not validate credentials"
        )
    return api_key

# --- Pydantic Models ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    history: list[ChatMessage] = []

class FileRecord(BaseModel):
    file_id: str
    filename: str
    upload_date: str

# --- API Endpoints ---
@app.post("/upload", response_model=FileRecord, dependencies=[Depends(get_api_key)])
async def upload_file(file: Annotated[UploadFile, File()]):
    logger.info(f"Received file upload request for: {file.filename}")
    try:
        record = handle_upload_file(file)
        logger.info(
            f"Successfully processed and indexed file: {file.filename} "
            f"with file_id: {record['file_id']}"
        )
        return record
    except Exception as e:
        logger.exception(
            f"Error processing upload for file: {file.filename}", 
            exc_info=e
        )
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/files", response_model=list[FileRecord], dependencies=[Depends(get_api_key)])
async def list_files():
    logger.info("Received request to list files.")
    return get_all_files_metadata()

@app.delete("/files/{file_id}", dependencies=[Depends(get_api_key)])
async def delete_file(file_id: str):
    logger.info(f"Received request to delete file: {file_id}")
    try:
        handle_delete_file(file_id)
        logger.info(f"Successfully deleted file: {file_id}")
        return {"status": "success", "message": "File deleted"}
    except Exception as e:
        logger.exception(f"Error deleting file: {file_id}", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/chat", dependencies=[Depends(get_api_key)])
async def chat(request: ChatRequest) -> StreamingResponse:
    logger.info("Received request for streaming chat.")
    try:
        history_tuples = [(msg.role, msg.content) for msg in request.history]
        return StreamingResponse(
            handle_streaming_chat(request.question, history_tuples),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    except Exception as e:
        logger.exception("Error during streaming chat.", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/chat/blocking", dependencies=[Depends(get_api_key)])
async def chat_blocking(request: ChatRequest) -> dict[str, str]:
    logger.info("Received request for blocking chat.")
    try:
        history_tuples = [(msg.role, msg.content) for msg in request.history]
        answer = handle_blocking_chat(request.question, history_tuples)
        return {"answer": answer}
    except Exception as e:
        logger.exception("Error during blocking chat.", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    logger.info("Starting HR Policy RAG backend server.")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
