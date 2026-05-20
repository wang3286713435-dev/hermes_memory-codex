# NEXT_CODEX_A_PROMPT

## Phase 2.106 Codex B Review / Docs + Checklist Baseline Gate

You are Codex A. Do not implement a new runtime phase.

Phase 2.106 Platform Stable Hermes Freeze Readiness has been implemented as docs / checklist content and must now be reviewed before any baseline.

## Review Scope

Review these files:

1. `docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md`
2. `docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md`
3. `docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`
4. `eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

## Review Checklist

1. Freeze target must be exactly scoped as `Phase 2 Stable Hermes for Platform Integration`.
2. Stable baseline must not be described as production rollout.
3. Stable baseline must not be described as full Phase 2 PRD / Roadmap closeout.
4. Stable baseline must include catalog-only asset query, Gateway permission / redaction, Missing Evidence, safe IDs / traces, shared contract alignment, and known risk list.
5. Docs must distinguish `must_fix_before_platform_stable_freeze`, `can_freeze_with_known_risk`, `move_to_phase3_plus`, and `requires_user_business_decision`.
6. Test-machine update prompt must keep `<PHASE_2_STABLE_HERMES_BASELINE_TAG>` placeholder until a future authorized baseline tag exists.
7. Freeze checklist JSON must be sanitized and must not include raw platform reports, secrets, raw DB rows, NAS paths, customer data, raw answers, or raw files.
8. Shared `DigitalDeliveryProject` files must not be modified by this phase.
9. Unrelated `docs/digital-delivery-standards/` files must not be staged by default.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest. This phase is docs / readiness planning only.

## Optional Baseline Only If User Explicitly Authorizes

If the user explicitly authorizes Phase 2.106 baseline, stage only:

1. `docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md`
2. `docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md`
3. `docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`
4. `eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`
5. `docs/NEXT_CODEX_A_PROMPT.md`
6. `docs/ACTIVE_PHASE.md`
7. `docs/PHASE_BACKLOG.md`
8. `docs/HANDOFF_LOG.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

Do not stage:

1. `reports/agent_runs/latest.json`
2. `docs/digital-delivery-standards/`
3. any runtime code
4. any tests
5. any shared `DigitalDeliveryProject` files

Suggested commit message:

```text
docs: add phase 2.106 stable hermes freeze readiness
```

Suggested tag:

```text
phase-2.106-platform-stable-hermes-freeze-readiness-baseline
```

## Hard Boundaries

1. Do not write runtime code.
2. Do not modify tests.
3. Do not modify platform repo files.
4. Do not modify shared `DigitalDeliveryProject` files.
5. Do not connect DB / NAS / Gateway / API / OpenSearch / Qdrant / MinIO.
6. Do not run API / CLI / Gateway / DB / NAS smoke.
7. Do not execute SQL.
8. Do not write memory / facts / documents / chunks.
9. Do not scan / copy / parse NAS files.
10. Do not expose raw path / raw row / raw answer / secrets.
11. Do not execute repair / backfill / reindex / cleanup / delete.
12. Do not enter production rollout.
13. Do not enter Phase 3.

Stop after Codex B review or user-authorized baseline. Do not auto-enter Phase 2.107 or Phase 3.
