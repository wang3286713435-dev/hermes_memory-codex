# Codex Test-Machine Runtime Preflight Smoke Prompt

## Purpose

Run the Phase 2.88 runtime evidence write preflight runner on the Mac mini / test machine only.

This prompt is for a preflight check only. Stop after the preflight result. Do not call a writer.

## Reviewed Ref

Use only:

- commit: `b09c3d1`
- tag: `phase-2.88-runtime-evidence-write-preflight-baseline`

If the local checkout is not exactly this commit or tag, stop and report `Pause`.

## Hard Boundaries

Do not:

1. call `EvidenceOnlyWriter.write()`
2. import or run any runtime path that invokes writer execution
3. write real Hermes DB rows
4. write platform DB rows
5. run API / CLI Agent runtime wiring
6. run parser
7. copy scratch files
8. read raw file content
9. scan NAS
10. write OpenSearch / Qdrant / MinIO
11. write audit table outside existing normal retrieval audit behavior
12. enable Agent answer integration
13. run Agent DB / NAS CRUD
14. repair / cleanup / backfill / reindex / delete / migration
15. enter production rollout
16. enable real-write feature flags
17. treat `preflight_ready_for_operator_stop` as write authorization

## Required Inputs

The operator must provide local ignored paths for:

1. operator approval JSON
2. preflight output JSON under ignored `reports/evidence_write_runtime_preflight/`
3. worktree status capture file under an ignored local path

The operator approval JSON must contain refs to prerequisite reports. Confirm those refs exist, but do not print raw path values, filenames, NAS paths, raw text, raw DB rows, source payloads, secrets, or sensitive business values.

## Required Checks Before Running

1. Confirm git commit:

   ```bash
   git rev-parse --short HEAD
   git tag --points-at HEAD
   ```

2. Confirm ignored output policy:

   ```bash
   git check-ignore reports/evidence_write_runtime_preflight/sample.json
   ```

3. Confirm approval JSON parses without printing content:

   ```bash
   UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool <local_ignored_operator_approval_json> >/dev/null
   ```

4. Capture worktree status to a local ignored file:

   ```bash
   git status --short > <local_ignored_worktree_status_file>
   ```

If any check fails, stop and report `Pause`.

## Only Allowed Command

Run only:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase288_runtime_evidence_write_preflight.py \
  --approval-json <local_ignored_operator_approval_json> \
  --output <local_ignored_preflight_report_json> \
  --expected-git-commit b09c3d1 \
  --worktree-status-file <local_ignored_worktree_status_file>
```

Do not run writer, parser, API smoke, DB smoke, index smoke, object-store smoke, NAS scan, repair, reindex, cleanup, migration, or rollout commands.

## Report Only Sanitized Fields

Return only:

1. API / CLI status only if checked without side effects
2. git commit / tag match
3. decision state
4. expected commit match
5. worktree clean true/false
6. prerequisite refs present true/false
7. `would_invoke_writer`
8. `db_writes`
9. parser / copy / NAS / index / object-store / Agent answer flags
10. pause/no-go reasons
11. sanitized output report filename only

Do not print:

1. raw approval JSON
2. local absolute paths
3. true filenames
4. true NAS paths
5. raw text
6. raw DB rows
7. secrets
8. source payloads
9. sensitive business values

## Decision Rules

### Go

Only if the command returns `preflight_ready_for_operator_stop` and all forbidden action flags remain false.

Go still means stop. It does not authorize writer invocation.

### Pause

If approval, refs, output ignore policy, git ref, or worktree state are incomplete or unclear.

### No-Go

If scope, target environment, feature flags, unsafe refs, missing idempotency, missing fingerprint, missing `write_run_id`, or forbidden action attempts are detected.

## Required Final Statement

End with:

```text
Preflight completed. Writer invocation remains blocked. Real DB writes remain blocked. Separate authorization is required for any future runtime evidence write smoke.
```
