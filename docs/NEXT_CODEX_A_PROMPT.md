# NEXT_CODEX_A_PROMPT

## Phase 2.112g Header-only Stable Owner Restore Fix

You are Codex A for the Hermes natural-language import closeout line.

Work in:

```text
/Users/Weishengsu/.hermes/hermes-agent
```

Do not work in the platform repo. Do not run real OpenWebUI / 8642 import on the development machine.

## Why This Exists

Phase 2.112f did not pass the real test-machine OpenWebUI / 8642 validation.

2.112f successfully surfaced continuity diagnostics, but the actual same-session follow-up restore still failed.

Latest test-machine evidence:

```text
explicit_alias_import: pass
document_id: 2baf5527-42c9-4467-8856-573e54c97121
version_id: b2efc465-cde8-4aef-a113-5c8615929719
chunk_count: 6
indexed_count: 6
import_alias_status: alias_bound
import_alias_missing: false
import_alias_continuity_status: stored
import_alias_continuity_owner_source: gateway_session_key
import_alias_continuity_persistent: true

same_session_retrieval: fail
retrieval_alias_status: alias_missing
alias_missing: true
retrieval_suppressed: true
retrieval_evidence_document_ids: []
citation_present: false
retrieval_alias_continuity_status: stored
retrieval_alias_continuity_owner_source: gateway_session_key
retrieval_alias_continuity_persistent: true
retrieval_stable_owner_missing: true
```

Codex B diagnosis:

```text
2.112f fixed diagnostics propagation, but not the actual restore.
The likely blocker is header-only stable owner extraction:
follow-up requests may carry X-Hermes-Session-Id only as a header, with no accepted body session_id.
_gateway_session_key_from_headers(..., accepted_session_id=None) does not currently treat X-Hermes-Session-Id as a fallback stable owner header.
```

## Must Read First

Read:

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112G_HEADER_ONLY_STABLE_OWNER_RESTORE_FIX.md`
2. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112F_ALIAS_CONTINUITY_RESTORE_FIX.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112E_API_SERVER_STABLE_OWNER_BRIDGE_FIX.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112D_ALIAS_CONTINUITY_SCOPE_REVIEW_FIX.md`
5. Hermes agent `gateway/platforms/api_server.py`
6. Hermes agent `run_agent.py`
7. Hermes agent `agent/memory_kernel/session_document_scope.py`
8. Existing targeted tests under `tests/gateway/` and `tests/agent/`

## Task

Implement the smallest safe fix so that `X-Hermes-Session-Id` is accepted as a stable owner source even when it is present only as a request header and `accepted_session_id` is not provided.

Required behavior:

1. Body/session accepted id `abc` and header-only `X-Hermes-Session-Id: abc` must resolve to the same safe owner identity.
2. Import turn using accepted session id and follow-up turn using header-only `X-Hermes-Session-Id` must restore the same owner-scoped alias continuity record.
3. Follow-up `@建筑类数据样表` restore must return `alias_resolution.status=alias_resolved`.
4. Restore success must set `alias_missing=false`, `retrieval_suppressed=false`, and scoped filters to the imported `document_id/version_id`.
5. Restore success must not include `stable_owner_missing=true`.
6. Missing stable owner, cross-owner, expired, stale, and conflict cases must continue to fail closed.

## Preserve These Safety Rules

1. No alias-global restore.
2. No ordinary long-term memory alias persistence.
3. No raw owner/header/session/token/path/file content in diagnostics.
4. No cross-owner restore.
5. No restore on conflict, expired candidate, stale candidate, or missing stable owner.
6. Import diagnostics are still not retrieval evidence.
7. Facts / metadata / snapshot / transcript still cannot replace retrieval evidence.

## Allowed Files

Modify only the minimum required files, likely:

1. `gateway/platforms/api_server.py`
2. `tests/gateway/test_api_server.py`
3. `tests/agent/test_session_document_scope.py`
4. `tests/agent/test_natural_file_import_runtime.py`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`

If additional files are necessary, explain why in your final handoff.

## Required Tests

Run:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py -q
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
```

Add/update tests for:

1. header-only `X-Hermes-Session-Id` generates the same effective stable owner behavior as accepted `session_id`;
2. import accepted-session turn -> follow-up header-only turn restores alias continuity;
3. restored decision has `alias_missing=false`, no `stable_owner_missing`, and scoped `document_id/version_id`;
4. missing stable owner still fail-closes;
5. cross-owner restore denied;
6. conflict/expired candidates denied.

## Hard Prohibitions

Do not:

1. run real upload/import on the development machine;
2. connect to production or test-machine DB;
3. write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
4. scan NAS or folders;
5. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
6. modify platform repo;
7. stage unrelated dirty files;
8. claim Phase 2 natural import closeout before test-machine OpenWebUI / 8642 retrieval + citation passes.

## Final Report Required

Report:

1. changed files;
2. tests run and exact results;
3. whether header-only `X-Hermes-Session-Id` is now accepted as stable owner;
4. whether follow-up alias restore is covered by tests;
5. whether restore success avoids `stable_owner_missing=true`;
6. any excluded dirty files;
7. whether Codex B review is needed.

Stop after the bounded fix. Do not tag or push unless explicitly requested by Codex B/user.
