# Phase 2.80 Controlled Scratch Parser Dry-run Planning

## Goal

Phase 2.80 plans a future controlled parser dry-run over the same small-batch scratch-copy boundary validated in Phase 2.79a.

This phase is planning only. It does not invoke parsers, read real file contents, copy files, write databases, write indexes, or connect parsed previews to Agent final answers.

## Prior Evidence

Phase 2.79a Mac mini / test-machine small batch NAS scratch-copy smoke returned `go`.

Validated fields:

1. `sample_count=3`.
2. `copied_count=3`.
3. `hashes_computed=3`.
4. `cleanup_status=all_deleted`.
5. `secret_printed=false`.
6. `raw_row_output=false`.
7. `true_business_data_output=false`.
8. `true_nas_path_output=false`.
9. `writes_performed=false`.
10. `parser_invoked=false`.
11. `production_rollout=false`.
12. `db_writes=false`.
13. `opensearch_writes=false`.
14. `qdrant_writes=false`.
15. `minio_writes=false`.
16. `agent_answer_integration=false`.

This proves only:

1. Permission proof can gate a tiny sample.
2. 1-3 non-sensitive samples can be copied to local scratch.
3. Hashes can be computed.
4. Scratch cleanup can complete.
5. Report output can stay sanitized.

It does not prove parser safety, ingestion, indexing, or Agent answer use.

## Phase 2.80a Preconditions

Phase 2.80a may start only after explicit authorization and review.

Required preconditions:

1. Phase 2.79a smoke result remains `go`.
2. The exact sample boundary remains 1-3 files.
3. Sample files are still small, non-sensitive, active, scoped, and not catalog-only.
4. Scratch copy is performed only through the existing controlled runtime boundary.
5. Parser dry-run is enabled only for the smoke command, not by changing default env.
6. Parser output is written only to local ignored preview / manifest paths.
7. Scratch files and parser previews are deleted or kept only in explicitly ignored local temp paths as instructed by the smoke plan.
8. Operator confirms no true NAS path, secret, raw row, true filename, or sensitive content is printed.

## Allowed File Types

Initial parser dry-run may cover only small files from:

1. Office document formats already supported by Hermes parsers.
2. PDF.
3. TXT / Markdown.
4. CSV.
5. XLSX.

Do not include:

1. RVT / DWG / IFC / NWD / large BIM models.
2. Scanned image-heavy PDFs requiring OCR.
3. Archives.
4. Whole directories.
5. Files over the Phase 2.79a size threshold.

## Allowed Actions In Phase 2.80a

Only after separate Phase 2.80a authorization:

1. Reuse the Phase 2.79a permission proof check.
2. Reuse the same sample size and file-type limits.
3. Generate scratch copy plan.
4. Copy eligible items to local scratch.
5. Run parser in dry-run / preview mode only.
6. Generate local sanitized parser preview manifest.
7. Record parser type, status, extracted text length bucket, page / sheet / slide count bucket if available.
8. Compute hash and cleanup copied scratch files.
9. Output sanitized Go / Pause / No-Go summary.

## Forbidden Actions

Even in Phase 2.80a:

1. Do not write `documents`.
2. Do not write `chunks`.
3. Do not write OpenSearch.
4. Do not write Qdrant.
5. Do not write MinIO.
6. Do not write platform DB or Hermes DB.
7. Do not connect parsed preview to Agent final answer.
8. Do not persist document contents in tracked files.
9. Do not output raw extracted text.
10. Do not output true NAS paths, secrets, raw rows, or sensitive business data.
11. Do not scan NAS or copy directories.
12. Do not run OCR / ASR / BIM model parsing.
13. Do not perform repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Sanitized Parser Preview Contract

Parser preview may include only:

1. `parser_status`: `parsed|skipped|failed`.
2. `parser_type`: sanitized parser identifier.
3. `file_type`: sanitized extension or type family.
4. `text_length_bucket`: `empty|small|medium|large`.
5. `structure_summary`: sanitized counts only, such as page / sheet / slide / row buckets.
6. `warnings`: sanitized warning codes.
7. `cleanup_status`.
8. Safety booleans.

Parser preview must not include:

1. Full extracted text.
2. True filenames.
3. True NAS paths.
4. Raw DB rows.
5. Secrets.
6. Customer / project / business-sensitive values.
7. Parsed content intended for Agent answer context.

## Stop Conditions

Stop with `pause` or `no_go` if:

1. Phase 2.79a permission proof cannot be reproduced.
2. Sample set changes outside the approved 1-3 file boundary.
3. Any selected file becomes unsupported or sensitive.
4. Scratch copy fails.
5. Cleanup fails.
6. Parser tries to write `documents`, `chunks`, DB, OpenSearch, Qdrant, or MinIO.
7. Parser emits raw content to terminal, chat, tracked files, or report.
8. OCR / ASR / BIM parser is triggered.
9. Any secret, raw row, true NAS path, or true business data appears.
10. Agent answer integration is attempted.

## Report Contract

Phase 2.80a report must remain sanitized:

```json
{
  "decision": "go|pause|no_go",
  "sample_count": 0,
  "copied_count": 0,
  "parsed_preview_count": 0,
  "cleanup_status": "all_deleted|partial|failed|not_run",
  "parser_invoked": true,
  "parser_dry_run_only": true,
  "documents_written": false,
  "chunks_written": false,
  "db_writes": false,
  "opensearch_writes": false,
  "qdrant_writes": false,
  "minio_writes": false,
  "agent_answer_integration": false,
  "raw_text_output": false,
  "secret_printed": false,
  "raw_row_output": false,
  "true_nas_path_output": false,
  "true_business_data_output": false,
  "production_rollout": false
}
```

## Go / Pause / No-Go

Go:

1. Approved samples are copied and cleaned.
2. Parser dry-run preview completes.
3. No raw text or sensitive data is printed.
4. No DB / index / object-store writes occur.
5. No Agent answer integration occurs.

Pause:

1. Parser unsupported for one or more sample files.
2. Preview output needs human review but no unsafe action happened.
3. Environment is unclear.
4. Cleanup needs manual confirmation but no source data was modified.

No-Go:

1. Parser writes content to DB / indexes / object storage.
2. Raw extracted text or sensitive content is exposed.
3. Agent final answer uses parsed preview.
4. Cleanup fails with copied scratch content remaining.
5. Any repair / backfill / reindex / rollout behavior is triggered.

## Current Conclusion

Phase 2.80 only prepares the dry-run parser boundary.

Phase 2.80a must be separately authorized before any parser command is run.
