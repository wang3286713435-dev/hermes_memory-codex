# Phase 2 Retrieval Contract

## 1. Scope

Phase 2 starts by stabilizing the enterprise retrieval contract and building the minimal dense + sparse retrieval skeleton.

This phase does not implement rerank, facts joins, OCR, multi-agent workflows, complex permission policy, citation text rendering, or large ingestion refactors.

## 2. Request Contract

Canonical request fields:

- `query`: user query text.
- `route_type`: optional route label produced by Hermes memory kernel routing.
- `retrieval_mode`: `sparse`, `dense`, or `hybrid`.
- `top_k`: maximum returned result count.
- `filters`: metadata filter object.
- `enable_dense`: whether dense retrieval is allowed.
- `enable_sparse`: whether sparse retrieval is allowed.
- `enable_hybrid`: whether hybrid retrieval is allowed.
- `debug`: whether diagnostics should be returned.
- `query_vector`: optional precomputed 1024-dimensional query vector.

## 3. Filter Contract

Supported in Phase 2:

- `source_type`
- `document_id`
- `document_type`
- `is_latest`

Currently reported as unsupported when supplied:

- `project_id`
- `customer_id`
- `confidentiality_level`
- `permission_tags`
- arbitrary `extra` filter fields

Unsupported fields must be returned in `ignored_filters`; they must not be silently dropped.

## 4. Result Contract

Canonical response fields:

- `items` / `results`: normalized retrieval items.
- `backend`: selected backend or fallback backend.
- `retrieval_mode`: effective retrieval mode.
- `dense_status`: `executed`, `skipped`, `unavailable`, `failed`, or `not_executed`.
- `sparse_status`: `executed`, `skipped`, `unavailable`, `failed`, or `not_executed`.
- `citations`: citation payload placeholder for downstream reuse.
- `applied_filters`: supported filters actually applied.
- `ignored_filters`: unsupported filters intentionally not applied.
- `trace`: diagnostics for dense, sparse, hybrid, fallback, and future rerank hook.

Each result may include:

- `retrieval_sources`: e.g. `dense`, `sparse`, `database_fallback`.
- `scores`: per-source score map.

## 5. Dense Adapter Status

Dense retrieval now uses Qdrant as the primary backend through `QdrantDenseRetriever`.
The legacy `/search` HTTP adapter is retained only as a compatibility path when
`VECTOR_STORE_PROVIDER=existing`.

Current behavior:

- Uses `QDRANT_URL`, `QDRANT_COLLECTION`, and `QDRANT_VECTOR_SIZE=1024`.
- Sends `query_vector`, `top_k`, and mapped metadata filters to Qdrant `/points/search`.
- Uses the supplied `query_vector` when present.
- When `query_vector` is absent, uses Aliyun `text-embedding-v3` to generate a 1024-dimensional vector if `ALIYUN_EMBEDDING_API_KEY` is configured.
- Returns `unavailable` when neither `query_vector` nor embedding credentials are available.
- Returns `failed` when Qdrant request or response handling fails.
- Keeps hybrid retrieval fail-open: dense failure does not prevent sparse retrieval.

This is a minimal query-time embedding integration. Batch ingestion, full index
rebuild, and embedding version governance remain outside Phase 2.1-Qdrant.

### 5.1 Qdrant Search Request Contract

The Qdrant adapter sends:

```json
{
  "vector": [0.0],
  "limit": 10,
  "filter": {
    "must": [
      {"key": "source_type", "match": {"value": "upload"}},
      {"key": "document_id", "match": {"value": "doc-id"}},
      {"key": "document_type", "match": {"value": "tender"}},
      {"key": "is_latest", "match": {"value": true}}
    ]
  },
  "with_payload": true,
  "with_vector": false
}
```

The vector must be 1024-dimensional.

### 5.2 Qdrant Point Payload Contract

Each Qdrant point payload should include:

```json
{
  "chunk_id": "chunk-id",
  "document_id": "doc-id",
  "version_id": "version-id",
  "text": "chunk text",
  "source_type": "upload",
  "document_type": "tender",
  "is_latest": true,
  "source_name": "document title",
  "source_uri": "local://document",
  "heading_path": ["Section"],
  "page_start": 1,
  "page_end": 1,
  "metadata": {}
}
```

Adapter normalization rules:

