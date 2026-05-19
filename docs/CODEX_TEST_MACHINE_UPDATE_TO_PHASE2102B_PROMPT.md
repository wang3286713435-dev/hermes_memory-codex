# Codex Test Machine Prompt: Update Hermes Memory To Phase 2.102b

You are the test-machine Codex. Execute only this bounded update verification task, then stop.

## Goal

Safely update the active Hermes Memory test-machine checkout to:

```text
phase-2.102b-metric-scoring-pack-baseline
```

This is a read-only repository update and local validation task. It is not a runtime smoke, rollout, DB/NAS test, upload, repair, or service restart.

## Locate Repository

Find the active Hermes Memory repo, preferring:

```text
/Users/hermes/code/Hermes_memory
```

If that path does not exist, locate the active Hermes Memory checkout and report the path.

## Precondition

Before checkout:

```bash
git status --short --untracked-files=all
```

Hard stop if the worktree is not clean.

Do not stash, reset, clean, delete, or modify files.

## Update Steps

Run only:

```bash
git fetch --tags
git checkout phase-2.102b-metric-scoring-pack-baseline
```

Then verify:

```bash
git rev-parse --short HEAD
git describe --tags --exact-match
git status --short --untracked-files=all
```

Expected tag:

```text
phase-2.102b-metric-scoring-pack-baseline
```

## Required File Checks

Verify these files exist:

1. `scripts/phase2102b_metric_scoring_pack.py`
2. `tests/test_phase2102b_metric_scoring_pack.py`
3. `docs/PHASE2102B_METRIC_SCORING_PACK.md`
4. `eval/phase2_inventory/phase2_eval_inventory_manifest.json`

## Safe Local Validation

Run only:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile scripts/phase2102b_metric_scoring_pack.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_phase2102b_metric_scoring_pack.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/phase2_eval_inventory_manifest.json >/dev/null
```

## Hard Boundaries

1. Do not restart services unless separately authorized.
2. Do not run API / CLI / Gateway / DB / NAS smoke.
3. Do not connect to DB / NAS / Gateway / OpenSearch / Qdrant / MinIO.
4. Do not read or output secrets, tokens, credentials, `.env` values, storage paths, NAS paths, or raw DB rows.
5. Do not run parser, scratch copy, writer smoke, repair, backfill, reindex, delete, migration, or rollout.
6. Do not upload files.
7. Do not modify code or docs.
8. Do not commit, tag, or push.

## Report

Return:

1. repo path
2. HEAD
3. exact tag
4. clean status
5. required file checks
6. validation results
7. whether update to Phase 2.102b is Go / Pause / No-Go
8. any blocker
