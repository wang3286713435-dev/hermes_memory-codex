# Phase 2.104c Governed Document Evidence Search Contract Plan

## 1. Purpose

Phase 2.104c defines a future-only `document_evidence_search` contract for governed evidence retrieval.

It does not implement runtime search. It does not expose a new tool, parser, writer, indexer, DB path, NAS path, Gateway call, or production rollout.

The core rule is:

```text
No document content answer without all three gates:
1. current Platform permission proof;
2. evidence availability status that allows governed evidence query;
3. citation-bearing evidence returned by an authorized evidence search path.
```

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`
- `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`
- `eval/phase2_inventory/evidence_availability_contract_examples.json`
- `eval/phase2_inventory/memory_continuity_permission_examples.json`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`

Shared `DigitalDeliveryProject` sources:

- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `integration-contracts/feedback_contract.md`
- `docs/01_capability_matrix.md`
- `RISK_RED_LINES.md`

Shared docs status: available.

## 3. Contract Scope

`document_evidence_search` is a future governed evidence retrieval interface.

It may only run after:

1. current Platform permission proof is present and valid;
2. catalog permission does not deny the current request;
3. Evidence Availability says governed evidence may be queried;
4. memory continuity references, if present, have only narrowed candidate IDs after permission passes;
5. the future evidence search path returns citation-bearing evidence.

It must never:

1. answer from catalog metadata alone;
2. answer from Hermes memory references;
3. bypass denied or stale platform permission;
4. expose raw storage paths, raw NAS paths, raw DB rows, secrets, tokens, credentials, or `.env` values;
5. claim DWG / RVT / BIM content understanding unless a later parser / component-index phase explicitly supports that modality;
6. run parser, writer, scratch copy, backfill, reindex, repair, DB query, Gateway smoke, or NAS scan.

## 4. Mandatory Gate Sequence

### 4.1 `platform_permission_gate`

Input fields:

- `tenant_id`
- `requester_id`
- `project_scope`
- `permission_proof_ref`
- `query_id`
- `trace_id`

Pass condition:

- Permission proof is current, server-issued or server-validated, and scoped to the requester / tenant / project.

Fail condition:

- Permission proof is missing, stale, expired, mismatched, or denied.

Safe response:

- Return `blocked_permission_denied` or `requires_permission_refresh` style user wording.

Forbidden behavior:

- Trust frontend-provided scope without platform validation.
- Use memory, feedback, prior session, or catalog row as permission proof.

### 4.2 `catalog_permission_gate`

Input fields:

- `file_ids`
- `model_ids`
- `document_ids`
- `project_scope`
- `catalog_permission_decision`
- `source_views`

Pass condition:

- Catalog response allows safe metadata visibility for the current request.

Fail condition:

- Catalog response denies the source or indicates the source is outside current scope.

Safe response:

- Return safe denial without source content, raw path, or sensitive metadata.

Forbidden behavior:

- Treat catalog permission as authorization for full-text evidence.
- Reveal denied source details.

### 4.3 `evidence_availability_gate`

Input fields:

- `evidence_availability_status`
- `source_kind`
- `source_view`
- `document_ids`
- `version_ids`
- `evidence_mode_hint`

Pass condition:

- Status is compatible with governed evidence query, such as `evidence_indexed` / `ready_for_evidence_query`.

Fail condition:

- Status is `catalog_only`, `parser_required`, `unsupported_type`, `permission_denied`, `manual_review_required`, or otherwise not queryable.

Safe response:

- Return Missing Evidence or manual review wording with the specific missing evidence reason.

Forbidden behavior:

- Run parser implicitly.
- Query vector / full-text evidence when the availability state does not allow it.
- Treat `evidence_indexed` as a permission bypass.

### 4.4 `memory_continuity_candidate_gate`

Input fields:

- `memory_candidate_refs`
- `related_file_ids`
- `related_model_ids`
- `query_id`
- `trace_id`
- `last_evidence_mode`
- `last_permission_decision_summary`

Pass condition:

- Memory references are low-sensitive candidate hints only, and platform permission has already passed.

Fail condition:

- Memory contains forbidden raw path, raw row, file content, customer-sensitive note, secret, token, or full permission proof.

Safe response:

- Use memory refs only to narrow candidate IDs after permission passes, or reject / ignore unsafe memory fields.

Forbidden behavior:

- Use memory refs as content evidence.
- Use memory refs to bypass permission denial.
- Claim "Hermes remembered file contents."

### 4.5 `document_evidence_query_gate`

Input fields:

- `query`
- `document_ids`
- `version_ids`
- `file_ids`
- `model_ids`
- `evidence_mode_hint`
- `source_views`
- `query_id`
- `trace_id`

Pass condition:

- A future authorized evidence search path exists, all previous gates passed, and query scope is bounded to allowed sources.

Fail condition:

- No authorized evidence search path exists, scope is too broad, source modality is unsupported, or the request attempts raw path / raw row / unsupported content access.

Safe response:

- Return Missing Evidence or manual review; do not execute search.

Forbidden behavior:

- Implement or call runtime `document_evidence_search` in this phase.
- Query DB, NAS, OpenSearch, Qdrant, Gateway, or parser directly.

### 4.6 `citation_response_gate`

Input fields:

- `results`
- `citations`
- `document_id`
- `version_id`
- `chunk_id`
- `source_location`
- `evidence_mode`

Pass condition:

- Every content claim is backed by citation metadata from authorized evidence.

Fail condition:

