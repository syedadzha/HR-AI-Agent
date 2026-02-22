import os
import shutil
from datetime import datetime

from fastapi import UploadFile

from database import add_file_metadata, delete_file_metadata
from ingest import delete_file_from_index, process_and_index_file

DATA_DIR = "data"


def handle_upload_file(file: UploadFile) -> dict:
    """
    Saves, processes, and indexes an uploaded file, then cleans up.
    Returns the metadata record of the new file.
    """
    file_location = os.path.join(DATA_DIR, str(file.filename))

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process and Index
        file_id = process_and_index_file(file_location, str(file.filename))

        # Create record (matches FileRecord Pydantic model)
        record = {
            "file_id": file_id,
            "filename": str(file.filename),
            "upload_date": datetime.now().isoformat(),
        }

        # Save metadata to DB
        add_file_metadata(
            file_id=record["file_id"],
            filename=record["filename"],
            upload_date=record["upload_date"],
        )

        return record
    finally:
        # Cleanup local file
        if os.path.exists(file_location):
            os.remove(file_location)


def handle_delete_file(file_id: str):
    """
    Deletes a file from the vector index and the metadata database.
    """
    # First, delete from vector index
    delete_file_from_index(file_id)

    # Then, delete from metadata database
    delete_file_metadata(file_id)
