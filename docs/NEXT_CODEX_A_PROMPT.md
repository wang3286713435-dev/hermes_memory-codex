# NEXT_CODEX_A_PROMPT

## Phase 2.104a Codex B Review / Docs + Fixture Baseline Gate

This is not an implementation prompt. Codex A must not start Phase 2.104b unless the user explicitly authorizes it.

## Current State

Phase 2.104a docs / contract fixture work is complete and waiting for Codex B review.

Created:

1. `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`
2. `eval/phase2_inventory/evidence_availability_contract_examples.json`

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

Review `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md` and `eval/phase2_inventory/evidence_availability_contract_examples.json` for:

1. Status enum coverage: `catalog_only`, `parser_required`, `evidence_indexed`, `unsupported_type`, `permission_denied`, `manual_review_required`.
2. Required fields: `evidence_availability_status`, `safe_user_message`, `missing_evidence_reason`, `permission_decision`, `source_kind`, `source_view`, file/model ID, allowed/forbidden actions, optional IDs, trace/query IDs.
3. Clear field safety rules: no raw `storage_path`, NAS path, raw DB row, SQL, file正文, secrets, tokens, credentials, or unsupported DWG/RVT/BIM content claims.
4. Clear status semantics: when each status applies, whether Hermes may answer content-level questions, Missing Evidence wording, safe next action, forbidden action.
5. Fixture cases are fully sanitized and use fake IDs only.
6. `evidence_indexed` is not described as current platform `document_evidence_search` runtime.
7. `related_file_ids` are not treated as content evidence.
8. Shared follow-up is listed without editing shared folder files.

## Validation Commands

Before any baseline, rerun:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/evidence_availability_contract_examples.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest for this phase unless tests are changed.

## Optional Baseline If Codex B Review Passes

Only after explicit user authorization:

```bash
git add docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md \
  eval/phase2_inventory/evidence_availability_contract_examples.json \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md
git commit -m "docs: add phase 2.104a evidence availability contract"
git tag phase-2.104a-evidence-availability-contract-baseline
git push origin main
git push origin phase-2.104a-evidence-availability-contract-baseline
```

Do not stage `reports/agent_runs/latest.json`.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not implement `document_evidence_search`.
4. Do not implement new tools.
5. Do not run API / CLI / Gateway / DB / NAS smoke.
6. Do not connect to DB / NAS / Gateway.
7. Do not execute SQL.
8. Do not read or output raw rows, NAS paths, storage paths, secrets, tokens, or `.env` values.
9. Do not claim DWG/RVT/BIM content understanding.
10. Do not claim NAS full-text search or NAS semantic collection is current.
11. Do not claim `related_file_ids` means Hermes has read or remembered file contents.
12. Do not write `documents/chunks`, OpenSearch, Qdrant, MinIO, platform DB, Hermes DB, or Hermes memory.
13. Do not move to Phase 3 or production rollout.
14. Do not stage unrelated `docs/digital-delivery-standards/`.
