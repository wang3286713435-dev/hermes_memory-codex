# Phase 2.55 Internal MVP Real Upload Smoke Plan

## Summary

Phase 2.55 plans a small, controlled, non-sensitive real file upload smoke for the internal Hermes MVP.

This is not production rollout. This phase does not upload a file, does not run API / CLI smoke, and does not write DB, OpenSearch, Qdrant, facts, document_versions, or audit_logs. It only defines the authorization gate, test-file requirements, smoke steps, expected trace fields, stop conditions, and sanitized run record shape for a later Phase 2.55a.

Phase 2.55a may run the real upload smoke only after the user explicitly provides a small non-sensitive file path and authorizes the upload.

## Scope

Phase 2.55 scope:

1. Define what file is allowed for an internal MVP real upload smoke.
2. Define pre-flight checks before any upload.
3. Define the smallest acceptable upload / ingestion / retrieval / CLI validation flow.
4. Define expected evidence, citation, metadata, and File Steward diagnostics.
5. Define stop / pause conditions.
6. Define sanitized run record fields.
7. Define the Phase 2.55a authorization gate.

## Non-scope

Phase 2.55 explicitly does not:

1. Upload any file.
2. Read real file content.
3. Run Hermes_memory API smoke.
4. Run Hermes CLI smoke.
5. Write DB / facts / document_versions / audit_logs / OpenSearch / Qdrant.
6. Execute repair / backfill / reindex / cleanup / delete / migration.
7. Enter production rollout.
8. Enter Data Steward / BIM / NAS / TB file pool implementation.
9. Modify retrieval contract.
10. Modify memory kernel main architecture.

## Sample File Requirements

Allowed test file:

1. One small file only.
2. Non-sensitive.
3. Manually selected and explicitly authorized by the user.
4. Prefer `.txt`, `.md`, `.docx`, `.xlsx`, or `.pptx` with a tiny amount of safe sample content.
5. Must not contain real customer secrets, bid secrets, personal identity data, credentials, commercial pricing secrets, or confidential project details.
6. Must not be a directory, NAS path, recursive folder, or TB-scale BIM/model asset.
7. Must be safe to leave as a test document/version/index record after smoke.

Disallowed test file:

1. Real customer sensitive file.
2. Full tender source package unless separately approved.
3. Any file requiring cleanup/delete after upload.
4. Any file whose content cannot be summarized in a sanitized run record.

## Pre-flight Checklist

Before Phase 2.55a real smoke, the operator must confirm:

1. User provided an explicit file path.
2. User explicitly authorized upload.
3. File is small and non-sensitive.
4. Hermes_memory API `/health` is healthy.
5. Environment variables point to the intended local/internal MVP services.
6. `DATABASE_URL` is not accidentally pointing to the wrong environment.
7. `OPENSEARCH_URL` is reachable.
8. `QDRANT_URL` and `QDRANT_COLLECTION` match the active MVP collection.
9. Hermes CLI starts successfully.
10. Current repo dirty state is known and no unrelated changes will be committed.
11. Operator understands this is internal controlled MVP smoke, not production rollout.

## Smoke Steps

Phase 2.55a should use the smallest flow that proves the loop works:

1. Record pre-flight state:
   - API health.
   - CLI availability.
   - repo branch / commit.
   - sanitized file name or fake label.
2. Upload exactly one authorized file through the existing upload path.
3. Record ingestion result:
   - `document_id`.
   - `version_id`.
   - `source_name`.
   - `file_type`.
   - chunk count.
   - OpenSearch indexing status if available.
   - Qdrant / dense indexing status if available.
4. Query the newly uploaded document by explicit file title or natural file reference.
5. Bind an alias for the new document in a fresh Hermes session.
6. Ask one simple content question that should be answered from the uploaded file.
7. Ask one file metadata / citation count question.
8. Confirm retrieval evidence is only from the uploaded document.
9. Confirm File Steward diagnostics show metadata without treating metadata as answer evidence.
10. Save a sanitized run record to an ignored local reports path.

## Expected Trace / Citation Fields

The smoke should capture:

