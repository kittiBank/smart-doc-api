# smart-doc-api — Project Scope

## Description

A backend API service (no UI yet) that scans document images / PDFs and uses AI to:

- **Read text (OCR)** from Thai and English documents
- **Classify documents** — receipts, income/expense records, appointment cards, government documents, others
- **Extract key data** into structured JSON and store it in a database
- **Answer questions via chat (Ask AI)** — e.g. "What did I spend on the 5th?", "Summarize this document", "Which documents mention vehicle registration renewal?"

**Learning goals:** free local LLMs, structured output, vector DB, RAG, tool calling

---

## Tech Stack

| Area | Tool |
|---|---|
| Language / Packaging | Python 3.12+, uv |
| API Framework | FastAPI |
| Validation / Schema | Pydantic |
| LLM Runtime (local) | Ollama |
| OCR Model | Typhoon OCR (`scb10x/typhoon-ocr1.5-3b`) |
| Chat / Extraction Model | Qwen or Gemma (3B–8B) |
| Embedding Model | bge-m3 |
| Database | PostgreSQL + pgvector |
| ORM / Migrations | SQLAlchemy (or SQLModel) + Alembic |
| PDF → Image | PyMuPDF |
| Thai text (chunking) | PyThaiNLP |
| Infra | Docker + docker-compose |
| Testing | pytest |

---

## Flow Overview

### 1) Document ingestion — `POST /documents`

```
Upload file (image / PDF)
  → Convert PDF pages to images
  → OCR (Typhoon OCR) → markdown text
  → LLM classifies document type
  → LLM extracts fields using the type's schema (validated by Pydantic)
  → Save to Postgres (documents / transactions)
  → Chunk text + create embeddings → store in pgvector
```

### 2) Ask AI — `POST /chat`

```
User question
  → LLM picks a tool (tool calling)
      ├─ query_transactions  → SQL  (amounts / dates / totals)
      ├─ get_document        → fetch by id (summarize a document)
      └─ search_documents    → RAG  (semantic search)
  → LLM writes the answer + cites source documents
```

---

## Phases

Status: ⬜ Not started · 🟨 In progress · ✅ Done

| #   | Phase                   | Details                                                                                    | Status | Notes |
| --- | ----------------------- | ------------------------------------------------------------------------------------------ | ------ | ----- |
| 0   | Setupฬฬฬฬ               | Project structure, uv, FastAPI, docker-compose (Postgres + pgvector), Ollama + pull models | ⬜      |       |
| 1   | Upload & OCR            | `POST /documents` accepts a file → OCR → text                                              | ⬜      |       |
| 2   | Classify & Extract      | Classify type + extract fields by schema → save to DB                                      | ⬜      |       |
| 3   | Query API (SQL)         | Search / filter / sum income & expenses (no LLM yet)                                       | ⬜      |       |
| 4   | RAG                     | Thai chunking → embeddings → vector search + metadata filtering                            | ⬜      |       |
| 5   | Ask AI (Chat)           | `POST /chat` + tool calling (SQL / get doc / RAG) + source citations                       | ⬜      |       |
| 6   | Evaluation              | Test set of 20–30 questions, measure retrieval accuracy (recall@k)                         | ⬜      |       |
| 7   | (Optional) Improvements | Hybrid search, reranker, background jobs, auth                                             | ⬜      |       |

---

## Notes

- Real documents contain personal data (ID numbers, addresses, health info) → use sample files during development and **never push real files to Git** (add them to `.gitignore`).
- Everything runs locally via Ollama → no cost, and data never leaves the machine.
