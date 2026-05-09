# Phase 2.56d Natural Import Runtime Wiring

## Summary

Phase 2.56d adds the minimum Hermes main runtime hook for natural-language file import.

This phase does not upload real files. It only proves that explicit import intent is intercepted before ordinary retrieval / LLM answer flow and that the default runtime fails closed when real upload is disabled.

## Implemented Scope

Hermes main repo:

1. Added `agent/memory_kernel/natural_file_import_runtime.py`.
2. Added a small `run_agent.py` preflight hook before the normal conversation / memory kernel retrieval flow.
3. Kept real upload disabled by default through `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED`.
4. Returned structured diagnostics for import intent without treating diagnostics as retrieval evidence.
5. Added fake-adapter tests for success, failure, missing `document_id`, missing `version_id`, and safety flags.

Hermes_memory:

1. Updated phase handoff docs.
2. Updated ignored `reports/agent_runs/latest.json`.

## Runtime Behavior

Non-import prompts:

1. `maybe_handle_natural_file_import(...)` returns `None`.
2. Existing conversation / retrieval flow proceeds unchanged.

Explicit import prompts:

1. Runtime calls natural import preflight before memory kernel retrieval / LLM answer.
2. If real upload is disabled, the turn returns structured diagnostics:
   - `natural_import_detected=true`
   - `real_upload_enabled=false`
   - `upload_adapter_status=disabled`
   - `ingestion_status=not_executed`
   - `import_failed_reason=real_upload_disabled`
3. The turn does not continue into ordinary retrieval / LLM answer.

Fake adapter tests:

1. `real_upload_enabled=True` with fake adapter can return `document_id/version_id/chunk_count/indexed_count`.
2. Alias diagnostics can be seeded in the fake success path.
3. Failure and missing required fields fail closed and do not bind alias.

## Safety Invariants

The runtime diagnostic response keeps:

1. `retrieval_evidence_document_ids=[]`
2. `import_diagnostics_as_retrieval_evidence=false`
3. `metadata_as_answer=false`
4. `facts_as_answer=false`
5. `snapshot_as_answer=false`
6. `transcript_as_fact=false`
7. `requires_retrieval_evidence=true`
8. `third_document_contamination=false`

## Validation

Hermes main:

```bash
./.venv/bin/python -m py_compile \
  run_agent.py \
  agent/memory_kernel/natural_file_import.py \
  agent/memory_kernel/natural_file_import_flow.py \
  agent/memory_kernel/natural_file_upload_adapter.py \
  agent/memory_kernel/natural_file_import_runtime.py

./.venv/bin/python -m pytest -o addopts='' \
  tests/agent/test_natural_file_import.py \
  tests/agent/test_natural_file_import_flow.py \
  tests/agent/test_natural_file_import_runtime.py -q
```

Result: `28 passed`.

Runtime disabled-path smoke:

```bash
HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=0 \
  ./.venv/bin/hermes chat -Q --max-turns 1 \
  -q '请把 /tmp/demo.docx 导入企业记忆，并绑定为 @测试文件'
```

Result: returned natural import diagnostics with `real_upload_enabled=false`, `upload_adapter_status=disabled`, `ingestion_status=not_executed`, and no retrieval evidence.

## Non-goals

Phase 2.56d does not:

1. Upload real files.
2. Call the real Hermes_memory upload API.
3. Read the user-authorized file body.
4. Write DB / facts / document_versions / audit_logs.
5. Write OpenSearch / Qdrant.
6. Execute cleanup / delete / repair / backfill / reindex / migration.
7. Modify retrieval contract.
8. Modify memory kernel main architecture.
9. Enter Data Steward / DB / NAS / BIM branch implementation.
10. Enter production rollout.

## Next Step

Codex B should review Phase 2.56d.

If accepted, Phase 2.56e may reuse the user-authorized `.docx` file for a real natural-language import smoke.
