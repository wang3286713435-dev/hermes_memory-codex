# Phase 2.104 Platform Layered Capability Plan

## 1. Purpose

Phase 2.104 turns the current platform handoff from a safe `catalog-only` integration note into an actionable layered capability plan:

```text
Catalog Layer -> Evidence Layer -> Memory Layer -> Orchestration Layer
```

The key decision is deliberately conservative: the platform can use the Catalog Layer now, but Evidence, Memory continuity, and Orchestration require separate contracts and later authorization before they become runtime capabilities.

## 2. Sources Reviewed

Hermes repo sources reviewed:

- `docs/PHASE2103_TEST_MACHINE_UPDATE_AND_CAPABILITY_HANDOFF.md`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`
- `docs/PHASE2102B_METRIC_SCORING_PACK.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`
- `docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`
- `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
- `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`

Shared `DigitalDeliveryProject` sources reviewed:

- `README.md`
- `PROJECT_CHARTER.md`
- `RISK_RED_LINES.md`
- `agent-briefings/hermes_agent_bootstrap.md`
- `agent-briefings/hermes_capability_handoff.md`
- `docs/01_capability_matrix.md`
- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `integration-contracts/feedback_contract.md`
- `05 平台协同与流程标准/标准到Hermes边界.md`

Shared docs status: available.

## 3. Current Problem

The current platform integration is safe but too narrow.

1. It exposes read-only catalog lookup through a permission-aware Gateway.
2. It does not yet expose governed document evidence retrieval.
3. It does not yet expose low-sensitive memory continuity in a way the platform can safely display.
4. It does not yet expose feedback-driven evaluation or issue intake as a repeatable product surface.
5. If the platform only exposes catalog lookup, users may see Hermes as a path-question bot rather than an evidence-first enterprise memory kernel.

The correction is not to jump to unsafe capabilities. Phase 2.104 keeps these out of scope:

- DB CRUD or Agent-generated SQL.
- NAS scan, NAS copy, or raw storage path exposure.
- DWG / RVT / BIM semantic interpretation.
- Full-text or semantic NAS collection claims.
- Production rollout.

## 4. Layered Capability Model

| Layer | Status | Safe Current Capability | Not Current / Must Not Claim | Next Contract |
|---|---|---|---|---|
| Catalog Layer | Current | `asset_catalog_search`, file/model IDs, safe metadata, server-side permission decision, Missing Evidence for content-level questions | File正文 evidence, raw row, storage path, NAS path, DWG/RVT content understanding | Maintain catalog tool contract and Missing Evidence policy |
| Evidence Layer | Next | Design only: governed/indexed/authorized content evidence with citations | Runtime `document_evidence_search` exposure, parser/writer enablement, NAS semantic search | Evidence Availability Contract; future Document Evidence Search Contract |
| Memory Layer | Next | Design only: low-sensitive continuity using `related_file_ids`, `related_model_ids`, `query_id`, `trace_id`, feedback labels, and low-sensitive user preferences | Claiming Hermes read, stored, or remembered file contents; using memory references as evidence | Memory Continuity Contract; Feedback Contract |
| Orchestration Layer | Later | Planning language only for supervised routing, review, monitoring, and sub-agent coordination | Autonomous repair, DB writes, rollout, unmanaged sub-agent execution | Future supervised orchestration contract |

## 5. Required Platform / Gateway Contracts

### 5.1 Evidence Availability Contract

The platform needs an explicit status before it asks Hermes to answer content-level questions.

Suggested statuses:

- `catalog_only`: only catalog metadata is available; content-level answer requires Missing Evidence.
- `parser_required`: content evidence needs parsing/indexing before retrieval can answer.
- `evidence_indexed`: governed evidence is indexed and may be queried if permission allows.
- `unsupported_type`: current system does not support the file type or content modality.
- `permission_denied`: requester cannot access this evidence.
- `manual_review_required`: answer requires human review or external confirmation.

Required response fields:

- `document_id` or `file_id`
- `version_id` when available
- `evidence_availability_status`
- `permission_decision`
- `reason`
- `next_step`

Non-goals:

- No raw path.
- No raw row.
- No file content.
- No implicit parser execution.

### 5.2 Document Evidence Search Contract

`document_evidence_search` is future-only. It should not be exposed as current platform capability until a separate implementation phase authorizes it.

Minimum future request shape:

- `query`
- `project_scope`
- `document_ids` or `file_ids`
- optional `version_ids`
- optional evidence mode hints
- requester / tenant metadata

Minimum future response shape:

- `evidence_status`
- `document_id`
- `version_id`
- `chunk_id`
- citation refs: paragraph, page, sheet/cell range, slide, or section
- `permission_decision`
- `missing_evidence_reason` when no governed evidence is available

This contract must return citations or explicit Missing Evidence. It must not return raw storage paths, full raw rows, secrets, tokens, or unsupported file-content claims.

### 5.3 Memory Continuity Contract

Memory continuity is low-sensitive reference continuity, not file-content memory.

Allowed low-sensitive fields:

- `related_file_ids`
- `related_model_ids`
- `query_id`
- `trace_id`
- feedback labels
- low-sensitive user preferences, such as preferred explanation style or preferred project context wording

Forbidden fields:

- raw path
- raw row
- raw content
- customer-sensitive text
- secret or token
- DWG / RVT / BIM content

Memory continuity can help the platform preserve context, but every content-level answer still needs current governed evidence or Missing Evidence.

### 5.4 Feedback Contract

