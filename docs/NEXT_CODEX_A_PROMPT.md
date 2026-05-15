# NEXT_CODEX_A_PROMPT

## Phase 2.88 Runtime Evidence Write Preflight Runner Baseline

Phase 2.88 implementation has been completed.
Codex B review has passed.

Previous baseline:

- commit: `3b01b0f`
- tag: `phase-2.87d-runtime-evidence-write-execution-pack-baseline`
- pushed: true

## Review Result

Codex B verified:

1. The runner is preflight-only and does not import or call `EvidenceOnlyWriter.write()`.
2. The service validates required approval fields, expiry, `target_environment=test_machine_only`, allowed action, scope limits, feature flags, payload fingerprint, idempotency key, `write_run_id`, git/worktree inputs, and prerequisite report refs.
3. Decision states are limited to `preflight_ready_for_operator_stop`, `preflight_pause`, and `preflight_no_go`.
4. Scope remains capped at 1 document, 1 document version, and 20 chunks.
5. Agent answer, index write, API / CLI runtime, parser, NAS, object-store, platform DB, repair, reindex, delete, cleanup, migration, and rollout flags remain blocked.
6. CLI output is sanitized and does not print raw approval content, secrets, raw text, true filename, true NAS path, raw DB rows, or sensitive business values.
7. Runtime preflight reports are ignored under `reports/evidence_write_runtime_preflight/`.
8. Target tests, Data Steward regression, py_compile, diff check, latest JSON validation, and ignore check pass.

## Goal

Create the Phase 2.88 selective Git baseline and stop.

This prompt does not authorize runtime evidence write execution.
This prompt does not authorize calling `EvidenceOnlyWriter.write()`.
This prompt does not authorize real DB writes.
This prompt does not authorize Phase 2.89.

## Allowed Files For Baseline

Stage only:

1. `app/services/asset_catalog/evidence_write_runtime_preflight.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase288_runtime_evidence_write_preflight.py`
4. `tests/test_data_steward_evidence_write_runtime_preflight.py`
5. `reports/evidence_write_runtime_preflight/.gitignore`
6. `reports/evidence_write_runtime_preflight/README.md`
7. `docs/PHASE288_RUNTIME_EVIDENCE_WRITE_PREFLIGHT.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any other file is dirty, stop and report.

## Validation

Run before baseline:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_runtime_preflight.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_write_runtime_preflight.py scripts/phase288_runtime_evidence_write_preflight.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
git diff --cached --check
git diff --cached --name-only
```

Do not run API / CLI smoke.
Do not run DB smoke.
Do not run writer.
Do not run parser.
Do not copy files.

## Commit / Tag

Commit message:

```text
feat: add phase 2.88 runtime evidence write preflight
```

Tag:

```text
phase-2.88-runtime-evidence-write-preflight-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. calling `EvidenceOnlyWriter.write()`
2. runtime evidence write execution
3. real DB write
4. API / CLI runtime wiring
5. parser execution
6. scratch copy
7. raw file content read
8. NAS scan
9. OpenSearch / Qdrant / MinIO write
10. platform DB write
11. audit table write outside normal existing retrieval audit behavior
12. Agent answer integration
13. Agent DB / NAS CRUD
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout
16. enabling real-write feature flags outside local fixture validation
17. entering Phase 2.89 without a separate prompt

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation preflight stops before writer invocation
7. confirmation Phase 2.89 remains blocked pending separate authorization
8. confirmation no real DB / parser / copy / index / object-store / Agent answer action occurred
