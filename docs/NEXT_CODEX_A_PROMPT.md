# NEXT_CODEX_A_PROMPT

## Phase 2.105 Codex B Review / Docs + Fixture Baseline Gate

You are Codex A. Do not implement a new runtime phase.

Phase 2.105 docs / contract / fixture planning has been implemented and needs Codex B review before any baseline.

## Current Phase 2.105 Outputs

Review these files:

1. `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`
2. `docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md`
3. `eval/phase2_inventory/hermes_platform_authority_alignment_examples.json`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Review Checklist

Codex B should verify:

1. Hermes is framed as enterprise agent kernel, not platform plugin.
2. Platform UI owns user surface / display / front-end interaction.
3. Platform Gateway owns login, project switch, permission proof, project_scope, path redaction, forbidden-field scan, and platform audit.
4. Hermes Kernel owns session continuity, reasoning state, tool orchestration, evidence / Missing Evidence policy, memory continuity boundary, response trace semantics, and cross-tool synthesis.
5. Data Steward / Catalog is treated as a Hermes capability module, not the whole Hermes identity.
6. Current Gateway safety model is preserved.
7. The docs do not ask Hermes to naked-connect to DB, generate SQL, expose raw path, write memory/facts, or run runtime evidence search.
8. Coupling health definition distinguishes safety health, capability health, and architecture authority health.
9. Go / Pause / No-Go criteria are clear.
10. Fixture cases use fake IDs only and include all required booleans.
11. Fixture booleans remain false for:
    - `should_make_platform_reasoning_owner`
    - `should_treat_data_steward_as_whole_hermes`
    - `should_expose_raw_path`
    - `should_use_history_without_revalidation`

## Required Validation Before Any Baseline

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/hermes_platform_authority_alignment_examples.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest. This phase is docs / contract fixtures only.

## Optional Baseline Only If Explicitly Authorized

If and only if the user explicitly authorizes baseline:

1. Stage only Phase 2.105 files:
   - `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`
   - `docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md`
   - `eval/phase2_inventory/hermes_platform_authority_alignment_examples.json`
   - `docs/NEXT_CODEX_A_PROMPT.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/PHASE_BACKLOG.md`
   - `docs/HANDOFF_LOG.md`
   - `docs/TODO.md`
   - `docs/DEV_LOG.md`
2. Do not stage ignored `reports/agent_runs/latest.json`.
3. Do not stage unrelated `docs/digital-delivery-standards/` files.
4. Commit message:

```text
docs: add phase 2.105 hermes platform authority alignment
```

5. Tag:

```text
phase-2.105-hermes-platform-authority-alignment-baseline
```

6. Push `origin/main` and tag only after commit/tag succeed.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not modify platform repo files.
4. Do not modify shared DigitalDeliveryProject files.
5. Do not implement Gateway/session runtime changes.
6. Do not connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
7. Do not execute SQL.
8. Do not run API / CLI / Gateway smoke.
9. Do not write Hermes memory.
10. Do not write facts.
11. Do not write documents/chunks.
12. Do not scan/copy/parse NAS files.
13. Do not expose or store raw path, raw row, raw answer text, secrets, tokens, credentials, or `.env` values.
14. Do not enter production rollout.
15. Do not stage unrelated `docs/digital-delivery-standards/` files.

## Stop Condition

After Codex B review or user baseline instruction, stop and report concise status. Do not auto-enter Phase 2.106.
