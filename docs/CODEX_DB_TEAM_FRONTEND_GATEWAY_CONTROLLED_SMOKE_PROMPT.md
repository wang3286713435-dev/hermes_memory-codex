# Codex C / DB Team Prompt: Frontend Gateway Controlled Smoke

## Purpose

Run a future read-only controlled smoke for the platform frontend / Gateway Hermes integration.

This prompt is a handoff artifact only until the operator explicitly authorizes the smoke. It must not be treated as production rollout approval.

## Scope

Validate that the platform Gateway and frontend-facing Hermes entrypoints expose only sanitized, permission-aware, catalog-only responses.

Allowed once separately authorized:

1. Read-only HTTP requests against the provided platform Gateway base URL.
2. Sanitized response inspection.
3. Forbidden-field negative scans.
4. Permission-denied and Missing Evidence behavior checks.
5. Final report generation with redacted excerpts only.

Forbidden:

1. Direct database access, SQL, DB CRUD, migrations, repair, cleanup, delete, backfill, reindex.
2. Direct NAS access, NAS scan, scratch copy, parser invocation, writer smoke.
3. OpenSearch / Qdrant / MinIO / object-store / platform DB / Hermes memory writes.
4. Reading DWG / RVT / NWD / IFC content.
5. Exposing true storage paths, raw rows, NAS paths, raw file content, secrets, tokens, bearer values, or credentials.
6. Production rollout or enabling Agent final-answer integration from catalog rows.

## Required Placeholders

Fill these before any smoke. If any required placeholder is missing, stop with `Pause`.

```text
PLATFORM_REPO_PATH=<PLATFORM_REPO_PATH>
PLATFORM_BRANCH_OR_COMMIT=<PLATFORM_BRANCH_OR_COMMIT>
ENV_LABEL=<ENV_LABEL>
GATEWAY_BASE_URL=<GATEWAY_BASE_URL>
REQUESTER_ID=<REQUESTER_ID>
TENANT_ID=<TENANT_ID>
PROJECT_ID_OR_SCOPE=<PROJECT_ID_OR_SCOPE>
FILE_ID=<FILE_ID>
MODEL_ID=<MODEL_ID>
SOURCE_VIEW=<SOURCE_VIEW>
```

Rules:

1. Use a non-production or explicitly approved controlled environment.
2. Do not paste secrets, bearer tokens, cookies, raw credentials, internal storage paths, or private rows into this report.
3. Treat `PROJECT_ID_OR_SCOPE` as an input to the Gateway only if the server derives or validates the effective permission scope. Frontend-provided `project_scope` must not be trusted.
4. Keep all response excerpts short and sanitized.

## Pre-flight

Before requests:

1. Confirm target branch / commit and environment label.
2. Confirm no pending platform changes are required by this smoke.
3. Confirm the Gateway base URL is not production unless separately authorized.
4. Confirm no direct DB, NAS, Hermes API, parser, writer, index, object-store, or production tool access is being used.
5. Confirm the report destination is local and sanitized.

## Endpoint Case Matrix

| Case | Request | Goal | Expected Safe Result |
|---|---|---|---|
| capabilities | `GET /api/data-steward/hermes/capabilities` | Confirm user-facing Hermes naming and safe capability disclosure | Uses Hermes naming; no raw/internal endpoints or secrets |
| health | `GET /api/data-steward/hermes/health` | Confirm read-only health surface | Status only; no storage paths, raw rows, credentials |
| chat | `POST /api/data-steward/chat` | Confirm Gateway-mediated chat path | Safe fields present; catalog-only content is Missing Evidence |
| catalog search | `POST /api/data-steward/catalog/search` | Confirm catalog metadata preview only | Safe catalog identifiers only; no raw paths/content |
| compatibility | `POST /api/agent/hermes/chat` | Confirm compatibility route is safe or deprecated | No unsafe fields; no raw/internal leakage |
| permission denied | configured denied request | Confirm fail-closed permission behavior | `permission_decision=DENIED` or equivalent; no unauthorized data |
| catalog-only content question | DWG / RVT / BIM content question | Confirm catalog rows are not used as content evidence | Missing Evidence / `asset_catalog_only`; no model-content claims |

## Safe Response Fields

Expected safe fields may include:

1. `query_id`
2. `trace_id`
3. `file_id`
4. `model_id`
5. `source_view`
6. `permission_decision`
7. `missingEvidence`
8. `evidenceMode`
9. Hermes user-facing naming

These fields are diagnostic only. Their presence does not authorize content ingestion or Agent answer integration.

## Forbidden-field Scan

