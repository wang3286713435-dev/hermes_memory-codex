# NEXT_CODEX_A_PROMPT

## Phase 2.100a Codex B Review / Selective Docs Baseline Preparation

You are Codex A. Do not implement runtime code. Do not enter Phase 2.101 until Codex B review passes.

## Background

Phase 2.100a fixed Codex B review blockers in the Phase 2 / Phase 3 boundary acceptance audit:

1. Added explicit `PRD.md` §13 MVP acceptance rows.
2. Split Data Steward / BIM into Phase 2 catalog-only trial planning/boundary and Phase 3+ productization/deep BIM capability.
3. Added automatic evaluation pipeline and retrieval quality dashboard/evidence-pack rows.
4. Cleaned confusing duplicate boundary-audit / DEV_LOG sections.

Main audit file:

1. `docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`

Current conclusion remains:

1. Phase 2 closeout readiness: no.
2. The project is an internal controlled MVP candidate, but original PRD/Roadmap acceptance still has incomplete or unevidenced items.
3. Do not enter Phase 3, production rollout, repair executor, or runtime implementation from this state.

## Next Task

Perform Codex B style review of Phase 2.100a. If accepted, prepare selective docs baseline only.

## Files Eligible For Review / Baseline

1. `docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage or commit `reports/agent_runs/latest.json`.

## Review Checklist

1. Matrix includes all required columns from Phase 2.100.
2. Matrix covers the required 16 acceptance areas.
3. Matrix explicitly covers `PRD.md` §13 MVP acceptance items.
4. Data Steward / BIM Phase 2 catalog-only trial planning is separate from Phase 3+ productization.
5. Automatic eval pipeline and retrieval quality dashboard/evidence-pack gaps are visible.
6. Phase 2 is not claimed closed.
7. Phase 3 transition is not recommended before gap closure or explicit user reclassification.
8. No runtime code, DB/API/NAS/Gateway smoke, repair, rollout, migration, backfill, or reindex was performed.

## Optional Baseline If Review Passes

Commit message:

```text
docs: audit phase 2 closeout boundary
```

Tag:

```text
phase-2.100a-phase2-boundary-audit-baseline
```

Push `origin/main` and tag only if the user explicitly authorizes baseline.

## Hard Boundaries

1. Do not enter Phase 2.101 automatically.
2. Do not implement runtime code.
3. Do not write DB, NAS, OpenSearch, Qdrant, MinIO, Gateway, or platform systems.
4. Do not execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
5. Do not modify retrieval contract or memory kernel main architecture.
6. Do not claim Phase 2 closeout readiness.

## Required Validation Before Any Baseline

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```