1. `document_id`.
2. `version_id`.
3. `source_name`.
4. `file_type` or `document_type`.
5. `retrieval_evidence_document_ids`.
6. `retrieval_evidence_version_ids` if available.
7. citation fields:
   - `source_name`.
   - `document_id`.
   - `version_id`.
   - `chunk_id`.
   - structured location fields if the file is Excel / PPTX / transcript-like.
8. File Steward fields:
   - `file_answer_metadata_required_fields`.
   - `file_answer_metadata_echo_required=true`.
   - `document_id`.
   - `version_id`.
   - `title` or equivalent source title.
   - `source_name`.
   - `source_type`.
   - `citation_count`.
9. safety flags:
   - `metadata_as_answer=false`.
   - `facts_as_answer=false`.
   - `snapshot_as_answer=false`.
   - `transcript_as_fact=false` when applicable.
   - `requires_retrieval_evidence=true`.

## Stop Conditions

Stop immediately and do not continue the smoke if any of the following occurs:

1. API `/health` is not healthy.
2. User did not explicitly authorize upload.
3. File appears sensitive or too large.
4. Upload returns an error.
5. Ingestion fails before producing a `document_id`.
6. No `version_id` is produced.
7. Chunking fails.
8. OpenSearch indexing fails in a way that prevents retrieval.
9. Qdrant / dense indexing fails and the smoke requires dense verification.
10. Hermes CLI cannot start.
11. Alias binding fails and cannot be diagnosed.
12. Retrieval evidence contains an unexpected third document.
13. Metadata / snapshot / facts / transcript replaces retrieval evidence.
14. Answer is produced without citation when evidence should exist.
15. The operator would need cleanup/delete/repair/reindex to continue.

If a stop condition triggers, record a sanitized failure run record and stop. Do not repair automatically.

## Sanitized Run Record Fields

The later Phase 2.55a run record should be local and ignored by Git.

Recommended fields:

```json
{
  "phase": "Phase 2.55a",
  "dry_run": false,
  "production_rollout": false,
  "user_authorized_upload": true,
  "file_label": "sanitized label only",
  "file_type": "",
  "api_health": "",
  "cli_available": false,
  "document_id": "",
  "version_id": "",
  "source_name": "",
  "chunk_count": 0,
  "opensearch_status": "",
  "qdrant_status": "",
  "alias": "",
  "alias_resolution_status": "",
  "retrieval_evidence_document_ids": [],
  "citation_fields_present": [],
  "metadata_as_answer": false,
  "facts_as_answer": false,
  "snapshot_as_answer": false,
  "requires_retrieval_evidence": true,
  "third_document_contamination": false,
  "stop_condition": "",
  "result": "pass|partial|fail",
  "notes": []
}
```

The run record must not include full file content, secrets, personal data, original sensitive path details, or raw LLM output beyond sanitized excerpts.

## Phase 2.55a Authorization Gate

Phase 2.55a is not authorized by this planning document.

To enter Phase 2.55a, the user must explicitly provide:

1. A small non-sensitive file path.
2. Permission to upload that file into the internal MVP environment.
3. Permission to create test document/version/chunk/index records.
4. Acceptance that the smoke does not perform cleanup/delete/repair/reindex.
5. Confirmation that this remains internal controlled MVP smoke, not production rollout.

Without all five items, Codex A must stop and request authorization.

## Relationship To Data Steward

Data Steward / BIM / NAS / TB file pools remain post-MVP product-line work.

Phase 2.55 only plans a single-file internal smoke for the existing Hermes memory pipeline. It does not authorize:

1. Directory ingestion.
2. NAS crawl.
3. BIM model parsing.
4. Data asset catalog implementation.
5. Project/file governance UI.
6. Production scheduler or cron.
7. Bulk import.

Any Data Steward work requires a separate phase, separate sample strategy, and separate risk review.

## Phase 2.55 Completion Criteria

Phase 2.55 planning is complete when:

1. The allowed sample file boundary is documented.
2. Pre-flight and stop conditions are documented.
3. Smoke steps and expected trace/citation fields are documented.
4. Sanitized run record fields are documented.
5. Phase 2.55a authorization gate is explicit.
6. The docs state clearly that no upload has been performed in Phase 2.55.

