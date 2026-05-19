# Phase 2.104a Evidence Availability Contract

## 1. Purpose

Phase 2.104a defines the Evidence Availability Contract for Platform Gateway and Hermes.

The contract answers one narrow question before Hermes attempts any content-level answer:

> Is governed evidence available for this source, or is the system limited to catalog metadata / Missing Evidence?

This phase is docs and fixtures only. It does not implement `document_evidence_search`, does not connect to Platform / DB / NAS, and does not expose any new runtime capability.

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`
- `docs/PHASE2102B_METRIC_SCORING_PACK.md`
- `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`
- `eval/phase2_inventory/phase2_eval_inventory_manifest.json`

Shared `DigitalDeliveryProject` sources:

- `agent-briefings/hermes_capability_handoff.md`
- `docs/01_capability_matrix.md`
- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `integration-contracts/feedback_contract.md`
- `RISK_RED_LINES.md`

Shared docs status: available.

## 3. Contract Scope

The Evidence Availability Contract is a routing and safety contract. It must be evaluated before any future evidence search or answer generation step treats a file/model as content evidence.

It separates:

1. catalog metadata only;
2. content evidence that requires parser/indexing work;
3. governed evidence that is indexed and may be searched if permission allows;
4. unsupported modalities;
5. permission-denied sources;
6. manual-review-only cases.

It does not authorize:

- DB CRUD or SQL.
- NAS scan, copy, or raw path exposure.
- parser execution.
- OpenSearch / Qdrant / MinIO writes.
- DWG / RVT / BIM content understanding.
- production rollout.

## 4. Status Enum

Current enum:

| Status | Meaning |
|---|---|
| `catalog_only` | Only safe catalog metadata is available. Content-level questions must return Missing Evidence. |
| `parser_required` | The source is visible, but content evidence requires parsing/indexing before retrieval can answer. |
| `evidence_indexed` | Governed content evidence is indexed and may be searched if permission allows. This is a contract state, not a current platform tool promise. |
| `unsupported_type` | The file/model modality is not supported for governed evidence retrieval in the current system. |
| `permission_denied` | The requester is not authorized to access the source or evidence. |
| `manual_review_required` | Available metadata/evidence is ambiguous, conflicting, or too risky for automated answer. |

Backlog-only candidates:

- `indexing_in_progress`
- `evidence_stale`
- `source_missing`
- `requires_human_confirmation`

These backlog statuses are not part of the Phase 2.104a fixture contract.

## 5. Required Fields

Every response must include:

1. `evidence_availability_status`
2. `safe_user_message`
3. `missing_evidence_reason`
4. `permission_decision`
5. `source_kind`
6. `source_view`
7. `file_id` or `model_id`
8. `allowed_next_actions`
9. `forbidden_actions`

Optional fields:

1. `document_id`
2. `version_id`
3. `trace_id`
4. `query_id`

Field notes:

- `source_view` must be a safe view label such as `catalog_metadata_view`, `governed_evidence_view`, or `sanitized_manual_review_view`.
- `file_id`, `model_id`, `document_id`, and `version_id` must be safe identifiers, not raw storage paths or source system rows.
- `trace_id` and `query_id` support observability and feedback; they are not content evidence.

## 6. Field Safety Rules

The contract must never return:

1. raw `storage_path`;
2. raw NAS path;
3. raw DB row;
4. SQL;
5. file正文;
6. DWG / RVT / BIM content claims;
7. secrets, tokens, credentials, or `.env` values;
8. customer-sensitive text;
9. raw file names if they contain sensitive customer/project names.

Interpretation rules:

1. Catalog metadata is not content evidence.
2. `related_file_ids` are not content evidence.
3. `query_id` and `trace_id` are observability references, not proof of document content.
4. `evidence_indexed` means governed evidence may be queried by a future authorized search path; it does not by itself expose `document_evidence_search`.

## 7. Status Semantics

### 7.1 `catalog_only`

Applies when:

- Platform Gateway can return safe catalog metadata.
- No governed content evidence is available to Hermes for the question.

May Hermes answer content-level questions: no.

Required Missing Evidence wording:

> I can identify candidate sources from authorized catalog metadata, but I do not have governed content evidence for this question. Catalog metadata cannot verify file contents. Missing Evidence: content evidence is not indexed or available for this query.

Safe next actions:

- show safe catalog metadata;
- ask user to request manual review;
- ask platform to prepare parser/indexing workflow in a later authorized phase.

Forbidden actions:

- treat filename/path/catalog fields as content proof;
- claim DWG/RVT/BIM internals were read;
- query vector store as if content evidence exists.

### 7.2 `parser_required`

Applies when:

- Source is known and allowed at catalog level.
- Content answer requires parsing/indexing that has not been performed.

May Hermes answer content-level questions: no.

Required Missing Evidence wording:

> The source is visible in the catalog, but this question requires parsed content evidence that is not available yet. Missing Evidence: parser/indexing is required before Hermes can answer with citations.

Safe next actions:

- record parser/indexing prerequisite;
- route to future ingestion workflow after authorization;
- return manual review recommendation.

Forbidden actions:

- run parser implicitly;
- infer content from file name or catalog metadata;
- claim the parser has already read the file.

### 7.3 `evidence_indexed`

Applies when:

- Governed content evidence is indexed.
- Permission allows potential retrieval.
- Future evidence search may return citations.

May Hermes answer content-level questions: yes, only through an authorized evidence search path with citations.

Required Missing Evidence wording when retrieval still returns nothing:

> Governed evidence is indexed, but no citation-backed evidence was returned for this query. Missing Evidence: no matching indexed evidence was found.

Safe next actions:

- future `document_evidence_search` may query governed evidence;
- return citation-backed chunks/sheet/slide/paragraph refs if available;
- show Missing Evidence when no citation is found.

Forbidden actions:

- answer without citations;
- expose raw source text beyond approved citation snippets;
- treat `evidence_indexed` as permission bypass.

### 7.4 `unsupported_type`

Applies when:

- The source modality is visible but unsupported for governed evidence retrieval.
- Examples include unsupported BIM model internals, unsupported CAD internals, or file types without a parser path.

May Hermes answer content-level questions: no.

Required Missing Evidence wording:

> The source is visible in the catalog, but this content type is not currently supported for governed evidence retrieval. Missing Evidence: unsupported content modality.

Safe next actions:

- show safe catalog metadata;
- recommend manual review;
- add parser/support request to backlog.

Forbidden actions:

- claim semantic understanding of unsupported files;
- generate BIM/CAD/component facts without evidence;
- create a fake parser result.

### 7.5 `permission_denied`

Applies when:

- Requester lacks permission for the source or evidence.
- Platform Gateway or policy layer denies access.

May Hermes answer content-level questions: no.

Required Missing Evidence wording:

> I cannot return evidence for this source because the current requester is not authorized to access it.

Safe next actions:

- show denial reason if safe;
- ask user to request permission through approved workflow;
- log trace/audit metadata through existing authorized paths.

Forbidden actions:

- leak file names, raw paths, or snippets from denied evidence;
- use memory references to bypass denial;
- answer from prior context if permission is denied.

### 7.6 `manual_review_required`

Applies when:

- Metadata conflicts.
- Evidence status is ambiguous.
- Answer could affect compliance, contract, delivery, or sensitive operational decisions.

May Hermes answer content-level questions: no automated definitive answer.

Required Missing Evidence wording:

> The available metadata or evidence state is insufficient for an automated answer. Missing Evidence: manual review is required before this can be treated as verified.

Safe next actions:

- create a review note or issue intake;
- show sanitized conflicting metadata summary;
- ask a human reviewer to confirm source/evidence.

Forbidden actions:

- choose one conflicting source as truth;
- mark the answer as verified;
- execute any repair or data change.

## 8. Fixture File

The Phase 2.104a fixture file is:

`eval/phase2_inventory/evidence_availability_contract_examples.json`

Fixture rules:

1. Use fake IDs only, such as `file_demo_001`, `model_demo_001`, `query_demo_001`.
2. Do not include real project names.
3. Do not include real file names.
4. Do not include raw paths, raw rows, true asset UIDs, source IDs, secrets, tokens, or customer-sensitive content.
5. Booleans must make forbidden behavior explicit:
   - `should_treat_catalog_as_content_evidence=false`
   - `should_expose_raw_path=false`
   - `should_invoke_parser=false`
   - `should_query_vector_store=false` unless the fixture explicitly represents a future authorized `evidence_indexed` path.

## 9. Shared Follow-up

No shared folder files were edited in Phase 2.104a.

Recommended shared follow-up after Codex B review:

1. Mirror the accepted enum and required fields into shared `integration-contracts`.
2. Add a compact Evidence Availability row to shared `docs/01_capability_matrix.md` if the shared owner wants product-facing status labels.
3. Keep `document_evidence_search` as future-only until a separate authorized implementation phase exists.

## 10. Phase 2.104a Conclusion

Phase 2.104a provides a docs-only Evidence Availability Contract and sanitized fixtures. It is ready for Codex B review after validation, but it does not authorize runtime evidence search, parser execution, DB/NAS access, index writes, or production rollout.
