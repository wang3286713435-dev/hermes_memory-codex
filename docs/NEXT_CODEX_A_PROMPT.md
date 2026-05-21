# NEXT_CODEX_A_PROMPT

## Phase 2.112d Alias Continuity Scope Review Fix

Codex B reviewed Phase 2.112c and found one blocker. Execute this one bounded fix, then stop for Codex B review.

## Required Reading

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112C_OPENWEBUI_ALIAS_CONTINUITY_FIX_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112D_ALIAS_CONTINUITY_SCOPE_REVIEW_FIX.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

Then inspect `/Users/Weishengsu/.hermes/hermes-agent`.

## Review Finding

Phase 2.112c tests pass, but the implementation stores continuity candidates keyed only by alias:

```text
_alias_continuity: dict[alias, list[FileAliasBinding]]
_continuity_candidates(alias)
```

This is too broad. A globally unique alias could restore a document imported by another session/user/project. That violates the bounded enterprise-agent safety model.

## Required Fix

Narrow alias continuity so it is scoped by a safe owner key:

1. Prefer explicit stable session / conversation / gateway scope when available.
2. If no stable owner key exists, fallback must be short-lived and process-local.
3. Persisted storage must not restore unscoped fallback aliases across process restart.
4. Different continuity owners must not restore each other’s imported alias.
5. Add TTL / stale cleanup or equivalent expiration.
6. Keep conflict behavior fail-closed and retrieval-suppressed.
7. Keep alias continuity records non-evidence.

## Allowed Files

Allowed Hermes agent files:

1. `agent/memory_kernel/session_document_scope.py`
2. `run_agent.py`
3. `agent/memory_kernel/natural_file_import_runtime.py` only if diagnostics need a small update
4. Targeted tests under `tests/agent/` and `tests/gateway/`
5. Hermes agent `docs/TODO.md` / `docs/DEV_LOG.md`

Do not stage unrelated dirty files:

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`

## Required Tests

Add or update tests proving:

1. Same continuity owner can restore `@alias` after API-derived session drift.
2. Different continuity owner cannot restore another owner’s `@alias`.
3. Unscoped fallback continuity is not persisted across a new store load.
4. TTL/stale continuity does not restore.
5. Alias conflict still suppresses retrieval and asks for clarification.
6. Diagnostics do not expose raw session tokens, paths, secrets, raw rows, or content.

Suggested commands:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_chat_session_id_drifts_when_openwebui_sends_only_latest_user_message -q
```

If you add a new targeted gateway/session-owner test, run it explicitly too.

## Completion Report

Report:

1. Changed files.
2. How continuity owner key is computed.
3. Which fallback is process-local / non-persistent.
4. TTL/stale behavior.
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
7. announce Phase 2 full closeout before real OpenWebUI / 8642 validation passes.
