# NEXT_CODEX_A_PROMPT

## Phase 2.112f Alias Continuity Restore Fix

You are Codex A for the Hermes natural-language import closeout line.

Work in:

```text
/Users/Weishengsu/.hermes/hermes-agent
```

Do not work in the platform repo. Do not run real OpenWebUI / 8642 import on the development machine.

## Why This Exists

Phase 2.112e did not pass the real test-machine OpenWebUI / 8642 validation.

Latest test-machine evidence:

```text
explicit_alias_import: pass
import_alias_status: alias_bound
import alias continuity: stored
follow-up @建筑类数据样表 retrieval: fail
retrieval_alias_status: alias_missing
alias_missing: true
retrieval_suppressed: true
retrieval_evidence_document_ids: []
citation_present: false
```

Follow-up diagnostics showed that import stored owner-scoped continuity, but follow-up alias-missing retrieval did not restore it and did not expose alias-continuity diagnostics.

Root cause category:

```text
hermes_alias_store_restore_bug
```

## Must Read First

Read:

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112F_ALIAS_CONTINUITY_RESTORE_FIX.md`
2. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112E_API_SERVER_STABLE_OWNER_BRIDGE_FIX.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112D_ALIAS_CONTINUITY_SCOPE_REVIEW_FIX.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112C_OPENWEBUI_ALIAS_CONTINUITY_FIX_PLAN.md`
5. Hermes agent `run_agent.py`
6. Hermes agent `agent/memory_kernel/session_document_scope.py`
7. Hermes agent natural import runtime / flow files
8. Existing targeted tests under `tests/agent/` and `tests/gateway/`

## Task

Implement the smallest safe fix so that:

1. Successful natural import still stores alias continuity under the safe owner key.
2. Follow-up `@alias` resolution attempts owner-scoped continuity restore when normal alias resolution returns `alias_missing`.
3. Follow-up alias-missing responses always include sanitized diagnostics:
   - `alias_continuity_status`
   - `alias_continuity_owner_source`
   - `alias_continuity_persistent`
   - `stable_owner_missing`
4. If restore succeeds, retrieval must be scoped to the imported `document_id/version_id`.
5. If restore cannot safely happen, retrieval remains suppressed.

## Preserve These Safety Rules

1. No alias-global restore.
2. No ordinary long-term memory alias persistence.
3. No raw owner/header/session values in diagnostics.
4. No cross-owner restore.
5. No restore on conflict, expired candidate, stale candidate, or missing stable owner.
6. Import diagnostics are still not retrieval evidence.
7. Facts / metadata / snapshot / transcript still cannot replace retrieval evidence.

## Allowed Files

Modify only the minimum required files, likely:

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

If additional files are necessary, explain why in your final handoff.

## Required Tests

Run:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_chat_session_id_drifts_when_openwebui_sends_only_latest_user_message tests/gateway/test_api_server.py::test_gateway_session_key_prefers_accepted_hermes_session_header tests/gateway/test_api_server.py::test_chat_completions_passes_accepted_session_header_as_stable_owner -q
```

Add/update tests for:

1. same-owner import -> follow-up `@alias` restore;
2. alias-missing branch emits `alias_continuity_*` diagnostics;
3. stable owner missing still fail-closed;
4. cross-owner restore denied;
5. conflicting candidates denied;
6. restored retrieval filters include only imported `document_id/version_id`.

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
3. whether follow-up alias restore is covered by tests;
4. whether alias-continuity diagnostics are emitted on follow-up alias-missing;
5. any excluded dirty files;
6. whether Codex B review is needed.

Stop after the bounded fix. Do not tag or push unless explicitly requested by Codex B/user.
