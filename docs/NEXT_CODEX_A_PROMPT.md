# NEXT_CODEX_A_PROMPT

## Phase 2.112e Runtime Candidate Review Passed

Status: Codex B review passed. Do not run more development in Codex A unless test-machine validation returns a new blocker.

## Current Runtime Candidate

Hermes agent:

```text
commit: 091fd7414
tag: phase-2.112e-api-server-owner-bridge-runtime-test-candidate
remote: backup2
```

## What Changed

1. Natural import alias continuity remains owner-scoped; alias-global restore is still forbidden.
2. API server now passes stable owner into `AIAgent` when available.
3. Accepted stable owner sources:
   - `X-Hermes-Session-Id`
   - `X-OpenWebUI-Conversation-Id`
   - `X-OpenWebUI-Chat-Id`
   - `X-Conversation-Id`
4. Raw owner values are not returned in diagnostics; `SessionDocumentScopeStore` hashes owner values before trace / persistence.
5. Missing stable owner still fails closed with `stable_owner_missing`.

## Verification

Codex B re-ran:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_chat_session_id_drifts_when_openwebui_sends_only_latest_user_message tests/gateway/test_api_server.py::test_gateway_session_key_prefers_accepted_hermes_session_header tests/gateway/test_api_server.py::test_gateway_session_key_accepts_whitelisted_openwebui_conversation_header tests/gateway/test_api_server.py::test_gateway_session_key_ignores_non_whitelisted_request_headers tests/gateway/test_api_server.py::test_create_agent_passes_gateway_session_key_to_ai_agent tests/gateway/test_api_server.py::test_chat_completions_passes_accepted_session_header_as_stable_owner tests/gateway/test_api_server.py::test_chat_completions_passes_openwebui_conversation_header_as_stable_owner -q
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
```

Results:

1. py_compile passed.
2. API server owner bridge targeted tests: `7 passed`.
3. Natural import / upload client / session scope regression: `106 passed`.
4. Local same-owner drift reproduction restored `@alias` without raw owner leakage.

## Next Required Action

Test-machine Codex should:

1. checkout `phase-2.112e-api-server-owner-bridge-runtime-test-candidate` in `/Users/hermes/code/hermes-agent`;
2. keep Hermes_memory at the current reviewed handoff baseline or update only if required by the test-machine prompt;
3. restart 8642 Hermes backend with natural import real upload flag enabled;
4. run real OpenWebUI / 8642 validation:
   - natural-language import of the authorized small sample;
   - `@alias` follow-up retrieval;
   - retrieval evidence contains only imported `document_id`;
   - citation is visible and manually checkable;
   - no facts/metadata/snapshot/transcript substitutes evidence;
   - no third-document contamination;
   - no raw path/secret/token/raw row/content leakage.

## Hard Boundaries

Do not:

1. continue Codex A implementation without a new blocker;
2. repeat real import on the development machine;
3. write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
4. scan NAS or folders;
5. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
6. stage unrelated dirty files;
7. announce Phase 2 full closeout before real OpenWebUI / 8642 validation passes.
