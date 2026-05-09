# Phase 2.56b Natural Import Real Smoke Plan

## Summary

Phase 2.56b plans a user-authorized real smoke for natural-language single-file import.

This phase is planning-only. It does not execute the smoke, upload files, start API / CLI validation, or write DB / OpenSearch / Qdrant records.

The target is to define the authorization gate, sample requirements, execution steps, validation fields, stop conditions, and run record expectations for a later Phase 2.56c.

## Goal

Validate that a user can say a natural-language command such as:

```text
请把 /path/to/safe-demo.docx 导入企业记忆，并绑定为 @测试文件
```

and, only after explicit authorization and feature-flag enablement, Hermes can:

1. Detect natural import intent.
2. Pass parser and filesystem preflight.
3. Call the existing Hermes_memory upload path through the adapter boundary.
4. Return `document_id` and `version_id`.
5. Seed a session alias.
6. Run a minimal retrieval smoke against the imported document.
7. Save a sanitized ignored run record.

## Authorization Gate

Phase 2.56c real smoke may start only when the user explicitly provides:

1. A single small non-sensitive file path.
2. Permission to upload through the natural-language import path.
3. Permission to create test document / version / chunk / OpenSearch / Qdrant records.
4. Acceptance that cleanup / delete / repair / backfill / reindex are not authorized by default.
5. Confirmation that this remains an internal controlled MVP smoke, not production rollout.

Without all five items, Codex A must stop.

## Sample Requirements

Allowed sample:

1. One file only.
2. Small file suitable for local MVP smoke.
3. Non-sensitive and user-selected.
4. Prefer `.txt`, `.md`, `.docx`, `.xlsx`, or `.pptx`.
5. Safe to leave as a test document/version/index record after smoke.

Disallowed sample:

1. Directory or folder.
2. NAS / network disk path.
3. BIM model package or TB-scale file pool.
4. Batch / recursive import target.
5. Customer secrets, bid secrets, personal sensitive data, credentials, confidential contract terms, or commercial pricing secrets.
6. Any sample requiring cleanup/delete to continue.

## Execution Steps For Phase 2.56c

1. Record repo branch / HEAD / dirty state.
2. Confirm Hermes_memory API `/health`.
3. Confirm Hermes CLI starts.
4. Run parser preflight on the natural-language import command.
5. Confirm:
   - `natural_import_detected=true`
   - one source path only
   - no directory / NAS / BIM / bulk wording
   - extension is supported
6. Run filesystem metadata check:
   - file exists
   - regular file
   - readable
   - size is within agreed local smoke limit
7. Enable the natural import real-upload feature flag for this smoke only.
8. Call the existing Hermes_memory upload path through the adapter boundary.
9. Record upload result:
   - `document_id`
   - `version_id`
   - `chunk_count`
   - `indexed_count`
10. Seed session alias only after both `document_id` and `version_id` are present.
11. Ask one minimal retrieval question against the alias.
12. Confirm evidence only comes from the imported document.
13. Confirm import diagnostics are not retrieval evidence.
14. Save sanitized run record under an ignored local reports path.
15. Stop for Codex B review.

## Required Validation Fields

Phase 2.56c must capture:

1. `natural_import_detected`
2. `real_upload_enabled`
3. `upload_adapter_status`
4. `ingestion_status`
5. `document_id`
6. `version_id`
7. `chunk_count`
8. `indexed_count`
9. `alias_resolution.status`
10. `alias_resolution.resolved_document_id`
11. `alias_resolution.resolved_version_id`
12. `retrieval_evidence_document_ids`
13. `retrieval_evidence_version_ids`
14. `import_diagnostics_as_retrieval_evidence=false`
15. `metadata_as_answer=false`
16. `facts_as_answer=false`
17. `snapshot_as_answer=false`
18. `transcript_as_fact=false` when applicable
19. `requires_retrieval_evidence=true`
20. `third_document_contamination=false`

## Stop Conditions

Stop immediately if any of the following occurs:

1. API `/health` is unhealthy.
2. Hermes CLI is unavailable.
3. User authorization is incomplete.
4. File path is missing.
5. Multiple paths are detected.
6. Path is a directory or directory-like.
7. NAS / network disk / batch / BIM / TB wording is detected.
8. Extension is unsupported.
9. File does not exist, is unreadable, or is too large for the agreed smoke.
10. Feature flag cannot be locally scoped to this smoke.
11. Upload fails.
12. Upload succeeds without `document_id`.
13. Upload succeeds without `version_id`.
14. Chunking or indexing fails in a way that prevents retrieval smoke.
15. Alias bind fails.
16. Retrieval evidence contains an unexpected third document.
17. Answer is produced without citation when evidence should exist.
18. Metadata / facts / snapshot / transcript replaces retrieval evidence.
19. Continuing would require cleanup/delete/repair/backfill/reindex.

If a stop condition triggers, write a sanitized failure run record and stop. Do not repair automatically.

## Non-goals

Phase 2.56b / 2.56c do not include:

1. Directory import.
2. NAS / network disk crawl.
3. BIM / TB-scale file pool ingestion.
4. Data Steward implementation.
5. Production rollout.
6. Cleanup / delete / repair / backfill / reindex.
7. Retrieval contract changes.
8. Memory kernel main architecture changes.
9. Automatic business decisions.

## Run Record

The later Phase 2.56c run record must be local and ignored by Git.

Recommended minimum fields:

```json
{
  "phase": "Phase 2.56c",
  "dry_run": false,
  "production_rollout": false,
  "user_authorized_upload": true,
  "natural_import_detected": true,
  "real_upload_enabled": true,
  "upload_adapter_status": "",
  "ingestion_status": "",
  "document_id": "",
  "version_id": "",
  "chunk_count": 0,
  "indexed_count": 0,
  "alias": "",
  "alias_resolution_status": "",
  "retrieval_evidence_document_ids": [],
  "import_diagnostics_as_retrieval_evidence": false,
  "metadata_as_answer": false,
  "facts_as_answer": false,
  "snapshot_as_answer": false,
  "requires_retrieval_evidence": true,
  "third_document_contamination": false,
  "cleanup_delete_repair_reindex_authorized": false,
  "stop_condition": "",
  "result": "pass|partial|fail"
}
```

The run record must not include full file contents, credentials, secrets, personal sensitive data, raw LLM output, or unredacted customer-sensitive material.

## Next Step

Codex B should review this plan. If accepted, do a docs-only baseline first.

Phase 2.56c may execute real natural-language import smoke only after the user provides a file path and explicit authorization.
