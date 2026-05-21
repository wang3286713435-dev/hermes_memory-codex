# Phase 2.112c OpenWebUI Alias Continuity Fix Plan

## 1. Background

Phase 2.112b fixed the development-machine alias hydration path, but the real Mac mini / OpenWebUI / 8642 validation still paused.

Latest test-machine evidence:

```text
backend_port: 8642
backend_health: pass
real_upload_flag_visible_to_backend: true
source_file_preflight: exists / regular / small_lt_1mb / suffix=.xlsx

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

This means upload and indexing are no longer the blocker. The blocker is the OpenAI-compatible chat path losing or failing to recover the alias continuity needed for the next user turn.

## 2. Working Root-cause Hypothesis

The current runtime relies on one of these conditions:

1. A stable `X-Hermes-Session-Id` or equivalent session key is available across turns.
2. The follow-up request includes previous assistant diagnostics in conversation history.

The real OpenWebUI / 8642 path appears not to provide enough stable session/history context for Phase 2.112b hydration to fire reliably. As a result:

1. Natural import succeeds and initially reports `alias_bound`.
2. Follow-up `@建筑类数据样表` arrives as a new or under-contextualized request.
3. The in-memory/session alias map is not restored.
4. Retrieval is suppressed as `alias_missing=true`.

## 3. Phase 2.112c Goal

Codex A should implement the smallest safe runtime fix that preserves alias continuity for real OpenWebUI / 8642 usage.

Required outcome:

1. Natural import success stores an alias continuity record outside ordinary long-term memory.
2. A follow-up `@alias` query in the OpenAI-compatible path resolves to the imported `document_id/version_id` even when the previous assistant diagnostics are not present.
3. If the same alias maps to multiple possible documents, Hermes must fail closed and ask the user to choose from safe candidates.
4. Retrieval evidence must still come only from actual retrieval chunks; import diagnostics, metadata, and alias continuity records are not answer evidence.

## 4. Allowed Implementation Scope

Allowed files / modules in the Hermes agent repo:

1. `gateway/platforms/api_server.py`
2. `run_agent.py`
3. `agent/memory_kernel/session_document_scope.py`
4. `agent/memory_kernel/natural_file_import_runtime.py`
5. `agent/memory_kernel/natural_file_import_flow.py`
6. Targeted tests for API-server chat continuity, natural import runtime, session document scope, and OpenAI-compatible request simulation.
7. Hermes agent docs / TODO / DEV_LOG.

Allowed design options:

1. Persist a local alias-continuity registry keyed by the safest available request/session signal.
2. Prefer explicit `X-Hermes-Session-Id` when present.
3. If OpenWebUI provides a stable conversation/user/thread identifier in request metadata, use it after sanitization.
4. If no reliable session key exists, use a bounded local alias registry with TTL and conflict detection.
5. Emit sanitized diagnostics such as `alias_continuity_status`, `alias_continuity_source`, `api_session_key_source`, and `history_message_count`.

## 5. Hard Boundaries

Forbidden:

1. Do not store aliases in ordinary long-term memory as text.
2. Do not treat import diagnostics or alias-continuity registry entries as retrieval evidence.
3. Do not answer from upload metadata.
4. Do not expose raw file paths, file content, secrets, tokens, raw DB rows, or raw storage locators.
5. Do not scan NAS or folders.
6. Do not write DB / facts / document_versions / OpenSearch / Qdrant / MinIO.
7. Do not execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
8. Do not modify platform Gateway / DB / NAS contracts.
9. Do not broaden DWG/RVT/BIM content claims.

## 6. Required Tests

Codex A should add or update targeted tests for:

1. Import turn stores alias continuity after successful upload/index.
2. Follow-up request with only the latest user message and no previous assistant diagnostics resolves the alias.
3. Follow-up request with OpenAI-compatible session drift resolves an unambiguous alias safely.
4. Conflicting alias candidates suppress retrieval and ask for clarification.
5. Alias continuity records never become retrieval evidence.
6. `metadata_as_answer=false`, `facts_as_answer=false`, `snapshot_as_answer=false`, `transcript_as_fact=false`.
7. No raw path / secret / raw content appears in diagnostics or answer.
8. Existing natural import / upload client / session scope tests still pass.

## 7. Verification Commands

Suggested minimum verification in the Hermes agent repo:

```bash
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q
```

Codex A should locate and run any existing gateway/API-server tests that cover `gateway/platforms/api_server.py`; if none exist, add a small targeted test for OpenAI-compatible alias continuity.

## 8. Acceptance Criteria

Development-machine acceptance:

1. py_compile passes.
2. Targeted natural import / session / gateway tests pass.
3. The fix is selectively staged; unrelated dirty files are excluded.
4. Codex A stops for Codex B review and does not run real import.

Test-machine acceptance:

1. 8642 backend health is pass.
2. `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true`.
3. Import succeeds with `document_id/version_id/chunk_count/indexed_count`.
4. Follow-up `@alias` resolves with `alias_missing=false`.
5. `retrieval_suppressed=false`.
6. `retrieval_evidence_document_ids` contains only the imported document.
7. Citation is present.
8. No forbidden action or data leak occurs.

## 9. Closeout Decision

Phase 2 full closeout remains blocked until Phase 2.112c passes real OpenWebUI / 8642 alias + retrieval + citation validation, or the user explicitly moves natural import usability out of Phase 2.
