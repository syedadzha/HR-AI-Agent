import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join("data", "metadata.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initializes the database and creates the file_metadata table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT NOT NULL UNIQUE,
        filename TEXT NOT NULL,
        upload_date TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def add_file_metadata(file_id: str, filename: str, upload_date: str):
    """Adds a new file record to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO file_metadata (file_id, filename, upload_date) VALUES (?, ?, ?)",
            (file_id, filename, upload_date)
        )
        conn.commit()
    finally:
        conn.close()

def get_all_files_metadata() -> List[Dict[str, Any]]:
    """Retrieves all file records from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT file_id, filename, upload_date FROM file_metadata ORDER BY upload_date DESC")
        files = [dict(row) for row in cursor.fetchall()]
        return files
    finally:
        conn.close()

def delete_file_metadata(file_id: str):
    """Deletes a file record from the database by its file_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM file_metadata WHERE file_id = ?", (file_id,))
        conn.commit()
    finally:
        conn.close()
