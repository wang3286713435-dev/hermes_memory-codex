# Hermes Memory

Hermes Memory is the built-in memory kernel for the enterprise Hermes AI Agent. It provides the first-stage foundation for document ingestion, parsing, chunking, hybrid retrieval, citation-first answers, version-aware metadata, governance hooks, and memory writeback.

## 1. Scope

This repository implements the Phase 1 engineering skeleton defined in:

- `docs/PRD.md`
- `docs/TECHNICAL_DESIGN.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE_DECISION_RECORD.md`

The current Phase 1 loop focuses on:

1. FastAPI backend service.
2. Configuration management.
3. PostgreSQL metadata models and ingestion state.
4. Document upload and storage.
5. Document parsing for `txt`, `md`, `html`, `pdf`, and `docx`.
6. Structure-aware chunking by heading and paragraph, with length fallback.
7. OpenSearch BM25 chunk indexing.
8. Retrieval API with metadata filters.
9. Citation normalization for downstream agent answers.
10. Built-in memory kernel for agent query routing, retrieval orchestration, context building, citation generation, governance, and writeback.
11. Health check API.
12. Docker Compose with PostgreSQL, Redis, OpenSearch, and MinIO.

## 2. Technology Stack

Final MVP stack:

1. Backend: Python FastAPI.
2. Async tasks: Celery + Redis.
3. Metadata and structured facts: PostgreSQL.
4. Vector store: existing 1024-dimensional vector database.
5. Full-text search: OpenSearch.
6. Object storage: MinIO.
7. OCR: PaddleOCR integration point.
8. Rerank: bge-reranker compatible service integration point.
9. Observability: structured logging, with OpenTelemetry/Prometheus/Grafana/Loki reserved for follow-up.

## 3. Local Setup

Create the environment file:

```bash
cp .env.example .env
```

Start the stack:

```bash
docker compose up --build
```

Health check:

```bash
curl http://localhost:8000/health
```

API docs:

```text
http://localhost:8000/docs
```

## 4. Phase 1 Verification

Create a sample document:

```bash
cat > /tmp/hermes-sample.md <<'EOF'
# 招标资料

## 项目背景

智慧园区项目需要支持统一身份认证、知识检索和权限治理。

## 资质要求

投标方应具备软件开发能力、项目实施经验和信息安全管理能力。
EOF
```

Upload and ingest the document:

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/tmp/hermes-sample.md" \
  -F "title=智慧园区招标资料" \
  -F "source_type=tender" \
  -F "document_type=md"
```

Search indexed chunks:

```bash
curl -X POST "http://localhost:8000/api/v1/retrieval/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "资质要求",
    "top_k": 5,
    "filters": {
      "source_type": "tender"
    },
    "include_citations": true
  }'
```

Expected response contains `results[*].chunk_id`, `document_id`, `version_id`, `source_name`, `heading_path`, `page_start`, `page_end`, and chunk text.

Ask through the built-in Hermes memory kernel:

```bash
curl -X POST "http://localhost:8000/api/v1/agent/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "智慧园区项目有哪些资质要求？",
    "user_id": "u-demo",
    "session_id": "s-demo",
    "filters": {
      "source_type": "tender"
    },
    "citation_required": true
  }'
```

The agent path goes through `app/memory_kernel`, which owns query routing, governance filtering, retrieval orchestration, context building, citation generation, and memory writeback. Retrieval and citation services remain modular dependencies, but they are no longer wired into the agent as external add-ons.

If OpenSearch is unavailable, retrieval falls back to PostgreSQL `ILIKE` search and returns `backend=database_fallback`. Dense vector retrieval is intentionally marked as TODO until the existing 1024-dimensional vector database adapter is connected.

## 5. Development

Install locally:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run syntax checks:

```bash
python -m compileall app
```

Run migrations explicitly when not using `DB_AUTO_CREATE_TABLES=true`:

```bash
alembic upgrade head
```

## 6. Project Layout

```text
app/
  api/          HTTP API routers.
  core/         Settings, logging, application lifecycle.
  db/           Database engine, sessions, base model.
  memory_kernel/Built-in Hermes memory kernel orchestration.
  models/       SQLAlchemy persistence models.
  schemas/      Pydantic request and response schemas.
  services/     Domain services for ingestion, parsing, chunking, retrieval, agent, citation.
  worker/       Celery application and background task entry points.
```

## 7. Current Boundary

This is a minimal runnable Phase 1 knowledge loop. It does not yet implement dense vector retrieval, OCR, production-grade permission filtering, or LLM answer generation. Those are explicit follow-up items.
