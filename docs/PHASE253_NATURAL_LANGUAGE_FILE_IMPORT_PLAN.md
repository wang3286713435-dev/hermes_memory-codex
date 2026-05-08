# Phase 2.53 Natural Language File Import MVP Boundary Planning

## Goal

Phase 2.53 defines the MVP boundary for importing one explicit local file into Hermes enterprise memory from Hermes CLI / Agent conversation.

Example target utterance:

`把 /path/to/file.pdf 导入企业记忆，标题叫 XXX，绑定为 @XXX`

This phase is planning and entry-point reconnaissance only. It does not implement upload from the Agent, run API / CLI smoke, upload real files, or change contracts.

## User Scenarios

1. Import one explicit local file path into enterprise memory.
2. Optionally set title, document type, source type, and session alias.
3. Return import result fields for operator review: `document_id`, `version_id`, ingestion / indexing status, citation readiness, and alias readiness.
4. Allow follow-up retrieval by alias or document id after a successful import.

## Existing Hermes Memory Capability To Reuse

Hermes_memory already has the ingestion path this feature should reuse:

1. `POST /api/v1/documents/upload` in `app/api/routes/documents.py`.
2. `DocumentIngestionService.ingest_uploaded_file()` in `app/services/ingestion/service.py`.
3. Existing parsing, chunking, citation record, version governance, duplicate version detection, OpenSearch indexing, and Qdrant dense indexing.
4. Existing `DocumentIngestResponse` fields: `document_id`, `version_id`, `chunk_count`, `indexed_count`, and `message`.

Phase 2.53a should not change `DocumentIngestResponse`, ingestion contract, retrieval contract, DB schema, or memory kernel main architecture.

## Hermes Main Repo Candidate Entry Points

| Area | Candidate | Boundary |
|---|---|---|
| Intent parser | `agent/memory_kernel/session_document_scope.py` or small adjacent parser | Detect explicit import verbs and local path only; keep separate from ordinary document scope when possible. |
| Orchestration | `run_agent.py` before retrieval / kernel request | Import should happen before retrieval; failed import must fail closed and avoid pretending evidence exists. |
| Adapter | `agent/memory_kernel/adapters/hermes_memory_adapter.py` | Add a small upload wrapper only in a future implementation phase; no contract change. |
| Alias seed | `SessionFileAliasStore` / `FileAliasBinding` | Bind alias only after upload returns `document_id` and `version_id`. |
| Trace / context | `agent/memory_kernel/context_builder.py` | Show import diagnostics separately from retrieval evidence. |
| Tests | Existing session scope / adapter tests or new focused tests | Prefer mocked upload path before any real API smoke. |

## MVP Boundary

Allowed in the future MVP:

1. One explicit local file path.
2. Explicit import verbs such as `导入`, `上传`, `收录到企业记忆`, `加入企业记忆`, `写入企业记忆`.
3. Optional title, document type, source type, and session-level alias.
4. Reuse existing Hermes_memory upload / ingestion / indexing behavior.
5. Fail-closed diagnostics when path, adapter, API, ingestion, or alias binding fails.

Not allowed in the MVP:

1. Directory import, recursive import, NAS scan, cloud drive scan, or TB-level BIM file pool import.
2. Moving or deleting original files.
3. Replacing file server / asset catalog / Data Steward responsibilities.
4. Bulk queue, scheduler, cron, rollout, or production automation.
5. Automatic evidence pack generation.
6. Retrieval contract or memory kernel main architecture changes.

## Safety Rules

1. Import must require explicit intent. A prompt such as `帮我看看这个路径` or `总结这个文件` must not auto-import.
2. Missing path, nonexistent path, directory path, unsupported extension, too-large file, unavailable API, upload failure, ingestion failure, and missing post-upload `document_id` must fail closed.
3. Alias binding must not occur unless upload succeeded and returned both `document_id` and `version_id`.
4. Failed import must not create retrieval evidence, citations, confirmed facts, audit approval, or rollout evidence.
5. Future responses must keep `facts_as_answer=false`, `snapshot_as_answer=false`, and `transcript_as_fact=false`.

## Future Trace Fields

Suggested trace / response diagnostics for Phase 2.53a:

1. `natural_import_detected`
2. `import_action`
3. `import_source_path`
4. `import_title`
5. `document_id`
6. `version_id`
7. `ingestion_status`
8. `citation_ready`
9. `alias_requested`
10. `alias_resolution`
11. `import_failed_reason`

The trace should distinguish import diagnostics from retrieval evidence.

## Suggested Phase 2.53a Minimum Implementation

1. Implement parser tests for explicit import utterances and non-import utterances.
2. Add a mocked Hermes_memory upload adapter path.
3. Seed alias only after mocked upload success.
4. Add trace / response tests for success and fail-closed cases.
5. Do not run real upload smoke until a separate user-authorized phase.

## Future Real Smoke Requirements

Real import smoke should be a separate authorized phase and use one small non-sensitive file.

Minimum evidence for that future phase:

1. `/health` available.
2. Explicit local file path approved by the user.
3. Upload returns `document_id` and `version_id`.
4. Ingestion/indexing status reported.
5. Alias binding succeeds only after successful upload.
6. Follow-up retrieval can cite the imported file.

## Non-Goals

1. Production rollout.
2. Automatic tender review, automatic bid, automatic business decision, or repair authorization.
3. Data Steward / Building Asset Catalog implementation.
4. TB-level BIM ingestion, recursive directory import, or storage governance.
5. Facts automatic extraction or facts replacing retrieval evidence.
6. Retrieval contract change.
7. Memory kernel main architecture rewrite.

## Current Conclusion

Phase 2.53 confirms the feature is feasible as a small Hermes main repo consumption-layer addition that reuses existing Hermes_memory upload / ingestion. The next implementation should be Phase 2.53a with mocked tests first; real upload smoke requires a separate explicit authorization.