- Evidence lacks citation, source identifiers, version, chunk, page / sheet / slide / transcript location, or contains raw path / raw row.

Safe response:

- Answer only cited claims; otherwise return Missing Evidence.

Forbidden behavior:

- Answer from uncited snippets.
- Dump full raw document text.
- Use catalog metadata or memory refs as citations.

### 4.7 `missing_evidence_fallback_gate`

Input fields:

- failed gate name
- `missing_evidence_reason`
- safe next actions
- `query_id`
- `trace_id`

Pass condition:

- The system can provide a safe explanation and next action without leaking sensitive source details.

Fail condition:

- The fallback would reveal denied content, raw path, secret, or unsupported internals.

Safe response:

- State the missing gate and safe next action.

Forbidden behavior:

- Guess content.
- Claim capability that does not exist.
- Use "maybe" language as if it were evidence.

## 5. Future Request Shape

Planning-only fields:

```json
{
  "query": "string",
  "tenant_id": "string",
  "requester_id": "string",
  "project_scope": "object",
  "permission_proof_ref": "string",
  "file_ids": ["string"],
  "model_ids": ["string"],
  "document_ids": ["string"],
  "version_ids": ["string"],
  "evidence_mode_hint": "string",
  "source_views": ["string"],
  "query_id": "string",
  "trace_id": "string",
  "memory_candidate_refs": {
    "related_file_ids": ["string"],
    "related_model_ids": ["string"],
    "last_evidence_mode": "string"
  }
}
```

`memory_candidate_refs` can only narrow candidates after platform permission passes. They cannot authorize, answer, cite, or override Missing Evidence.

## 6. Future Response Shape

Planning-only fields:

```json
{
  "status": "string",
  "evidence_mode": "string",
  "permission_decision": "string",
  "evidence_availability_status": "string",
  "results": [],
  "citations": [],
  "missing_evidence": [],
  "query_id": "string",
  "trace_id": "string",
  "safe_next_actions": [],
  "forbidden_actions_observed": []
}
```

Each result must contain safe identifiers and citation metadata only:

- `document_id`
- `version_id`
- `chunk_id`
- `source_kind`
- `source_view`
- `citation_location`
- short approved excerpt when the future evidence path permits it

Results must not contain:

- raw path;
- raw DB row;
- SQL;
- secret / token / credential;
- raw file content dump;
- storage URI;
- unsupported DWG / RVT / BIM internals.

## 7. Status Enum

| Status | Meaning |
|---|---|
| `ready_for_evidence_query` | All pre-query gates pass and governed evidence may be queried by a future authorized path. |
| `blocked_permission_denied` | Current platform permission denies the requester. |
| `blocked_catalog_only` | Only catalog metadata is available; content answer requires Missing Evidence. |
| `blocked_parser_required` | Parser / indexing is required before governed evidence exists. |
| `blocked_unsupported_type` | Current system does not support governed evidence retrieval for the modality. |
| `blocked_memory_reference_only` | Memory candidate exists but cannot act as evidence or authorization. |
| `manual_review_required` | Evidence or permission state is ambiguous, conflicting, or too risky for automated answer. |
| `query_executed_with_citations` | Future evidence search returned citation-bearing evidence. |
| `query_executed_missing_evidence` | Future evidence search ran but returned no citation-backed matching evidence. |

## 8. Citation Requirements

Supported future evidence must cite location:

1. PDF / Office: `document_id`, `version_id`, `chunk_id`, page, section, paragraph, or approved source location.
2. Excel: `document_id`, `version_id`, `chunk_id`, sheet name, cell range or row range.
3. PPTX: `document_id`, `version_id`, `chunk_id`, slide number, slide title.
4. Meeting transcript: `document_id`, `version_id`, `chunk_id`, transcript segment / timestamp if available, and explicit `transcript_as_fact=false`.
5. DWG / RVT / BIM: not supported by this planning contract unless a later parser / component-index phase exists and is separately authorized.

If citation requirements are not met, the response must be Missing Evidence or manual review.

## 9. Fixture File

The Phase 2.104c fixture file is:

`eval/phase2_inventory/document_evidence_search_contract_examples.json`

Fixture rules:

1. Use fake IDs only, such as `file_demo_201`, `doc_demo_201`, `chunk_demo_201`, `query_demo_201`, `trace_demo_201`.
2. Do not include real project names, real file names, raw paths, raw rows, asset UIDs, source IDs, secrets, tokens, or customer-sensitive content.
3. Every case must make these booleans explicit:
   - `should_execute_search`
   - `should_answer_content`
   - `should_use_memory_as_evidence`
   - `should_expose_raw_path`
   - `should_claim_dwg_rvt_understanding`
4. `should_use_memory_as_evidence`, `should_expose_raw_path`, and `should_claim_dwg_rvt_understanding` must always be false.

## 10. Shared Follow-up

No shared folder files were edited in Phase 2.104c.

Recommended shared follow-up after Codex B review:

1. Mirror the gate sequence and status enum into shared `integration-contracts`.
2. Keep `document_evidence_search` marked future-only until a runtime phase implements and validates it.
3. Add citation shape examples for PDF / Office / Excel / PPTX / meeting transcript evidence.

## 11. Phase 2.104c Conclusion

Phase 2.104c provides a docs-only future `document_evidence_search` contract plan and sanitized fixtures.

It is ready for Codex B review after validation, but it does not authorize runtime evidence search, parser execution, DB/NAS/Gateway access, OpenSearch/Qdrant/MinIO writes, memory runtime behavior, or production rollout.
