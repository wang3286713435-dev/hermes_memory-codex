# NEXT_CODEX_A_PROMPT

## Phase 2.104b Codex B Review / Docs + Fixture Baseline Gate

This is not an implementation prompt. Codex A must not start Phase 2.104c unless the user explicitly authorizes it.

## Current State

Phase 2.104b docs / contract fixture work is complete and waiting for Codex B review.

Created:

1. `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`
2. `eval/phase2_inventory/memory_continuity_permission_examples.json`

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

Review `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md` and `eval/phase2_inventory/memory_continuity_permission_examples.json` for:

1. Three-layer permission model is explicit:
   - `platform_permission`
   - `catalog_permission_decision`
   - `memory_continuity_reference`
2. Platform permission proof remains the final authority.
3. Catalog permission decision is scoped only to current catalog response.
4. Hermes memory continuity is only a low-sensitive UX hint.
5. Memory references never grant access, bypass denial, or become content evidence.
6. Allowed memory fields are low-sensitive references only.
7. Forbidden memory fields exclude raw paths, raw rows, file正文, DWG/RVT/BIM content, customer-sensitive notes, secrets, full permission proof, and unauthorized ACL snapshots.
8. Access revalidation is required for each new answer / session boundary.
9. Fixtures are sanitized, use fake IDs, and cover all required cases.
10. Shared follow-up is listed without editing shared folder files.

## Validation Commands

Before any baseline, rerun:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/memory_continuity_permission_examples.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest for this phase unless tests are changed.

## Optional Baseline If Codex B Review Passes

Only after explicit user authorization:

```bash
git add docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md \
  eval/phase2_inventory/memory_continuity_permission_examples.json \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md
git commit -m "docs: add phase 2.104b memory continuity permission contract"
git tag phase-2.104b-memory-continuity-permission-contract-baseline
git push origin main
git push origin phase-2.104b-memory-continuity-permission-contract-baseline
```

Do not stage `reports/agent_runs/latest.json`.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not implement memory runtime read / write behavior.
4. Do not implement `document_evidence_search`.
5. Do not implement new tools.
6. Do not run API / CLI / Gateway / DB / NAS smoke.
7. Do not connect to DB / NAS / Gateway.
8. Do not execute SQL.
9. Do not read or output raw rows, NAS paths, storage paths, secrets, tokens, or `.env` values.
10. Do not claim memory references are content evidence.
11. Do not claim Hermes preserves access after permission changes.
12. Do not write `documents/chunks`, OpenSearch, Qdrant, MinIO, platform DB, Hermes DB, or Hermes memory.
13. Do not enter Phase 3 or production rollout.
14. Do not stage unrelated `docs/digital-delivery-standards/`.
