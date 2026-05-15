# Phase 2.87c Controlled Runtime Evidence Write Smoke Plan

## Status

- Phase: 2.87c
- Scope: docs-only planning
- Previous baseline: `44cc837`, tag `phase-2.87b-evidence-only-writer-baseline`
- Current decision: future runtime evidence write smoke remains `Pause` until a separate reviewed prompt authorizes test-machine execution.

This document defines the minimum control surface for a future first runtime use of the Phase 2.87b evidence-only writer. It does not authorize API / CLI wiring, parser execution, file copying, NAS scan, DB write, index write, repair, or rollout.

## Non-Goals

- No runtime smoke execution.
- No API / CLI runtime wiring.
- No parser execution.
- No scratch copy.
- No raw file content read.
- No NAS scan.
- No OpenSearch / Qdrant / MinIO write.
- No platform DB write.
- No audit table write outside existing retrieval audit behavior.
- No Agent answer integration.
- No Agent DB / NAS CRUD.
- No repair / cleanup / backfill / reindex / delete / migration.
- No production rollout.

## Future Smoke Scope

A future Phase 2.87d or later smoke may only be considered for:

- one approved source asset
- one `Document`
- one `DocumentVersion`
- up to 20 `Chunk` rows
- matching `CitationRecord` rows
- one dedicated `write_run_id`
- one dedicated operator approval id
- non-production Mac mini / test-machine only

Anything beyond that scope is `No-Go`.

## Prerequisite Chain

The future runtime smoke must prove every item in this chain before any write path can be called:

1. DB v1.1 catalog asset is available through a reviewed read-only view or REST/API path with `project_scope`.
2. Permission proof exists for the selected source asset and test operator.
3. One small approved source asset reference is selected without storing raw NAS path, raw filename, or raw content in tracked docs.
4. Scratch copy and sanitized parser preview have been completed in prior phases, if needed, without DB/index/object-store writes.
5. Sanitized evidence manifest exists and contains no raw text, true filename, true path, secret, raw DB row, or sensitive business payload.
6. Evidence-write eligibility report exists and reaches the reviewed eligible state.
7. Evidence-write payload plan exists and is fingerprinted.
8. Evidence-write preflight report exists and reaches a reviewed ready state.
9. Evidence-write dry-run report exists and is reviewed.
10. Evidence-write rehearsal report exists and is reviewed.
11. Phase 2.87a exact write targets are confirmed: `Document`, `DocumentVersion`, `Chunk`, `CitationRecord`.
12. Phase 2.87b evidence-only writer baseline is checked out or otherwise reviewed.
13. Operator approval JSON is present, valid, unexpired, and matches the selected payload.
14. Git worktree, environment, and service state are clean enough for a one-run test-machine smoke.

If any prerequisite is missing, stale, mismatched, or unverifiable, the result is `Pause` or `No-Go`.

## Operator Approval JSON

The future operator approval must be explicit and must not be inferred from chat text. Required fields:

```json
{
  "approval_version": "hermes_evidence_write_operator_approval.v1",
  "approval_id": "",
  "approved_by": "",
  "approved_at": "",
  "expires_at": "",
  "target_environment": "test_machine_only",
  "target_git_commit": "44cc837-or-reviewed-successor",
  "source_system": "",
  "source_asset_ref": "",
  "project_scope": "",
  "permission_proof_ref": "",
  "sanitized_manifest_ref": "",
  "eligibility_report_ref": "",
  "payload_plan_ref": "",
  "preflight_report_ref": "",
  "dry_run_ref": "",
  "rehearsal_ref": "",
  "rollback_dry_run_ref": "",
  "write_run_id": "",
  "evidence_write_idempotency_key": "",
  "expected_payload_fingerprint": "",
  "max_documents": 1,
  "max_document_versions": 1,
  "max_chunks": 20,
  "allowed_write_action": "first_real_hermes_evidence_write_smoke",
  "feature_flags_expected": {
    "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED": true,
    "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED": true,
    "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED": false,
    "PLATFORM_ASSET_INDEX_WRITE_ENABLED": false,
    "PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED": false
  },
  "writes_authorized": true,
  "operator_notes": ""
}
```

`operator_notes` may describe intent, but it must not contain raw file content, true NAS path, secrets, or sensitive business details.

## Feature Flags

Default values must remain off:

```text
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=false
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED=false
PLATFORM_ASSET_INDEX_WRITE_ENABLED=false
PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED=false
```

For a future one-run smoke, only these may be true after separate authorization:

```text
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=true
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=true
```

Agent answer integration, index write, and API / CLI runtime wiring must remain false unless a later phase explicitly changes the boundary.

## Transaction And Commit Boundary

A future smoke-only runner or service must use the Phase 2.87b `EvidenceOnlyWriter` with an injected SQLAlchemy session and a single scoped transaction:

