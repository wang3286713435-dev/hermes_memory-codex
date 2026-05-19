# NEXT_CODEX_A_PROMPT

## Phase 2.101 Codex B Review / Selective Docs Baseline Preparation

You are Codex A. This prompt is for the next bounded review/baseline-prep step. Do not implement runtime features and do not enter Phase 2.102 automatically.

## Background

Phase 2.101 implementation is complete as a docs-only planning artifact:

1. New document: `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
2. Purpose: classify Phase 2.100a PRD / Roadmap / Technical Design acceptance gaps into closeout blockers, evidence-pack requirements, user-decision backlog candidates, Phase 3+ candidates, and already-satisfied evidence rows.
3. Current conclusion: Phase 2 closeout readiness is still `no`.

## Required Reading

Read before doing anything:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
5. `docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Goal

Review whether Phase 2.101 is ready for selective docs baseline.

This is not a Phase 2 closeout. It is only a baseline-prep / review step for the gap closure plan.

## Allowed Files

Only touch these if needed:

1. `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`
8. ignored `reports/agent_runs/latest.json`

## Review Checklist

Verify that `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`:

1. States that Phase 2 remains open.
2. Includes the required decision taxonomy.
3. Covers all gaps from Phase 2.100a:
   - structured entity and relationship querying
   - structured fact extraction vs manual/evidence-backed facts
   - tender deep fields
   - project/customer/qualification/case relationships
   - version difference view
   - incremental update/delete/invalidation/old chunk lifecycle
   - department/project/confidentiality permission strategy
   - feedback into eval loop
   - PRD/Roadmap eval metrics
   - knowledge administrator backend / human validation
   - parser/source evidence
   - Mac mini / employee trial evidence
   - natural-language import usability
   - Gateway catalog-only evidence
   - Data Steward catalog-only Phase 2 boundary
   - Data Steward productization / graph / spatial / DWG/RVT/BIM Phase 3+ candidate
4. Does not claim Phase 2 closeout readiness.
5. Does not silently move Phase 2 requirements to Phase 3 without user approval.

## Optional Baseline

Only if the user explicitly authorizes Git baseline:

1. Stage only the allowed docs files.
2. Commit message:
   `docs: plan phase 2 acceptance gap closure`
3. Tag:
   `phase-2.101-prd-acceptance-gap-closure-plan-baseline`
4. Push `origin/main` and the tag.

Do not commit/tag/push without explicit user authorization.

## Hard Boundaries

1. Do not implement code.
2. Do not run API / CLI / Gateway / DB / NAS smoke.
3. Do not connect to DB or NAS.
4. Do not execute SQL.
5. Do not read real reports, raw rows, NAS paths, storage paths, or secrets.
6. Do not write DB, OpenSearch, Qdrant, MinIO, platform systems, Gateway, Hermes memory, `documents`, or `chunks`.
7. Do not execute parser, scratch copy, writer smoke, repair, cleanup, backfill, reindex, delete, migration, or rollout.
8. Do not claim Phase 2 closeout readiness.
9. Do not enter Phase 2.102 or Phase 3 automatically.

## Validation

Run lightweight docs validation:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

No pytest is required unless code is changed, which should not happen.

## Final Report

Return:

1. Review result.
2. Modified files.
3. Validation result.
4. Whether selective docs baseline is recommended.
5. Whether Phase 2 closeout is ready.
6. Whether user decision is needed before Phase 2.102.
