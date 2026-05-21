# NEXT_CODEX_A_PROMPT

## Phase 2.112c OpenWebUI Alias Continuity Fix

You are Codex A for the Hermes agent runtime. Execute one bounded implementation step, then stop for Codex B review.

## Required Reading

Read these files first:

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112_NATURAL_IMPORT_WORKSPACE_RETRIEVAL_FIX_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/PHASE2112C_OPENWEBUI_ALIAS_CONTINUITY_FIX_PLAN.md`
3. `/Users/Weishengsu/Hermes_memory/docs/CODEX_TEST_MACHINE_PHASE2112_NATURAL_IMPORT_VALIDATION_PROMPT.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
7. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

Then inspect the Hermes agent repo at `/Users/Weishengsu/.hermes/hermes-agent`.

## Current Runtime Evidence

The Phase 2.112b candidate was correctly checked out on the test machine:

```text
Hermes_memory: e459b5a / phase-2.112b-runtime-candidate-handoff-baseline
hermes-agent: 1d02a791 / phase-2.112b-natural-import-alias-runtime-test-candidate
8642 restarted to current hermes-agent code
both worktrees clean
```

The real OpenWebUI / 8642 smoke still paused:

```text
explicit_alias_import: partial
document_id: 2baf5527-42c9-4467-8856-573e54c97121
version_id: b2efc465-cde8-4aef-a113-5c8615929719
chunk_count: 6
indexed_count: 6
alias_status: import initially alias_bound; follow-up alias_missing

same_session_retrieval: fail
alias_missing: true
retrieval_suppressed: true
retrieval_evidence_document_ids: []
citation_present: false
```

Interpretation: upload/index succeeded; the remaining blocker is OpenAI-compatible / OpenWebUI alias continuity across turns.

## Goal

Implement the smallest safe runtime fix so that a successful natural import can be retrieved by `@alias` in the real OpenWebUI / 8642 path even when previous assistant diagnostics are not included in follow-up request history.

## Required Behavior

1. Natural import success stores a bounded alias-continuity record outside ordinary long-term memory.
2. Follow-up `@alias` resolves to the imported `document_id/version_id` when unambiguous.
3. If the alias is ambiguous, Hermes must suppress retrieval and ask the user to choose from safe candidates.
4. Import diagnostics, metadata, and alias-continuity records must never become answer evidence.
5. Retrieval answers still require citation-bearing retrieval evidence.
6. Add sanitized diagnostics for alias continuity, for example:
   - `alias_continuity_status`
   - `alias_continuity_source`
   - `api_session_key_source`
   - `history_message_count`

## Allowed Files

You may modify only bounded Hermes agent runtime/docs/tests needed for this fix:

1. `gateway/platforms/api_server.py`
2. `run_agent.py`
3. `agent/memory_kernel/session_document_scope.py`
4. `agent/memory_kernel/natural_file_import_runtime.py`
5. `agent/memory_kernel/natural_file_import_flow.py`
6. Targeted tests under `tests/agent/` and gateway/API-server tests if needed.
7. Hermes agent `docs/TODO.md` / `docs/DEV_LOG.md`.
8. Hermes_memory phase docs only if needed for handoff sync.

Do not stage unrelated dirty files such as adapter trace polish, repo hygiene notes, or dependency lockfile changes unless this task directly requires them and Codex B can review them.

## Required Tests

Add or update tests proving:

1. Import turn stores alias continuity after successful upload/index.
2. Follow-up request with only the latest user message and no previous assistant diagnostics resolves the alias.
3. OpenAI-compatible session drift does not break an unambiguous alias.
4. Conflicting alias candidates suppress retrieval and produce clarification.
5. Alias continuity records are not retrieval evidence.
6. No raw path, secret, raw file content, raw DB row, or raw storage locator appears in diagnostics/output.
7. Existing natural import / upload client / session scope tests still pass.

Suggested commands:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
```

Also locate and run any existing gateway/API-server tests relevant to `gateway/platforms/api_server.py`. If none exist, add and run a small targeted test for OpenAI-compatible alias continuity.

## Hard Boundaries

Do not:

1. Repeat real import in development.
2. Store alias as ordinary long-term memory text.
3. Treat import diagnostics or metadata as retrieval evidence.
4. Write DB / facts / document_versions / OpenSearch / Qdrant / MinIO.
5. Scan NAS or folders.
6. Execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
7. Modify platform Gateway / DB / NAS contracts.
8. Expose raw paths, file content, secrets, tokens, raw DB rows, or raw storage locators.
9. Claim DWG/RVT/BIM content understanding.

## Completion Report

Stop after one bounded fix and report:

1. Changed files.
2. Root-cause summary.
3. How alias continuity is keyed and fail-closed.
4. Tests run and results.
5. Whether a new runtime test-candidate tag is recommended.
6. Whether Codex B review is required.
7. Whether test-machine validation is required.
