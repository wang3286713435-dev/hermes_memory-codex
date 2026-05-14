# NEXT_CODEX_A_PROMPT

## Phase 2.82a Git Baseline Task

Phase 2.82a evidence-write eligibility dry-run implementation is complete and ready for selective baseline after validation.

This baseline must only capture the local eligibility evaluator dry-run. Do not enter future evidence-write payload generation, parser execution, DB/index write, or Agent answer integration.

## Summary

Implemented:

1. `app/services/asset_catalog/evidence_eligibility.py`
2. `scripts/phase282a_evidence_write_eligibility.py`
3. `tests/test_data_steward_evidence_write_eligibility.py`
4. `reports/nas_evidence_eligibility/.gitignore`
5. `reports/nas_evidence_eligibility/README.md`
6. `docs/PHASE282A_EVIDENCE_WRITE_ELIGIBILITY_DRY_RUN.md`

Key boundary:

1. Eligibility report is a dry-run review artifact.
2. `eligible_for_evidence_write_planning` does not authorize writes.
3. Missing permission proof defaults to `DENIED`.
4. Human review approval only approves a later planning phase.
5. Phase 2.82a does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.

## Allowed Stage Files

Only stage these files:

1. `app/services/asset_catalog/evidence_eligibility.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase282a_evidence_write_eligibility.py`
4. `tests/test_data_steward_evidence_write_eligibility.py`
5. `reports/nas_evidence_eligibility/.gitignore`
6. `reports/nas_evidence_eligibility/README.md`
7. `docs/PHASE282A_EVIDENCE_WRITE_ELIGIBILITY_DRY_RUN.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage real manifest or real eligibility report artifacts.

## Validation Commands

Run:

```bash
uv run python -m py_compile app/services/asset_catalog/evidence_eligibility.py scripts/phase282a_evidence_write_eligibility.py
uv run --extra dev pytest tests/test_data_steward_evidence_write_eligibility.py -q
uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_eligibility/example.json
```

## Hard Boundaries

Forbidden:

1. Generate future evidence-write payloads.
2. Write `documents` or `chunks`.
3. Write platform DB or Hermes DB.
4. Write OpenSearch, Qdrant, or MinIO.
5. Execute parser.
6. Copy real files.
7. Read raw file contents.
8. Scan NAS.
9. Agent DB / NAS CRUD.
10. Agent final answer integration.
11. Treat manifest or eligibility report as document evidence.
12. Repair / cleanup source data / backfill / reindex / delete / migration.
13. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `chore: add phase 2.82a evidence eligibility dry-run`
5. Tag:
   - `phase-2.82a-evidence-eligibility-dry-run-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter next phase.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No real manifest / eligibility report artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
