"""Build and persist a FAISS index from OpenAgenda events."""

import json
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_FILE = Path("data/events.jsonl")
INDEX_DIR = Path("embeddings/faiss_index")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_events(file_path: Path) -> list[Document]:
    """Load JSONL events and convert them into LangChain Documents."""
    documents = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            title = event.get("title", {}).get("fr", "")
            description = event.get("description", {}).get("fr", "")
            location = event.get("location", {})
            city = location.get("city", {})

            date = event.get("dateRange", {}).get("fr", "")

            timing = event.get("timings", [{}])[0]
            begin = timing.get("begin") or event.get("timings", [{}])[0].get("begin", "")
            end = timing.get("end") or event.get("timings", [{}])[0].get("end", "")

            page_content = (
                f"Title: {title}. Description: {description}. "
                f"Location: {city}. Date: {date}. Start: {begin}, End: {end}."
            )

            metadata = {
                "uid": event.get("uid", ""),
                "begin": begin,
                "end": end,
                "location":  city
            }

            # Uncomment for debugging
            # print(f"Content: {page_content}")
            # print(f"Metadata: {metadata}")
            documents.append(Document(page_content=page_content, metadata=metadata))
    return documents


def build_vector_index(documents: list[Document]):
    """Create and save a FAISS index from a list of Documents."""
    print(f"Building vector index using {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.from_documents(documents, embeddings)
    INDEX_DIR.parent.mkdir(parents=True, exist_ok=True)
    db.save_local(str(INDEX_DIR))
    print(f"FAISS index saved to {INDEX_DIR}")
    return len(documents)

def rebuild_vector_index():
    """Rebuild the index from the JSONL dataset."""
    docs = load_events(DATA_FILE)
    return build_vector_index(docs)

if __name__ == "__main__":
    print("Rebuilding vector index...")
    docs = load_events(DATA_FILE)
    print(f"{len(docs)} documents loaded.")
    build_vector_index(docs)
