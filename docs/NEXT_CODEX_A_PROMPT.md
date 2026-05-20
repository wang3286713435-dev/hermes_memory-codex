# NEXT_CODEX_A_PROMPT

## Phase 2.108 Review / Baseline Gate

You are Codex A in the Hermes_memory mainline. This is a docs / contract baseline task. Do not implement runtime features.

## Goal

Review and baseline the Phase 2.108 standalone kernel freeze contract.

The purpose of Phase 2.108 is to ensure:

```text
Platform catalog-only integration is a safety surface, not the product ceiling of Hermes.
Hermes remains an independent enterprise Agent kernel with its own workspace, context, memory, evidence, retrieval, file governance, and future NAS governance paths.
```

## Required Reading

Read these files first:

```text
docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md
docs/PRD.md
docs/ROADMAP.md
docs/TECHNICAL_DESIGN.md
docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md
docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md
docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md
eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/TODO.md
docs/DEV_LOG.md
```

Also read the shared `DigitalDeliveryProject` files if available:

```text
integration-contracts/hermes_kernel_authority_contract.md
integration-contracts/platform_to_hermes_contract.md
agent-briefings/hermes_capability_handoff.md
docs/01_capability_matrix.md
```

## Baseline Scope

Allowed files for selective staging:

```text
docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/TODO.md
docs/DEV_LOG.md
docs/NEXT_CODEX_A_PROMPT.md
docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md
eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json
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
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

## Review Checklist

Confirm:

1. `docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md` states Hermes is an enterprise Agent kernel, not a platform plugin.
2. Platform catalog-only / Gateway read-only mode is described as current safety surface, not Hermes product ceiling.
3. Standalone Hermes workspace, session/context, memory, evidence, retrieval, file governance, and NAS governance paths are preserved.
4. Phase 2 stable tag remains platform integration baseline only, not production rollout or full Phase 2 closeout.
5. Phase 3 unlock path remains future: native session, Evidence Layer, Memory Layer, NAS governance, orchestration.
6. No runtime code, DB, NAS, Gateway, API, parser, memory, index, object-store, or platform repo behavior is changed.

## Hard Boundaries

Do not:

1. Modify runtime code or tests.
2. Connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
3. Execute SQL.
4. Run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
5. Write Hermes memory, facts, documents, chunks, OpenSearch, Qdrant, MinIO, DB, or NAS.
6. Print secrets, raw paths, raw DB rows, raw answers, or customer data.
7. Enter Phase 3.
8. Stage unrelated shared mirror files or `docs/digital-delivery-standards/`.

## Commit / Tag

If validation passes and only the allowed files are staged, commit:

```bash
git add docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md \
  docs/ACTIVE_PHASE.md docs/PHASE_BACKLOG.md docs/HANDOFF_LOG.md \
  docs/TODO.md docs/DEV_LOG.md docs/NEXT_CODEX_A_PROMPT.md \
  docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md \
  eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json

git commit -m "docs: add phase 2.108 standalone kernel freeze contract"
git tag phase-2.108-standalone-kernel-freeze-contract-baseline
git push origin main
git push origin phase-2.108-standalone-kernel-freeze-contract-baseline
```

Stop after baseline. Do not enter Phase 2 final closeout or Phase 3 without explicit user instruction.
