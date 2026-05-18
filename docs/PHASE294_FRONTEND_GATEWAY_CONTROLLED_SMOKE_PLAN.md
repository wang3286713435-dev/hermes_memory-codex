# Phase 2.94 Frontend / Gateway Controlled Smoke Plan

## 1. Summary

Phase 2.94 defines a future controlled, read-only frontend / Gateway smoke for the Hermes 数据管家 integration.

This phase is planning only. It does not run the smoke, implement Gateway code, connect to a real database, read NAS content, invoke parsers, write indexes, or enter rollout.

Planning decision:

```yaml
decision: plan_ready
scope: read_only_frontend_gateway_controlled_smoke
runtime_execution: false
production_rollout: false
agent_db_crud: false
nas_scan: false
content_ingestion: false
```

The future smoke may only verify safe Gateway behavior and sanitized response shape. It must not be used as permission to run Agent DB CRUD, SQL generation, NAS scan, evidence ingestion, parser execution, writer smoke, or production rollout.

## 2. Preconditions

Before any future controlled smoke is executed, the operator / database team must provide:

1. Reviewed platform branch / commit.
2. Confirmed target environment name.
3. Gateway base URL or local endpoint, if and only if runtime smoke is separately authorized.
4. Sanitized test project / tenant / requester identifiers.
5. Sanitized catalog fixture identifiers for at least one file and one model asset.
6. A permission-denied test case that does not reveal sensitive data.
7. A catalog-only DWG / RVT / BIM content-level question that must return Missing Evidence.
8. Confirmation that no real `storage_path`, raw row, NAS path, raw file content, secret, token, or credential material is present in expected output.

Required repository state before future smoke:

1. Hermes Memory worktree clean.
2. This plan reviewed by Codex B.
3. Separate explicit runtime prompt issued.
4. Runtime prompt remains read-only.

## 3. Smoke Case Matrix

| Case | Endpoint / flow | Purpose | Expected result | Must not do |
|---|---|---|---|---|
| Capabilities | `GET /api/data-steward/hermes/capabilities` | Verify public Gateway capability path and Hermes naming | `agentName=Hermes` or equivalent visible Hermes naming | Do not call raw/internal Hermes as public contract |
| Health | `GET /api/data-steward/hermes/health` | Verify Gateway liveness | Safe OK / degraded status without secrets | Do not expose env vars, tokens, DB strings, or internal paths |
| Chat | `POST /api/data-steward/chat` | Verify read-only chat path and traceability | Safe response with `query_id` / `trace_id` and no forbidden fields | Do not write DB, memory, indexes, files, or issue SQL |
| Catalog search | `POST /api/data-steward/catalog/search` | Verify catalog preview shape | Safe asset metadata with `file_id` / `model_id` / `source_view` | Do not expose true storage path, raw row, raw content, or NAS URI |
| Compatibility chat | `POST /api/agent/hermes/chat` | Verify internal / compatibility route remains bounded | Compatibility route works or returns safe compatibility response | Do not make it the frontend public contract |
| Permission denied | Gateway request with denied project / requester | Verify fail-closed behavior | `permission_decision=DENIED` or equivalent safe denial | Do not leak why-denied sensitive internals or asset paths |
| Catalog-only content question | Ask content-level DWG / RVT / BIM question from catalog-only asset | Verify no fake content evidence | `status=missing_evidence`, `evidenceMode=missing_evidence`, `missingEvidence` includes `asset_catalog_only` | Do not claim BIM component / drawing content understanding |

## 4. Required Sanitized Inputs

Future smoke must use sanitized inputs only:

1. `requester_id`: non-production test value.
2. `tenant_id` / project id: non-sensitive test value.
3. `projectFilters`: ordinary frontend filters, not trusted permission proof.
4. Server-generated `project_scope`: produced by platform backend Gateway.
5. `file_id` / `model_id`: stable opaque identifiers.
6. `source_view`: safe catalog view name or enum.
7. Queries:
   - capabilities request.
   - health request.
   - safe catalog search.
   - safe chat request.
   - permission-denied request.
   - catalog-only DWG / RVT / BIM content question.

Inputs must not include true NAS paths, local absolute paths, raw database rows, secrets, tokens, or real customer-sensitive content.

## 5. Expected Safe Response Fields

Future smoke should check for these fields where applicable:

1. `query_id`.
2. `trace_id`.
3. `file_id`.
4. `model_id`.
5. `source_view`.
6. `permission_decision`.
7. `missingEvidence`.
8. `evidenceMode`.
9. Visible product name: `Hermes` / `Hermes 数据管家`.

Safe response principles:

1. Identifiers should be opaque and stable.
2. Catalog metadata may describe asset existence, type, size class, version, owner category, or safe source view.
3. Catalog metadata must not be presented as document content evidence.
4. Missing Evidence must be explicit for content-level questions where no ingested evidence exists.

## 6. Forbidden Fields / Negative Assertions

Future smoke must fail if any response contains:

