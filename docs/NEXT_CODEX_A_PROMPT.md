# NEXT_CODEX_A_PROMPT

## Phase 2.84 Docs Baseline Task

Phase 2.84 controlled evidence write preflight planning is complete and Codex B review has passed.

This baseline must only capture the docs-only preflight planning. Do not enter Phase 2.84a and do not implement a preflight runner.

## Summary

New planning document:

1. `docs/PHASE284_CONTROLLED_EVIDENCE_WRITE_PREFLIGHT_PLAN.md`

The plan defines the final preflight contract required before any future NAS-derived dry-run payload can be considered for controlled `documents` / `chunks` write phases.

Key boundary:

1. Preflight contract is planning-only.
2. Preflight contract is not write authorization.
3. Future `write_preflight_ready_for_dry_run` does not mean written, indexed, or answerable.
4. Actual `documents/chunks` writes remain forbidden in Phase 2.84.
5. Phase 2.84 does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.

## Allowed Stage Files

Only stage these files:

1. `docs/PHASE284_CONTROLLED_EVIDENCE_WRITE_PREFLIGHT_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage any real manifest, eligibility, payload, or preflight artifact.

## Validation Commands

Run:

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
```

## Hard Boundaries

Forbidden:

1. Implement preflight runner.
2. Generate preflight report artifact.
3. Execute controlled evidence write preflight.
4. Write `documents` or `chunks`.
5. Write platform DB or Hermes DB.
6. Write OpenSearch, Qdrant, or MinIO.
7. Execute parser.
8. Copy real files.
9. Read raw file contents.
10. Scan NAS.
11. Agent DB / NAS CRUD.
12. Agent final answer integration.
13. Treat manifest, eligibility report, payload plan, or preflight contract as document evidence.
14. Repair / cleanup source data / backfill / reindex / delete / migration.
15. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `docs: baseline phase 2.84 evidence write preflight plan`
5. Tag:
   - `phase-2.84-evidence-write-preflight-plan-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter Phase 2.84a.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed docs files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No manifest / eligibility / payload / preflight artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
