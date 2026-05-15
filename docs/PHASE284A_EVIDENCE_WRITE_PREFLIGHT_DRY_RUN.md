# Phase 2.84a Evidence Write Preflight Dry-run

## Summary

Phase 2.84a implements a local controlled evidence-write preflight evaluator.

The evaluator consumes an ignored local `nas_evidence_write_payload.v0` payload plan plus an explicit operator approval JSON, then emits an ignored local `nas_evidence_write_preflight.v0` report.

This phase still does not write `documents`, write `chunks`, write OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not copy files, run parser, read raw content, scan NAS, or connect Data Steward content to Agent final answers.

## Implemented Scope

1. Added `app.services.asset_catalog.evidence_preflight`.
2. Added `scripts/phase284a_evidence_write_preflight.py`.
3. Added ignored local report directory `reports/nas_evidence_preflight/`.
4. Added tests for ready, not allowed, no-go, approval mismatch, scope cap rejection, sanitized artifact writing, and CLI summary output.

## Preflight Gates

The dry-run report can reach `write_preflight_ready_for_dry_run` only when:

1. Payload version is `nas_evidence_write_payload.v0`.
2. Payload state is `payload_ready_for_write_dry_run`.
3. Payload remains `dry_run=true`.
4. Payload `writes_authorized=false`.
5. Payload safety flags are clear.
6. No forbidden payload keys are present.
7. Candidate document and candidate chunks are present.
8. Chunk count is within the default cap.
9. Citation coverage is complete.
10. Idempotency key can be derived.
11. Rollback plan can be described.
12. Lock strategy is explicit.
13. Operator approval matches the exact payload run id, is unexpired, and stays within tiny approved caps.

## Decision States

1. `write_preflight_not_allowed`
2. `write_preflight_ready_for_dry_run`
3. `write_preflight_no_go`

No decision state authorizes production rollout or actual evidence writes.

## Operator Approval Boundary

Operator approval is treated as a preflight gate only. It is not persisted as production authorization and cannot be reused across payloads.

The evaluator records only sanitized approval facts such as whether the payload run id matched, whether an approval timestamp exists, whether expiry is valid, and the approved caps. It does not store secrets or business notes in the report.

## Safety Boundary

The Phase 2.84a evaluator always outputs:

1. `dry_run=true`
2. `writes_authorized=false`
3. `documents_written=false`
4. `chunks_written=false`
5. `db_writes=false`
6. `opensearch_writes=false`
7. `qdrant_writes=false`
8. `minio_writes=false`
9. `agent_answer_integration=false`
10. `production_rollout=false`

## Still Forbidden

1. Writing `documents`.
2. Writing `chunks`.
3. Writing OpenSearch.
4. Writing Qdrant.
5. Writing MinIO.
6. Writing platform DB or Hermes DB.
7. Running parser.
8. Copying real files.
9. Reading raw file contents.
10. Scanning NAS.
11. Agent DB / NAS CRUD.
12. Agent final answer integration.
13. Treating manifest, eligibility report, payload plan, or preflight report as document evidence.
14. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Validation

Completed:

1. RED: `UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_preflight.py -q` failed because the preflight module and CLI did not exist.
2. GREEN: `UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_preflight.py -q` passed with `7 passed`.

Final validation:

1. `uv run python -m py_compile app/services/asset_catalog/evidence_preflight.py scripts/phase284a_evidence_write_preflight.py`
2. `uv run --extra dev pytest tests/test_data_steward_evidence_write_preflight.py -q`
3. `uv run --extra dev pytest tests/test_data_steward_*.py -q`
4. `git diff --check`
5. JSON and ignore checks for local ignored report files.

Result:

1. py_compile passed.
2. Target preflight tests passed: `7 passed`.
3. Data Steward regression passed: `111 passed`.
4. `git diff --check` passed.
5. `reports/agent_runs/latest.json` and `reports/nas_evidence_preflight/example.json` ignore checks passed.

## Current Conclusion

Phase 2.84a provides the final local dry-run safety gate before any future controlled evidence-write dry-run implementation is considered.

It still does not make NAS content answerable by the Agent.
