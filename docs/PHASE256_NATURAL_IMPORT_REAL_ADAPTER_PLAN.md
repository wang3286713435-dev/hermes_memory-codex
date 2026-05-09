# Phase 2.56 Natural Import Real Adapter Skeleton

## Status

Phase 2.56a completed the first implementation slice for a natural-language file import upload adapter boundary in the Hermes main repo.

This is not a real upload feature yet. Real upload remains disabled by default and requires a later user-authorized smoke phase.

## Scope

Phase 2.56a adds:

1. A small `natural_file_upload_adapter.py` boundary in Hermes main.
2. A feature-flagged upload adapter with `enabled=False` by default.
3. Flow diagnostics that fail closed with `real_upload_disabled` when a valid import request reaches the adapter path without explicit enablement.
4. Fake adapter tests proving successful upload results can return `document_id` / `version_id` and seed a session alias when explicitly enabled.
5. Tests proving upload failure does not bind alias and import diagnostics are never retrieval evidence.

## Boundary

Phase 2.56a does not:

1. Call Hermes_memory upload API.
2. Upload files.
3. Read file contents.
4. Run API / CLI smoke.
5. Write DB / facts / document_versions / audit_logs.
6. Write OpenSearch / Qdrant.
7. Modify retrieval contract.
8. Modify memory kernel main architecture.
9. Enter Data Steward / NAS / BIM / TB-scale ingestion.
10. Enter production rollout.

## Diagnostics

Expected stable diagnostics:

1. `real_upload_enabled=false` by default.
2. `upload_adapter_status=disabled` when upload is blocked by feature flag.
3. `import_failed_reason=real_upload_disabled` when the request is valid but real upload is not enabled.
4. `retrieval_evidence_document_ids=[]`.
5. `import_diagnostics_as_retrieval_evidence=false`.
6. `facts_as_answer=false`.
7. `snapshot_as_answer=false`.
8. `transcript_as_fact=false`.

## Validation

Hermes main targeted validation:

```bash
./.venv/bin/python -m py_compile \
  agent/memory_kernel/natural_file_import.py \
  agent/memory_kernel/natural_file_import_flow.py \
  agent/memory_kernel/natural_file_upload_adapter.py

./.venv/bin/python -m pytest -o addopts='' \
  tests/agent/test_natural_file_import.py \
  tests/agent/test_natural_file_import_flow.py \
  tests/agent/test_natural_file_upload_adapter.py -q
```

Result: `25 passed`.

## Next Step

Codex B should review Phase 2.56a. If accepted, Phase 2.56b may plan a user-authorized real natural-language import smoke using a small non-sensitive file.

Phase 2.56b must still keep cleanup / delete / repair / backfill / reindex out of scope unless separately authorized.
