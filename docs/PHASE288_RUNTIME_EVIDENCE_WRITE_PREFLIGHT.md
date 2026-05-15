# Phase 2.88 Runtime Evidence Write Preflight Runner

## Status

- Phase: 2.88
- Scope: local dry-run / preflight-only implementation
- Previous baseline: `3b01b0f`, tag `phase-2.87d-runtime-evidence-write-execution-pack-baseline`
- Current decision: preflight runner may validate readiness and produce an ignored local report, but must stop before any writer invocation.

## Implemented Files

- `app/services/asset_catalog/evidence_write_runtime_preflight.py`
- `scripts/phase288_runtime_evidence_write_preflight.py`
- `tests/test_data_steward_evidence_write_runtime_preflight.py`
- `reports/evidence_write_runtime_preflight/.gitignore`
- `reports/evidence_write_runtime_preflight/README.md`

## Behavior

The runner reads a local operator approval JSON and validates:

1. required approval fields
2. approval version
3. approval expiry
4. `target_environment=test_machine_only`
5. expected git commit
6. optional sanitized worktree status
7. one-run scope limits
8. allowed write action
9. feature flags
10. idempotency key / write run id / payload fingerprint
11. local prerequisite report refs
12. sanitized report markers

It returns one of:

- `preflight_ready_for_operator_stop`
- `preflight_pause`
- `preflight_no_go`

`preflight_ready_for_operator_stop` is not write authorization. It means the operator must stop before any future writer invocation.

## Safety Guarantees

The runner does not:

- call `EvidenceOnlyWriter.write()`
- write DB rows
- wire API / CLI runtime paths
- run parser
- copy files
- read raw file content
- scan NAS
- write OpenSearch / Qdrant / MinIO
- write platform DB
- write audit table
- enable Agent answer integration
- execute repair / cleanup / backfill / reindex / delete / migration
- enter rollout

The report always includes:

- `dry_run=true`
- `writes_authorized=false`
- `would_invoke_writer=false`
- safety flags showing no side effects

## CLI

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase288_runtime_evidence_write_preflight.py \
  --approval-json <local-ignored-approval.json> \
  --output <local-ignored-runtime-preflight.json> \
  --expected-git-commit <reviewed-commit> \
  --worktree-status-file <optional-sanitized-status-file>
```

The CLI writes a sanitized report to the requested output path and prints a minimal sanitized summary.

## Report Storage

Default local report directory:

```text
reports/evidence_write_runtime_preflight/
```

Real report JSON files are ignored by default and must not be committed.

## Validation

Validation completed:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_evidence_write_runtime_preflight.py -q  # 10 passed
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_write_runtime_preflight.py scripts/phase288_runtime_evidence_write_preflight.py  # passed
UV_CACHE_DIR=/private/tmp/uv-cache uv run --extra dev pytest tests/test_data_steward_*.py -q  # 143 passed
git diff --check  # passed
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null  # passed
git check-ignore reports/agent_runs/latest.json  # passed
```

Local fixture CLI smoke used only temporary files and returned `preflight_ready_for_operator_stop` with `would_invoke_writer=false` and `db_writes=false`.

## Current Conclusion

Phase 2.88 implements a local preflight-only runner. It narrows future runtime smoke risk by validating approval, refs, flags, limits, idempotency, and sanitized reports before any writer can be invoked. It does not authorize the smoke itself.
