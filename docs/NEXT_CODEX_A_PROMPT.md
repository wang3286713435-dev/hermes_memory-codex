# NEXT_CODEX_A_PROMPT

## Phase 2.112b Natural Import Alias Binding / Retrieval Blocker Fix

Codex A is the development agent. Execute one bounded fix in `/Users/Weishengsu/.hermes/hermes-agent`.

Codex B has reviewed the previous Phase 2.112 targeted tests, but the real OpenWebUI -> 8642 validation paused. Do not baseline the previous implementation.

## Latest Test-machine Evidence

The test-machine operator Codex ran one authorized small-file natural import through OpenWebUI / 8642:

```text
backend_port=8642
real_upload_enabled=true
upload_adapter_status=executed
ingestion_status=upload_succeeded
document_id=6e89bbe8-599f-47e3-9cca-d8e7b7ae4f1b
version_id=0df440d0-9f2b-4fd5-8a84-19435fdd1b2f
chunk_count=6
indexed_count=6
```

The import succeeded, but alias / retrieval failed:

```text
title bind result=alias_bind_failed
follow-up @建筑类数据样表 retrieval alias_missing=true
retrieval_suppressed=true
citation not verifiable
```

Conclusion: import / indexing path is working; the blocker is the alias persistence / title alias binding / same-session scoped retrieval chain.

## Goal

Fix the runtime path so that a successful natural import creates a reliable same-session file alias and makes immediate follow-up retrieval work through the alias.

The user-facing target is:

```text
User: 帮我导入这个文件。
Hermes: 文件我已经记下了，别名我设定为：@xxx。
User: 围绕 @xxx 总结文件内容。
Hermes: resolves @xxx -> imported document_id/version_id -> retrieves citation-bearing evidence.
```

## Required Behavior

1. Natural import success with explicit alias must persist a session alias as `alias_bound`.
2. Natural import success without alias must generate and report one safe deterministic alias.
3. Title-derived alias binding must not return `alias_bind_failed` when `document_id/version_id` are already known from import success.
4. Follow-up `@alias` in the same OpenWebUI / 8642 conversation must resolve to the imported `document_id/version_id`.
5. Follow-up retrieval must set `retrieval_suppressed=false` when the imported alias is available.
6. Follow-up retrieval must scope to the imported `document_id/version_id`, not broad search.
7. Alias persistence must not rely on ordinary long-term memory quota.
8. Import diagnostics / upload metadata must not become retrieval evidence.
9. If scoped retrieval still returns no chunks, Hermes must return honest Missing Evidence and include diagnostics, not hallucinate content.

## Suggested Investigation

Trace the actual OpenAI-compatible 8642 path from import response to alias resolution:

```text
run_agent.py
agent/memory_kernel/natural_file_import_flow.py
agent/memory_kernel/natural_file_import_runtime.py
agent/memory_kernel/session_document_scope.py
```

Look specifically for:

1. alias normalization differences between `建筑类数据样表` and `@建筑类数据样表`;
2. session ID / conversation state not being carried across OpenWebUI requests;
3. alias state written to one store but read from another;
4. title binding path ignoring known `document_id/version_id`;
5. retrieval suppression being triggered before imported alias resolution.

## Allowed Files

Only modify files needed for this blocker:

```text
/Users/Weishengsu/.hermes/hermes-agent/run_agent.py
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/natural_file_import_flow.py
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/natural_file_import_runtime.py
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_flow.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_runtime.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py
```

If another file is required, stop and report why before editing it.

Do not include existing unrelated dirty files in this phase:

```text
/Users/Weishengsu/.hermes/hermes-agent/uv.lock
/Users/Weishengsu/.hermes/hermes-agent/docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_memory_kernel_adapter_reload.py
```

## Required Tests

Add or update tests that fail on the current Pause behavior:

1. successful import + explicit alias -> `alias_bound`;
2. follow-up `@alias` -> `alias_resolved`;
3. follow-up alias retrieval does not set `retrieval_suppressed=true`;
4. retrieval scope includes imported `document_id/version_id`;
5. alias persistence does not require ordinary memory write;
6. import diagnostics are not accepted as content evidence;
7. auto alias is generated and works when alias omitted.

Run:

```text
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py run_agent.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
```

## Hard Boundaries

Do not:

1. Repeat real import from this development task.
2. Use ordinary long-term memory text as file alias storage.
3. Treat import diagnostics, metadata, or upload success as retrieval evidence.
4. Scan NAS, folders, or multiple files.
5. Modify platform Gateway / DB / NAS Data Steward contracts.
6. Write DB / facts / document_versions / OpenSearch / Qdrant / MinIO.
7. Execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
8. Baseline or push runtime changes before Codex B review and test-machine validation.

## Completion Report

Report:

```text
files changed:
tests added/updated:
py_compile result:
targeted pytest result:
root cause:
how alias_bind_failed is prevented:
how alias_missing/retrieval_suppressed is prevented:
ordinary memory required for alias: true/false
ready for Codex B review: yes/no
```

Stop after the bounded fix. Do not proceed to baseline or Phase 2.113.
