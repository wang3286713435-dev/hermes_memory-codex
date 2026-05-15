# NEXT_CODEX_A_PROMPT

## Phase 2.87b Evidence-only Writer Service Baseline

Phase 2.87b implementation has been completed.
Codex B review has passed.

The implementation files are:

1. `app/services/asset_catalog/evidence_writer.py`
2. `app/services/asset_catalog/__init__.py`
3. `tests/test_data_steward_evidence_writer.py`
4. `docs/PHASE287B_EVIDENCE_ONLY_WRITER.md`

## Goal

Baseline the Phase 2.87b evidence-only writer implementation.

This prompt does not authorize Phase 2.87c.
This prompt does not authorize any real evidence write.

Do not run writer against real DB.
Do not wire API / CLI runtime.
Do not run parser / copy / DB / index / object-store / Agent answer smoke.

## Review Result

Codex B verified:

1. `EvidenceOnlyWriter` writes only through an injected SQLAlchemy session used by tests.
2. Allowed write targets are limited to `Document`, `DocumentVersion`, `Chunk`, and `CitationRecord`.
3. No API / CLI runtime wiring was added.
4. No parser, file copy, NAS scan, OpenSearch, Qdrant, MinIO, audit log, Agent answer, repair, reindex, or rollout path was added.
5. Gates fail closed for missing approval / flags, over-limit payloads, forbidden raw fields, missing idempotency, and unsafe environment.
6. Idempotency metadata is persisted under `metadata_json`.
7. Duplicate same key / same fingerprint is detected without new rows.
8. Same key / different fingerprint becomes no-go.
9. Rollback dry-run lists only rows associated with the write run and does not delete rows.
10. Tests cover target behavior and Data Steward regression.

## Allowed Files For Baseline

Stage only:

1. `app/services/asset_catalog/evidence_writer.py`
2. `app/services/asset_catalog/__init__.py`
3. `tests/test_data_steward_evidence_writer.py`
4. `docs/PHASE287B_EVIDENCE_ONLY_WRITER.md`
5. `docs/NEXT_CODEX_A_PROMPT.md`
6. `docs/ACTIVE_PHASE.md`
7. `docs/PHASE_BACKLOG.md`
8. `docs/HANDOFF_LOG.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any other tracked or untracked file is dirty, stop and report.

## Validation

Run before baseline:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_writer.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_writer.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

## Commit / Tag

Commit message:

```text
feat: add phase 2.87b evidence-only writer
```

Tag:

```text
phase-2.87b-evidence-only-writer-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. running writer against real DB
2. API / CLI runtime wiring
3. parser execution
4. file copy
5. raw file content read
6. NAS scan
7. platform DB write
8. audit table write
9. OpenSearch / Qdrant / MinIO write
10. Agent answer integration
11. Agent DB / NAS CRUD
12. repair / cleanup / backfill / reindex / delete / migration
13. production rollout
14. enabling real-write feature flags outside tests
15. entering Phase 2.87c without a separate prompt and operator approval planning

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Phase 2.87b remains test-local writer implementation only
7. confirmation that Phase 2.87c remains blocked pending separate authorization
8. confirmation that no real DB / parser / copy / index / object-store / Agent answer action occurred
