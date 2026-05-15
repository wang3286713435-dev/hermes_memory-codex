# Phase 2.87d Runtime Evidence Write Smoke Execution Pack

## Status

- Phase: 2.87d
- Scope: docs-only / handoff planning
- Previous baseline: `490b5ca`, tag `phase-2.87c-runtime-evidence-write-smoke-plan-baseline`
- Current decision: future runtime evidence write smoke remains blocked until a later explicit execution prompt and operator approval.

This pack turns the Phase 2.87c smoke plan into a concrete test-machine handoff. It does not execute the smoke, does not wire API / CLI runtime code, and does not authorize any DB / index / object-store write.

## Required Test-Machine Preconditions

The future smoke may only be considered when all of the following are true:

1. Machine is non-production Mac mini / test-machine.
2. Git ref is a reviewed commit or tag, starting from `phase-2.87c-runtime-evidence-write-smoke-plan-baseline` or an explicitly approved successor.
3. Worktree has no unexpected dirty files.
4. Operator approval JSON exists in an ignored local path.
5. All prior report refs exist and are sanitized.
6. Feature flags are default-off before review.
7. The selected payload remains within the one-run tiny boundary.
8. The execution operator understands that `approved_for_smoke` does not mean repair, rollout, Agent answer, index write, parser execution, NAS scan, or production deployment.

If any precondition is missing, the decision is `Pause`.

## Reviewed Refs / Tags

Minimum reviewed refs:

- Phase 2.87b writer baseline: `44cc837`, tag `phase-2.87b-evidence-only-writer-baseline`
- Phase 2.87c runtime smoke plan baseline: `490b5ca`, tag `phase-2.87c-runtime-evidence-write-smoke-plan-baseline`

Any successor commit must be explicitly named in operator approval and Codex B review.

## Environment Keys By Name Only

Future smoke planning may reference these key names, without storing values in tracked docs:

```text
DATABASE_URL
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED
PLATFORM_ASSET_INDEX_WRITE_ENABLED
PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED
HERMES_ENV
HERMES_EVIDENCE_WRITE_OPERATOR_APPROVAL
HERMES_EVIDENCE_WRITE_REPORT_DIR
```

No secret, DSN value, token, password, raw NAS path, raw filename, or raw file content may be committed.

## Operator Approval JSON

The approval must be a local ignored JSON file. Suggested path shape:

```text
reports/evidence_write_approvals/<approval_id>.json
```

Required schema summary:

- `approval_version`
- `approval_id`
- `approved_by`
- `approved_at`
- `expires_at`
- `target_environment`
- `target_git_commit`
- `source_system`
- `source_asset_ref`
- `project_scope`
- `permission_proof_ref`
- `sanitized_manifest_ref`
- `eligibility_report_ref`
- `payload_plan_ref`
- `preflight_report_ref`
- `dry_run_ref`
- `rehearsal_ref`
- `rollback_dry_run_ref`
- `write_run_id`
- `evidence_write_idempotency_key`
- `expected_payload_fingerprint`
- `max_documents`
- `max_document_versions`
- `max_chunks`
- `allowed_write_action`
- `feature_flags_expected`
- `writes_authorized`
- `operator_notes`

Approval is invalid if it includes raw content, true NAS path, true filename, secrets, or a scope larger than one source asset / one document / one version / 20 chunks.

## Required Prior Report Refs

The future execution prompt must name sanitized local report refs for:

1. permission proof
2. sanitized parser preview
3. sanitized evidence manifest
4. evidence-write eligibility report
5. evidence-write payload plan
6. evidence-write preflight report
7. evidence-write dry-run report
8. evidence-write rehearsal report
9. rollback dry-run reference

These refs are evidence of review readiness only. They are not document evidence and must not be used in Agent answers.

## Feature Flag Expectations

Default state:

```text
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=false
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED=false
PLATFORM_ASSET_INDEX_WRITE_ENABLED=false
PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED=false
```

Future one-run smoke may only consider enabling:

```text
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=true
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=true
```

All other flags remain false unless a separate phase explicitly changes the boundary.

## One-Run Write Boundary

The future writer invocation, if separately authorized, must be limited to:

- one approved source asset
- one `Document`
- one `DocumentVersion`
- up to 20 `Chunk` rows
- matching `CitationRecord` rows
- one `write_run_id`
- one idempotency key
- one operator approval id

No OpenSearch, Qdrant, MinIO, platform DB, audit table write, parser, NAS, Agent answer, repair, cleanup, backfill, reindex, delete, migration, or rollout may be part of the same run.

## Preflight-Only Command Outline

The following commands are inspection-only and do not authorize a writer invocation:

```bash
git rev-parse HEAD
git tag --points-at HEAD
git status --short

UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool "$HERMES_EVIDENCE_WRITE_OPERATOR_APPROVAL" >/dev/null

# Inspect referenced local reports by path only.
# Do not print raw contents into tracked files.
# Do not invoke writer.
# Do not run parser.
# Do not copy files.
# Do not scan NAS.
```

Future execution may add a smoke-only command only in a later separately authorized phase. Phase 2.87d does not define or run that command.

## Mandatory Stop Points

Stop before any writer invocation when:

1. approval JSON is absent, expired, invalid, or mismatched
2. target git ref differs from approval
3. unexpected dirty files exist
4. report refs are missing or unsafe
5. payload fingerprint differs from approval
6. feature flags differ from approval
7. scope exceeds limits
8. rollback dry-run ref is missing
9. operator asks to include parser/copy/NAS/index/object-store/platform DB/audit/Agent answer/repair/rollout in the same run

## Expected Sanitized Report Fields

A future execution report must be ignored local JSON and include:

- `report_version`
- `write_run_id`
- `operator_approval_id`
- `target_environment`
- `git_commit`
- `status`
- `write_executed`
- `created_counts`
- `idempotency_status`
- `rollback_dry_run_before`
- `rollback_dry_run_after`
- `post_write_inspection`
- `forbidden_actions`
- `sanitized=true`

It must not include raw text, true filenames, true NAS paths, secrets, raw DB rows, sensitive business values, or full source payloads.

## Rollback Dry-Run And Idempotency Checks

Future execution must verify:

1. pre-write rollback dry-run is empty or reports a reviewed duplicate state for the same `write_run_id`
2. post-write rollback dry-run lists only rows created under the dedicated `write_run_id`
3. rerun with same idempotency key and same payload fingerprint creates zero new rows
4. rerun with same idempotency key and different payload fingerprint is `No-Go`
5. rollback dry-run remains diagnostic and does not delete, repair, invalidate, or cleanup rows

## Go / Pause / No-Go

### Go

For Phase 2.87d itself, `Go` only means the execution pack is ready for Codex B review.

### Pause

Pause if approval, refs, flags, clean worktree, rollback dry-run, payload fingerprint, or test-machine status are not fully verified.

### No-Go

No-Go if the request includes runtime execution in this phase, real DB write, API / CLI wiring, parser, copy, raw content read, NAS scan, index/object-store/platform DB write, Agent answer, repair, reindex, delete, migration, rollout, or feature flag enablement.

## Current Conclusion

Phase 2.87d remains handoff-only. The next step is Codex B review of this execution pack and the test-machine prompt. Real smoke execution requires a later explicit authorization.
