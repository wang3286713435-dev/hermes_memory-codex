# NEXT_CODEX_A_PROMPT

## Phase 2.84a Evidence Write Preflight Dry-run Baseline Task

Phase 2.84a local evidence-write preflight dry-run implementation is complete and Codex B review is ready for selective baseline.

Do not enter Phase 2.85. Do not implement actual evidence writes.

## Summary

New implementation:

1. `app/services/asset_catalog/evidence_preflight.py`
2. `scripts/phase284a_evidence_write_preflight.py`
3. `tests/test_data_steward_evidence_write_preflight.py`
4. `reports/nas_evidence_preflight/.gitignore`
5. `reports/nas_evidence_preflight/README.md`
6. `docs/PHASE284A_EVIDENCE_WRITE_PREFLIGHT_DRY_RUN.md`

The implementation consumes an ignored local `nas_evidence_write_payload.v0` payload plan and an explicit operator approval JSON, then emits an ignored local `nas_evidence_write_preflight.v0` report.

Key boundary:

1. `write_preflight_ready_for_dry_run` is not write authorization.
2. Preflight report is not document evidence.
3. No `documents` / `chunks` writes occur.
4. No OpenSearch / Qdrant / MinIO writes occur.
5. No parser, copy, NAS scan, DB write, or Agent final answer integration occurs.

## Allowed Stage Files

Only stage these files:

1. `app/services/asset_catalog/evidence_preflight.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase284a_evidence_write_preflight.py`
4. `tests/test_data_steward_evidence_write_preflight.py`
5. `reports/nas_evidence_preflight/.gitignore`
6. `reports/nas_evidence_preflight/README.md`
7. `docs/PHASE284A_EVIDENCE_WRITE_PREFLIGHT_DRY_RUN.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage any real manifest, eligibility, payload, preflight, parser preview, scratch, DB, NAS, or Agent answer artifact.

## Validation Commands

Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_preflight.py scripts/phase284a_evidence_write_preflight.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_preflight.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_preflight/example.json
```

Expected:

1. Target preflight tests pass.
2. Data Steward regression passes.
3. `reports/agent_runs/latest.json` remains ignored.
4. Real preflight JSON outputs remain ignored.

## Hard Boundaries

Forbidden:

1. Actual evidence write.
2. Write `documents` or `chunks`.
3. Write platform DB or Hermes DB.
4. Write OpenSearch, Qdrant, or MinIO.
5. Execute parser.
6. Copy real files.
7. Read raw file contents.
8. Scan NAS.
9. Agent DB / NAS CRUD.
10. Agent final answer integration.
11. Treat manifest, eligibility report, payload plan, or preflight report as document evidence.
12. Repair / cleanup source data / backfill / reindex / delete / migration.
13. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `chore: add phase 2.84a evidence write preflight dry-run`
5. Tag:
   - `phase-2.84a-evidence-write-preflight-dry-run-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter Phase 2.85.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed Phase 2.84a files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No manifest / eligibility / payload / preflight artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