- `chunk_id` may be payload `chunk_id` or Qdrant point `id`.
- `document_id`, `version_id`, `source_type`, heading/page fields may be payload top-level or in `metadata`.
- `text`, `snippet`, or `content` may provide result text.
- results without `chunk_id` are skipped and counted in trace.
- normalized dense results use `retrieval_sources=["dense"]` and `scores={"dense": score}`.

## 6. Sparse / BM25 Status

Sparse retrieval remains OpenSearch BM25 over chunk text.

Phase 2 metadata filters are applied to OpenSearch:

- `source_type`
- `document_id`
- `document_type`
- `is_latest`

If OpenSearch fails, database fallback remains available for development and resilience.

## 7. Hybrid Status

Minimal hybrid retrieval performs:

1. Dense candidate retrieval when enabled.
2. Sparse candidate retrieval when enabled.
3. Deduplication by `chunk_id`.
4. Simple score fusion by summing per-source scores.
5. Trace output showing dense, sparse, and hybrid behavior.

This is intentionally simple and must not be treated as final ranking quality.

Phase 2.1 validation:

- Dense-only path is verified against a local HTTP vector backend test server.
- Hybrid path is verified with real dense HTTP call plus controlled sparse candidates.
- External production vector backend validation remains pending until `VECTOR_STORE_URL` is configured.

Phase 2.1-Qdrant validation:

- Qdrant adapter path is verified against a fake Qdrant-compatible HTTP server.
- Collection creation, point upsert, search request, filter mapping, result normalization, hybrid merge, and fail-open are covered by tests.
- Real local Qdrant container + OpenSearch sparse hybrid is validated on 2026-04-22 when `query_vector` is provided (embedding bypassed).
- Real Aliyun `text-embedding-v3` query embedding is validated on 2026-04-22: 1024-dimensional vectors are returned and the Qdrant dense-only / hybrid retrieval path succeeds without supplying `query_vector`.

## 8. Rerank Hook

Phase 2.2 fixes the internal rerank hook point without integrating a real
reranker model.

Rerank position:

1. dense / sparse retrieval executes.
2. hybrid candidates are merged and deduplicated when `retrieval_mode=hybrid`.
3. internal candidate pool is built.
4. rerank hook executes.
5. final `SearchResponse.results` is produced.

The external retrieval contract remains unchanged:

- no new `retrieval_mode`
- `SearchResponse.results` remains the final downstream result list
- `ContextBuilder` and citation generation consume only final `results`

### 8.1 Internal Candidate Pool

The candidate pool is an internal retrieval service structure. It is not a new
API response object and must not become a context-building input.

Trace fields:

- `dense_returned`: dense candidate count before candidate pool
- `sparse_returned`: sparse candidate count before candidate pool
- `before_dedupe`: candidates before deduplication
- `after_dedupe`: candidates after `chunk_id` deduplication
- `raw_count`: candidates before deduplication
- `deduped_count`: candidates after `chunk_id` deduplication
- `source_counts`: per-source raw candidate counts
- `dedupe_key`: currently `chunk_id` for hybrid
- `score_policy`: `score_sum_by_source` for hybrid, `score_desc` otherwise

### 8.2 Internal Rerank Contract

`RerankRequest`:

- `query`
- `candidates`
- `top_k`
- `retrieval_mode`
- `trace_id`

`RerankOutcome`:

- `results`
- `status`
- `provider`
- `trace`

Phase 2.2 ships only `NoopReranker`:

- provider: `noop`
- status: `skipped`
- behavior: preserve score-descending order
- diagnostics: input/output count, top_k, retrieval_mode, reason
- required trace aliases: `candidate_count_in`, `candidate_count_out`, `elapsed_ms`, `reason_if_skipped`, `fail_open`

All rerank failures must fail open to the candidate pool. In that case
`rerank_status=failed_open`, and final results are selected from the
score-sorted candidate pool.

Real reranker model integration remains outside Phase 2.2.

### 8.3 Phase 2.2 Closeout

Phase 2.2 is considered complete as a preparation stage:

- candidate pool exists internally
- rerank hook position is fixed
- `RerankRequest` / `RerankOutcome` are defined
- `NoopReranker` is diagnostic
- rerank fail-open is implemented
- trace exposes candidate pool and rerank status
- minimum tests and a minimal evaluation entry exist

Phase 2.2 is not a completed rerank capability. Ranking quality is unchanged because no real reranker model is integrated.

