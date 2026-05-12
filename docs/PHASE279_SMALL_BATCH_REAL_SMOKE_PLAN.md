# Phase 2.79 Small Batch Real Smoke Planning

## Goal

Phase 2.79 defines the authorization gates and execution shape for a later Mac mini / test-machine small-batch real scratch-copy smoke.

This phase is planning only. It does not connect to real NAS, does not copy real enterprise files, does not invoke parsers, and does not write platform DB, Hermes DB, `documents`, `chunks`, OpenSearch, Qdrant, or MinIO.

## Current Baseline

- Previous phase: Phase 2.78 Controlled Local Scratch Runtime
- Commit: `5da558e`
- Tag: `phase-2.78-local-scratch-runtime-baseline`
- Runtime capability: local fixture copy -> sha256 -> sanitized run record -> cleanup
- Still not proven: real NAS mount, real enterprise file copy, parser connection, selective indexing, or Agent answer over NAS file content

## Phase 2.79a Preconditions

Phase 2.79a may start only after explicit user authorization and Codex B review.

Required preconditions:

1. Mac mini / test machine has checked out reviewed Hermes refs.
2. `PLATFORM_ASSET_READONLY_DB_CONTRACT_VERSION=delivery_platform.asset_views.v1.1`.
3. `PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false` by default.
4. `PLATFORM_ASSET_BATCH_COPY_ENABLED=false` by default.
5. Scratch runtime options are enabled only for the smoke command, not by changing default env.
6. REST/API Key `project_scope` or equivalent permission proof is available through a secure local channel.
7. Test operator can confirm project scope before any copy plan is generated.
8. Scratch root is local to the Mac mini / test machine and is disposable.
9. No real raw row, secret, NAS path, project private name, or business-sensitive value is printed in chat or committed files.

## Sample Selection

Use 1-3 files only.

Recommended selection:

1. Small non-sensitive Office / PDF / text / CSV / XLSX files.
2. Single file size <= 50 MB.
3. Total copied size <= 200 MB.
4. `lifecycle_status=active`.
5. `index_eligibility` is not `catalog_only`.
6. `confidentiality_level` is known and acceptable for the smoke.
7. Storage locator exists.
8. File belongs to a project covered by the requester `project_scope`.

Do not select:

1. RVT / DWG / IFC / NWD / large BIM model files.
2. Whole project directories.
3. Files with `confidentiality_level=UNKNOWN`.
4. Files with missing storage locator.
5. Files requiring broad NAS scan.
6. Files with unclear permission tags or project scope.

## Allowed Actions In Phase 2.79a

Only after explicit Phase 2.79a authorization:

1. Structure / redacted catalog check.
2. Permission proof check.
3. Scratch copy plan generation.
4. Local scratch copy for `would_copy` items only.
5. SHA256 calculation of copied local scratch files.
6. Cleanup of copied scratch files.
7. Sanitized run record generation.

## Not Allowed In Phase 2.79a

Even with smoke authorization:

1. Parser invocation.
2. Ingestion.
3. Writing `documents` or `chunks`.
4. Writing OpenSearch, Qdrant, or MinIO.
5. Agent final answer integration over copied file content.
6. Bulk NAS scan.
7. Whole project copy.
8. BIM model copy.
9. DB / NAS CRUD.
10. Repair, backfill, reindex, cleanup, delete, migration, or rollout.

## Stop Conditions

Phase 2.79a must stop with Pause / No-Go if any condition appears:

1. Permission proof missing.
2. `project_scope` does not include the target project.
3. `permission_tags` are insufficient or ambiguous.
4. `index_eligibility=catalog_only`.
5. `confidentiality_level=UNKNOWN`.
6. `lifecycle_status` is not `active`.
7. File size exceeds threshold.
8. Total copied size would exceed threshold.
9. Storage locator is missing.
10. Scratch copy fails.
11. Cleanup fails.
12. Script output exposes raw row, secret, true NAS path, or true business data.
13. Parser is invoked.
14. Any DB / index / object-store write occurs.

## Sanitized Report Contract

The Phase 2.79a report must be a sanitized Go / Pause / No-Go summary.

Required fields:

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
  "agent_answer_integration": false
}
```

Allowed evidence:

1. Counts.
2. Boolean safety fields.
3. Redacted project scope pass / fail.
4. Redacted file type / size buckets.
5. Sanitized hash presence or hash prefix only if approved by operator.
6. Cleanup status.

Disallowed evidence:

1. Raw DB rows.
2. Secrets.
3. True NAS paths.
4. True business-sensitive filenames if not already sanitized.
5. Document contents.
6. Parser outputs.
7. Full copied file paths.

## Go / Pause / No-Go

Go:

1. 1-3 eligible files copied to local scratch.
2. Hash calculated.
3. Cleanup completed.
4. No secret / raw row / true business data printed.
5. No parser or DB / index write occurred.

Pause:

1. Environment or permission proof unclear.
2. No eligible small sample found.
3. Cleanup status needs manual check but no data mutation occurred.
4. Report is incomplete but no unsafe action occurred.

No-Go:

1. Permission failure.
2. Secret / raw row / true business data output.
3. Parser invoked.
4. DB / index / object-store write occurred.
5. Bulk copy or unsupported model file copy attempted.
6. Cleanup failed with copied file remaining.

## Phase 2.79 Conclusion

Phase 2.79 completes only the planning and handoff boundary for a later small-batch real smoke.

It does not authorize Phase 2.79a execution. Phase 2.79a must be a separate, explicitly approved task.

