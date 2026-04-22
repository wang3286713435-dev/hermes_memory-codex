# Phase 2.2 Closeout and Real Reranker Adapter Preparation

## 1. Closeout Scope

Phase 2.2 closes the rerank preparation stage. It introduces the internal structures required by future real reranker integration, but it does not implement or call a real reranker model.

This closeout covers:

- candidate pool
- rerank hook
- rerank contract
- diagnostic noop reranker
- rerank fail-open
- trace and diagnostics
- minimum tests
- minimum evaluation entry

## 2. Completed Baseline

### 2.1 Candidate Pool

Candidate pool is now an internal retrieval service structure. It is built after dense/sparse retrieval and hybrid merge, before the rerank hook.

Trace includes:

- `dense_returned`
- `sparse_returned`
- `before_dedupe`
- `after_dedupe`
- `raw_count`
- `deduped_count`
- `source_counts`
- `dedupe_key`
- `score_policy`

Candidate pool is not exposed as a new API contract and is not consumed by `ContextBuilder` or citation generation.

### 2.2 Rerank Hook

The rerank hook is fixed at:

1. dense / sparse retrieval
2. hybrid merge and dedupe
3. candidate pool build
4. rerank hook
5. final `SearchResponse.results`

No new retrieval mode was introduced.

### 2.3 Rerank Contract

`RerankRequest` contains:

- `query`
- `candidates`
- `top_k`
- `retrieval_mode`
- `trace_id`

`RerankOutcome` contains:

- `results`
- `status`
- `provider`
- `trace`

### 2.4 Noop Reranker

`NoopReranker` is the only active reranker in Phase 2.2.

It does not call a model and does not improve ranking quality. It preserves score-descending order and returns diagnostics:

- `status=skipped`
- `provider=noop`
- `reason_if_skipped`
- `elapsed_ms`
- `fail_open`
- `candidate_count_in`
- `candidate_count_out`

### 2.5 Fail-open

Rerank failures are fail-open. If the reranker raises an exception, retrieval returns score-descending candidate pool results and records:

- `rerank_status=failed_open`
- `fail_open=true`
- failure reason and error in trace

## 3. What Is Not Complete

Phase 2.2 must not be described as “rerank completed.”

The following are still not implemented:

- real reranker model
- real reranker adapter
- reranker service configuration
- timeout and retry policy against a real model service
- rerank quality evaluation set
- latency and cost validation
- permission-aware rerank governance

## 4. Commit Boundary

Recommended Phase 2.2 closeout commit boundary:

- `app/services/retrieval/rerank.py`
- `app/services/retrieval/service.py`
- `app/services/retrieval/interfaces.py`
- `app/services/evaluation/**`
- `tests/test_rerank_hook.py`
- `docs/PHASE22_RERANK_PREP.md`
- `docs/PHASE22_CLOSEOUT.md`
- `docs/PHASE2_RETRIEVAL_CONTRACT.md`
- `docs/TODO.md`
- `docs/DEV_LOG.md`

Suggested commit:

```text
feat(retrieval): add rerank preparation hook and diagnostics
```

If splitting commits:

```text
feat(retrieval): add candidate pool and rerank hook
test(retrieval): cover noop rerank and fail-open behavior
docs(retrieval): close out phase 2.2 rerank preparation
```

## 5. Real Reranker Adapter Preparation

### 5.1 Why the Next Stage Is Reasonable

The next stage can move into real reranker adapter design because:

- candidate pool provides stable rerank input
- rerank hook position is fixed
- rerank contract is explicit
- fail-open behavior is implemented
- trace exposes candidate counts and rerank status
- final results remain compatible with context and citation layers

The project should not stay on noop indefinitely because noop does not improve ordering quality and cannot validate rerank latency, cost, or ranking benefit.

### 5.2 Integration Boundary

The real reranker must:

- operate only on candidate pool candidates
- return final ranked `SearchResult` items through `RerankOutcome`
- preserve retrieval contract semantics
- fail open on timeout, service error, or invalid response
- avoid changing `ContextBuilder` and citation generation

The real reranker must not:

- introduce a new retrieval mode
- bypass metadata filters
- access facts, OCR, permissions, or agent orchestration internals
- mutate document/chunk storage

### 5.3 Recommended Adapter Contract

Keep the existing internal contract:

- `RerankRequest`
- `RerankOutcome`

Recommended additional trace fields for a real adapter:

- `provider`
- `model`
- `status`
- `elapsed_ms`
- `timeout_ms`
- `fail_open`
- `candidate_count_in`
- `candidate_count_out`
- `reason_if_skipped`
- `error_type`
- `remote_request_id`

Timeout should be short and explicit. Initial recommendation: `1500ms` to `3000ms`, with fail-open on timeout.

### 5.4 Candidate Pool Strategy

Initial recommendation:

- dense candidate target: 20
- sparse candidate target: 20
- hybrid deduped candidate pool: 20 to 40
- rerank input cap: 30
- final top_k: request `top_k`

Reasoning:

- 10 or fewer candidates often leaves rerank with too little room to improve ranking.
- More than 40 candidates increases latency and cost before quality has been measured.
- A 30-candidate cap is a practical first step for enterprise Chinese document retrieval.

The current retrieval service still uses request `top_k` for upstream calls. A future adapter stage may add an internal candidate multiplier without changing public `top_k` semantics.

### 5.5 Reranker Options

Recommended route 1: API reranker service.

- Fastest to integrate.
- Operationally isolated.
- Easier timeout/fail-open handling.
- Good fit for proving ranking benefit before hosting a model.

Recommended route 2: lightweight cross-encoder or BGE reranker service.

- Better control over deployment and data path.
- More predictable for private enterprise data.
- Requires service hosting, monitoring, latency tuning, and model lifecycle work.

Do not implement both routes at the same time. Start with one adapter behind the existing `Reranker` interface.

### 5.6 Minimum Evaluation Before Implementation

Before enabling a real reranker by default, prepare:

- 30 to 50 representative Chinese enterprise queries
- expected relevant `chunk_id` or document references
- coverage across tenders, company documents, and WeChat articles
- baseline results without real rerank
- reranked results with trace

Minimum metrics:

- top-1 hit
- top-3 hit
- top-5 hit
- latency p50 / p95
- fail-open count

This is not a platform. It is a small golden query set for adapter validation.

## 6. Next Step

The next phase should be “real reranker adapter design and spike,” not production rollout.

The first implementation step should define one provider adapter, timeout handling, and evaluation against a small golden query set.
