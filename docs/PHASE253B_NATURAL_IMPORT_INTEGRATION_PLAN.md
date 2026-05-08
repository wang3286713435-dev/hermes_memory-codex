# Phase 2.53b Natural Language File Import Integration Plan

## 1. Scope

Phase 2.53b is a planning-only phase for integrating the existing natural language file import parser into the Hermes agent consumption path.

This phase does not implement adapter code, does not call the Hermes_memory upload API, does not upload files, and does not run API or CLI smoke tests.

## 2. Current Baseline

Completed baselines:

1. Phase 2.53 planning baseline:
   - Hermes_memory commit: `f92a342`
   - tag: `phase-2.53-natural-language-file-import-plan-baseline`
2. Phase 2.53a parser / dry-run planner baseline:
   - Hermes main repo commit: `f15a56de7`
   - Hermes_memory commit: `c841104`
   - tag: `phase-2.53a-natural-file-import-parser-baseline`

Current parser capability:

1. Detects explicit single-file import intent.
2. Parses `source_path`, optional title, `document_type`, `source_type`, and alias.
3. Fails closed for negated import intent.
4. Fails closed for missing path, multiple paths, directory-like path, bulk import, NAS / network disk, and BIM batch wording.
5. Emits dry-run diagnostics only.
6. Does not access the filesystem, read file contents, call Hermes_memory, or perform upload.

## 3. Recommended Invocation Layer

Recommended design: add a small independent import preflight layer before normal retrieval / answer flow.

Preferred order:

1. `run_agent.py` receives raw user text and session context.
2. A lightweight preflight function calls `parse_natural_file_import()`.
3. If no import intent is detected, the normal MemoryKernel path continues unchanged.
4. If import intent is detected but dry-run / fail-closed diagnostics apply, return import diagnostics without invoking retrieval.
5. In a later implementation phase, if import intent is valid and real upload is explicitly enabled, call a Hermes_memory upload adapter.
6. After successful upload, seed session alias / active document state, then return import diagnostics.

Why not place the first call inside retrieval:

1. Natural language import is an ingestion action, not a retrieval query.
2. Retrieval evidence and import diagnostics must remain separate.
3. A failed import should not silently fall through into ordinary retrieval and create misleading answers.

Why not put the full behavior directly inside `MemoryKernel`:

1. The parser and upload preflight are edge-intent handling, not kernel architecture.
2. Keeping it as a small preflight layer avoids changing the memory kernel main architecture.
3. The kernel can still receive the final session state after successful upload / alias seed.

## 4. Minimal Hermes_memory Upload Adapter Boundary

Future adapter name can be implementation-specific, but the boundary should stay narrow.

Input fields:

1. `source_path`: local absolute or user-visible path from parser result.
2. `title`: optional display title.
3. `document_type`: optional normalized document type.
4. `source_type`: optional normalized source type.

Optional future fields, not required for the first adapter:

1. `requester_id`
2. `tenant_id`
3. `session_id`
4. `alias`

Successful output fields:

1. `document_id`
2. `version_id`
3. `chunk_count`
4. `indexed_count`
5. `message`

Failure output fields:

1. `error_type`
2. `error_message`
3. `failed_reason`

Adapter rules:

1. It must call the existing Hermes_memory upload path instead of creating a second ingestion contract.
2. It must not change `DocumentIngestResponse` unless a future phase proves the current contract cannot carry minimum fields.
3. It must not hide partial indexing failures; these should be surfaced in diagnostics.
4. It must not bind alias unless both `document_id` and `version_id` are present.

## 5. Alias Seed Boundary

Alias seed should happen only after successful upload.

Rules:

1. If upload succeeds and returns `document_id` plus `version_id`, the session alias can be bound.
2. Alias binding remains session-level only.
3. Project-level alias, persistent alias registry, and Data Steward alias management are out of scope.
4. If upload fails, alias binding must not happen.
5. If alias binding fails after upload succeeds, diagnostics must show `alias_resolution.status=alias_bind_failed`.
6. A failed alias bind must never be represented as `alias_resolved`.

