# Phase 2.89 Test-Machine Runtime Preflight Smoke Plan

## Status

- Phase: 2.89
- Scope: docs-only / handoff-only
- Reviewed repo ref: `b09c3d1`
- Reviewed tag: `phase-2.88-runtime-evidence-write-preflight-baseline`
- Current decision: prepare Mac mini / test-machine instructions for running the Phase 2.88 preflight runner only.

This phase does not run the preflight runner. It does not authorize writer invocation, real DB writes, parser execution, NAS copy/scan, index/object-store writes, Agent answer integration, repair, reindex, or rollout.

## Objective

Prepare a test-machine handoff package that lets Codex C / operator run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase288_runtime_evidence_write_preflight.py \
  --approval-json <local_ignored_operator_approval_json> \
  --output <local_ignored_preflight_report_json> \
  --expected-git-commit b09c3d1 \
  --worktree-status-file <local_ignored_worktree_status_file>
```

The command must validate readiness and stop at `preflight_ready_for_operator_stop`, `preflight_pause`, or `preflight_no_go`.

## Required Local Ignored Inputs

The test machine must provide local ignored paths for:

1. operator approval JSON
2. permission proof report ref
3. sanitized manifest report ref
4. eligibility report ref
5. payload plan ref
6. preflight report ref
7. dry-run report ref
8. rehearsal report ref
9. rollback dry-run report ref
10. worktree status capture file
11. output report under `reports/evidence_write_runtime_preflight/`

Tracked docs may name path shapes only. They must not contain secrets, raw text, true filenames, true NAS paths, raw DB rows, source payloads, or sensitive business values.

## Preflight Stop Condition

`preflight_ready_for_operator_stop` means:

1. preflight checks passed
2. the operator must stop
3. writer invocation is still not authorized
4. real DB writes are still not authorized
5. a separate explicit prompt is required before any future runtime evidence write smoke

`preflight_ready_for_operator_stop` must never be described as write execution, document evidence creation, index creation, or Agent answer readiness.

## Go / Pause / No-Go

### Go

For Phase 2.89, Go means this handoff package is ready for Codex B review.

For the future test-machine run, Go means only that the preflight command returned `preflight_ready_for_operator_stop` and the operator stopped.

### Pause

Pause if:

1. approval JSON is missing, expired, malformed, or mismatched
2. any prerequisite report ref is missing
3. worktree status is not clean
4. target git commit does not match `b09c3d1`
5. required local ignored output directory is not ignored
6. CLI output includes path, filename, raw content, secret, raw DB row, or sensitive business value

### No-Go

No-Go if:

1. `target_environment` is not `test_machine_only`
2. scope exceeds 1 document, 1 document version, or 20 chunks
3. `allowed_write_action` is not `first_real_hermes_evidence_write_smoke`
4. forbidden feature flags are true
5. report refs appear unsafe
6. payload fingerprint, idempotency key, or `write_run_id` is missing
7. any step attempts writer invocation, parser execution, NAS copy/scan, DB write, index/object-store write, Agent answer integration, repair, reindex, delete, migration, or rollout

## Sanitized Report Requirements

The future output report must be ignored local JSON under `reports/evidence_write_runtime_preflight/`.

It may include:

- decision state
- expected commit match
- worktree clean true/false
- prerequisite ref presence
- `would_invoke_writer=false`
- `db_writes=false`
- parser/copy/NAS/index/object-store/Agent answer flags
- pause/no-go reasons

It must not include:

- raw approval JSON
- secrets
- raw text
- true filename
- true NAS path
- raw DB rows
- source payloads
- sensitive business values
- unredacted absolute local paths in tracked files

## Explicit Non-Authorization

Phase 2.89 is not runtime evidence write execution.

It does not authorize:

1. `EvidenceOnlyWriter.write()`
2. real Hermes DB writes
3. platform DB writes
4. parser execution
5. scratch copy
6. raw file content read
7. NAS scan
8. OpenSearch / Qdrant / MinIO writes
9. audit table writes beyond existing normal retrieval audit behavior
10. Agent answer integration
11. repair / cleanup / backfill / reindex / delete / migration
12. production rollout
13. enabling real-write feature flags outside a future explicitly authorized test-machine run

## Next Step

Codex B should review this plan and `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`.

If review passes, the next prompt may baseline these docs. The actual test-machine preflight run still requires separate explicit authorization.
