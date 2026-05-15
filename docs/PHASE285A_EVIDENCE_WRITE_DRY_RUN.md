# Phase 2.85a Evidence Write Dry-run Runner

## Goal

Phase 2.85a adds a local-only evidence write dry-run runner.

It consumes an ignored local `nas_evidence_write_preflight.v0` report and produces an ignored local `nas_evidence_write_dry_run.v0` report.

The runner simulates candidate documents, chunks, citations, idempotency, and rollback records in memory. It does not write production stores.

## Boundary

Phase 2.85a does not:

1. write `documents`
2. write `chunks`
3. write platform DB or Hermes DB
4. write OpenSearch
5. write Qdrant
6. write MinIO
7. execute parser
8. copy real files
9. read raw file contents
10. scan NAS
11. run Agent DB / NAS CRUD
12. integrate with Agent final answers
13. treat the dry-run report as production evidence
14. run repair / cleanup / backfill / reindex / delete / migration
15. enter production rollout

## Decision States

1. `write_dry_run_not_allowed`
2. `write_dry_run_go`
3. `write_dry_run_no_go`

`write_dry_run_go` means only that local simulation succeeded. It does not authorize real writes and does not make content answerable by Hermes.

## Input Gates

The runner may proceed only when:

1. `preflight_version == "nas_evidence_write_preflight.v0"`
2. `decision.preflight_state == "write_preflight_ready_for_dry_run"`
3. `dry_run == true`
4. `writes_authorized == false`
5. side-effect safety flags are false
6. `payload_ref.asset_ref` exists
7. `payload_ref.source_view` exists
8. `payload_ref.platform_contract_version` exists
9. `idempotency.idempotency_key` exists
10. `citation_coverage.complete == true`
11. `rollback.rollback_plan_available == true`
12. `locks.lock_required == true`
13. forbidden raw fields are absent

## Output

The generated report includes:

1. `write_dry_run_version`
2. `run_id`
3. `preflight_ref`
4. `simulated_store`
5. `simulated_documents`
6. `simulated_chunks`
7. `simulated_citations`
8. `idempotency`
9. `rollback`
10. `safety`
11. `dry_run`
12. `writes_authorized`
13. `decision`

## Storage Policy

Reports under `reports/nas_evidence_write_dry_run/` are ignored local artifacts.

They must not be committed and must not be used as production evidence.

## Validation

Phase 2.85a validation covers:

1. py_compile for service and CLI
2. target dry-run tests
3. Data Steward regression
4. diff / JSON / ignore checks

No API, CLI, DB, NAS, parser, index, object-store, or Agent final answer smoke is required.
