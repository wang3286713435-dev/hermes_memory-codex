# NEXT_CODEX_A_PROMPT

## Phase 2.90 Test-Machine Update / Preflight Result Baseline

Phase 2.90 test-machine repository update gate and Phase 2.89 runtime preflight have completed.

Previous baseline:

- commit: `4e0bd62`
- tag: `phase-2.89-test-machine-runtime-preflight-handoff-baseline`
- pushed: true

## Verified Test-Machine Results

Test-machine repository update:

- status: `go`
- repo: `/Users/hermes/code/Hermes_memory`
- head: `4e0bd62`
- tag: `phase-2.89-test-machine-runtime-preflight-handoff-baseline`
- worktree clean: true
- required docs present: true

Test-machine runtime preflight:

- status: `go`
- decision state: `preflight_ready_for_operator_stop`
- expected commit match: true
- worktree clean: true
- prerequisite refs present: true
- prerequisite refs sanitized: true
- sanitized output report filename: `phase289-runtime-preflight-report-001.json`
- writer invoked: false
- DB writes: false
- parser invoked: false
- scratch copy: false
- NAS scanned: false
- OpenSearch / Qdrant / MinIO writes: false
- Agent answer integration: false
- production rollout: false

## Goal

Create the Phase 2.90 selective docs baseline and stop.

This baseline only records:

1. test-machine repository update correction
2. runtime preflight prompt correction
3. test-machine update `Go`
4. runtime preflight `preflight_ready_for_operator_stop`

This prompt does not authorize writer invocation.
This prompt does not authorize real DB writes.
This prompt does not authorize parser, NAS copy, index/object-store write, Agent answer integration, repair/reindex, or rollout.

## Allowed Files For Baseline

Stage only:

1. `docs/CODEX_TEST_MACHINE_UPDATE_TO_PHASE289_PROMPT.md`
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
Do not run preflight runner.
Do not run writer.
Do not run parser.
Do not copy files.

## Commit / Tag

Commit message:

```text
docs: record phase 2.90 test-machine preflight readiness
```

Tag:

```text
phase-2.90-test-machine-preflight-readiness-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. calling `EvidenceOnlyWriter.write()`
2. runtime evidence write execution
3. real DB write
4. API / CLI Agent runtime wiring
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
16. enabling real-write feature flags for execution
17. entering a writer invocation phase without separate explicit authorization

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation preflight reached `preflight_ready_for_operator_stop`
7. confirmation writer / DB / parser / copy / NAS / index / object-store / Agent answer actions remain blocked
8. final `git status --short`