Feedback should connect user judgment to eval and issue intake without turning feedback into unreviewed memory evidence.

Allowed fields:

- `query_id`
- `trace_id`
- related file/model IDs
- feedback label, such as `helpful`, `wrong_document`, `missing_evidence`, `wrong_boundary`, `needs_human_review`
- optional sanitized note

Forbidden fields:

- raw file content
- raw row
- NAS path / storage path
- secret / token / credential
- unreviewed customer-sensitive content

Feedback can feed evaluation inventory and triage, but it must not automatically write long-term factual memory or repair data.

### 5.5 Capability Response Contract

The platform UI must be able to distinguish:

- `current`: usable now.
- `backlog`: designed or planned, not exposed yet.
- `future`: explicitly outside current phase.
- `unsupported`: not supported under current system constraints.

Suggested response fields:

- `capability`
- `status`
- `safe_user_message`
- `missing_prerequisites`
- `allowed_actions`
- `forbidden_actions`

This avoids overclaiming and gives product teams a safe way to show what Hermes can and cannot do.

## 6. User-Facing Capability Boundary

### What The Platform Can Say Now

The platform can say:

> Hermes can search the authorized asset catalog and identify candidate files or models by safe metadata. If only catalog evidence is available, Hermes will say Missing Evidence for content-level questions.

The platform can also say:

> Hermes can keep low-sensitive references such as related file IDs, model IDs, query IDs, trace IDs, and feedback labels for continuity, but these references do not mean Hermes has read or remembered file contents.

### What The Platform Must Not Say Now

The platform must not say:

- Hermes can read all NAS files.
- Hermes can answer from DWG/RVT/BIM contents.
- Hermes has built NAS full-text or semantic search.
- Hermes can run SQL or perform DB CRUD.
- Hermes remembers file contents because it has `related_file_ids`.
- Catalog metadata is the same as document evidence.

### Content-Level Questions Under Catalog-Only Evidence

For DWG / RVT / BIM / PDF / Office content-level questions, Hermes should answer in this style when only catalog evidence exists:

> I can identify candidate files from the authorized catalog, but I do not have governed content evidence for this file yet. I cannot verify the requested content from catalog metadata alone. Missing Evidence: document evidence is not indexed or available for this query.

If the file type is unsupported:

> The file is visible in the catalog, but this content type is not currently supported for governed evidence retrieval. I can return catalog metadata and recommend manual review.

If permission denies access:

> I cannot return evidence for this file because the current requester is not authorized for that evidence.

### Low-Sensitive Memory Wording

Safe wording:

> I can keep low-sensitive references to related files, models, query IDs, trace IDs, and feedback labels to help continue the workflow. These references do not include file contents and do not replace evidence citations.

Unsafe wording:

> I remember what is inside that file.

> I already read the model and can answer from it.

> These related file IDs prove the content answer.

## 7. Mainline Phase Recommendations

Phase 2.104a: Evidence Availability Contract docs + fixtures.

- Define exact status enum and response examples.
- Add fixture examples for `catalog_only`, `parser_required`, `evidence_indexed`, `unsupported_type`, `permission_denied`, and `manual_review_required`.
- No runtime tool implementation unless separately authorized.

Phase 2.104b: low-sensitive Memory Continuity Contract docs + tests.

- Define what can enter continuity memory.
- Add contract tests or fixtures that reject raw path/raw row/raw content/secret fields.
- Keep `related_file_ids` as references, not evidence.

Phase 2.104c: `document_evidence_search` planning only.

- Design future request/response contract.
- Require citation refs and permission decisions.
- Do not implement parser, indexer, or runtime Gateway exposure in the planning phase.

Phase 2.104d: feedback / scoring linkage to eval inventory.

- Map feedback labels to Phase 2 eval inventory and scoring pack.
- Preserve sanitized feedback boundaries.
- Do not write feedback directly into long-term facts or memory without a later reviewed phase.

Any implementation phase requires separate user authorization.

## 8. Shared Folder Sync Notes

Shared folder status: available.

Observed shared entries:

1. `agent-briefings/hermes_capability_handoff.md` exists and already describes the layered map: current Catalog Layer, future Evidence Layer, low-sensitive Memory Layer, and later eval / deeper platform exposure.
2. `docs/01_capability_matrix.md` includes Hermes layer entries for catalog metadata, future evidence retrieval, low-sensitive memory continuity, Evidence Availability Contract, and future orchestration.
3. `integration-contracts/catalog_tool_contract.md` supports the current read-only `asset_catalog_search` boundary.
4. `integration-contracts/missing_evidence_policy.md` supports catalog-only Missing Evidence wording.
5. `integration-contracts/feedback_contract.md` supports low-sensitive feedback without raw path/raw row/file content.
6. `RISK_RED_LINES.md` reinforces that catalog metadata is not file正文 evidence, related IDs do not mean content was read, and DWG/RVT/BIM content understanding is not current.

Shared follow-up:

- If Phase 2.104a creates exact Evidence Availability fixture wording, mirror the final enum and examples into the shared `integration-contracts` folder.
- If Phase 2.104b creates exact low-sensitive memory fixture wording, mirror the final memory boundary into the shared capability matrix.
- Do not baseline or edit shared folder files from this Hermes repo docs-only phase.

## 9. Phase 2.104 Conclusion

Phase 2.104 is ready for Codex B review as a docs-only layered capability plan. It does not close Phase 2, does not expose runtime Evidence/Memory/Orchestration layers, and does not authorize production rollout.
