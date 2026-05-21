# NEXT_CODEX_A_PROMPT

## Phase 2.112 Natural Import Workspace Retrieval Fix Review Handoff

Codex A has completed the bounded implementation for Phase 2.112. Do not repeat the implementation automatically.

## Current Status

- Natural import success without explicit alias now generates a deterministic safe alias.
- Successful import can persist session file alias state as `alias_bound`.
- Same-session `@alias` resolution carries `document_id` and `version_id` filters for scoped retrieval.
- Natural import success response is re-rendered after alias persistence, so diagnostics no longer stay at `alias_seeded`.
- Bounded fuzzy file discovery currently scans only session aliases, returns safe candidates, and suppresses ordinary retrieval when clarification is needed.

## Verification Already Run

```text
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py run_agent.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
```

Result: `97 passed`.

## Next Required Step

Codex B should review the Phase 2.112 diff before any Git baseline.

Review scope:

```text
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/natural_file_import_flow.py
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/natural_file_import_runtime.py
/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py
/Users/Weishengsu/.hermes/hermes-agent/run_agent.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_flow.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_runtime.py
/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py
```

## Required Codex C Validation After Review

Run one authorized small-file natural import through the real OpenWebUI / 8642 path and verify:

```text
natural_import_detected=true
real_upload_enabled=true
upload_adapter_status=executed
ingestion_status=upload_succeeded
document_id present
version_id present
alias_resolution.status=alias_bound or alias_resolved
same-session @alias retrieval_evidence_document_ids=[imported document_id]
citation present
third_document_contamination=false
```

## Hard Boundaries

Do not:

1. Run real upload unless the user explicitly authorizes the exact file path.
2. Store file alias bindings as ordinary long-term memory text.
3. Treat import diagnostics or upload metadata as retrieval evidence.
4. Scan NAS, folders, or multiple files.
5. Modify platform Gateway / DB / NAS Data Steward contracts.
6. Execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
7. Baseline without Codex B review and explicit user authorization.

## Expected Outcome

If Codex B review passes, prepare a Codex C validation prompt. Only after real validation passes should Phase 2.112 be considered ready for Git baseline.
