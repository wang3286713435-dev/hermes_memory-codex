# NEXT_CODEX_A_PROMPT

## Phase 2.83 Docs Baseline Task

Phase 2.83 evidence-write payload contract planning is complete and Codex B review has passed.

This baseline must only capture the docs-only payload contract planning. Do not enter Phase 2.83a and do not implement a payload builder.

## Summary

New planning document:

1. `docs/PHASE283_EVIDENCE_WRITE_PAYLOAD_CONTRACT_PLAN.md`

The plan defines the future contract for a dry-run payload that could describe candidate `documents` / `chunks` writes from sanitized NAS parser previews.

Key boundary:

1. Payload contract is planning-only.
2. Payload contract is not document evidence.
3. Future `payload_ready_for_write_dry_run` does not mean written, indexed, or answerable.
4. Candidate chunks in this planning phase must not include raw extracted text.
5. Phase 2.83 does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.

## Allowed Stage Files

Only stage these files:

1. `docs/PHASE283_EVIDENCE_WRITE_PAYLOAD_CONTRACT_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage any real manifest, eligibility, or payload artifact.

## Validation Commands

Run:

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
```

## Hard Boundaries

Forbidden:

1. Implement payload builder.
2. Generate payload report artifact.
3. Generate future evidence-write payloads.
4. Write `documents` or `chunks`.
5. Write platform DB or Hermes DB.
6. Write OpenSearch, Qdrant, or MinIO.
7. Execute parser.
8. Copy real files.
9. Read raw file contents.
10. Scan NAS.
11. Agent DB / NAS CRUD.
12. Agent final answer integration.
13. Treat manifest, eligibility report, or payload contract as document evidence.
14. Repair / cleanup source data / backfill / reindex / delete / migration.
15. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `docs: baseline phase 2.83 evidence payload contract plan`
5. Tag:
   - `phase-2.83-evidence-payload-contract-plan-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter Phase 2.83a.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed docs files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No manifest / eligibility / payload report artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
