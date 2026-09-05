# database.py
# SQLite storage for document chunks and their embedding vectors.

import sqlite3
import json

from config import DATABASE_PATH


def get_connection():
    """Open a connection to the SQLite database. Caller is responsible for closing it."""
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    """Create the documents table if it doesn't exist.

    Columns: content (chunk text), embedding (vector, stored as a JSON
    string since SQLite has no array type), source (originating filename,
    used for citations).
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL,
            source TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def clear_documents():
    """Delete all rows from documents (keeps the table). Used by ingest.py to rebuild from scratch each run."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM documents")
    connection.commit()
    connection.close()


def insert_document(content, embedding, source):
    """Insert one chunk with its embedding (list of floats, serialized to JSON) and source file."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO documents (content, embedding, source) VALUES (?, ?, ?)",
        (content, json.dumps(embedding), source),
    )
    connection.commit()
    connection.close()


def get_all_documents():
    """Return every stored chunk as a list of dicts, with embedding deserialized back to a list of floats."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, content, embedding, source FROM documents")
    rows = cursor.fetchall()
    connection.close()

    documents = []
    for row_id, content, embedding_json, source in rows:
        documents.append({
            "id": row_id,
            "content": content,
            "embedding": json.loads(embedding_json),
            "source": source,
        })
    return documents


if __name__ == "__main__":
    # python database.py sets up the database file.
    init_db()
    print(f"Database ready: {DATABASE_PATH}")
