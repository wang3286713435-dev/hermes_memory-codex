# NEXT_CODEX_A_PROMPT

## Phase 2.109 Final Freeze Checklist Baseline Gate

You are Codex A in the Hermes_memory mainline. This is a docs / checklist baseline task. Do not implement runtime features.

## Goal

Review and baseline the Phase 2 final freeze checklist.

This phase must keep three decisions separate:

```text
Platform stable integration freeze: Go.
Standalone Hermes kernel preservation: Go.
Full Phase 2 PRD / Roadmap closeout: Pause.
```

## Required Reading

Read:

```text
docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md
eval/phase2_inventory/phase2_final_freeze_checklist.json
docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md
docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md
docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md
docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md
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
docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md
eval/phase2_inventory/phase2_final_freeze_checklist.json
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
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/phase2_final_freeze_checklist.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

## Review Checklist

Confirm:

1. The checklist does not claim full Phase 2 PRD / Roadmap closeout.
2. Platform stable integration freeze is `go`.
3. Standalone Hermes kernel preservation is `go`.
4. Full Phase 2 PRD / Roadmap closeout is `pause`.
5. Phase 3 planning is allowed only with explicit known-gap carryover.
6. Production rollout remains `no_go`.
7. No runtime code, tests, DB, NAS, Gateway, API, parser, memory, index, object-store, or platform repo behavior is changed.

## Hard Boundaries

Do not:

1. Modify runtime code or tests.
2. Connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
3. Execute SQL.
4. Run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
5. Write Hermes memory, facts, documents, chunks, OpenSearch, Qdrant, MinIO, DB, or NAS.
6. Print secrets, raw paths, raw DB rows, raw answers, or customer data.
7. Declare full Phase 2 closeout unless every paused metric / governance gap has evidence or explicit user exception.
8. Stage unrelated shared mirror files or `docs/digital-delivery-standards/`.

## Commit / Tag

If validation passes and only the allowed files are staged, commit:

```bash
git add docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md \
  eval/phase2_inventory/phase2_final_freeze_checklist.json \
  docs/ACTIVE_PHASE.md docs/PHASE_BACKLOG.md docs/HANDOFF_LOG.md \
  docs/TODO.md docs/DEV_LOG.md docs/NEXT_CODEX_A_PROMPT.md

git commit -m "docs: add phase 2 final freeze checklist"
git tag phase-2.109-final-freeze-checklist-baseline
git push origin main
git push origin phase-2.109-final-freeze-checklist-baseline
```

Stop after baseline. Do not enter Phase 3 implementation without explicit user instruction.
