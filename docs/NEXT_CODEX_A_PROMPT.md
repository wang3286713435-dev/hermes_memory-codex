# NEXT_CODEX_A_PROMPT

## Phase 2.112g Runtime Candidate Ready / Await Test-machine Validation

Do not implement another runtime fix in Codex A unless a new test-machine report fails.

Current state:

```text
Hermes agent runtime candidate:
commit = 20d9fb561
tag = phase-2.112g-header-owner-restore-runtime-test-candidate
remote = backup2
Codex B development-machine review = passed
```

## What Was Fixed

Phase 2.112g fixed the header-only stable owner restore path:

1. `X-Hermes-Session-Id` is now accepted as a gateway stable owner fallback header.
2. Accepted import turn and header-only follow-up turn produce the same safe owner behavior.
3. Follow-up alias continuity restore is covered by targeted tests with scoped `document_id/version_id`.
4. Restore success avoids `stable_owner_missing=true`.

## Verified Locally

Codex B reran:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile gateway/platforms/api_server.py run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/gateway/test_api_server.py::test_gateway_session_key_accepts_header_only_hermes_session_id_as_stable_owner tests/gateway/test_api_server.py::test_gateway_session_key_header_only_matches_accepted_session_owner tests/gateway/test_api_server.py::test_header_only_hermes_session_owner_restores_import_alias_continuity -q
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
```

Results:

```text
py_compile: passed
gateway targeted tests: 3 passed
natural import / upload client / session scope regression: 109 passed
git diff --check: passed
```

Known environment note:

```text
Full tests/gateway/test_api_server.py still requires async pytest plugin for existing async tests.
The 2.112g targeted sync tests passed in the current .venv.
```

## Next Required Action

Test-machine Codex should:

1. checkout `phase-2.112g-header-owner-restore-runtime-test-candidate` in `/Users/hermes/code/hermes-agent`;
2. restart 8642;
3. confirm `/health` passes and `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible;
4. run the same OpenWebUI / 8642 natural import validation:
   - explicit alias import for `@建筑类数据样表`;
   - follow-up `@建筑类数据样表` retrieval;
   - confirm `alias_resolution.status=alias_resolved`;
   - confirm `alias_missing=false`;
   - confirm `retrieval_suppressed=false`;
   - confirm `retrieval_evidence_document_ids` non-empty;
   - confirm citation is present and manually checkable.

## Hard Boundaries

Do not:

1. repeat development-machine real upload/import;
2. run DB/facts/document_versions/OpenSearch/Qdrant/MinIO writes;
3. scan NAS;
4. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
5. modify platform repo;
6. claim Phase 2 natural import closeout until test-machine OpenWebUI / 8642 retrieval + citation passes.

## If Test-machine Validation Passes

Return the sanitized report to Codex B for final review.

## If Test-machine Validation Fails

Return:

1. exact checkout head/tag;
2. 8642 health and feature flag visibility;
3. import diagnostics;
4. follow-up diagnostics;
5. whether `X-Hermes-Session-Id` was present;
6. whether `stable_owner_missing` is still present;
7. whether `retrieval_evidence_document_ids` is empty;
8. whether citation is missing.