1. `storage_path`.
2. `storage_uri`.
3. `storagePath`.
4. `storageUri`.
5. `/Volumes`.
6. `nas://`.
7. `smb://`.
8. raw row.
9. SQL fragment.
10. token.
11. secret.
12. bearer.
13. raw file content.
14. true NAS path.
15. credential material.
16. generated SQL intended for execution.
17. any write / repair / ingestion action treated as executable.

Recommended negative scan should inspect full JSON response bodies and user-visible frontend text.

## 7. Missing Evidence / `asset_catalog_only` Checks

For catalog-only content questions:

1. Response status must be `missing_evidence` or equivalent.
2. `evidenceMode` must be `missing_evidence` or equivalent.
3. `missingEvidence` must include `asset_catalog_only`.
4. User-visible copy must clearly state that catalog metadata is not file content evidence.
5. The response must not infer DWG / RVT / NWD / IFC internals, BIM components, drawing notes, or model contents.
6. The response must not cite catalog rows as if they were parsed document chunks.

Pass condition:

```yaml
catalog_metadata_as_content_evidence: false
missing_evidence_visible: true
asset_catalog_only_visible: true
```

## 8. Permission-denied Checks

Future smoke must include at least one denied request.

Expected behavior:

1. Denied response is fail-closed.
2. `permission_decision` is `DENIED` or equivalent.
3. Denial copy is user-safe and does not expose sensitive internals.
4. Response does not include asset details that the requester is not allowed to see.
5. Response does not include true paths, raw rows, raw content, or permission policy internals.
6. Denied request does not trigger DB writes, memory writes, index writes, parser execution, NAS scan, repair, or rollout.

No-Go if a denied request returns accessible asset metadata, content evidence, raw paths, or any write-capable action.

## 9. Go / Pause / No-Go Criteria

### Go

All must hold:

1. Capabilities / health / chat / catalog / compatibility cases return safe bounded responses.
2. Visible naming remains Hermes / Hermes 数据管家.
3. `project_scope` is server-generated, not frontend-trusted.
4. Required safe identifiers appear where expected.
5. Forbidden fields are absent.
6. Catalog-only content question returns Missing Evidence / `asset_catalog_only`.
7. Permission-denied case fails closed.
8. No write path is observed or implied.

### Pause

Pause if:

1. Required trace / safe identifier fields are missing but no leak occurs.
2. Permission-denied copy is unclear but does not leak sensitive data.
3. Compatibility route behavior is ambiguous.
4. Missing Evidence copy is present but weak.
5. Smoke output is incomplete or not sufficiently sanitized for review.

### No-Go

No-Go if:

1. Any forbidden field appears.
2. Frontend trusts user-supplied `project_scope`.
3. Raw/internal Hermes endpoint is used as the public frontend contract.
4. Catalog metadata is treated as content evidence.
5. Denied request returns unauthorized asset data.
6. Any DB / memory / index / object-store write occurs.
7. Any parser, NAS scan, scratch copy, repair, cleanup, backfill, reindex, migration, or rollout occurs.
8. Any response exposes secret, token, credential, true NAS path, raw row, or raw file content.

## 10. Handoff Requirements For Codex C / Database Team

If a future runtime smoke is authorized, the handoff must include:

1. Exact platform branch / commit.
2. Gateway base URL and environment label.
3. Sanitized requester / tenant / project identifiers.
4. Sanitized test asset identifiers.
5. Exact curl / frontend steps.
6. Expected safe fields per endpoint.
7. Forbidden-field scan list.
8. Go / Pause / No-Go criteria from this plan.
9. Explicit statement that the smoke is read-only.
10. Explicit statement that smoke results are not production rollout approval.

Codex C / database team report must include:

1. Endpoint results.
2. Sanitized response excerpts.
3. Forbidden-field scan result.
4. Permission-denied result.
5. Missing Evidence / `asset_catalog_only` result.
6. Confirmation no writes / parser / NAS scan / rollout occurred.
7. Final Go / Pause / No-Go recommendation.

## 11. Non-goals

This phase does not:

1. Implement Gateway code.
2. Run actual Gateway smoke.
3. Connect to real DB, NAS, platform API, Hermes API, OpenSearch, Qdrant, MinIO, or production systems.
4. Add Agent DB CRUD.
5. Generate SQL.
6. Scan NAS.
7. Invoke parser.
8. Copy scratch files.
9. Run writer smoke against real DB.
10. Write `documents`, `document_versions`, `chunks`, `citations`, indexes, object store, platform DB, or Hermes long-term memory.
11. Read DWG / RVT / NWD / IFC content.
12. Expose true `storage_path`, raw row, NAS path, raw content, secret, or credential material.
13. Execute repair, cleanup, backfill, reindex, delete, migration, or rollout.

## 12. Recommendation

Recommended next step after Codex B review:

```yaml
next_phase_candidate: Phase 2.94a controlled smoke handoff prompt
default_runtime_execution: false
requires_explicit_authorization: true
codex_c_validation: only_after_authorization
database_team_participation: required_for_platform_endpoint_smoke
```

Do not execute a runtime smoke from this plan alone.
