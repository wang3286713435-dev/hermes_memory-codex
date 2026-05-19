# Phase 2.97 Frontend Gateway Read-only Trial Runbook / Operator Checklist

## 1. Scope

This runbook defines a limited internal frontend trial for the Platform Frontend / Gateway read-only Hermes Data Steward integration.

It is not a production rollout plan. It is not a smoke execution report. It does not authorize Gateway code changes, Agent DB CRUD, Agent-generated SQL, NAS scan/copy, parser invocation, writer execution, index/object-store writes, or production release.

Previous baseline:

- commit: `6fff43f`
- tag: `phase-2.96-gateway-controlled-smoke-result-review-baseline`
- pushed: true

## 2. Purpose

The trial verifies that a small set of internal users can use the frontend Gateway path for read-only Data Steward / Hermes catalog interactions while preserving safety boundaries:

1. project-scoped authentication
2. catalog-only evidence boundary
3. permission-denied fail-closed behavior
4. forbidden-field redaction
5. no runtime writes or side effects
6. Missing Evidence behavior for content-level DWG / RVT / BIM questions

## 3. Non-goals

This trial does not include:

1. production rollout
2. unrestricted user access
3. Agent DB CRUD
4. Agent-generated SQL
5. NAS scan/copy
6. parser invocation
7. scratch copy
8. writer smoke against real DB
9. writing `documents`, `document_versions`, `chunks`, or `citations`
10. OpenSearch / Qdrant / MinIO / platform DB / Hermes memory writes
11. DWG / RVT / NWD / IFC content reading
12. treating catalog metadata as file content evidence
13. exposing true storage path / NAS path / raw row / raw content / secret / token
14. repair / cleanup / backfill / reindex / delete / migration

## 4. Trial Users / Roles

Allowed trial participants:

1. internal operator
2. product reviewer
3. frontend reviewer
4. platform Gateway reviewer
5. Hermes reviewer

All trial users must understand that this is a read-only internal trial and must not use it to validate production release.

## 5. Environment Labels And Reviewed Refs

Each trial run must record:

1. environment label: `internal_readonly_trial`
2. frontend build ref
3. platform Gateway backend ref
4. Hermes_memory baseline ref: `6fff43f`
5. Hermes_memory baseline tag: `phase-2.96-gateway-controlled-smoke-result-review-baseline`
6. project id label or sanitized project alias
7. operator name
8. trial timestamp

Raw secrets, bearer token values, true storage paths, NAS paths, raw rows, and raw file content must not be recorded.

## 6. Authentication Path

Required auth path:

1. normal platform login
2. project switch
3. project-scoped bearer token
4. Gateway request using the project-scoped token

The frontend must not be trusted as the source of `project_scope`. The backend Gateway must generate or validate project scope server-side.

## 7. Allowed Endpoints

Allowed endpoints:

1. `GET /api/data-steward/hermes/capabilities`
2. `GET /api/data-steward/hermes/health`
3. `POST /api/data-steward/chat`
4. `POST /api/data-steward/catalog/search`
5. `POST /api/agent/hermes/chat` only if compatibility route is still needed

No endpoint may be used for mutation, repair, ingestion, index writing, file parsing, NAS scanning, or production rollout.

## 8. Allowed Query Types

Allowed query categories:

1. asset catalog lookup
2. file/model/project metadata filtering
3. safe capability / health checks
4. catalog-only boundary explanations
5. permission-denied behavior checks
6. content-level DWG / RVT / BIM questions that must return Missing Evidence / `asset_catalog_only`

Disallowed query categories:

1. requests to read file content from catalog metadata
2. requests to expose raw storage path or NAS location
3. requests to parse DWG / RVT / NWD / IFC content
4. requests to write, repair, delete, reindex, backfill, ingest, or copy files
5. requests to create long-term Hermes memory from NAS content

## 9. Required Response Checks

For each query, record whether the response contains:

1. `query_id` if available
2. `trace_id` if available
3. safe `file_id`
4. safe `model_id`
5. safe `source_view`
6. `permission_decision`
7. `evidenceMode`
8. `missingEvidence`
9. no raw storage path / URI
10. no raw row / SQL / raw file content

If `query_id` or `trace_id` is unavailable, the trial may continue only if review remains possible through other safe correlation fields. If traceability is blocked, mark `Pause`.

## 10. Forbidden-field Scan Checklist

Scan every response for:

1. true secret value
2. true token value
3. password
4. bearer credential value
5. `storage_path`
6. `storage_uri`
7. `storagePath`
8. `storageUri`
9. `/Volumes`
10. `nas://`
11. `smb://`
12. raw row
13. SQL fragment
14. raw file content
15. DWG / RVT internal content claims based only on catalog metadata

