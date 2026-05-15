# Phase 2.86a Temp Evidence Write Rehearsal

## Goal

Phase 2.86a adds a local temp repository evidence-write rehearsal runner.

It consumes an ignored local `nas_evidence_write_dry_run.v0` report and produces an ignored local `nas_evidence_write_rehearsal.v0` report.

The runner rehearses insert ordering for document, document version, chunk, and citation records in an isolated in-memory or temp SQLite repository. It does not write real Hermes DB tables.

## Input Gate

The runner may proceed only when:

1. `write_dry_run_version == "nas_evidence_write_dry_run.v0"`.
2. `decision.write_dry_run_state == "write_dry_run_go"`.
3. `dry_run == true`.
4. `writes_authorized == false`.
5. side-effect safety flags are false.
6. simulated documents, chunks, and citations are present.
7. idempotency key is present.
8. forbidden raw fields are absent.

## Temp Repository Boundary

The service supports:

1. in-memory repository for service tests.
2. temp SQLite repository for CLI rehearsal.

The temp repository may create rehearsal-only rows for:

1. `rehearsal_documents`
2. `rehearsal_document_versions`
3. `rehearsal_chunks`
4. `rehearsal_citations`

It must not call production repository methods or connect to the real Hermes DB.

## Decision States

1. `rehearsal_not_allowed`
2. `rehearsal_go`
3. `rehearsal_no_go`

`rehearsal_go` means only that temp repository write ordering succeeded. It does not authorize real writes and does not make NAS content answerable by Hermes.

## Idempotency and Rollback

The rehearsal runner uses the write dry-run idempotency key and full sanitized input fingerprint.

It must:

1. detect same-run duplicates.
2. reject idempotency conflicts.
3. produce a rollback dry-run section listing temp-only rehearsal refs.
4. keep rollback scoped to the rehearsal repository.

Rollback must not delete NAS files, platform DB rows, Hermes DB rows, OpenSearch documents, Qdrant points, MinIO objects, or source data.

## Report Storage

Reports under `reports/nas_evidence_write_rehearsal/` are ignored local artifacts.

They must not be committed and must not be treated as production evidence.

## Hard Forbidden Actions

Phase 2.86a does not:

1. write real `documents`.
2. write real `chunks`.
3. write real `document_versions`.
4. write audit tables.
5. write platform DB or Hermes DB.
6. write OpenSearch.
7. write Qdrant.
8. write MinIO.
9. execute parser.
10. copy real files.
11. read raw file contents.
12. scan NAS.
13. run Agent DB / NAS CRUD.
14. integrate with Agent final answers.
15. treat dry-run or rehearsal artifacts as production evidence.
16. run repair / cleanup / backfill / reindex / delete / migration.
17. enter production rollout.

## Validation

Phase 2.86a validation covers:

1. target rehearsal tests.
2. py_compile for service and CLI.
3. Data Steward regression.
4. diff / JSON / ignore checks.

No API, DB, NAS, parser, index, object-store, or Agent final answer smoke is required.
