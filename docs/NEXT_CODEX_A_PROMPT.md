# NEXT_CODEX_A_PROMPT

## Phase 2.83a Git Baseline Task

Phase 2.83a evidence-write payload dry-run implementation is complete and ready for selective baseline after validation.

This baseline must only capture the local payload dry-run builder. Do not enter controlled evidence write preflight, actual `documents/chunks` writes, parser execution, DB/index write, or Agent answer integration.

## Summary

Implemented:

1. `app/services/asset_catalog/evidence_payload.py`
2. `scripts/phase283a_evidence_write_payload.py`
3. `tests/test_data_steward_evidence_write_payload.py`
4. `reports/nas_evidence_payloads/.gitignore`
5. `reports/nas_evidence_payloads/README.md`
6. `docs/PHASE283A_EVIDENCE_WRITE_PAYLOAD_DRY_RUN.md`

Key boundary:

1. Payload plan is a dry-run artifact.
2. `payload_ready_for_write_dry_run` does not authorize writes.
3. Candidate document / chunk records do not include raw extracted text.
4. Payload plan is not document evidence and cannot be used in Agent final answers.
5. Phase 2.83a does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.

## Allowed Stage Files

Only stage these files:

1. `app/services/asset_catalog/evidence_payload.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase283a_evidence_write_payload.py`
4. `tests/test_data_steward_evidence_write_payload.py`
5. `reports/nas_evidence_payloads/.gitignore`
6. `reports/nas_evidence_payloads/README.md`
7. `docs/PHASE283A_EVIDENCE_WRITE_PAYLOAD_DRY_RUN.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage real manifest, eligibility, or payload artifacts.

## Validation Commands

Run:

```bash
uv run python -m py_compile app/services/asset_catalog/evidence_payload.py scripts/phase283a_evidence_write_payload.py
uv run --extra dev pytest tests/test_data_steward_evidence_write_payload.py -q
uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_payloads/example.json
```

## Hard Boundaries

Forbidden:

1. Execute controlled evidence write preflight.
2. Write `documents` or `chunks`.
3. Write platform DB or Hermes DB.
4. Write OpenSearch, Qdrant, or MinIO.
5. Execute parser.
6. Copy real files.
7. Read raw file contents.
8. Scan NAS.
9. Agent DB / NAS CRUD.
10. Agent final answer integration.
11. Treat manifest, eligibility report, or payload plan as document evidence.
12. Repair / cleanup source data / backfill / reindex / delete / migration.
13. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `chore: add phase 2.83a evidence payload dry-run`
5. Tag:
   - `phase-2.83a-evidence-payload-dry-run-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter next phase.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No real manifest / eligibility / payload artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
