# Phase 2.96 Gateway Controlled Smoke Result Review

## 1. Scope

This phase is docs-only / report-review only.

It reviews the latest Frontend / Gateway controlled smoke report returned by the platform side. It does not rerun smoke, connect to Gateway, connect to DB / NAS / Hermes API, implement Gateway code, run parsers, invoke writers, write indexes, or enter rollout.

Previous baseline:

- commit: `3d70626`
- tag: `phase-2.95-shared-contract-alignment-baseline`
- pushed: true

## 2. Review Decision

Decision: `Go` for read-only controlled Gateway smoke.

The report is accepted as evidence that the limited read-only Gateway smoke path passed the required product gates under normal platform authentication.

This decision does not authorize production rollout.

## 3. Auth Path Reviewed

The smoke used the normal platform authorization flow:

1. `POST /api/core/auth/login`: `200`
2. `POST /api/core/projects/{PROJECT_ID}:switch`: `200`
3. Subsequent Gateway requests used a project-scoped bearer token.

The reviewed path did not rely on bypassed authentication or client-trusted project scope.

## 4. Endpoints Covered

Covered endpoints and behaviors:

1. `/api/data-steward/hermes/capabilities`: `200 pass`
2. `/api/data-steward/hermes/health`: `200 pass`
3. `/api/data-steward/chat`: `200 pass`
4. `/api/data-steward/catalog/search`: `200 pass`
5. `/api/agent/hermes/chat`: `200 pass`
6. invalid project permission denied: `200 pass`, fail closed
7. catalog-only content question: `200 pass`, Missing Evidence / `asset_catalog_only`

The two most important product gates that passed are:

1. permission-denied behavior fails closed
2. catalog-only content questions return Missing Evidence / `asset_catalog_only`

## 5. Forbidden-field Scan

The report found no forbidden-field leak:

1. no true secret / token / password / bearer / credential value
2. no NAS path, `/Volumes`, `nas://`, or `smb://`
3. no raw row, SQL, storage path, or raw file content
4. safe status field `secretPrinted=false` is not a leak

This review preserves the existing red line: true `storage_path`, raw row, NAS path, raw content, secret, token, bearer, and credential material must not be exposed.

## 6. Side-effect Flags

Reported side effects:

1. DB write: no
2. NAS scan/copy: no
3. parser: no
4. writer: no
5. OpenSearch / Qdrant / MinIO write: no
6. rollout: no

No runtime mutation is authorized by this review.

## 7. What This Go Authorizes

This `Go` authorizes only this conclusion:

1. the read-only controlled Gateway smoke report is accepted as passing
2. the reviewed Gateway path can be treated as ready for the next docs-only internal trial runbook phase
3. Phase 2.97 may plan a bounded Frontend Gateway Read-only Trial Runbook / Operator Checklist

## 8. What This Go Does Not Authorize

This `Go` does not authorize:

1. production rollout
2. Agent DB CRUD
3. Agent-generated SQL
4. NAS scan/copy
5. parser invocation
6. scratch copy
7. writer smoke against real DB
8. writing `documents`, `document_versions`, `chunks`, or `citations`
9. OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory writes
10. treating catalog metadata as content evidence
11. DWG / RVT / BIM content understanding
12. exposing true `storage_path`, raw row, NAS path, raw content, secret, token, bearer, or credential material
13. repair / cleanup / backfill / reindex / delete / migration
14. entering rollout

## 9. Remaining Caveats

1. The report is still a controlled smoke result, not a production readiness certificate.
2. Gateway behavior must remain fail-closed on permission-denied requests.
3. Catalog search remains catalog-only metadata lookup; it is not file content retrieval.
4. Missing Evidence must remain the required response for catalog-only content questions.
5. Any future runtime trial must stay read-only unless separately planned, reviewed, and explicitly authorized.

## 10. Recommended Next Step

Recommended next phase:

```text
Phase 2.97 Frontend Gateway Read-only Trial Runbook / Operator Checklist
```

The next phase should remain docs-only. It should create an operator checklist for a limited internal frontend trial and must explicitly remain separate from production rollout.

## 11. Runtime Boundary Confirmation

During this Phase 2.96 review, Codex A did not:

1. run frontend / Gateway smoke again
2. implement Gateway code
3. connect to real DB / platform API / Hermes API
4. perform Agent DB CRUD
5. generate or execute SQL
6. scan/copy NAS
7. invoke parser / writer / scratch copy
8. write documents / chunks / citations / indexes / object store
9. read DWG / RVT / NWD / IFC content
10. execute repair / cleanup / backfill / reindex / delete / migration
11. enter production rollout
