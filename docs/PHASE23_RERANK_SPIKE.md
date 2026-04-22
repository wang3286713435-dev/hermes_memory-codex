# Phase 2.3 Real Reranker Adapter Design and Spike

## 1. Scope

Phase 2.3 starts the real reranker adapter spike. It does not enable a production reranker by default.

This phase focuses on one provider route only:

- primary route: Alibaba Cloud Model Studio Text Rerank API
- backup route: BGE / lightweight cross-encoder service, documented only

This phase does not implement facts joins, OCR, multi-agent workflows, complex permission policy, retrieval mode expansion, large ingestion changes, or an evaluation platform.

## 2. Provider Decision

The first real reranker spike should use Alibaba Cloud Model Studio Text Rerank API.

Reasons:

- API integration fits the current `RerankRequest` / `RerankOutcome` boundary.
- It avoids local model serving work during the spike.
- It supports text rerank models such as `qwen3-rerank` and `gte-rerank-v2`.
- The API returns original document indexes and relevance scores, which can be mapped back to existing `SearchResult` objects.
- Timeout and fail-open behavior can be enforced at adapter level.

BGE / cross-encoder remains a backup route because it requires model hosting, deployment monitoring, latency tuning, and model lifecycle management.

## 3. Adapter Boundary

The real reranker adapter must operate only on candidate pool candidates.

It must not:

- change public `retrieval_mode`
- bypass metadata filters
- mutate `SearchResult` contract semantics
- expose candidate pool as a new API contract
- require `ContextBuilder` or citation generation to understand reranker internals

It must:

- accept `RerankRequest`
- return `RerankOutcome`
- fail open on timeout, API error, invalid response, or missing credentials
- preserve original candidates when fail-open occurs
- record diagnostic trace

## 4. Alibaba Text Rerank Adapter Design

### 4.1 Configuration

Recommended configuration keys:

- `RERANK_PROVIDER=aliyun`
- `RERANK_ENABLED=false` by default during spike
- `ALIYUN_RERANK_API_KEY`
- `ALIYUN_RERANK_BASE_URL=https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`
- `ALIYUN_RERANK_MODEL=gte-rerank-v2` for the first spike
- `ALIYUN_RERANK_TIMEOUT_MS=2500`
- `RERANK_INPUT_CAP=30`

API key policy:

- `ALIYUN_RERANK_API_KEY` is preferred when configured.
- If `ALIYUN_RERANK_API_KEY` is empty, rerank falls back to `ALIYUN_EMBEDDING_API_KEY`.
- If both are empty, the adapter returns `failed_open`.

This allows embedding and rerank to share the same Alibaba Cloud Model Studio key by default while preserving future separate-key configuration.

`qwen3-rerank` is also viable, but `gte-rerank-v2` has a larger documented document count limit and a stable text-only request shape. Model choice should be validated with the golden query set before default enablement.

### 4.2 Input Mapping

`RerankRequest.query` maps to provider `query`.

Each `SearchResult` candidate maps to one provider document string.

Recommended document string format:

```text
标题: {source_name}
路径: {heading_path}
正文: {text}
```

Rules:

- truncate each document text before sending if needed
- preserve the original candidate index
- do not send internal metadata unless needed for text relevance
- do not include permission tags or confidential metadata in the reranker input

### 4.3 Provider Request Shape

For `gte-rerank-v2`:

```json
{
  "model": "gte-rerank-v2",
  "input": {
    "query": "用户问题",
    "documents": ["候选文档 1", "候选文档 2"]
  },
  "parameters": {
    "top_n": 10,
    "return_documents": false
  }
}
```

### 4.4 Output Mapping

Provider response results contain:

- original document `index`
- `relevance_score`

Adapter mapping:

- find original `SearchResult` by index
- set or update `scores["rerank"]`
- optionally set `metadata["rerank_score"]`
- sort by provider result order
- return `RerankOutcome.results`

If the provider returns fewer than requested results, append remaining original candidates by previous score order only if the spike requires stable output count. Initial recommendation: return provider top_n only, where `top_n=request.top_k`.