The next stage should design and spike one real reranker adapter behind the existing internal contract.

### 8.4 Phase 2.3 Real Reranker Spike Boundary

Phase 2.3 selects Alibaba Cloud Model Studio Text Rerank API as the first real reranker spike route.

The adapter must keep the existing internal contract:

- input: `RerankRequest`
- output: `RerankOutcome`
- public retrieval modes remain `sparse`, `dense`, and `hybrid`
- final downstream result remains `SearchResponse.results`

Initial provider route:

- provider: `aliyun_text_rerank`
- first spike model: `gte-rerank-v2`
- alternative model for comparison: `qwen3-rerank`
- backup route: BGE / lightweight cross-encoder service, documented only

Initial candidate strategy:

- dense target: 20
- sparse target: 20
- hybrid deduped pool: 20 to 40
- rerank input cap: 30
- final top_k: request `top_k`

The real adapter must fail open on missing credentials, timeout, provider errors, invalid response, or empty result.

Phase 2.3 implementation note:

- `AliyunTextReranker` exists but is disabled by default.
- Enablement requires `RERANK_ENABLED=true` and `RERANK_PROVIDER=aliyun`.
- `scores["rerank"]` and `metadata["rerank_score"]` are auxiliary only.
- downstream context and citation layers must not depend on rerank-specific fields.
- fail-open status remains `failed_open`.

## 9. Phase 2.1-gate Real Backend Status

Gate conclusion as of the current environment:

- Real `VECTOR_STORE_URL`: not configured in the current shell or `.env`.
- Displayed backend address: unavailable; no sensitive endpoint is present to redact.
- `VECTOR_STORE_API_KEY`: not configured; whether production backend requires it is unconfirmed.
- Backend filter support: unconfirmed. The adapter passes supported filters, but production backend behavior is not verified.
- `query_vector` requirement: unconfirmed. The adapter sends `query` and optional `query_vector`; production backend support for query-only search is not verified.
- Real `/search` return format: unconfirmed. The normalized contract below is based on the adapter contract and local HTTP backend test, not on a production backend response.

Because no real backend endpoint is configured, dense-only and real hybrid gate validation are not considered complete.

### 9.1 Redacted Request Sample

```json
{
  "query": "投标截止日期",
  "query_vector": null,
  "top_k": 5,
  "filters": {
    "source_type": "upload",
    "document_id": "doc-1",
    "is_latest": true
  },
  "vector_dimension": 1024
}
```

### 9.2 Expected `/search` Response Shape

The adapter accepts either `results` or `items`:

```json
{
  "results": [
    {
      "chunk_id": "chunk-1",
      "score": 0.91,
      "snippet": "命中的 chunk 摘要",
      "metadata": {
        "document_id": "doc-1",
        "version_id": "ver-1",
        "source_type": "upload",
        "heading_path": ["招标文件", "时间要求"]
      }
    }
  ]
}
```

### 9.3 Adapter-normalized Result Sample

```json
{
  "chunk_id": "chunk-1",
  "document_id": "doc-1",
  "version_id": "ver-1",
  "text": "命中的 chunk 摘要",
  "score": 0.91,
  "source_type": "upload",
  "heading_path": ["招标文件", "时间要求"],
  "retrieval_sources": ["dense"],
  "scores": {
    "dense": 0.91
  }
}
```

### 9.4 Main-chain Consumption Compatibility

`context_builder` consumes only the unified `SearchResponse` / `SearchResult` contract:

- `chunk_id`
- `document_id`
- `version_id`
- `text`
- `source_name`
- `heading_path`
- `page_start`
- `page_end`
- `backend`
- `retrieval_mode`
- `dense_status`
- `sparse_status`
- `applied_filters`
- `ignored_filters`

`citation` generation consumes only the unified `SearchResult` contract and does not depend on dense-only or sparse-only private fields.

The memory kernel trace currently exposes:

- `route_type`
- `retrieval_mode`
- `route_reason`
- `backend`
- `dense_retrieval_status`
- `sparse_retrieval_status`
- `applied_filters`
- `ignored_filters`
- `retrieval_trace`
- `context_items`
- `citations`

This is sufficient for Phase 2.1-gate diagnostics, but real backend endpoint, filter behavior, and response shape remain unverified until `VECTOR_STORE_URL` is configured.
