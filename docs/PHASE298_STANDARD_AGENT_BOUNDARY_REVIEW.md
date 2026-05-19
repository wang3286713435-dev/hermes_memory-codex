# Phase 2.98 Digital Delivery Standard Agent Boundary Review

## Scope

This phase reviews the shared Digital Delivery standard documents as Hermes Agent answer-boundary inputs.

Previous baseline:

- Commit: `05e7275`
- Tag: `phase-2.97-frontend-gateway-readonly-trial-runbook-baseline`
- Pushed: true

This is a docs-only review. It does not modify shared standard files, runtime code, databases, indexes, object storage, NAS files, or Gateway behavior.

## Shared Files Reviewed

1. `/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject/standards/digital_delivery_standard_v0.1.md`
2. `/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject/standards/standard_rule_matrix.md`
3. `/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject/standards/standard_to_agent_boundary.md`
4. `/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject/standards/evidence_level_standard.md`
5. `/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject/standards/standard_to_platform_mapping.md`

## Overall Conclusion

The shared Digital Delivery Standard v0.1 is usable as a Hermes catalog-only answer boundary basis.

It must not be treated as evidence that Hermes currently supports DWG parsing, RVT parsing, BIM component-level understanding, NAS semantic search, or compliance judgment from file content.

Current Hermes-safe answer mode remains:

- catalog metadata only
- read-only
- permission-aware
- Missing Evidence when content/model evidence is absent
- no overclaim from filename, directory, path, manifest, preview, or metadata-only fields

## Rule Matrix Assessment

The current `standard_rule_matrix.md` contains `R001-R043`, not only 40 rules.

Rule groups:

- `R001-R021` and `R041`: usable for restricted catalog-level answers when project scope, permission proof, and safe metadata are available.
- `R022-R026` and `R042-R043`: backlog / Missing Evidence leaning; current answers should be conservative.
- `R027-R040`: future-only; current Hermes must return Missing Evidence unless explicit parse or component evidence is supplied.

Directory-level fields such as discipline, stage, drawing number, model number, and naming pattern can support catalog lookup or triage. They are not compliance conclusions.

## Agent Boundary Assessment

`standard_to_agent_boundary.md` is broadly clear for Hermes prompt/tool boundary use:

- `can_answer` separates current catalog-level responses from unsupported future content questions.
- `must_missing_evidence` correctly marks absent content/model evidence cases.
- `risk_of_overclaim` highlights where the Agent is likely to overstate capability.
- Future rules are correctly represented as `no / yes / high`.

Hermes should adopt the file as a prompt/tool-description source, not as runtime capability proof.

## DWG Boundary

DWG questions about layer, title block, external reference, block attribute, annotation, coordinate, geometry, or drawing content require `dwg_parse_evidence`.

Current Hermes answer policy:

- It may answer only from catalog metadata such as file name, project, discipline, source view, lifecycle status, and safe identifiers.
- It must not infer drawing content from file name, directory path, drawing number, manifest presence, or preview status.
- It must return Missing Evidence for content-level questions.

## RVT Boundary

RVT questions about Level, Grid, Sheet, View, Family, Type, model elements, schedules, internal model structure, or model content require `rvt_parse_evidence`.

Current Hermes answer policy:

- It may report catalog-visible model asset metadata.
- It must not claim model internals are searchable or understood.
- It must return Missing Evidence for model-content questions.

## BIM Component Boundary

BIM component questions about parameters, component lists, LOD/LOI, component existence, component count, equipment attributes, or model element semantics require `component_evidence` or `manual_evidence`.

Current Hermes answer policy:

- It may say the platform currently has only catalog/model-file metadata.
- It must state content-level retrieval is not supported when component evidence is absent.
- It must not treat `component_index_status=NOT_REQUIRED` as complete or searchable component indexing.

## Permission, Path, And Conflict Safety

Hermes should fail closed when `project_scope`, permission proof, or trusted requester context is missing.

Safety rules:

- Raw `storage_path`, NAS path, SMB URI, absolute filesystem path, or raw row data must not be exposed.
- Path evidence should be redacted or represented by safe asset identifiers.
- Field conflicts between directory, file name, metadata, manifest, and platform records require human or platform source confirmation.
- `updated_at` is not NAS file mtime.
- `process_status` is not semantic index status.
- `checksum=null` does not mean unchanged.
- `component_index_status=NOT_REQUIRED` does not mean component index is complete or searchable.

## Overclaim Risks

1. Some shared docs still contain `Hermes / Jarvis`. Hermes should remain the official Agent name; Jarvis should be treated as legacy / non-official wording.
2. Naming, discipline, stage, drawing number, and model number checks are directory-level clues, not compliance conclusions.
3. Manifest existence is not formal delivery-package completeness.
4. Preview status cannot replace DWG / RVT / BIM content parsing.
5. Catalog metadata must not be converted into document evidence or semantic search evidence.
6. Future standard rules must not be presented as current Hermes capabilities.

## Standardized Answer Templates

### DWG Missing Evidence

> I can see catalog metadata for this DWG asset, but I do not have `dwg_parse_evidence` for its layer, title block, xref, block attribute, annotation, coordinate, or drawing content. Current evidence is catalog-only, so this question requires Missing Evidence / manual review.

### RVT Missing Evidence

> I can see catalog metadata for this RVT model asset, but I do not have `rvt_parse_evidence` for Level, Grid, Sheet, View, Family, Type, or model internals. Current evidence is catalog-only, so this question requires Missing Evidence / manual review.

### BIM Component Missing Evidence

> I do not have `component_evidence` or `manual_evidence` for component existence, parameters, LOD/LOI, or component lists. Current Hermes retrieval does not support content-level BIM component lookup from this evidence set.

### Permission Missing / Fail Closed

> I do not have trusted project scope or permission proof for this request. Hermes must fail closed and cannot return catalog details or evidence for this asset.

### Field Conflict

> The available catalog fields conflict. Directory, filename, manifest, and platform metadata are not sufficient to decide the authoritative value. This requires human or platform source confirmation.

### Raw Path Redaction

> The source contains a storage path or NAS path, but raw paths are sensitive and cannot be exposed. I can refer only to safe asset identifiers, redacted path hints, or approved catalog fields.

## Recommended Next Steps

1. Later update Hermes prompt and tool descriptions to use the standardized Missing Evidence / fail-closed templates.
2. Consider a shared-doc follow-up to replace `Hermes / Jarvis` wording with official Hermes naming and mark Jarvis as legacy / non-official.
3. Keep these shared docs as a contract source for Agent boundary design.
4. Do not change runtime behavior in Phase 2.98.
5. Do not enter Phase 2.99 until Codex B reviews this boundary record and the docs baseline is complete.

## Runtime Boundary Confirmation

This phase did not:

- modify runtime code
- modify shared standard files
- connect to DB / NAS / platform API / Hermes API
- run frontend / Gateway smoke
- invoke parser, writer, scratch copy, reindex, backfill, repair, cleanup, delete, or migration
- write `documents`, `document_versions`, `chunks`, `citations`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes long-term memory
- enter production rollout
