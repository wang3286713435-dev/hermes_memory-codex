# NEXT_CODEX_A_PROMPT

## Phase 2.86a Temp Evidence Write Rehearsal Review / Baseline Gate

Phase 2.86a temp evidence write rehearsal implementation has been completed.
Codex B review has passed.

The implementation files are:

1. `app/services/asset_catalog/evidence_write_rehearsal.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase286a_temp_evidence_write_rehearsal.py`
4. `tests/test_data_steward_evidence_write_rehearsal.py`
5. `reports/nas_evidence_write_rehearsal/.gitignore`
6. `reports/nas_evidence_write_rehearsal/README.md`
7. `docs/PHASE286A_TEMP_EVIDENCE_WRITE_REHEARSAL.md`
8. phase handoff docs

## Goal

Baseline the Phase 2.86a implementation.

Do not enter Phase 2.87.
Do not execute a real write.
Do not run runtime smoke.

## Required Gate

Git baseline is authorized for the allowlisted Phase 2.86a files only.

Do not stage any other dirty file if one appears.

## Allowed Files For Future Baseline

Stage only:

1. `app/services/asset_catalog/evidence_write_rehearsal.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase286a_temp_evidence_write_rehearsal.py`
4. `tests/test_data_steward_evidence_write_rehearsal.py`
5. `reports/nas_evidence_write_rehearsal/.gitignore`
6. `reports/nas_evidence_write_rehearsal/README.md`
7. `docs/PHASE286A_TEMP_EVIDENCE_WRITE_REHEARSAL.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

## Validation

Run before any baseline:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_rehearsal.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_write_rehearsal.py scripts/phase286a_temp_evidence_write_rehearsal.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_write_rehearsal/example.json
git status --short
```

## Suggested Commit / Tag

Commit message:

```text
feat: add phase 2.86a evidence write rehearsal
```

Tag:

```text
phase-2.86a-evidence-write-rehearsal-baseline
```

## Hard Boundaries

Forbidden:

1. real evidence write
2. write real `documents`, `chunks`, `document_versions`, or audit tables
3. write platform DB or Hermes DB
4. write OpenSearch, Qdrant, or MinIO
5. execute parser
6. copy real files
7. read raw file contents
8. scan NAS
9. Agent DB / NAS CRUD
10. Agent final answer integration
11. treat dry-run / rehearsal artifacts as production evidence
12. repair / cleanup source data / backfill / reindex / delete / migration
13. production rollout
14. enter Phase 2.87 without a separate explicit prompt

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash if baseline executed
4. tag if baseline executed
5. push result if baseline executed
6. confirmation that only temp SQLite / in-memory repository rehearsal was used
7. confirmation that no real DB/index/object-store/parser/file/NAS/Agent answer action occurred
8. whether Phase 2.87 remains blocked pending separate authorization
