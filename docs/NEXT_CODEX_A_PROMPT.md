# NEXT_CODEX_A_PROMPT

## Phase 2.89 Test-Machine Runtime Preflight Smoke Handoff Baseline

Phase 2.89 docs-only / handoff-only package has been reviewed by Codex B.

Reviewed previous baseline:

- commit: `b09c3d1`
- tag: `phase-2.88-runtime-evidence-write-preflight-baseline`
- pushed: true

## Review Result

Codex B verified:

1. `docs/PHASE289_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PLAN.md` is docs-only / handoff-only.
2. `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md` is directly usable by Mac mini / test-machine Codex.
3. Reviewed ref is fixed to `b09c3d1` / `phase-2.88-runtime-evidence-write-preflight-baseline`.
4. The only allowed future command is `scripts/phase288_runtime_evidence_write_preflight.py`.
5. The prompt requires local ignored approval JSON, local ignored worktree status file, and local ignored output report.
6. The prompt forbids printing raw approval content, secrets, raw text, true filenames, true NAS paths, raw DB rows, source payloads, and sensitive business values.
7. `preflight_ready_for_operator_stop` is documented as a stop condition, not write authorization.
8. Writer invocation, real DB writes, parser, NAS copy/scan, OpenSearch / Qdrant / MinIO writes, platform DB writes, Agent answer integration, repair/reindex/delete/migration, rollout, and enabling real-write feature flags remain blocked.
9. Static validation passed.

## Goal

Create the Phase 2.89 selective docs baseline and stop.

This prompt does not authorize running the test-machine prompt.
This prompt does not authorize running the preflight runner.
This prompt does not authorize runtime evidence write execution.
This prompt does not authorize writer invocation or real DB writes.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE289_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PLAN.md`
2. `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`
3. `docs/NEXT_CODEX_A_PROMPT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any other file is dirty, stop and report.

## Validation

Run before baseline:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
git diff --cached --check
git diff --cached --name-only
```

Do not run pytest.
Do not run API / CLI smoke.
Do not run DB smoke.
Do not run the preflight runner.
Do not run writer.
Do not run parser.
Do not copy files.

## Commit / Tag

Commit message:

```text
docs: add phase 2.89 test-machine preflight handoff
```

Tag:

```text
phase-2.89-test-machine-runtime-preflight-handoff-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. running the test-machine prompt on this machine
2. running the preflight runner in this phase
3. calling `EvidenceOnlyWriter.write()`
4. runtime evidence write execution
5. real DB write
6. API / CLI Agent runtime wiring
7. parser execution
8. scratch copy
9. raw file content read
10. NAS scan
11. OpenSearch / Qdrant / MinIO write
12. platform DB write
13. audit table write outside normal existing retrieval audit behavior
14. Agent answer integration
15. Agent DB / NAS CRUD
16. repair / cleanup / backfill / reindex / delete / migration
17. production rollout
18. enabling real-write feature flags
19. entering a future writer invocation phase without separate authorization

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation test-machine prompt was not executed
7. confirmation preflight runner was not executed
8. confirmation writer / DB / parser / copy / NAS / index / object-store / Agent answer actions remain blocked
9. final `git status --short`
