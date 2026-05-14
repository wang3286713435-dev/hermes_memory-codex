# NEXT_CODEX_A_PROMPT

## Phase 2.82 Docs Baseline Task

Phase 2.82 evidence-write eligibility planning is complete and Codex B review has passed.

This baseline must only capture the docs-only eligibility planning. Do not enter Phase 2.82a and do not implement an eligibility evaluator.

## Summary

New planning document:

1. `docs/PHASE282_EVIDENCE_WRITE_ELIGIBILITY_PLAN.md`

The plan defines the gates required before any future NAS-derived sanitized manifest can be considered for evidence-write planning.

Key boundary:

1. A manifest is review-only.
2. A manifest is not document evidence.
3. `approved` never means written, indexed, or answerable.
4. Missing permission proof defaults to `DENIED`.
5. Phase 2.82 does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.

## Allowed Stage Files

Only stage these files:

1. `docs/PHASE282_EVIDENCE_WRITE_ELIGIBILITY_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage any real manifest artifact.

## Validation Commands

Run:

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
```

## Hard Boundaries

Forbidden:

1. Implement eligibility evaluator.
2. Generate eligibility report artifact.
3. Execute parser.
4. Copy real files.
5. Read raw file contents.
6. Write platform DB / Hermes DB / `documents` / `chunks`.
7. Write OpenSearch / Qdrant / MinIO.
8. Scan NAS.
9. Agent DB / NAS CRUD.
10. Agent final answer integration.
11. Treat manifest as document evidence.
12. Repair / cleanup source data / backfill / reindex / delete / migration.
13. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `docs: baseline phase 2.82 evidence write eligibility plan`
5. Tag:
   - `phase-2.82-evidence-write-eligibility-plan-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter Phase 2.82a.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed docs files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No manifest / eligibility report artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
