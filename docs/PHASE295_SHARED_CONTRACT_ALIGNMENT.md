# Phase 2.95 Shared Contract Alignment

## Scope

Phase 2.95 formally adopts the shared `DigitalDeliveryProject` document space as a cross-project contract input for Hermes / Data Steward / digital delivery standard coordination.

This phase is docs-only and contract-alignment-only. It does not authorize runtime smoke, DB/NAS/API access, Gateway implementation, parser/writer/index writes, Agent DB CRUD, or rollout.

Shared document space:

```text
/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject
```

Previous Hermes baseline:

- commit: `712cd83`
- tag: `phase-2.94a-gateway-smoke-handoff-baseline`
- pushed: true

## Shared Files Read

Hermes has read and adopted the following files as Phase 2.95 contract inputs:

1. `README.md`
2. `PROJECT_CHARTER.md`
3. `RISK_RED_LINES.md`
4. `docs/01_capability_matrix.md`
5. `integration-contracts/platform_to_hermes_contract.md`
6. `integration-contracts/catalog_tool_contract.md`
7. `integration-contracts/missing_evidence_policy.md`
8. `integration-contracts/feedback_contract.md`
9. `integration-contracts/gateway_response_contract.md`
10. `standards/standard_to_agent_boundary.md`
11. `agent-briefings/hermes_agent_bootstrap.md`
12. `agent-briefings/hermes_agent_risk_notes.md`
13. `ops/document_ownership.md`
14. `ops/change_workflow.md`

## Hermes-owned Or Hermes-reviewed Shared Files

Per `ops/document_ownership.md`, Hermes is primary owner for:

1. `integration-contracts/catalog_tool_contract.md`
2. `integration-contracts/missing_evidence_policy.md`
3. `integration-contracts/feedback_contract.md`
4. `standards/standard_to_agent_boundary.md`
5. `ops/local_setup_hermes.md`

Hermes may review but does not primarily own:

1. `standards/standard_to_platform_mapping.md`
2. `integration-contracts/gateway_response_contract.md`

User / architecture coordinator confirmation is required before changing:

1. `PROJECT_CHARTER.md`
2. `RISK_RED_LINES.md`
3. `ROADMAP.md`
4. `standards/digital_delivery_standard_v0.1.md`
5. accepted ADR status

## Adopted Contract Boundaries

### Naming

1. Official product / Agent name is `Hermes`.
2. `Jarvis` is legacy / not official.
3. New Hermes-side docs, contracts, prompts, frontend copy, and Agent briefings must not use Jarvis as the active name.

Observed shared-doc state:

- Required shared files use Hermes as the official name.
- `Jarvis` appears only in historical / terminology context outside the required core contract files.
- No immediate shared-doc edit is required.

### Catalog Tool

Hermes adopts `asset_catalog_search` as the recommended / target tool contract for catalog-only asset metadata search.

Current boundary:

1. Read-only.
2. Fail-closed.
3. Catalog-only.
4. Does not read file content.
5. Does not parse DWG / RVT internals.
6. Does not imply NAS full-text search, NAS semantic search, DWG/RVT content understanding, or BIM component-level querying is available.
7. Must return a traceable `query_id`.
8. Must not expose raw `storage_path`.
9. `project_scope` must be generated or validated server-side by Platform Gateway; frontend-provided values are not trusted.

### Missing Evidence

Hermes adopts the shared Missing Evidence policy:

1. If a user asks for file text, DWG layers / title blocks / annotations / coordinates, RVT sheets / views / levels / families, BIM component parameters, PDF/Office content conclusions, or engineering semantic judgments, catalog metadata alone is not enough.
2. If only catalog metadata exists, Hermes must return Missing Evidence instead of inferring content.
3. `updated_at` must not be interpreted as NAS file mtime.
4. `process_status` must not be interpreted as semantic index status.
5. Missing Evidence should identify the evidence class needed, such as `full_text_evidence`, `dwg_parse_evidence`, `rvt_parse_evidence`, `component_evidence`, or `manual_evidence`.

### Memory And `related_file_ids`

Hermes may record low-sensitive `related_file_ids` when useful for context continuity.

Hermes must not write these into long-term memory:

1. NAS catalog row.
2. Raw `storage_path`.
3. Raw `storage_uri`.
4. NAS path.
5. File content.
6. DWG/RVT internals.
7. Secrets or credentials.

### Frontend / Gateway Permission Boundary

Hermes adopts the shared frontend / Gateway boundary:

1. `project_scope`, `permission_decision`, and permission context must be generated or validated server-side by Platform Gateway.
2. Frontend-provided scope values are not trusted.
3. `display_path` and `path_hint` are sanitized display fields and must not equal raw `storage_path`.
4. Gateway responses may include `query_id`, `trace_id`, `project_scope`, `asset_catalog_only`, `source_view`, `items`, `permission_decision`, `display_path`, `path_hint`, `capabilities`, `missing_evidence`, and `missing_evidence_reason`.
5. Gateway responses must not include raw `storage_path`, raw `storage_uri`, raw DB row, unredacted secrets, file content, or DWG/RVT internals.

### Standards Boundary

Hermes may explain catalog-only standard checks and evidence levels.

Hermes must distinguish:

1. current evidence-supported conclusions
2. catalog-level hints
3. backlog capabilities
4. future capabilities
5. Missing Evidence cases

Standards must mark rules as `current`, `backlog`, or `future`.

## Hermes Change Sync Rules

Hermes changes must update the shared document space when they affect:

1. Catalog Tool schema.
2. Gateway response fields.
3. Missing Evidence policy.
4. Memory write boundary.
5. `related_file_ids`.
6. Path redaction policy.
7. Prompt / tool description boundary.
8. Evidence-level interpretation.
9. A capability moving from backlog to current.
10. Any mismatch between implementation facts and shared docs.

Hermes-side PR / phase review should include a shared-contract check whenever Data Steward / NAS / Gateway / catalog-only behavior changes.

## Current Mismatch List

No required shared contract mismatch was found in Phase 2.95.

Observed notes:

1. `Jarvis` appears only in historical / terminology notes outside the required core contract files; this is acceptable and does not require a Phase 2.95 edit.
2. `asset_catalog_search` is described as a recommended / target contract, not as fully landed runtime capability; this matches Hermes current boundary.
3. Gateway response contract is Platform-owned but aligned with Hermes read-only / path-redaction / Missing Evidence boundaries.

## Shared Files Changed

None.

Phase 2.95 did not modify shared `DigitalDeliveryProject` files.

## Runtime Boundary Confirmation

Phase 2.95 did not:

1. run frontend / Gateway smoke
2. implement Gateway code
3. connect to real DB / platform API / Hermes API
4. run Agent DB CRUD
5. generate SQL
6. scan NAS
7. invoke parser
8. perform scratch copy
9. run writer smoke
10. write `documents`, `document_versions`, `chunks`, or `citations`
11. write OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
12. read DWG / RVT / NWD / IFC content
13. expose raw `storage_path`, raw row, NAS path, raw content, secret, token, bearer, or credential material
14. run repair / cleanup / backfill / reindex / delete / migration
15. enter production rollout

## Next Recommendation

Codex B should review this alignment document. If accepted, create a selective docs baseline for Phase 2.95.

Do not enter Phase 2.96 or run real frontend / Gateway smoke automatically.
