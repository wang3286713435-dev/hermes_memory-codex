# Phase 2.92 Read-only Gateway Acceptance Plan

## 1. Summary

Phase 2.92 defines the Hermes-side acceptance gates for the database platform team's read-only frontend Gateway integration.

This phase consumes the database team's sanitized review result for `hermes-readonly-frontend-gateway-access-review.md` and turns it into a bounded mainline checklist. It does not implement the Gateway in this repository, does not connect to the platform DB, does not read NAS files, and does not enable Agent answer integration.

Current decision:

```yaml
gateway_integration_track: allowed
allowed_scope: read_only_frontend_gateway
agent_name: Hermes
production_rollout: false
db_crud: false
sql_generation_by_agent: false
nas_scan: false
dwg_rvt_content_understanding: false
documents_chunks_index_write: false
```

## 2. Previous Baseline

Phase 2.91 Runtime Evidence Writer Smoke Gate baseline is complete:

- commit: `cf89e1e`
- tag: `phase-2.91-runtime-evidence-writer-smoke-gate-baseline`
- pushed: true

Phase 2.91 created a gate-only runtime writer smoke path. It still does not authorize real developer DB writes, Mac mini DB writes, parser execution, scratch copy, NAS scan, OpenSearch / Qdrant / MinIO writes, platform DB writes, or Agent answer integration.

## 3. Source Inputs

Primary source input:

- Database team sanitized access review: `hermes-readonly-frontend-gateway-access-review.md`
- Existing Hermes-side integration doc: `docs/DB_TEAM_HERMES_FRONTEND_GATEWAY_INTEGRATION_V3.md`
- Risk boundary: `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`

Relevant accepted database-team conclusion:

1. Gateway integration is Go only for read-only frontend access.
2. Platform backend should own the Gateway; frontend must not directly call raw Hermes internals.
3. The visible product name must be Hermes / Hermes 数据管家, not Jarvis / 贾维斯.
4. `project_scope` / permission proof must be generated server-side by the platform backend, not trusted from frontend input.
5. Catalog-only metadata is not document evidence and cannot answer DWG / RVT / NAS content questions.

## 4. Allowed Scope

Allowed for the database platform team:

1. Add a platform backend Gateway for Hermes read-only access.
2. Add platform-side health / capabilities checks for Hermes.
3. Add read-only catalog metadata preview backed by `FileAssetView` / `ModelAssetView` / safe REST equivalents.
4. Add a frontend Hermes panel or assistant entry point.
5. Rename visible product copy to `Hermes` / `Hermes 数据管家`.
6. Generate server-side `project_scope` / permission proof before calling Hermes.
7. Include sanitized `query_id`, `trace_id`, `file_id`, `model_id`, `source_view`, `permission_decision`, and `missing_evidence` fields in Gateway responses.
8. Add read-only audit trace for Gateway requests, excluding secrets, raw rows, raw NAS paths, and raw file content.

Allowed for Hermes Memory mainline:

1. Review Gateway reports and schemas.
2. Keep docs / contracts / prompts aligned.
3. Add future tests only when a bounded Hermes-side adapter or validation helper is explicitly approved.
4. Keep all DB / NAS / writer / parser / Agent answer feature flags default-off.

## 5. Hard Boundaries

Still forbidden in Phase 2.92:

1. Agent DB CRUD.
2. Agent-generated SQL.
3. Direct frontend-to-Hermes raw internal access.
4. Frontend-supplied `project_scope` treated as trusted permission proof.
5. Returning true `storage_path`, `storage_uri`, raw row, raw file name, secret, or NAS path to frontend.
6. Scanning NAS.
7. Reading DWG / RVT / NWD / IFC model contents.
8. Claiming BIM component-level understanding.
9. Treating catalog metadata as document evidence.
10. Writing `documents`, `document_versions`, `chunks`, `citations`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes long-term memory.
11. Running runtime evidence writer smoke against real DB.
12. Parser invocation, scratch copy, or raw content extraction.
13. Repair, cleanup, backfill, reindex, delete, migration, or production rollout.

## 6. P0 Acceptance Gates

The Gateway integration must Pause or No-Go if any P0 fails:

1. Visible UI text still uses `Jarvis` / `贾维斯` as the product name.
2. Frontend directly calls Hermes raw/internal endpoints instead of the platform backend Gateway.
3. Frontend sends `project_scope` and backend treats it as trusted.
4. Gateway response includes true `storage_path`, `storage_uri`, raw NAS path, raw row, raw file content, secret, or credential material.
5. Hermes or Gateway answers content-level questions about DWG / RVT / BIM models from catalog metadata alone.
6. Any request path writes platform DB, Hermes DB, `documents/chunks`, OpenSearch, Qdrant, MinIO, or long-term memory.
7. Any Agent path performs SQL generation, DB CRUD, NAS scan, repair, cleanup, backfill, reindex, delete, migration, or rollout.
8. Permission proof is missing and behavior is not fail-closed `DENIED`.

## 7. P1 Acceptance Gates

P1 issues do not always block a docs-only review, but they block calling the integration user-ready:

1. `operationPlan` / `request_evidence_ingestion_review` appears as executable action instead of draft / human-review-only.
2. `/api/agent/hermes/*` is exposed as a public frontend contract instead of internal / compatibility path.
3. `catalog_only` questions do not clearly separate catalog metadata from content evidence.
4. Missing Evidence is hidden or softened when the user asks for file content that has not been ingested.
5. Query response lacks stable `query_id` / `trace_id` for future feedback and audit.
6. Catalog result lacks stable `file_id` / `model_id` / `source_view`.
7. Permission-denied result is not explainable to the user in safe, non-sensitive language.

## 8. P2 / Backlog Gates

P2 items can be tracked after the first read-only Gateway milestone:

1. Feedback endpoint design.
2. Frontend-side progressive disclosure for catalog-only vs evidence-backed answers.
3. User education copy for DWG / RVT / BIM limitations.
4. Optional screenshot / UX review.
5. Future feature flags for evidence ingestion review request.
6. Future adapter tests for Gateway schema compatibility.

## 9. Expected Database Team Report

When the database team returns implementation results, the report should include:

1. Changed files.
2. Endpoint list and route ownership.
3. Frontend entry point and visible naming audit.
4. Whether frontend direct Hermes calls exist.
5. Permission proof generation location.
6. Response schema sample with sanitized field names only.
7. Forbidden field scan result.
8. Test results for health, catalog preview, permission deny, Missing Evidence, and capability boundary.
9. Confirmation no real `storage_path`, raw row, secret, NAS path, DWG / RVT content, DB write, NAS scan, or rollout occurred.
10. Go / Pause / No-Go decision.

## 10. Next Phase Candidates

Recommended next phase after Phase 2.92 baseline:

1. Phase 2.93: Review database team's read-only Gateway implementation report.
2. Phase 2.94: Add Hermes-side Gateway schema compatibility tests, only if needed.
3. Phase 2.95: Plan controlled frontend user flow smoke, still read-only and no Agent DB CRUD.

Do not jump directly to DB CRUD, NAS semantic indexing, evidence write runtime execution, or production rollout.

## 11. Database Team Initial Return

Database team has returned an initial sanitized read-only Gateway implementation report.

Reported completed:

1. Frontend user-facing copy was renamed to `Hermes` / `Hermes 数据管家` / `问 Hermes`.
2. Backend `capabilities.agentName` now returns `Hermes`.
3. Audit action naming moved from `agent.jarvis.*` to `agent.hermes.*`.
4. `frontend/`, `backend/delivery-data-steward/`, and focused scripts report no user-facing `贾维斯` / `Jarvis` / `jarvis` residue.
5. `/api/agent/hermes/*` is marked internal / compatibility only.
6. Frontend capabilities now call `/api/data-steward/hermes/capabilities`.
7. Frontend catalog preview no longer sends trusted `project_scope`; it sends ordinary `projectFilters`, while trusted `project_scope` is generated by the platform backend Gateway.
8. Gateway endpoint smoke passed for capabilities, health, chat, catalog search, and compatibility chat.
9. Focused script result: `PASS=11 FAIL=0`.
10. Forbidden-field assertions passed for `storage_path`, `storage_uri`, `storagePath`, `storageUri`, `/Volumes`, `nas://`, `smb://`, raw row, SQL fragment, token, secret, and bearer.
11. Content-level questions return `status=missing_evidence`, `evidenceMode=missing_evidence`, and `missingEvidence` containing `asset_catalog_only`.
12. Backend build, frontend build, health check, and `git diff --check` passed on the database platform side.

Preliminary Hermes-side assessment:

```yaml
phase_2_92_gate_result: provisionally_go
reason: reported result satisfies the major P0 gates defined in this plan
requires_phase_2_93_review: true
production_rollout: false
agent_db_crud: false
nas_scan: false
content_ingestion: false
```

This report should be reviewed in Phase 2.93 before any broader user-facing pilot or Hermes-side schema compatibility work.
