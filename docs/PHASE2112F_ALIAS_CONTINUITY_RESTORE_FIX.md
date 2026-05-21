# Phase 2.112f Alias Continuity Restore Fix

## 1. Status

Phase 2.112e did not pass the real OpenWebUI / 8642 natural import validation.

The test-machine retry confirmed:

1. `hermes-agent` was on `091fd741` / `phase-2.112e-api-server-owner-bridge-runtime-test-candidate`.
2. Hermes Memory was on `phase-2.112b-runtime-candidate-handoff-baseline`.
3. 8642 health passed.
4. `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` was visible to the backend.
5. Explicit alias import succeeded and reported `alias_bound`.
6. Follow-up `@建筑类数据样表` retrieval returned `alias_missing=true` and `retrieval_suppressed=true`.

## 2. New Diagnostic Finding

The follow-up read-only diagnostic reported:

1. Request header name `X-Hermes-Session-Id` was present.
2. `X-OpenWebUI-Conversation-Id`, `X-OpenWebUI-Chat-Id`, and `X-Conversation-Id` were not present.
3. Import response included:
   - `api_session_key_source=gateway_session_key`
   - `alias_continuity_status=stored`
   - `alias_continuity_owner_source`
   - `alias_continuity_persistent`
4. Import response did not show `stable_owner_missing`.
5. Follow-up response included:
   - `alias_resolution.status=alias_missing`
   - `alias_missing=true`
   - `retrieval_suppressed=true`
6. Follow-up response did not include:
   - `alias_continuity_status`
   - `alias_continuity_owner_source`
   - `alias_continuity_persistent`
   - `stable_owner_missing`

## 3. Root Cause Category

The current best root-cause category is:

```text
hermes_alias_store_restore_bug
```

This is no longer primarily a missing stable-owner-header issue. The import side stored owner-scoped continuity, but the follow-up alias-missing branch did not restore it or did not surface the restore diagnostics.

## 4. Codex A Objective

Codex A must implement a bounded Phase 2.112f fix in `hermes-agent`:

1. Ensure follow-up `@alias` resolution attempts owner-scoped alias continuity restore when normal alias resolution returns `alias_missing`.
2. Ensure the restore path uses the same safe owner key semantics as the import store path.
3. Ensure follow-up alias-missing responses always expose sanitized alias-continuity diagnostics:
   - `alias_continuity_status`
   - `alias_continuity_owner_source`
   - `alias_continuity_persistent`
   - `stable_owner_missing`
4. Preserve fail-closed behavior:
   - no stable owner -> suppress retrieval;
   - conflicting continuity candidates -> suppress retrieval and ask for clarification;
   - expired / stale continuity -> suppress retrieval;
   - no candidate -> suppress retrieval.
5. Do not reintroduce alias-global restore.

## 5. Allowed Files

Codex A may modify only the minimum necessary files in `/Users/Weishengsu/.hermes/hermes-agent`, likely:

1. `run_agent.py`
2. `agent/memory_kernel/session_document_scope.py`
3. `agent/memory_kernel/natural_file_import.py`
4. `agent/memory_kernel/natural_file_import_flow.py`
5. `agent/memory_kernel/natural_file_import_runtime.py`
6. `tests/agent/test_session_document_scope.py`
7. `tests/agent/test_natural_file_import_runtime.py`
8. `tests/gateway/test_api_server.py`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

If Codex A needs additional files, it must justify the need in the handoff.

## 6. Required Tests

Codex A must run targeted tests only:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_chat_session_id_drifts_when_openwebui_sends_only_latest_user_message tests/gateway/test_api_server.py::test_gateway_session_key_prefers_accepted_hermes_session_header tests/gateway/test_api_server.py::test_chat_completions_passes_accepted_session_header_as_stable_owner -q
```

Add or update tests proving:

1. Import stores owner-scoped continuity with `gateway_session_key`.
2. Follow-up latest-user-only `@alias` restores the stored document/version using the same owner.
3. Follow-up alias-missing path emits sanitized continuity diagnostics even when no restore happens.
4. Missing stable owner still fails closed.
5. Cross-owner restore remains denied.
6. Conflicting candidates remain fail-closed.

## 7. Hard Boundaries

Do not:

1. repeat real import on the development machine;
2. use ordinary long-term memory as alias persistence;
3. restore by alias globally;
4. write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
5. scan NAS or folders;
6. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
7. output raw owner values, raw paths, tokens, secrets, file contents, or raw rows;
8. stage unrelated dirty files.

## 8. Exit Criteria

Codex A stops after:

1. implementing the minimum code fix;
2. running required targeted tests;
3. updating Hermes agent TODO / DEV_LOG;
4. reporting changed files, test results, excluded dirty files, and whether Codex B review is needed.

Codex A must not create the final runtime baseline. Codex B will review first.