1. Validate feature flags, operator approval, target environment, git ref, payload fingerprint, limits, and idempotency key.
2. Run pre-write rollback dry-run for the target `write_run_id`.
3. Open one transaction.
4. Create exactly one `Document`.
5. Create exactly one `DocumentVersion`.
6. Create up to 20 `Chunk` rows.
7. Create matching `CitationRecord` rows.
8. Flush and verify counts, metadata, source refs, and idempotency fields.
9. Commit only if all checks pass.
10. Roll back on any exception or mismatch.

The transaction must not call OpenSearch, Qdrant, MinIO, platform DB, audit table write, parser, NAS, or Agent answer code.

## Rollback Dry-Run Verification

Rollback remains diagnostic unless a later repair phase is separately planned and approved.

Required checks:

- Before write: rollback dry-run for `write_run_id` returns no existing rows or reports a reviewed duplicate state.
- After commit: rollback dry-run lists only rows created under the dedicated `write_run_id`.
- Duplicate rerun: no new rows are created and rollback listing remains unchanged.
- Conflict rerun: same idempotency key with different payload fingerprint is `No-Go`.

The future smoke may inspect rollback scope but must not delete, cleanup, invalidate, or repair rows.

## Idempotency Behavior

- Same idempotency key and same payload fingerprint: return duplicate / no-op, with zero additional rows.
- Same idempotency key and different payload fingerprint: `No-Go`.
- Missing idempotency key: `No-Go`.
- Missing `write_run_id`: `No-Go`.
- Payload exceeds 1 document / 1 version / 20 chunks: `No-Go`.

## Post-Write Inspection

Post-write inspection must be scoped only by `write_run_id`.

Required observations:

- exactly one `Document`
- exactly one `DocumentVersion`
- chunk count <= 20
- citation count matches chunk/evidence plan
- all created rows carry the expected `write_run_id`
- all created rows carry source metadata without raw text or true source path
- `agent_answer_eligible=false`
- `index_write_eligible=false`
- `evidence_write_smoke=true`

No retrieval-answer test is part of this phase. A successful write smoke does not mean Hermes can answer from the new evidence.

## Sanitized Report Format

If a later phase generates a runtime smoke report, it must be an ignored local artifact, for example:

```text
reports/evidence_write_smoke/<write_run_id>.json
```

Required fields:

```json
{
  "report_version": "hermes_evidence_write_smoke_report.v1",
  "write_run_id": "",
  "operator_approval_id": "",
  "target_environment": "test_machine_only",
  "git_commit": "",
  "status": "go|pause|no_go|failed",
  "write_executed": false,
  "created_counts": {
    "documents": 0,
    "document_versions": 0,
    "chunks": 0,
    "citations": 0
  },
  "idempotency_status": "",
  "rollback_dry_run_before": {},
  "rollback_dry_run_after": {},
  "post_write_inspection": {},
  "forbidden_actions": {
    "parser_executed": false,
    "nas_scanned": false,
    "opensearch_written": false,
    "qdrant_written": false,
    "minio_written": false,
    "platform_db_written": false,
    "agent_answer_integration_enabled": false,
    "repair_executed": false,
    "rollout_executed": false
  },
  "sanitized": true
}
```

The report must exclude raw text, true filenames, true NAS paths, secrets, raw DB rows, and sensitive business values.

## Go / Pause / No-Go Rules

### Go

Only planning is `Go` in Phase 2.87c. A future runtime smoke may be `Go` only when every prerequisite and approval field is present, reviewed, unexpired, and limited to the test-machine tiny scope.

### Pause

Pause when:

- operator approval is missing, expired, or ambiguous
- prerequisite report refs are missing
- target git ref is not reviewed
- worktree has unexpected dirty files
- rollback dry-run was not produced
- service state is unclear
- row counts or payload fingerprint are not yet verified

### No-Go

No-Go when the request implies:

- parser execution
- scratch copy
- raw file content read
- NAS scan
- OpenSearch / Qdrant / MinIO write
- platform DB write
- audit table write beyond existing retrieval audit behavior
- Agent answer integration
- Agent DB / NAS CRUD
- repair / cleanup / backfill / reindex / delete / migration
- production rollout
- non-test-machine environment
- payload over 1 document / 1 version / 20 chunks
- idempotency conflict
- unsafe raw fields in payload or report

## Codex C / Test-Machine Validation Prompt Outline

Future Codex C validation must be separately authorized and should follow this outline:

1. Read this document and the operator approval JSON.
2. Confirm test-machine environment, git ref, feature flags, and clean worktree.
3. Confirm no API / CLI runtime wiring is being introduced.
4. Confirm all prerequisite report refs exist and are sanitized.
5. Do not run a writer unless a later prompt explicitly authorizes it.
6. If a later smoke-only runner exists and is authorized, execute exactly one `write_run_id`.
7. Inspect created rows only by `write_run_id`.
8. Run rollback dry-run after write; do not delete or mutate rows.
9. Emit sanitized report only.
10. Stop on any No-Go trigger.

## Current Conclusion

Phase 2.87c completes planning for a future controlled runtime evidence write smoke. It does not authorize the smoke. The next step is Codex B review of this plan and the handoff files. Baseline, runtime smoke, and Phase 2.87d require separate authorization.
