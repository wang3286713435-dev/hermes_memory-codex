# Phase 2.91 Runtime Evidence Writer Smoke Gate

## Status

- Phase: 2.91
- Scope: runtime evidence writer smoke gate implementation
- Previous baseline: `3ee37e3`, tag `phase-2.90-test-machine-preflight-readiness-baseline`
- Current decision: implementation complete locally; stop for Codex B review before any baseline or real test-machine writer smoke.

## Goal

Phase 2.91 adds a controlled runtime evidence writer smoke gate between:

1. Phase 2.88 runtime preflight report.
2. Phase 2.87b `EvidenceOnlyWriter`.
3. A future separately authorized Mac mini / test-machine one-run writer smoke.

Default behavior is gate-only. It validates the operator approval, preflight report, sanitized payload, git/worktree state, scope limits, feature flags, idempotency, forbidden raw fields, and side-effect flags, then writes a sanitized smoke report.

It does not call `EvidenceOnlyWriter.write()` unless a caller explicitly passes `execute_writer=True` with an injected test-local SQLAlchemy session.

## Implemented Files

- `app/services/asset_catalog/evidence_write_runtime_smoke.py`
- `scripts/phase291_runtime_evidence_write_smoke.py`
- `tests/test_data_steward_evidence_write_runtime_smoke.py`

## Decision States

The smoke gate returns:

- `writer_smoke_ready_for_operator_stop`: all checks passed, writer not invoked, no DB writes.
- `writer_smoke_executed`: writer invoked only through injected test-local/temp DB session.
- `writer_smoke_pause`: missing input, dirty worktree, missing flags, missing approval/payload/preflight, or execution requested without injected test session.
- `writer_smoke_no_go`: non-ready preflight, scope violation, forbidden feature flag, approval mismatch, forbidden raw field, or forbidden side effect.

## CLI

Default CLI mode is gate-only:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase291_runtime_evidence_write_smoke.py \
  --approval-json <local_ignored_operator_approval_json> \
  --preflight-report <local_ignored_preflight_report_json> \
  --payload-json <local_ignored_sanitized_payload_json> \
  --output <local_ignored_writer_smoke_report_json> \
  --expected-git-commit <commit_from_approval> \
  --worktree-status-file <local_ignored_worktree_status_file>
```

`--execute-writer` is accepted by the CLI but intentionally pauses because the CLI has no injected DB session. Execution is only supported by service-level tests or a later separately authorized runner that provides a reviewed test-machine session.

## Report Boundary

Report version:

```text
hermes_runtime_evidence_writer_smoke.v0
```

The report includes only sanitized control fields:

- decision
- write run id
- operator approval id
- target environment
- git/preflight state
- writer invocation flags
- created counts
- idempotency status
- rollback dry-run before/after
- forbidden action flags
- pause/no-go reasons

The report must not include raw text, true filename, true NAS path, raw DB row, source payload business values, secrets, or unredacted absolute local paths.

## Validation

Fresh validation completed:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_evidence_write_runtime_smoke.py -q
# 12 passed

UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile \
  app/services/asset_catalog/evidence_write_runtime_smoke.py \
  scripts/phase291_runtime_evidence_write_smoke.py
# passed

UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest \
  tests/test_data_steward_evidence_writer.py \
  tests/test_data_steward_evidence_write_runtime_preflight.py \
  tests/test_data_steward_evidence_write_runtime_smoke.py \
  -q
# 29 passed
```

Pending before baseline:

1. `git diff --check`
2. latest JSON validation
3. latest ignore check
4. Codex B review

## Non-Authorization

Phase 2.91 still does not authorize:

1. real developer DB or Mac mini DB writer invocation
2. parser execution
3. scratch copy
4. raw file content read
5. NAS scan
6. OpenSearch / Qdrant / MinIO writes
7. platform DB writes
8. Agent answer integration
9. repair / cleanup / backfill / reindex / delete / migration
10. rollout

Future real writer smoke requires a separate prompt, operator approval, clean reviewed checkout, and Codex B review.
