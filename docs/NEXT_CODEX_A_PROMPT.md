# NEXT_CODEX_A_PROMPT

## Phase 2.102b Codex B Re-review / Baseline Gate

You are Codex A. Do not continue implementation from this file until Codex B has re-reviewed Phase 2.102b.

## Current State

Phase 2.102b implementation and Codex B review fix are complete.

Changed files:

1. `scripts/phase2102b_metric_scoring_pack.py`
2. `tests/test_phase2102b_metric_scoring_pack.py`
3. `docs/PHASE2102B_METRIC_SCORING_PACK.md`
4. `docs/NEXT_CODEX_A_PROMPT.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`
10. ignored `reports/agent_runs/latest.json`

Existing unrelated untracked files under `docs/digital-delivery-standards/` are not part of Phase 2.102b and must not be staged by default.

## Re-review Checklist

Codex B should verify:

1. The scorer is offline-only and does not import Hermes runtime modules.
2. The scorer never connects to DB / NAS / Gateway / OpenSearch / Qdrant / MinIO.
3. `metric_eligible=false` cases are excluded from Top5 / citation denominators.
4. Any `forbidden_behaviors_observed` in any known result row, including ineligible cases, yields `status="blocked_for_review"`.
5. Missing eligible results yield `status="incomplete"` only when there are no forbidden violations.
6. Unknown result case IDs raise a clear error.
7. Raw text / raw rows / NAS path / storage path / secret fields are rejected.
8. `phase2_closeout_readiness=false` is stable.
9. PRD 100+ / Roadmap 300+ remain not satisfied with the current 19-case inventory.

## Required Validation Before Baseline

Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile scripts/phase2102b_metric_scoring_pack.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_phase2102b_metric_scoring_pack.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

## Baseline Candidate

Only if Codex B review passes and the user explicitly authorizes baseline:

1. stage only Phase 2.102b files listed above, excluding ignored `reports/agent_runs/latest.json`
2. commit message: `feat: add phase 2 metric scoring pack`
3. tag: `phase-2.102b-metric-scoring-pack-baseline`
4. push `origin/main`
5. push tag

## Hard Boundaries

1. Do not baseline without user authorization.
2. Do not stage `docs/digital-delivery-standards/`.
3. Do not run API / CLI / Gateway / DB / NAS smoke.
4. Do not read ignored private reports unless explicitly passed as `--results`.
5. Do not read raw rows / NAS paths / storage paths / secrets.
6. Do not write DB / OpenSearch / Qdrant / MinIO / Gateway / platform DB / Hermes memory.
7. Do not execute parser / scratch copy / writer smoke / repair / backfill / reindex / delete / migration / rollout.
8. Do not claim Phase 2 closeout readiness.
9. Do not enter Phase 2.103 or Phase 3 automatically.
