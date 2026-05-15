# NEXT_CODEX_A_PROMPT

## Phase 2.85a Selective Baseline Gate

Phase 2.85a Local Evidence Write Dry-run Runner implementation is complete pending review.

Only perform a selective Git baseline if Codex B / user approves this prompt.

Do not enter Phase 2.86. Do not perform real evidence writes.

## Allowed Stage Files

Only stage:

1. `app/services/asset_catalog/evidence_write_dry_run.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase285a_evidence_write_dry_run.py`
4. `tests/test_data_steward_evidence_write_dry_run.py`
5. `reports/nas_evidence_write_dry_run/.gitignore`
6. `reports/nas_evidence_write_dry_run/README.md`
7. `docs/PHASE285A_EVIDENCE_WRITE_DRY_RUN.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage real write-dry-run reports.

## Validation Commands

Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_write_dry_run.py scripts/phase285a_evidence_write_dry_run.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_dry_run.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_write_dry_run/example.json
git status --short
```

## Commit / Tag

Commit message:

```text
chore: add phase 2.85a evidence write dry-run runner
```

Tag:

```text
phase-2.85a-evidence-write-dry-run-baseline
```

Push `origin/main` and tag.

## Hard Boundaries

Forbidden:

1. real evidence write
2. write `documents` or `chunks`
3. write platform DB or Hermes DB
4. write OpenSearch, Qdrant, or MinIO
5. execute parser
6. copy real files
7. read raw file contents
8. scan NAS
9. Agent DB / NAS CRUD
10. Agent final answer integration
11. treat dry-run report as production evidence
12. repair / cleanup source data / backfill / reindex / delete / migration
13. production rollout

## Stop Condition

After baseline, stop.

Phase 2.86 controlled small-batch real Hermes evidence write planning requires a separate explicit prompt.
