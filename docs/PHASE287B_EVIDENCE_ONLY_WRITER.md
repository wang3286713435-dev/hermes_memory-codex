# Phase 2.87b Evidence-only Writer Service

## 1. Goal

Phase 2.87b introduces a dedicated evidence-only writer service for future test-machine real evidence write smoke.

This phase implements and tests the writer boundary only. It does not wire the writer to API / CLI runtime and does not execute a real DB smoke.

Baseline dependency:

1. Phase 2.87a commit: `fb7baba`
2. Phase 2.87a tag: `phase-2.87a-write-target-discovery-baseline`
3. pushed: true

## 2. Exact Write Targets

The dedicated service writes only through an injected SQLAlchemy session used by tests.

Allowed test-local write targets:

| Purpose | Model | Table |
|---|---|---|
| document shell | `Document` | `documents` |
| document version | `DocumentVersion` | `document_versions` |
| evidence chunk | `Chunk` | `chunks` |
| citation / lineage row | `CitationRecord` | `citations` |

`IngestionJob` is intentionally left out of Phase 2.87b to keep the writer boundary small.

## 3. Service API

Implemented in `app/services/asset_catalog/evidence_writer.py`:

1. `EVIDENCE_WRITE_VERSION`
2. `EvidenceOnlyWriter`
3. `EvidenceWriteDecision`
4. `EvidenceWriteRollbackPlan`
5. `build_evidence_write_result(payload)`

`EvidenceOnlyWriter.write(payload)` may create rows only when every gate passes. It does not call parser, storage, OpenSearch, Qdrant, MinIO, audit logging, NAS, API, CLI, or Agent answer integration.

## 4. Input Gates

The writer fails closed unless all gates pass:

1. supported payload version
2. real evidence write and smoke feature flags enabled in input
3. Agent answer and index write flags disabled
4. operator approval present
5. operator approval permits writes
6. target environment is `test_machine_only`
7. write run id matches approval
8. source asset ref matches approval
9. project scope matches approval
10. permission proof ref matches approval
11. rollback dry-run ref matches approval
12. `max_documents == 1`
13. `max_document_versions == 1`
14. `max_chunks == 20`
15. payload chunk count is `<= 20`
16. chunks include `sanitized_text`
17. idempotency key is present
18. no forbidden raw-field keys are present

Forbidden input keys include raw text, true filenames, NAS paths, source paths, scratch paths, raw rows, secrets, tokens, passwords, and API keys.

## 5. Idempotency Metadata

Run-scoped metadata is persisted under `metadata_json` on `Document`, `DocumentVersion`, and `Chunk`.

Required metadata:

1. `source_system`
2. `source_asset_ref`
3. `project_scope`
4. `permission_proof_ref`
5. `operator_approval_id`
6. `write_run_id`
7. `evidence_write_idempotency_key`
8. `evidence_write_payload_fingerprint`
9. `evidence_write_smoke=true`
10. `agent_answer_eligible=false`
11. `index_write_eligible=false`

No migration is added in this phase.

Duplicate behavior:

1. same idempotency key + same payload fingerprint -> `evidence_write_duplicate`
2. same idempotency key + different payload fingerprint -> `evidence_write_no_go`

## 6. Rollback Dry-run Boundary

`EvidenceOnlyWriter.build_rollback_dry_run(write_run_id)` returns a dry-run plan listing only rows created by that write run.

It lists row ids by:

1. `Document`
2. `DocumentVersion`
3. `Chunk`
4. `CitationRecord`

It does not delete rows and is not executable. It does not mutate NAS, platform DB, OpenSearch, Qdrant, MinIO, audit logs, or unrelated Hermes records.

## 7. Test-only DB / Session Boundary

Phase 2.87b tests use isolated SQLite sessions created by test code.

The writer is not exposed through:

1. API route
2. CLI script
3. background worker
4. upload ingestion path
5. parser path
6. runtime feature flag environment

## 8. Non-targets

Phase 2.87b does not:

1. execute real DB smoke
2. write platform DB
3. write audit logs
4. write OpenSearch
5. write Qdrant
6. write MinIO
7. copy or read files
8. scan NAS
9. execute parser
10. run repair / cleanup / backfill / reindex / delete / migration
11. integrate with Agent final answer
12. enter production rollout

## 9. Validation Results

Validation completed:

1. TDD RED observed for missing `app.services.asset_catalog.evidence_writer`.
2. `UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_writer.py -q` -> `7 passed`.
3. `UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_writer.py` -> passed.
4. `UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q` -> `133 passed`.

Final static validation is still required before any baseline:

1. `git diff --check`
2. latest JSON validation
3. latest ignore check
4. `git status --short`

## 10. Remaining Blockers Before Real Smoke

Real smoke remains blocked until a later phase separately authorizes:

1. Codex B review of Phase 2.87b implementation.
2. selective baseline.
3. test-machine operator approval JSON.
4. runtime smoke plan.
5. explicit decision about whether this service may be called by a smoke-only CLI or runner.
6. proof that runtime execution uses only the approved test machine and tiny scope.

Phase 2.87b implementation alone does not authorize Phase 2.87c or any real write.
