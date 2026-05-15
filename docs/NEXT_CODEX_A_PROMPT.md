# NEXT_CODEX_A_PROMPT

## Phase 2.85 Docs Baseline Gate

Phase 2.85 Controlled Evidence Write Dry-run Planning is complete.

Proceed only to a selective docs baseline if Codex B / user approves this prompt.

Do not enter Phase 2.85a. Do not implement a writer and do not execute any evidence write dry-run.

## Current Planning Artifact

1. `docs/PHASE285_CONTROLLED_EVIDENCE_WRITE_DRY_RUN_PLAN.md`

The planning artifact defines:

1. ignored local `nas_evidence_write_preflight.v0` input gate
2. `write_preflight_ready_for_dry_run` requirement
3. explicit operator approval
4. feature flags default off
5. local temp SQLite / in-memory simulation only
6. deterministic simulated document / chunk refs
7. idempotency and duplicate protection
8. rollback dry-run boundary
9. citation / evidence boundary
10. Go / Pause / No-Go
11. future Phase 2.85a / 2.86 split

## Allowed Stage Files

Only stage:

1. `docs/PHASE285_CONTROLLED_EVIDENCE_WRITE_DRY_RUN_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

Do not run pytest; Phase 2.85 is docs-only planning.

## Commit / Tag

Commit message:

```text
docs: baseline phase 2.85 evidence write dry-run plan
```

Tag:

```text
phase-2.85-evidence-write-dry-run-plan-baseline
```

Push `origin/main` and tag.

## Hard Boundaries

Forbidden:

1. implement evidence writer
2. execute evidence write dry-run
3. generate write-dry-run artifact
4. write `documents` or `chunks`
5. write platform DB or Hermes DB
6. write OpenSearch, Qdrant, or MinIO
7. execute parser
8. copy real files
9. read raw file contents
10. scan NAS
11. Agent DB / NAS CRUD
12. Agent final answer integration
13. treat manifest / eligibility / payload / preflight / future write-dry-run report as production evidence
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout

## Stop Condition

After baseline, stop.

Phase 2.85a local temp DB / in-memory evidence write dry-run runner requires a separate explicit prompt.
