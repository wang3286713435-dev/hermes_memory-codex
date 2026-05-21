# NEXT_CODEX_A_PROMPT

## Phase 2.112e API Server Stable Owner Bridge Fix

Codex B reviewed Phase 2.112d and found one remaining blocker. Execute this one bounded fix, then stop for Codex B review.

## Required Reading

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112D_ALIAS_CONTINUITY_SCOPE_REVIEW_FIX.md`
2. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112E_API_SERVER_STABLE_OWNER_BRIDGE_FIX.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

Then inspect `/Users/Weishengsu/.hermes/hermes-agent`.

## Review Finding

Phase 2.112d owner-scoped continuity is safer, but it does not yet satisfy the real OpenWebUI / 8642 blocker because the API server path does not pass a stable owner into `AIAgent`.

Observed:

```text
gateway/platforms/api_server.py::_create_agent(...)
AIAgent(..., session_id=session_id, platform="api_server", ...)
```

There is no `gateway_session_key`. When OpenWebUI sends only the latest user message, the derived `api-*` session id can drift. Then Phase 2.112d falls back to `process_local_fallback`, which is safe but cannot restore the imported alias across the drift.

## Required Fix

Add a bounded stable-owner bridge for the API server path:

1. Pass a stable `gateway_session_key` or equivalent continuity owner to `AIAgent` when an authenticated stable session / conversation id is available.
2. Prefer existing `X-Hermes-Session-Id` when accepted by the API server.
3. If adding additional OpenWebUI-compatible stable conversation headers, explicitly whitelist and sanitize them.
4. Do not use volatile request ids, timestamps, raw body text, aliases, raw tokens, raw paths, or secrets as continuity owner.
5. If no stable owner exists, keep fail-closed behavior and return sanitized diagnostics like `stable_owner_missing`.
6. Preserve Phase 2.112d owner-scope / TTL / conflict safety. Do not reintroduce alias-global restore.

## Allowed Files

Allowed Hermes agent files:

1. `gateway/platforms/api_server.py`
2. `run_agent.py` only if needed for diagnostics / owner handling
3. `agent/memory_kernel/session_document_scope.py` only if needed for diagnostics; do not weaken owner-scope safety
4. Targeted tests under `tests/gateway/` and `tests/agent/`
5. Hermes agent `docs/TODO.md` / `docs/DEV_LOG.md`

Do not stage unrelated dirty files:

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`

## Required Tests

Add or update tests proving:

1. API server passes an explicit stable owner key to `AIAgent`.
2. Same explicit owner restores `@alias` after API-derived session drift.
3. Different explicit owners do not restore each other’s aliases.
4. Without stable owner, follow-up remains fail-closed with sanitized `stable_owner_missing` diagnostics.
5. No raw owner value, token, path, secret, raw row, or content appears in diagnostics.
6. Existing Phase 2.112d TTL / stale / conflict tests still pass.

Suggested commands:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_chat_session_id_drifts_when_openwebui_sends_only_latest_user_message -q
```

If you add new API-server owner bridge tests, run them explicitly too.

## Completion Report

Report:

1. Changed files.
2. Which stable owner headers / sources are accepted.
3. How raw owner values are sanitized or hashed.
4. What happens when stable owner is missing.
5. Tests run and results.
6. Whether Codex B review is required.
7. Whether test-machine validation is still required.

## Hard Boundaries

Do not:

1. repeat real import in development;
2. write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
3. scan NAS or folders;
4. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
5. modify platform Gateway / DB / NAS contracts;
6. stage unrelated dirty files;
7. create runtime baseline/tag without Codex B review;
8. announce Phase 2 full closeout before real OpenWebUI / 8642 validation passes.
