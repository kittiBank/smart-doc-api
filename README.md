# smart-doc-api

Backend API that scans document images / PDFs, classifies and extracts structured data, and lets you ask AI about your documents — using **free local LLMs (Ollama)**, **PostgreSQL + pgvector** and **RAG**.

See [PROJECT_SCOPE.md](PROJECT_SCOPE.md) for scope, phases and status.

## Requirements

- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- Docker (for Postgres + pgvector)
- [Ollama](https://ollama.com) installed natively (uses the Mac GPU)

## Quick start

```bash
# 1. Environment
cp .env.example .env

# 2. Database (Postgres + pgvector)
docker compose up -d

# 3. Local models
ollama pull scb10x/typhoon-ocr1.5-3b
ollama pull qwen3:8b
ollama pull bge-m3

# 4. Install deps & run API
uv sync
uv run fastapi dev app/main.py
```

Open http://localhost:8000/docs

| Endpoint | Purpose |
|---|---|
| `GET /health` | API is up |
| `GET /health/ready` | Postgres + Ollama reachable |