Minimum alias diagnostics:

1. `alias`
2. `alias_resolution.status`
3. `resolved_document_id`
4. `resolved_version_id`
5. `alias_scope=session`
6. `alias_bind_failed_reason`

## 6. Import Diagnostics Boundary

Import diagnostics must be separate from retrieval evidence.

Minimum diagnostics:

1. `natural_import_detected`
2. `ingestion_status`
3. `document_id`
4. `version_id`
5. `alias_resolution`
6. `import_failed_reason`
7. `dry_run`

Additional recommended diagnostics:

1. `source_path`
2. `title`
3. `document_type`
4. `source_type`
5. `chunk_count`
6. `indexed_count`
7. `upload_adapter_status`
8. `filesystem_check_status`

Important answer boundary:

1. Import diagnostics are not retrieval citations.
2. Import diagnostics must not be labeled as evidence chunks.
3. Upload success does not mean the uploaded document has been semantically validated.
4. If import fails, the answer should report the import failure and not invent retrieved content.

## 7. Fail-closed Strategy

The import path should fail closed for:

1. Missing `source_path`.
2. Directory-like path.
3. Multiple paths.
4. Bulk / batch wording.
5. NAS / network disk / whole folder / TB BIM file pool wording.
6. Unsupported extension.
7. File does not exist, once filesystem check is introduced.
8. Hermes_memory API unavailable.
9. Upload failure.
10. Missing `document_id`.
11. Missing `version_id`.
12. Alias binding failure.
13. Ambiguous user intent such as "show / summarize / compare this file" without explicit import wording.

For fail-closed cases:

1. `dry_run` may remain true in planning / mocked phases.
2. `ingestion_status` should be `not_executed` or `failed`.
3. `import_failed_reason` must be explicit.
4. Normal retrieval should not be used as a fallback unless the user also asks a retrieval question against an already known document.

## 8. Phase Split

### Phase 2.53c: Mocked Adapter / Kernel Integration Tests

Allowed scope:

1. Wire parser preflight into a mocked or fake adapter path.
2. Add unit tests for valid import, fail-closed import, and alias seed after mocked success.
3. Verify import diagnostics are separate from retrieval evidence.
4. Keep real upload disabled.

Explicitly not allowed:

1. No real Hermes_memory API call.
2. No real file upload.
3. No DB / OpenSearch / Qdrant writes.
4. No API / CLI live smoke.

### Phase 2.53d: User-authorized Small-file Real Upload Smoke

Allowed only after explicit user authorization.

Candidate scope:

1. Use one small non-sensitive local file.
2. Call existing Hermes_memory upload API.
3. Confirm `document_id`, `version_id`, chunk / index counts.
4. Seed session alias after upload success.
5. Run one minimal retrieval query against the uploaded document.

Still not allowed:

1. No directory import.
2. No NAS / network disk scan.
3. No TB BIM file pool.
4. No Data Steward productization.
5. No automatic repair / backfill / reindex beyond the existing upload path.

## 9. Non-goals

1. No business code in Phase 2.53b.
2. No real upload adapter implementation.
3. No API / CLI smoke.
4. No filesystem content reading.
5. No directory recursion.
6. No NAS / enterprise network disk ingestion.
7. No TB BIM file pool ingestion.
8. No Data Steward / enterprise database / BIM model management.
9. No retrieval contract changes.
10. No memory kernel main architecture changes.
11. No repair / backfill / reindex / cleanup / delete / migration.
12. No production rollout.

## 10. Phase 2.53b Conclusion

The recommended path is to keep the natural language import parser as an explicit import preflight layer before normal retrieval. The next implementation phase should use a mocked upload adapter first, validate diagnostics and alias seed behavior, and continue to keep real file upload behind a separate user-authorized phase.

