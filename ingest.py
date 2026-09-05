# ingest.py
# Reads docs/, splits into chunks, embeds each chunk, and saves to SQLite.
#
# Rebuilds the database from scratch on every run so edited or removed
# documents don't leave stale data behind.

from pathlib import Path

from config import CHUNK_OVERLAP, CHUNK_SIZE
from database import clear_documents, init_db, insert_document
from retrieval import get_embedding

DOCS_DIR = Path("docs")


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into ~chunk_size-character chunks along paragraph boundaries.

    Each new chunk is prefixed with the last `overlap` characters of the
    previous one, so context isn't lost at the boundary.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > chunk_size:
            chunks.append(current)
            previous_chunk_tail = current[-overlap:]
            current = previous_chunk_tail + "\n\n" + paragraph
        elif current:
            current = current + "\n\n" + paragraph
        else:
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def main() -> None:
    init_db()
    clear_documents()

    document_files = sorted(DOCS_DIR.glob("*.md"))
    if not document_files:
        print(f"No .md documents found in '{DOCS_DIR}/'.")
        return

    total_chunks = 0
    for file_path in document_files:
        text = file_path.read_text(encoding="utf-8")
        chunks = split_into_chunks(text)
        print(f"{file_path.name}: split into {len(chunks)} chunks")

        for chunk in chunks:
            vector = get_embedding(chunk)
            insert_document(chunk, vector, source=file_path.name)
            total_chunks += 1

    print(f"\nSaved {total_chunks} chunks from {len(document_files)} documents to the database.")


if __name__ == "__main__":
    main()
