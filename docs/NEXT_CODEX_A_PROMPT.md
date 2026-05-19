# NEXT_CODEX_A_PROMPT

## Phase 2.104 Codex B Review / Docs Baseline Gate

This is not an implementation prompt. Codex A must not start Phase 2.104a unless the user explicitly authorizes it.

## Current State

Phase 2.104 docs-only planning is complete and waiting for Codex B review.

Created:

1. `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`

Updated:

1. `docs/ACTIVE_PHASE.md`
2. `docs/PHASE_BACKLOG.md`
3. `docs/HANDOFF_LOG.md`
4. `docs/TODO.md`
5. `docs/DEV_LOG.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. ignored `reports/agent_runs/latest.json`

Unrelated untracked `docs/digital-delivery-standards/` files remain out of scope and must not be staged by default.

## Codex B Review Checklist

Review `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md` for:

1. Clear distinction between current Catalog Layer and future Evidence / Memory / Orchestration layers.
2. No claim that `document_evidence_search` is current.
3. No claim that `related_file_ids`, `query_id`, or feedback labels mean Hermes read or remembered file contents.
4. No claim of DWG/RVT/BIM content understanding.
5. No claim of NAS full-text or NAS semantic collection as current capability.
6. Proper Missing Evidence wording for content-level DWG / RVT / BIM / PDF / Office questions under catalog-only evidence.
7. Shared folder sync notes correctly state that `agent-briefings/hermes_capability_handoff.md` and `docs/01_capability_matrix.md` already contain Hermes layer entries.
8. Phase 2.104a / 2.104b / 2.104c / 2.104d recommendations are planning-only and require separate authorization before implementation.

## Validation Commands

Before any baseline, rerun:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest for this phase unless tests are changed.

## Optional Baseline If Codex B Review Passes

Only after explicit user authorization:

```bash
git add docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md
git commit -m "docs: add phase 2.104 platform layered capability plan"
git tag phase-2.104-platform-layered-capability-plan-baseline
git push origin main
git push origin phase-2.104-platform-layered-capability-plan-baseline
```

Do not stage `reports/agent_runs/latest.json`.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not implement Phase 2.104a.
4. Do not implement new tools.
5. Do not run API / CLI / Gateway / DB / NAS smoke.
6. Do not connect to DB / NAS / Gateway.
7. Do not read or output raw rows, NAS paths, storage paths, secrets, tokens, or `.env` values.
8. Do not claim DWG/RVT/BIM content understanding.
9. Do not claim NAS full-text search or NAS semantic collection is current.
10. Do not claim `related_file_ids` means Hermes has read or remembered file contents.
11. Do not move to Phase 3 or production rollout.
12. Do not stage unrelated `docs/digital-delivery-standards/`.
