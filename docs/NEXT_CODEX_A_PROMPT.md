# NEXT_CODEX_A_PROMPT

## Phase 2.104c Codex B Review / Docs + Fixture Baseline Gate

You are Codex A. Do not implement Phase 2.104d automatically.

## Current State

Phase 2.104c docs / fixture planning has been completed locally:

1. `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md`
2. `eval/phase2_inventory/document_evidence_search_contract_examples.json`
3. updated `docs/ACTIVE_PHASE.md`
4. updated `docs/PHASE_BACKLOG.md`
5. updated `docs/HANDOFF_LOG.md`
6. updated `docs/TODO.md`
7. updated `docs/DEV_LOG.md`
8. updated ignored `reports/agent_runs/latest.json`

No runtime code, tests, parser, writer, DB, NAS, Gateway, OpenSearch, Qdrant, MinIO, or memory implementation was changed.

## Review Checklist

Codex B should verify:

1. `document_evidence_search` is consistently described as future-only.
2. No document content answer is allowed unless all three requirements are present:
   - current Platform permission proof;
   - Evidence Availability allows governed evidence query;
   - citation-bearing governed evidence is returned.
3. Gate sequence is complete:
   - `platform_permission_gate`
   - `catalog_permission_gate`
   - `evidence_availability_gate`
   - `memory_continuity_candidate_gate`
   - `document_evidence_query_gate`
   - `citation_response_gate`
   - `missing_evidence_fallback_gate`
4. Request shape includes:
   - `query`
   - `tenant_id`
   - `requester_id`
   - `project_scope`
   - `permission_proof_ref`
   - `file_ids`
   - `model_ids`
   - `document_ids`
   - `version_ids`
   - `evidence_mode_hint`
   - `source_views`
   - `query_id`
   - `trace_id`
   - `memory_candidate_refs`
5. Response shape includes:
   - `status`
   - `evidence_mode`
   - `permission_decision`
   - `evidence_availability_status`
   - `results`
   - `citations`
   - `missing_evidence`
   - `query_id`
   - `trace_id`
   - `safe_next_actions`
   - `forbidden_actions_observed`
6. Fixture cases cover:
   - `evidence_search_ready_pdf_with_citation`
   - `evidence_search_blocked_catalog_only_dwg`
   - `evidence_search_blocked_parser_required_pdf`
   - `evidence_search_blocked_permission_denied`
   - `evidence_search_blocked_memory_reference_only`
   - `evidence_search_excel_structured_citation`
   - `evidence_search_meeting_transcript_boundary`
   - `evidence_search_manual_review_conflicting_evidence`
   - `evidence_search_rvt_component_missing_evidence`
7. Fixtures use sanitized fake IDs only.
8. No fixture contains real file names, project names, raw paths, raw rows, asset UIDs, source IDs, secrets, tokens, or customer-sensitive content.
9. Memory candidate refs are never evidence, authorization, or citations.
10. DWG / RVT / BIM content understanding remains unsupported unless a later parser / component-index phase exists.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/document_evidence_search_contract_examples.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest for this phase. This is docs / fixture planning only.

## Optional Baseline Command

Only if the user explicitly authorizes baseline after review:

1. Stage only Phase 2.104c docs / fixture / handoff files.
2. Do not stage unrelated `docs/digital-delivery-standards/` files.
3. Commit message:

```text
docs: add phase 2.104c document evidence search contract
```

4. Tag:

```text
phase-2.104c-document-evidence-search-contract-baseline
```

5. Push `origin/main` and tag.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not implement `document_evidence_search`.
4. Do not implement parser, writer, scratch copy, indexing, Gateway, DB, NAS, or memory runtime behavior.
5. Do not run API / CLI / Gateway / DB / NAS smoke.
6. Do not connect to DB / NAS / Gateway.
7. Do not execute SQL.
8. Do not read or output raw rows, NAS paths, storage paths, secrets, tokens, or `.env` values.
9. Do not write documents/chunks, OpenSearch, Qdrant, MinIO, platform DB, Hermes DB, or Hermes memory.
10. Do not enter Phase 3 or production rollout.
11. Do not stage unrelated `docs/digital-delivery-standards/`.

## Stop Condition

After review or baseline, stop and report:

1. changed files;
2. validation result;
3. whether shared docs were readable;
4. key governed document evidence search boundary conclusion;
5. risks / blockers;
6. whether Codex B review is complete;
7. whether baseline was authorized and completed.
