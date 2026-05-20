# NEXT_CODEX_A_PROMPT

## Phase 2.107 Codex B Review / Docs + Matrix Baseline Gate

You are Codex A. Do not implement a new runtime phase.

Phase 2.107 Minimal Freeze Blocker Closure Plan has been implemented as docs / decision-matrix content and must now be reviewed before any baseline.

## Review Scope

Review these files:

1. `docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md`
2. `eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Review Checklist

1. Stable target must remain `Phase 2 Stable Hermes for Platform Integration`.
2. The plan must not create or imply a stable tag.
3. The plan must not declare Phase 2 fully closed.
4. The matrix must classify each blocker as exactly one of `must_close_before_stable_tag`, `freeze_with_known_risk`, `phase3_plus_deferred`, `user_business_decision_required`, or `already_satisfied`.
5. Must-close set must cover platform identity/wording, Gateway permission/path redaction, catalog-only safe refs, Missing Evidence, shared contract sync, and test-machine update.
6. Must-close set must incorporate the latest Platform / DB Agent alignment report: current `architecture_authority_health=orange`, 0B Gateway hardening, high-risk forbidden-field fail-closed, authority-health exposure, and frontend wording correction.
7. Known-risk freeze must include runtime session/thread refs, Evidence Layer, Memory runtime, and target-scale metrics when deferred; session/thread refs may be frozen only if 0B Gateway hardening makes the limitation explicit.
8. Phase 3+ deferrals must keep production rollout, full Data Steward, Agent DB CRUD/SQL, NAS semantic collection, and DWG/RVT/BIM content understanding out of the stable platform tag.
9. Natural import / file governance usability must remain a user business decision, not an implicit blocker or implicit deferral.
10. Shared `DigitalDeliveryProject` files must not be modified.
11. Unrelated `docs/digital-delivery-standards/` files must not be staged by default.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest. This phase is docs / decision-matrix planning only.

## Baseline Only After Codex B Approval

If Codex B approval is recorded for Phase 2.107 baseline, stage only:

1. `docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md`
2. `eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json`
3. `docs/NEXT_CODEX_A_PROMPT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

Do not stage:

1. `reports/agent_runs/latest.json`
2. `docs/digital-delivery-standards/`
3. any runtime code
4. any tests
5. any shared `DigitalDeliveryProject` files

Suggested commit message:

```text
docs: add phase 2.107 freeze blocker closure plan
```

Suggested tag:

```text
phase-2.107-minimal-freeze-blocker-closure-baseline
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
12. Do not create a stable tag without explicit user authorization.
13. Do not enter production rollout.
14. Do not enter Phase 3.

Stop after Codex B review or user-authorized baseline. Do not auto-enter Phase 2.108, stable tag creation, production rollout, or Phase 3.
