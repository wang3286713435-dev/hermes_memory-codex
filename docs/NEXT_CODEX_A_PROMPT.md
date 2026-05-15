# NEXT_CODEX_A_PROMPT

## Phase 2.87c Runtime Evidence Write Smoke Plan Baseline

Phase 2.87c docs-only planning has been completed.
Codex B review has passed.

Review target:

1. `docs/PHASE287C_RUNTIME_EVIDENCE_WRITE_SMOKE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/TODO.md`
5. `docs/DEV_LOG.md`
6. `docs/HANDOFF_LOG.md`

## Review Result

Codex B verified:

1. Phase 2.87c remains docs-only planning.
2. The future smoke scope is limited to one approved source asset, one `Document`, one `DocumentVersion`, up to 20 `Chunk` rows, matching `CitationRecord` rows, one `write_run_id`, and one operator approval id.
3. The prerequisite chain is explicit from DB v1.1 catalog asset through sanitized parser preview, manifest, eligibility, payload, preflight, dry-run, rehearsal, exact write targets, Phase 2.87b writer baseline, and operator approval.
4. Operator approval JSON includes target environment, source refs, report refs, idempotency key, payload fingerprint, feature flags, limits, expiry, and writes authorization.
5. Feature flags remain default-off; only future smoke-specific write flags may be enabled after separate authorization.
6. Transaction / commit boundary uses the Phase 2.87b `EvidenceOnlyWriter` with an injected SQLAlchemy session and excludes parser, NAS, index, object store, platform DB, audit write, and Agent answer code.
7. Rollback dry-run, idempotency rerun, and post-write inspection are scoped only by `write_run_id`.
8. Sanitized report format excludes raw text, true filenames, true NAS paths, secrets, raw DB rows, and sensitive business values.
9. Go / Pause / No-Go rules stop parser/copy/NAS/index/object-store/platform DB/audit/Agent answer/repair/rollout requests.

## Goal

Create the Phase 2.87c selective docs baseline and stop.

This prompt does not authorize Phase 2.87d.
This prompt does not authorize runtime evidence write smoke.
This prompt does not authorize real DB writes.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE287C_RUNTIME_EVIDENCE_WRITE_SMOKE_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any code, test, script, migration, report artifact, or unexpected file is dirty, stop and report.

## Validation

Run before baseline:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

Do not run API / CLI smoke.
Do not run DB smoke.
Do not run writer.
Do not run parser.
Do not copy files.

## Commit / Tag

Commit message:

```text
docs: add phase 2.87c runtime evidence write smoke plan
```

Tag:

```text
phase-2.87c-runtime-evidence-write-smoke-plan-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Still forbidden:

1. runtime evidence write smoke
2. real DB write
3. API / CLI runtime wiring
4. parser execution
5. scratch copy
6. raw file content read
7. NAS scan
8. OpenSearch / Qdrant / MinIO write
9. platform DB write
10. audit table write outside normal existing retrieval audit behavior
11. Agent answer integration
12. Agent DB / NAS CRUD
13. repair / cleanup / backfill / reindex / delete / migration
14. production rollout
15. entering Phase 2.87d without a separate prompt

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation Phase 2.87c is docs-only planning
7. confirmation Phase 2.87d remains blocked pending separate authorization
8. confirmation no real DB / parser / copy / index / object-store / Agent answer action occurred
