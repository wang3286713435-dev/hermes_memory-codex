# NEXT_CODEX_A_PROMPT

## Phase 2.87d Runtime Evidence Write Execution Pack Baseline

Phase 2.87d docs-only / handoff planning has been completed.
Codex B review has passed.

Review targets:

1. `docs/PHASE287D_RUNTIME_EVIDENCE_WRITE_EXECUTION_PACK.md`
2. `docs/CODEX_TEST_MACHINE_RUNTIME_EVIDENCE_WRITE_SMOKE_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/HANDOFF_LOG.md`

## Review Result

Codex B verified:

1. Phase 2.87d remains docs-only / handoff-only.
2. The execution pack lists test-machine preconditions, reviewed refs/tags, environment key names without values, operator approval JSON path/schema, required prior report refs, and feature flag expectations.
3. The one-run boundary remains one approved source asset, one `Document`, one `DocumentVersion`, up to 20 `Chunk` rows, matching `CitationRecord` rows, one `write_run_id`, and one operator approval id.
4. Preflight commands are inspection-only and do not invoke writer, parser, file copy, NAS scan, DB write, index write, object-store write, audit write, or Agent answer.
5. Mandatory stop points occur before any future writer invocation.
6. The future Codex C prompt is clear enough for test-machine use but still says not to execute unless a later explicit prompt authorizes it.
7. Sanitized report expectations exclude raw text, true filenames, true NAS paths, secrets, raw DB rows, and sensitive business values.
8. Rollback dry-run and idempotency expectations remain diagnostic and do not authorize delete / cleanup / repair.

## Goal

Create the Phase 2.87d selective docs baseline and stop.

This prompt does not authorize executing the test-machine prompt.
This prompt does not authorize runtime evidence write smoke.
This prompt does not authorize real DB writes.
This prompt does not authorize Phase 2.88.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE287D_RUNTIME_EVIDENCE_WRITE_EXECUTION_PACK.md`
2. `docs/CODEX_TEST_MACHINE_RUNTIME_EVIDENCE_WRITE_SMOKE_PROMPT.md`
3. `docs/NEXT_CODEX_A_PROMPT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any code, test, script, migration, report artifact, or unexpected file is dirty, stop and report.

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

Do not run API / CLI smoke.
Do not run DB smoke.
Do not run writer.
Do not run parser.
Do not copy files.

## Commit / Tag

Commit message:

```text
docs: add phase 2.87d runtime evidence write execution pack
```

Tag:

```text
phase-2.87d-runtime-evidence-write-execution-pack-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. executing the test-machine prompt
2. runtime evidence write smoke execution
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
16. enabling real-write feature flags
17. entering Phase 2.88 without a separate prompt

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation Phase 2.87d is docs-only / handoff-only
7. confirmation the future test-machine prompt was not executed
8. confirmation Phase 2.88 remains blocked pending separate authorization
9. confirmation no real DB / parser / copy / index / object-store / Agent answer action occurred
