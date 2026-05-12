# Codex Mac Mini Small Batch NAS Smoke Prompt

## Purpose

This prompt is for a later Phase 2.79a Mac mini / test-machine run. It is not authorized by Phase 2.79 planning alone.

Use it only after explicit user authorization.

## Goal

Run a controlled small-batch scratch-copy smoke for 1-3 small non-sensitive assets.

The smoke may validate:

1. Redacted catalog structure.
2. Permission proof / project scope.
3. Scratch copy plan.
4. Local scratch copy.
5. SHA256.
6. Cleanup.
7. Sanitized report.

It must not parse file contents, ingest documents, write indexes, or integrate with Agent final answers.

## Preconditions

Before any command:

1. Confirm reviewed Hermes refs are checked out.
2. Confirm working trees are clean.
3. Confirm `PLATFORM_ASSET_READONLY_DB_CONTRACT_VERSION=delivery_platform.asset_views.v1.1`.
4. Confirm default feature flags remain off:
   - `PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`
   - `PLATFORM_ASSET_BATCH_COPY_ENABLED=false`
5. Confirm runtime copy flags will be enabled only through smoke command options.
6. Confirm REST/API Key `project_scope` or equivalent permission proof exists through secure local env / secret storage.
7. Do not print secrets.
8. Do not print raw DB rows.
9. Do not print true NAS paths or sensitive filenames in the report.

If any precondition fails, stop with `Pause`.

## Sample Rules

Select only:

1. 1-3 files.
2. Small non-sensitive files.
3. Office / PDF / text / CSV / XLSX preferred.
4. Single file <= 50 MB.
5. Total size <= 200 MB.
6. `lifecycle_status=active`.
7. `index_eligibility` not `catalog_only`.
8. Known and acceptable `confidentiality_level`.
9. Storage locator present.
10. Project scope authorized.

Do not select:

1. RVT / DWG / IFC / NWD / BIM large model files.
2. Whole directories.
3. Any file with unknown confidentiality.
4. Any file with unclear project scope.
5. Any file requiring broad NAS scan.

## Allowed Actions

Allowed only after explicit authorization:

1. Redacted catalog check.
2. Permission proof check.
3. Scratch copy plan.
4. Local scratch copy for `would_copy` items.
5. SHA256 on local scratch copy.
6. Cleanup copied scratch files.
7. Sanitized run record.

## Forbidden Actions

Do not:

1. Invoke parser.
2. Ingest into Hermes Memory.
3. Write `documents`.
4. Write `chunks`.
5. Write OpenSearch.
6. Write Qdrant.
7. Write MinIO.
8. Write platform DB.
9. Scan NAS.
10. Bulk copy project folders.
11. Copy BIM large model files.
12. Perform Agent DB / NAS CRUD.
13. Repair / cleanup real source data / backfill / reindex / delete.
14. Enter rollout.

## Stop Conditions

Stop immediately with `Pause` or `No-Go` if:

1. Permission proof is missing.
2. Project scope is insufficient.
3. `permission_tags` are insufficient.
4. `index_eligibility=catalog_only`.
5. `confidentiality_level=UNKNOWN`.
6. `lifecycle_status` is not active.
7. Size threshold exceeded.
8. Storage locator missing.
9. Scratch copy fails.
10. Cleanup fails.
11. Output includes raw rows, secrets, true NAS paths, or true business data.
12. Parser is invoked.
13. Any DB / index / object-store write occurs.

## Report Format

Return a concise sanitized report:

```json
{
  "decision": "go|pause|no_go",
  "sample_count": 0,
  "copied_count": 0,
  "cleanup_status": "all_deleted|partial|failed|not_run",
  "hashes_computed": 0,
  "secret_printed": false,
  "raw_row_output": false,
  "true_business_data_output": false,
  "true_nas_path_output": false,
  "writes_performed": false,
  "parser_invoked": false,
  "production_rollout": false,
  "db_writes": false,
  "opensearch_writes": false,
  "qdrant_writes": false,
  "minio_writes": false,
  "agent_answer_integration": false,
  "pause_reasons": [],
  "no_go_reasons": []
}
```

## Final Boundary

This smoke is still not production rollout and not Data Steward full runtime coupling.

It only proves controlled local scratch copy for a tiny, authorized, non-sensitive sample set.

