import json
import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ingest import delete_file_from_index, process_and_index_file
from rag import chat_with_doc, stream_chat_with_doc

app = FastAPI(title="HR Policy RAG")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
FILES_METADATA_PATH = os.path.join(DATA_DIR, "files.json")

# Ensure data dir exists
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(FILES_METADATA_PATH):
    with open(FILES_METADATA_PATH, "w") as f:
        json.dump([], f)


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


def get_files_metadata() -> list[dict[str, str]]:
    with open(FILES_METADATA_PATH) as f:
        try:
            return json.load(f)  # type: ignore
        except json.JSONDecodeError:
            return []


def save_files_metadata(metadata: list[dict[str, str]]) -> None:
    with open(FILES_METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


@app.post("/upload", response_model=FileRecord)
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    file_location = os.path.join(DATA_DIR, str(file.filename))

    # Save locally
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process and Index
        file_id = process_and_index_file(file_location, str(file.filename))

        # Update metadata
        record = {
            "file_id": file_id,
            "filename": str(file.filename),
            "upload_date": "",  # Set in ingest, but we need it here.
            # Refactor ingest to return record or just grab date here.
        }
        # Actually ingest returns file_id only. Let's fix date here.
        from datetime import datetime

        record["upload_date"] = datetime.now().isoformat()

        metadata = get_files_metadata()
        metadata.append(record)
        save_files_metadata(metadata)

        # Cleanup local file (optional, requirement says "Temporary storage")
        # I'll keep it for now as "Data" folder usually implies persistence in these simple apps,
        # but the prompt says "temporary storage for uploads before processing".
        os.remove(file_location)

        return record
    except Exception as e:
        import traceback

        traceback.print_exc()
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/files", response_model=list[FileRecord])
async def list_files() -> list[dict[str, str]]:
    return get_files_metadata()


@app.delete("/files/{file_id}")
async def delete_file(file_id: str) -> dict[str, str]:
    try:
        delete_file_from_index(file_id)

        metadata = get_files_metadata()
        metadata = [f for f in metadata if f["file_id"] != file_id]
        save_files_metadata(metadata)

        return {"status": "success", "message": "File deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    try:
        # Convert Pydantic models to tuples
        history_tuples = [(msg.role, msg.content) for msg in request.history]

        return StreamingResponse(
            stream_chat_with_doc(request.question, history_tuples),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/chat/blocking")
async def chat_blocking(request: ChatRequest) -> dict[str, str]:
    try:
        # Convert Pydantic models to tuples
        history_tuples = [(msg.role, msg.content) for msg in request.history]
        answer = chat_with_doc(request.question, history_tuples)
        return {"answer": answer}
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