Any true leak is `No-Go`.

Safe boolean/status fields such as `secretPrinted=false` are not leaks if they do not reveal secret values.

## 11. Side-effect Checklist

Each trial run must record:

1. DB write: `no`
2. NAS scan/copy: `no`
3. parser: `no`
4. writer: `no`
5. OpenSearch / Qdrant / MinIO write: `no`
6. Hermes memory write of NAS content: `no`
7. rollout: `no`

Any unexpected write or side effect is `No-Go`.

## 12. Operator Checklist Before Trial

Before starting:

1. confirm this is an internal read-only trial
2. confirm reviewed refs are recorded
3. confirm users and roles are approved for trial scope
4. confirm no production rollout is being attempted
5. confirm no repair / backfill / reindex / delete / migration task is attached
6. confirm no raw secrets, bearer token values, storage paths, NAS paths, raw rows, or raw file content will be copied into the report
7. confirm trial questions are limited to allowed query types
8. confirm operator knows Go / Pause / No-Go criteria

## 13. Per-query Recording Template

```text
trial_id:
timestamp:
operator:
user_role:
environment_label:
frontend_ref:
gateway_ref:
hermes_memory_ref:
endpoint:
query:
expected_behavior:
http_status:
permission_decision:
evidenceMode:
missingEvidence:
query_id:
trace_id:
safe_file_ids:
safe_model_ids:
source_view:
forbidden_field_scan:
side_effect_flags:
decision: Go | Pause | No-Go
notes:
```

Do not record raw bearer tokens, raw paths, raw rows, SQL, or raw file content.

## 14. Go / Pause / No-Go Criteria

### Go

Go only if:

1. login and project switch work
2. Gateway endpoints return safe schemas
3. permission-denied request fails closed
4. catalog-only content question returns Missing Evidence / `asset_catalog_only`
5. no forbidden fields are exposed
6. no writes or side effects occur

### Pause

Pause if:

1. auth/session is unstable
2. safe identifiers are missing
3. trace/query IDs are missing in a way that blocks review
4. Missing Evidence copy is ambiguous
5. compatibility route behavior diverges from main Gateway route
6. operators cannot classify the response safely

### No-Go

No-Go if:

1. true secret/token/password/bearer/credential leaks
2. true storage path / NAS path / raw row / SQL / raw content leaks
3. denied request exposes catalog data
4. catalog metadata is presented as file content evidence
5. Hermes claims to understand DWG / RVT / BIM content from catalog-only evidence
6. any DB write, NAS scan/copy, parser, writer, index/object-store write, or rollout occurs

## 15. Feedback Capture Fields

Capture feedback as sanitized text:

1. trial_id
2. user_role
3. endpoint
4. query category
5. decision: Go / Pause / No-Go
6. issue severity: P0 / P1 / P2
7. sanitized issue summary
8. missing safe field
9. forbidden field category if any
10. copy / UX concern
11. recommended follow-up phase

Do not write feedback directly to Hermes long-term memory.

## 16. Escalation Rules

P0 escalation:

1. any secret / token / bearer / credential leak
2. any true storage path / NAS path / raw row / SQL / raw content leak
3. denied request exposes catalog data
4. any write side effect occurs
5. catalog metadata is presented as content evidence

P1 escalation:

1. Missing Evidence copy is ambiguous
2. trace/query ids absent and review is blocked
3. compatibility route diverges from main Gateway route
4. safe identifiers are inconsistent
5. frontend labels imply DWG / RVT content understanding when only catalog metadata is available

P2 escalation:

1. UX wording polish
2. latency concern without safety impact
3. optional trace enrichment
4. non-blocking copy improvements

## 17. Final Trial Summary Template

```text
trial_id:
date:
operator:
participants:
environment_label:
frontend_ref:
gateway_ref:
hermes_memory_ref:
cases_total:
cases_go:
cases_pause:
cases_no_go:
permission_denied_result:
catalog_only_missing_evidence_result:
forbidden_field_scan_result:
side_effect_result:
top_issues:
decision: Go | Pause | No-Go
recommended_next_step:
```

## 18. Authorization Boundary

Even if this trial returns Go, it authorizes only continued read-only internal trial usage under the same boundary.

It does not authorize:

1. production rollout
2. mutation endpoints
3. Agent DB CRUD
4. Agent-generated SQL
5. NAS scan/copy
6. content ingestion
7. parser/writer/index/object-store writes
8. DWG / RVT / BIM content understanding
9. raw storage path exposure
10. repair / migration / cleanup / delete / backfill / reindex

Any broader access requires a separate phase, separate review, and explicit authorization.
