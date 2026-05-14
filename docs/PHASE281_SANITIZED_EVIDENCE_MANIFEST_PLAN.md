# Phase 2.81 Sanitized Evidence Manifest Planning

## Goal

Phase 2.81 plans a sanitized evidence manifest layer for NAS-derived parser dry-run previews.

This phase is planning only. It does not generate real manifest artifacts, execute parsers, copy files, read real file contents, write databases, write indexes, or connect parsed previews to Agent final answers.

## Prior Evidence

Phase 2.80a Mac mini / test-machine controlled scratch parser dry-run returned `go`.

Validated fields:

1. `sample_count=3`.
2. `copied_count=3`.
3. `parsed_preview_count=3`.
4. `cleanup_status=all_deleted`.
5. `parser_invoked=true`.
6. `parser_dry_run_only=true`.
7. `documents_written=false`.
8. `chunks_written=false`.
9. `db_writes=false`.
10. `opensearch_writes=false`.
11. `qdrant_writes=false`.
12. `minio_writes=false`.
13. `agent_answer_integration=false`.
14. `raw_text_output=false`.
15. `secret_printed=false`.
16. `raw_row_output=false`.
17. `true_filename_output=false`.
18. `true_nas_path_output=false`.
19. `true_business_data_output=false`.
20. `production_rollout=false`.

This proves only:

1. Controlled scratch copy can feed parser dry-run.
2. Parser dry-run can produce sanitized preview.
3. Cleanup can complete after parser preview.
4. Raw text and sensitive identifiers can be excluded from the report.

It does not prove ingestion, indexing, document evidence creation, or Agent answer use.

## Manifest Purpose

The sanitized evidence manifest is a local, ignored artifact that summarizes whether NAS-derived parser preview produced usable evidence candidates without exposing raw content.

It should support later human and Codex review of:

1. Which asset produced a parser preview.
2. Whether the preview is eligible for a later evidence-writing phase.
3. Whether cleanup completed.
4. Which safety gates passed or failed.
5. Why a sample is still not allowed to enter `documents`, `chunks`, indexes, or Agent answer context.

## Manifest Scope

The manifest may be generated only from sanitized parser preview metadata.

It must not include:

1. Raw extracted text.
2. True filenames.
3. True NAS paths.
4. True project names.
5. Raw DB rows.
6. Secrets.
7. Business-sensitive values.
8. Full source paths.
9. Full scratch paths.
10. Prompt-ready document evidence.

## Manifest Location

Future manifest artifacts should be ignored local files, for example:

```text
reports/nas_evidence_manifests/*.json
reports/nas_evidence_manifests/*.md
```

Phase 2.81 should not create the directory or artifacts unless a later implementation phase explicitly does so with `.gitignore` / `README.md` policy.

## Proposed Manifest Schema

The future manifest should use a sanitized schema:

```json
{
  "manifest_version": "nas_evidence_manifest.v0",
  "run_id": "redacted-run-id",
  "created_at": "ISO-8601",
  "source": {
    "asset_ref": "redacted-or-hashed",
    "source_view": "FileAssetView|ModelAssetView|ProjectAssetView",
    "project_scope_proven": true,
    "permission_proof_status": "valid|missing|expired|insufficient",
    "storage_locator_present": true
  },
  "sample": {
    "file_type": "pdf|office|text|csv|xlsx|unknown",
    "size_bucket": "lt_1mb|1mb_to_50mb|gt_50mb",
    "confidentiality_status": "known|unknown|denied",
    "lifecycle_status": "active|not_active|unknown",
    "index_eligibility_status": "eligible_for_preview|catalog_only|unknown"
  },
  "parser_preview": {
    "parser_status": "parsed|skipped|failed",
    "parser_type": "sanitized-parser-id",
    "text_length_bucket": "empty|small|medium|large",
    "structure_summary": {
      "page_count_bucket": "none|one|two_to_five|gt_five|unknown",
      "sheet_count_bucket": "none|one|two_to_five|gt_five|unknown",
      "slide_count_bucket": "none|one|two_to_five|gt_five|unknown",
      "row_count_bucket": "none|lt_100|100_to_1000|gt_1000|unknown"
    },
    "warnings": ["sanitized_warning_code"]
  },
  "safety": {
    "raw_text_output": false,
    "true_filename_output": false,
    "true_nas_path_output": false,
    "raw_row_output": false,
    "secret_printed": false,
    "true_business_data_output": false,
    "documents_written": false,
    "chunks_written": false,
    "db_writes": false,
    "opensearch_writes": false,
    "qdrant_writes": false,
    "minio_writes": false,
    "agent_answer_integration": false
  },
  "cleanup": {
    "scratch_cleanup_status": "all_deleted|partial|failed|not_run",
    "preview_cleanup_status": "all_deleted|partial|failed|not_run"
  },
  "decision": {
    "manifest_status": "ready_for_review|pause|no_go",
    "next_allowed_phase": "review_only|evidence_write_planning|none",
    "reasons": ["sanitized_reason_code"]
  }
}
```

## Allowed Future Phase 2.81a Actions

Only after separate Phase 2.81a authorization:

1. Read sanitized parser preview metadata from ignored local temp output.
2. Generate a sanitized manifest in ignored local storage.
3. Validate the manifest schema.
4. Confirm no raw text, true filename, true NAS path, secret, raw row, or sensitive value is present.
5. Confirm all write flags remain false.
6. Output a sanitized Go / Pause / No-Go summary.

## Forbidden Actions

Even in Phase 2.81a:

1. Do not execute parser unless the phase explicitly reuses the existing parser dry-run boundary.
2. Do not copy new real files unless separately authorized.
3. Do not read or print raw extracted text.
4. Do not write `documents`.
5. Do not write `chunks`.
6. Do not write OpenSearch.
7. Do not write Qdrant.
8. Do not write MinIO.
9. Do not write platform DB or Hermes DB.
10. Do not connect manifest to Agent final answer.
11. Do not create prompt-ready document evidence.
12. Do not scan NAS or copy directories.
13. Do not perform repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Go / Pause / No-Go

Go:

1. Manifest is created only from sanitized preview metadata.
2. Manifest schema validates.
3. No raw text or sensitive identifiers are present.
4. No persistent system writes occur.
5. Manifest remains ignored and local.

Pause:

1. Preview metadata is incomplete.
2. Manifest schema has non-sensitive validation issues.
3. Human review is needed for parser warnings.
4. Cleanup state is unclear but no source data was modified.

No-Go:

1. Manifest includes raw text or sensitive identifiers.
2. Manifest is tracked by Git.
3. Any DB / index / object-store write occurs.
4. Agent answer integration is attempted.
5. Source data cleanup, repair, reindex, migration, or rollout is triggered.

## Current Conclusion

Phase 2.81 only plans the manifest boundary.

Phase 2.81a must be separately authorized before any manifest runner or artifact is created.