### 4.5 Timeout, Retry, and Fail-open

Initial policy:

- timeout: 2500 ms
- retry: 0 during spike
- fail-open: required

Fail-open cases:

- missing API key
- HTTP timeout
- non-2xx response
- malformed response
- invalid result index
- empty provider result

On fail-open, return score-descending candidate pool top_k and record:

- `status=failed_open`
- `fail_open=true`
- `provider=aliyun_text_rerank`
- `model`
- `elapsed_ms`
- `timeout_ms`
- `error_type`
- `remote_request_id` if present

## 5. Candidate Pool Strategy

Phase 2.3 fixes the initial rerank candidate strategy:

- dense target: 20
- sparse target: 20
- hybrid deduped candidate pool target: 20 to 40
- rerank input cap: 30
- final top_k: public request `top_k`

Implementation note:

The public `top_k` remains final result count. A future implementation may internally expand dense/sparse retrieval to collect enough candidates for rerank, but it must not change public `top_k` semantics.

Trace should include:

- `candidate_strategy.dense_target`
- `candidate_strategy.sparse_target`
- `candidate_strategy.rerank_input_cap`
- `candidate_strategy.final_top_k`
- `candidate_strategy.applied_input_count`

No dense/sparse fusion algorithm change is planned in this phase.

## 6. Golden Query Set

Minimum golden query set:

- 30 to 50 Chinese enterprise queries
- each query includes expected `chunk_id`, `document_id`, or expected key object
- include tenders, company documents, and WeChat articles

Recommended file path:

```text
eval/golden_queries/rerank_phase23.yaml
```

Recommended record shape:

```yaml
- id: rq-001
  query: "某项目的投标截止日期是什么？"
  expected:
    document_id: "doc-id"
    chunk_ids: ["chunk-id"]
    key_terms: ["投标截止日期"]
  tags: ["tender", "date"]
```

This is not an evaluation platform. It is a replayable baseline for the spike.

## 7. Spike Validation

Baseline:

- current retrieval pipeline with `NoopReranker`

Experiment:

- same retrieval pipeline with Alibaba Text Rerank adapter enabled

Minimum metrics:

- top-1 hit
- top-3 hit
- top-5 hit
- latency p50
- latency p95
- fail-open count

Proceed criteria:

- top-3 or top-5 hit rate improves on the golden set
- p95 latency remains acceptable for pre-model retrieval
- fail-open behavior is verified
- no regression in citation/context consumption

Do not enable production default based on ad hoc manual examples.

## 8. Current Blockers

The following must be confirmed before implementation is considered validated:

- `ALIYUN_RERANK_API_KEY`
- selected model: `gte-rerank-v2` or `qwen3-rerank`
- outbound network access to DashScope endpoint
- golden query file with expected references
- timeout budget accepted by Hermes main request path

## 9. Real API Gate Status

Latest smoke test status:

- `ALIYUN_RERANK_API_KEY`: not configured
- `ALIYUN_EMBEDDING_API_KEY`: configured in the active Hermes_memory environment
- provider: `aliyun_text_rerank`
- model: `gte-rerank-v2`
- raw base URL: `https://dashscope.aliyuncs.com`
- final request URL: `https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`
- outcome: `executed`
- `api_key_source`: `ALIYUN_EMBEDDING_API_KEY`
- HTTP status: `200`
- provider request id: observed in response headers/body
- response parsing: successful

The smoke test confirms that rerank correctly falls back to `ALIYUN_EMBEDDING_API_KEY`.
The request now completes a successful provider round-trip and the response can be parsed into ranked `SearchResult` objects.

## 10. Spike Baseline vs Experiment

Current spike uses the local gate dataset:

- Qdrant collection: `hermes_gate_chunks`
- OpenSearch index: `hermes_gate_chunks_os`
- golden query file: `eval/golden_queries/rerank_phase23.yaml`
- query count: `6`

This is a real but very small dataset. Metrics are for spike reference only and must not be treated as production-quality evidence.

Baseline (`NoopReranker`):

