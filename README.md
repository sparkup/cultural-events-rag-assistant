# Cultural Events RAG Assistant

> A practical Retrieval-Augmented Generation (RAG) assistant that answers questions about cultural events using OpenAgenda data, FAISS, and Mistral.

## Project Overview

This project builds a small RAG system that fetches public cultural events from the OpenAgenda API, embeds them into a FAISS index, and exposes a FastAPI endpoint for natural-language queries. It is designed as a reproducible, containerized demo that you can run locally.

## What This Project Is / Is Not

**This project is:**
- A working RAG pipeline built on real public event data
- A reference implementation using LangChain, FAISS, and Mistral
- A local demo API with `/ask` and `/rebuild` endpoints

**This project is not:**
- A production-ready or privacy-audited system
- A real-time event platform (data is snapshot-based)
- A recommendation engine with user profiles or personalization

## Tech Stack

- **LangChain** for RAG orchestration
- **Mistral AI** (API) for LLM responses
- **FAISS** for vector search
- **FastAPI** for the REST API
- **Sentence Transformers** for embeddings
- **Docker** for local execution

## Repository Structure

```
api/                # FastAPI app
scripts/            # Data ingestion + index build
embeddings/         # FAISS index output (generated)
data/               # Event JSONL (generated)
tests/              # API and retrieval checks
Dockerfile          # Local dev image
docker-compose.yaml # Docker orchestration
install.sh          # Helper to build/run the container
```

## Setup

### 1. Create your environment file

Copy the example and add your API keys:

```bash
cp .env.example .env
```

Required variables:

```
MISTRAL_API_KEY=your_mistral_key_here
OPENAGENDA_API_KEY=your_openagenda_key_here
```

### 2. Build the vector index

```bash
python scripts/ingest.py
python scripts/rebuild_index.py
```

This downloads events, writes `data/events.jsonl`, and creates a FAISS index in `embeddings/faiss_index`.

### 3. Run the API with Docker

```bash
docker compose up --build
```

Or use the helper script:

```bash
./install.sh
```

API docs will be available at:

```
http://localhost:8000/docs
```

## API Endpoints

- `POST /ask` - Query the RAG system
- `POST /rebuild` - Rebuild the FAISS index

Example request:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What events are happening in Lyon this week?"}'
```

## Testing

Run the lightweight checks:

```bash
python tests/api_test.py
python tests/evaluate_rag.py
```

## Notes and Limitations

- The OpenAgenda data can be in French depending on the source.
- The evaluation script performs keyword checks, not full semantic scoring.
- The FAISS index is generated locally and should not be committed.

## License

MIT License
