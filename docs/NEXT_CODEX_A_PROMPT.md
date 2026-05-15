# NEXT_CODEX_A_PROMPT

## Phase 2.86 Controlled Real Evidence Write Plan Review / Baseline Gate

Phase 2.86 docs-only planning has been completed.
Codex B review has passed.

The plan file is:

- `docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md`

Phase 2.85a baseline remains:

- commit: `380e7a0`
- tag: `phase-2.85a-evidence-write-dry-run-baseline`
- pushed: true

## Goal

Baseline the Phase 2.86 planning documents.

Do not implement Phase 2.86a.
Do not implement a writer.
Do not execute a real write.
Do not run runtime smoke.

## Required Gate

Git baseline is authorized for the allowlisted Phase 2.86 docs only.

Do not stage any other dirty file if one appears.

## Allowed Files For Future Baseline

Stage only:

1. `docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

## Validation

Run before any baseline:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

No pytest is required because Phase 2.86 is docs-only.

## Suggested Commit / Tag

Commit message:

```text
docs: plan phase 2.86 controlled real evidence write
```

Tag:

```text
phase-2.86-controlled-real-evidence-write-plan-baseline
```

## Hard Boundaries

Forbidden:

1. implement writer
2. execute real evidence write
3. write `documents`, `chunks`, `document_versions`, or audit tables
4. write platform DB or Hermes DB
5. write OpenSearch, Qdrant, or MinIO
6. execute parser
7. copy real files
8. read raw file contents
9. scan NAS
10. Agent DB / NAS CRUD
11. Agent final answer integration
12. treat dry-run artifacts as production evidence
13. repair / cleanup source data / backfill / reindex / delete / migration
14. production rollout
15. enter Phase 2.86a or 2.87 without a separate explicit prompt

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash if baseline executed
4. tag if baseline executed
5. push result if baseline executed
6. confirmation that no runtime write / parser / copy / DB / index / object-store mutation occurred
7. whether Phase 2.86a remains blocked pending separate authorization