Scan every response body, error body, trace body, and frontend-visible payload for:

```text
storage_path
storage_uri
storagePath
storageUri
/Volumes
nas://
smb://
raw row
raw_row
SQL
select *
insert into
update
delete from
token
secret
bearer
password
credential
raw file content
true NAS path
generated executable SQL
executable write action
repair action
ingestion action
```

If any forbidden field appears, mark the result `No-Go`.

## Permission-denied Requirements

For a denied request:

1. The Gateway must fail closed.
2. The response must expose `permission_decision=DENIED` or a clearly equivalent status.
3. The response must not include unauthorized catalog metadata, document text, path hints, model internals, raw row data, or storage locations.
4. The response may include a sanitized denial reason and `query_id` / `trace_id`.
5. Any unauthorized data leakage is `No-Go`.

## Catalog-only DWG / RVT / BIM Content-question Requirements

For questions that require DWG / RVT / NWD / IFC model content:

1. Do not infer BIM components, drawing contents, object properties, room data, dimensions, quantities, or design details from catalog metadata.
2. Do not treat a catalog row as document evidence or citation.
3. Return Missing Evidence semantics:
   - `status=missing_evidence` or equivalent
   - `evidenceMode=missing_evidence`
   - `missingEvidence` includes `asset_catalog_only`
4. The answer may say that only catalog metadata is available.
5. Any content-level claim from catalog metadata is `No-Go`.

## Go / Pause / No-Go

### Go

All of the following hold:

1. All endpoint cases return safe, sanitized results.
2. Permission-denied behavior is fail-closed.
3. Catalog-only content questions return Missing Evidence / `asset_catalog_only`.
4. No forbidden fields appear.
5. No DB / NAS / parser / writer / index / object-store / rollout side effects occur.
6. Safe fields are present or the report clearly explains equivalent fields.

### Pause

Use `Pause` when:

1. A safe field is missing but no leak occurred.
2. Trace ids or response schema are incomplete but sanitized.
3. Environment placeholders are incomplete.
4. The route exists but behavior is ambiguous.
5. Additional DB team clarification is needed before runtime decisions.

### No-Go

Use `No-Go` when:

1. Any forbidden field appears.
2. Frontend-provided `project_scope` is trusted without server-side permission derivation or validation.
3. Catalog metadata is treated as BIM / DWG / RVT / NWD / IFC content evidence.
4. Denied requests leak metadata, content, paths, raw rows, or internals.
5. Any write, repair, ingestion, parser, NAS scan, index/object-store write, or rollout occurs.
6. Secrets, tokens, bearer values, or credentials appear in output.

## Final Report Template

```markdown
# Frontend / Gateway Controlled Smoke Report

## Run Context

- platform repo path:
- branch / commit:
- env label:
- gateway base URL:
- requester / tenant:
- project or scope:
- run timestamp:

## Endpoint Status

| Case | Endpoint | Status | HTTP | Safe fields present | Notes |
|---|---|---|---|---|---|
| capabilities |  | pass / pause / fail |  |  |  |
| health |  | pass / pause / fail |  |  |  |
| chat |  | pass / pause / fail |  |  |  |
| catalog search |  | pass / pause / fail |  |  |  |
| compatibility |  | pass / pause / fail |  |  |  |
| permission denied |  | pass / pause / fail |  |  |  |
| catalog-only content question |  | pass / pause / fail |  |  |  |

## Forbidden-field Scan

| Surface | Result | Matched forbidden fields | Notes |
|---|---|---|---|
| response bodies | pass / fail |  |  |
| error bodies | pass / fail |  |  |
| frontend-visible payloads | pass / fail |  |  |
| traces | pass / fail |  |  |

## Permission-denied Result

- permission decision:
- fail-closed: yes / no
- unauthorized data leaked: yes / no
- sanitized excerpt:

## Missing Evidence / Catalog-only Result

- status:
- evidenceMode:
- missingEvidence:
- content claims made: yes / no
- catalog row used as evidence: yes / no

## Write / Side-effect Flags

| Side effect | Occurred |
|---|---|
| DB write | no |
| NAS scan/copy | no |
| parser invocation | no |
| writer smoke | no |
| OpenSearch write | no |
| Qdrant write | no |
| MinIO/object-store write | no |
| rollout | no |

## Final Decision

- decision: Go / Pause / No-Go
- reason:
- follow-up:
```

## Stop Rule

If the smoke encounters DB write, NAS scan, parser invocation, writer invocation, index/object-store write, raw path leak, secret leak, unauthorized data leak, or rollout behavior, stop immediately and report `No-Go`.