- top-1 hit: `0.8333`
- top-3 hit: `1.0`
- top-5 hit: `1.0`
- latency avg: `0.003 ms`
- latency p50: `0.004 ms`
- latency p95: `0.005 ms`
- fail-open count: `0`

Experiment (`AliyunTextReranker`, `gte-rerank-v2`):

- top-1 hit: `1.0`
- top-3 hit: `1.0`
- top-5 hit: `1.0`
- latency avg: `336.148 ms`
- latency p50: `343.035 ms`
- latency p95: `389.847 ms`
- fail-open count: `0`

Observed change:

- query `Qdrant dense hit B` improved from baseline top-1 miss to experiment top-1 hit
- other cases remained top-1 stable

Interpretation:

- rerank shows initial usefulness on the tiny gate dataset
- latency impact is visible and must be re-checked on a larger enterprise query set
- current sample size is too small for rollout decisions

## 11. Implementation Status

Phase 2.3 minimal adapter implementation is now present in code.

Implemented:

- `AliyunTextReranker`
- default model `gte-rerank-v2`
- `ALIYUN_RERANK_API_KEY` priority with `ALIYUN_EMBEDDING_API_KEY` fallback
- centralized document text mapping
- request mapping to Alibaba Text Rerank API
- result index mapping back to `SearchResult`
- auxiliary `scores["rerank"]`
- auxiliary `metadata["rerank_score"]`
- `failed_open` behavior for missing key, timeout, provider error, invalid response, empty result, and exception
- golden query file at `eval/golden_queries/rerank_phase23.yaml`
- minimal spike summary helper

The adapter is not enabled by default. It is selected only when:

```text
RERANK_ENABLED=true
RERANK_PROVIDER=aliyun
```

Real API validation is completed for the current Phase 2.3 gate path:

- `ALIYUN_EMBEDDING_API_KEY` fallback works for rerank
- DashScope endpoint round-trip succeeds
- `gte-rerank-v2` returns HTTP `200`
- response can be parsed into ranked `SearchResult` items

`rerank_score` is auxiliary only. Downstream context and citation logic must continue to depend on final `SearchResponse.results`, not on rerank-specific metadata.

## 12. Phase 2.3b Expanded Sample Validation

This round expands the previous 6 gate samples to a 48-query small evaluation set.

Evaluation corpus:

- Qdrant collection: `hermes_phase23_eval_qdrant`
- OpenSearch index: `hermes_phase23_eval_os`
- golden query file: `eval/golden_queries/rerank_phase23.yaml`
- query count: `48`

Corpus source:

- de-identified, near-real enterprise snippets
- compiled from tender material, company qualification handbook, WeChat articles, HR policy, contract clause, project delivery report, and proposal text
- still not a production-scale enterprise knowledge corpus

Baseline (`NoopReranker`):

- top-1 hit: `0.9583`
- top-3 hit: `1.0`
- top-5 hit: `1.0`
- latency avg: `0.002 ms`
- latency p50: `0.002 ms`
- latency p95: `0.004 ms`
- fail-open count: `0`

Experiment (`AliyunTextReranker`, `gte-rerank-v2`):

- top-1 hit: `1.0`
- top-3 hit: `1.0`
- top-5 hit: `1.0`
- latency avg: `358.34 ms`
- latency p50: `353.478 ms`
- latency p95: `458.05 ms`
- fail-open count: `0`

Observed change:

- top-1 improved on `2` queries
- no top-1 regression observed in the current 48-query set
- main improvements appear on ambiguous qualification-style queries

Representative improvements:

- `rq-004` `智慧园区项目有哪些资质要求？`
- `rq-006` `园区项目要求 ISO9001 吗？`

Interpretation:

- reranker benefit is more stable than the original 6-query gate sample
- current gain is visible but concentrated on a subset of ambiguous queries
- latency remains materially higher than noop and must be considered in any rollout strategy
- the result is strong enough to justify entering default-enable policy evaluation
- it is still not enough to enable rerank by default without a larger real-enterprise evaluation set
