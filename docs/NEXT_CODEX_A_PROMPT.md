# NEXT_CODEX_A_PROMPT

## Phase 2.110 Full Closeout Return Baseline Gate

You are Codex A in the Hermes_memory mainline. This is a docs / review baseline task. Do not implement runtime features.

## Goal

Review and baseline the Phase 2 full closeout return plan.

The key decision is:

```text
Stable platform integration baseline: keep.
Standalone Hermes kernel preservation: keep.
Full Phase 2 PRD / Roadmap closeout: returned.
Phase 2 completion announcement: blocked.
```

This is not a rollback of platform integration. It is a correction that prevents the project from announcing full Phase 2 completion before original PRD / Roadmap requirements have evidence.

## Required Reading

Read:

```text
docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md
eval/phase2_inventory/phase2_full_closeout_return_checklist.json
docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md
eval/phase2_inventory/phase2_final_freeze_checklist.json
docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md
docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md
docs/PHASE2102B_METRIC_SCORING_PACK.md
docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md
docs/PRD.md
docs/ROADMAP.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/TODO.md
docs/DEV_LOG.md
```

## Baseline Scope

Allowed files for selective staging:

```text
docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md
eval/phase2_inventory/phase2_full_closeout_return_checklist.json
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/TODO.md
docs/DEV_LOG.md
docs/NEXT_CODEX_A_PROMPT.md
```

Optional if changed by Codex B in the same reviewed work:

```text
reports/agent_runs/latest.json
```

Do not stage unrelated untracked files, especially:

```text
docs/digital-delivery-standards/
```

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/phase2_full_closeout_return_checklist.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

## Review Checklist

Confirm:

1. The plan answers the current real natural-language usage flow.
2. The plan states that current natural-language import is a controlled operator / API / CLI / checklist flow, not yet a fully productized one-sentence autonomous import flow.
3. Stable platform integration baseline remains kept.
4. Standalone Hermes kernel preservation remains kept.
5. Full Phase 2 PRD / Roadmap closeout is returned / reopened.
6. Phase 2 completion announcement is blocked until gaps are closed or explicitly reclassified.
7. Phase 3 planning is allowed only with explicit inherited gaps.
8. Production rollout remains forbidden.
9. No runtime code, tests, DB, NAS, Gateway, API, parser, memory, index, object-store, or platform repo behavior is changed.

## Hard Boundaries

Do not:

1. Modify runtime code or tests.
2. Connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
3. Execute SQL.
4. Run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
5. Write Hermes memory, facts, documents, chunks, OpenSearch, Qdrant, MinIO, DB, or NAS.
6. Print secrets, raw paths, raw DB rows, raw answers, or customer data.
7. Declare full Phase 2 completion.
8. Stage unrelated shared mirror files or `docs/digital-delivery-standards/`.

## Commit / Tag

If validation passes and only the allowed files are staged, commit:

```bash
git add docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md \
  eval/phase2_inventory/phase2_full_closeout_return_checklist.json \
  docs/ACTIVE_PHASE.md docs/PHASE_BACKLOG.md docs/HANDOFF_LOG.md \
  docs/TODO.md docs/DEV_LOG.md docs/NEXT_CODEX_A_PROMPT.md

git commit -m "docs: return phase 2 full closeout"
git tag phase-2.110-full-closeout-return-baseline
git push origin main
git push origin phase-2.110-full-closeout-return-baseline
```

Stop after baseline. Do not enter Phase 2.111 or Phase 3 implementation without explicit user instruction.
