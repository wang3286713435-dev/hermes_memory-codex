# Codex Test-Machine Runtime Evidence Write Smoke Prompt

## Purpose

This prompt is a future Codex C / test-machine handoff for a controlled runtime evidence write smoke.

It is not active authorization. Do not run the writer unless a later user prompt explicitly authorizes execution and provides a valid operator approval JSON path.

## Required Reading

Before doing anything, read:

1. `docs/PHASE287C_RUNTIME_EVIDENCE_WRITE_SMOKE_PLAN.md`
2. `docs/PHASE287D_RUNTIME_EVIDENCE_WRITE_EXECUTION_PACK.md`
3. `docs/PHASE287B_EVIDENCE_ONLY_WRITER.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Hard Boundaries

Do not:

1. run a writer without a later explicit execution authorization
2. write real DB rows
3. wire API / CLI runtime code
4. run parser
5. copy files
6. read raw file content
7. scan NAS
8. write OpenSearch / Qdrant / MinIO
9. write platform DB
10. write audit table outside normal existing retrieval audit behavior
11. enable Agent answer integration
12. run Agent DB / NAS CRUD
13. repair / cleanup / backfill / reindex / delete / migration
14. enter production rollout
15. enable real-write feature flags unless a later execution prompt explicitly instructs it

## Test-Machine Preflight Checklist

1. Confirm machine is non-production Mac mini / test-machine.
2. Confirm git ref:
   - `git rev-parse HEAD`
   - `git tag --points-at HEAD`
3. Confirm worktree:
   - `git status --short`
4. Confirm operator approval JSON path is present in the later execution prompt.
5. Confirm operator approval JSON parses:
   - `UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool "$HERMES_EVIDENCE_WRITE_OPERATOR_APPROVAL" >/dev/null`
6. Confirm approval matches reviewed git ref, test-machine environment, source asset ref, report refs, write_run_id, idempotency key, payload fingerprint, and limits.
7. Confirm all referenced reports are local, sanitized, and ignored.
8. Confirm feature flags match approval and remain default-off unless the later execution prompt explicitly authorizes the two smoke write flags.

Stop if any preflight item fails.

## Required Environment Key Names

The later execution prompt may reference these names only:

```text
DATABASE_URL
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED
PLATFORM_ASSET_INDEX_WRITE_ENABLED
PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED
HERMES_ENV
HERMES_EVIDENCE_WRITE_OPERATOR_APPROVAL
HERMES_EVIDENCE_WRITE_REPORT_DIR
```

Do not paste values into tracked files or chat summaries.

## Allowed Future Smoke Boundary

If a later prompt authorizes execution, the run must be limited to:

- one approved source asset
- one `Document`
- one `DocumentVersion`
- up to 20 `Chunk` rows
- matching `CitationRecord` rows
- one `write_run_id`
- one operator approval id
- one idempotency key
- non-production test machine only

## Stop Before Writer Invocation

Before any writer invocation, explicitly report:

- approval id
- write_run_id
- target git commit
- payload fingerprint
- max document/version/chunk limits
- feature flag state
- rollback dry-run readiness
- idempotency key presence
- clean worktree state

If the later prompt does not explicitly say to proceed after this stop point, stop.

## Sanitized Report Expectations

If a later authorized execution creates a report, it must be ignored local JSON and include:

```json
{
  "report_version": "hermes_evidence_write_smoke_report.v1",
  "write_run_id": "",
  "operator_approval_id": "",
  "target_environment": "test_machine_only",
  "git_commit": "",
  "status": "go|pause|no_go|failed",
  "write_executed": false,
  "created_counts": {
    "documents": 0,
    "document_versions": 0,
    "chunks": 0,
    "citations": 0
  },
  "idempotency_status": "",
  "rollback_dry_run_before": {},
  "rollback_dry_run_after": {},
  "post_write_inspection": {},
  "forbidden_actions": {
    "parser_executed": false,
    "nas_scanned": false,
    "opensearch_written": false,
    "qdrant_written": false,
    "minio_written": false,
    "platform_db_written": false,
    "agent_answer_integration_enabled": false,
    "repair_executed": false,
    "rollout_executed": false
  },
  "sanitized": true
}
```

Never include raw text, true filename, true NAS path, secrets, raw DB rows, or sensitive business values.

## Rollback / Idempotency Expectations

After any later authorized execution:

1. inspect rows only by `write_run_id`
2. run rollback dry-run after write
3. do not delete rows
4. do not repair rows
5. rerun idempotency only if the later prompt explicitly authorizes it
6. confirm duplicate rerun creates zero new rows
7. confirm fingerprint conflict is `No-Go`

## Completion Report Template

Return:

1. API / CLI status if checked
2. git ref / tag
3. approval id
4. write_run_id
5. decision: Go / Pause / No-Go
6. created counts if execution was separately authorized
7. rollback dry-run summary
8. idempotency summary
9. forbidden action flags
10. sanitized report path
11. whether any raw content, true path, DB/index/object-store/platform/audit/Agent answer action occurred

## Current Instruction

For Phase 2.87d, do not execute this prompt. This file is only a future handoff artifact.
