# Phase 2.112g Header-only Stable Owner Restore Fix

## 1. Background

Phase 2.112f did not pass the test-machine OpenWebUI / 8642 validation.

The 2.112f candidate successfully exposed alias-continuity diagnostics, but it still failed to restore the imported alias in the follow-up turn.

Latest test-machine evidence:

```text
hermes-agent: 78eb7715 / phase-2.112f-alias-continuity-restore-runtime-test-candidate
8642 backend: pass
HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true
Hermes Memory health: pass
worktree: clean

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

## 2. Codex B Diagnosis

Phase 2.112f fixed diagnostics propagation, but not the actual restore path.

The current likely root cause is the OpenAI-compatible API server stable-owner extraction:

1. Import can store alias continuity under `gateway_session_key`.
2. Follow-up requests may carry `X-Hermes-Session-Id` only as a header, without body `session_id`.
3. `_gateway_session_key_from_headers(..., accepted_session_id=None)` currently does not treat `X-Hermes-Session-Id` as a fallback stable owner header.
4. Follow-up restore therefore falls back to `process_local_fallback`, producing `stable_owner_missing=true`.
5. The response can still show stored continuity diagnostics from prior state, but the restore lookup is using a different owner key.

This is a header-only stable owner bridge bug, not an upload, indexing, usage-limit, or generic retrieval bug.

## 3. Required Fix

Codex A should implement the smallest safe fix so that `X-Hermes-Session-Id` works as a stable owner even when it appears only as a request header and `accepted_session_id` is not provided.

Required behavior:

1. Body/session accepted id `abc` and header-only `X-Hermes-Session-Id: abc` must produce the same safe owner identity.
2. Import turn using the accepted session id and follow-up turn using header-only `X-Hermes-Session-Id` must restore the same alias continuity record.
3. Successful restore must return `alias_resolution.status=alias_resolved`.
4. Successful restore must set `alias_missing=false`, `retrieval_suppressed=false`, and scoped filters to the imported `document_id/version_id`.
5. Follow-up restore must not emit `stable_owner_missing=true` when a valid `X-Hermes-Session-Id` header exists.

## 4. Safety Rules

Keep all previous safety boundaries:

1. No alias-global restore.
2. No ordinary long-term memory alias persistence.
3. No raw owner, header, session, token, path, or file content in diagnostics.
4. No cross-owner restore.
5. No restore on conflict, expired candidate, stale candidate, or missing stable owner.
6. Import diagnostics are not retrieval evidence.
7. Facts / metadata / snapshot / transcript cannot replace retrieval evidence.
8. Do not re-run real upload/import on the development machine.

## 5. Expected Code Areas

Likely files:

1. `/Users/Weishengsu/.hermes/hermes-agent/gateway/platforms/api_server.py`
2. `/Users/Weishengsu/.hermes/hermes-agent/tests/gateway/test_api_server.py`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
4. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_runtime.py`
5. `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
6. `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

If other runtime files are touched, Codex A must explain why.

## 6. Required Tests

Codex A must add or update tests for:

1. `_gateway_session_key_from_headers` accepts header-only `X-Hermes-Session-Id`.
2. accepted session id and header-only `X-Hermes-Session-Id` generate the same owner source / effective key behavior.
3. import turn with accepted session id and follow-up turn with header-only `X-Hermes-Session-Id` restores alias continuity.
4. restore success does not include `stable_owner_missing=true`.
5. no stable owner still fails closed.
6. cross-owner, expired, and conflict cases still fail closed.

Run:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py -q
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
```

## 7. Stop Condition

Stop after the bounded fix and local tests.

Do not tag or push unless Codex B explicitly approves after review.

Phase 2 natural import closeout remains blocked until the test machine proves:

```text
OpenWebUI / 8642 import -> follow-up @建筑类数据样表 retrieval -> retrieval_evidence_document_ids non-empty -> citation present
```

