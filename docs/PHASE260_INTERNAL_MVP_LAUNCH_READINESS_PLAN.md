# Phase 2.60 Internal MVP Launch Readiness Pack

## Goal

Phase 2.60 adds a read-only local readiness runner for Mac mini operators before internal controlled MVP usage.

The runner is a pre-use gate. It is not production rollout approval, not the second real natural import smoke, not Data Steward / DB / NAS / BIM implementation, and not an upload path.

## Scope

The runner checks whether local prerequisites appear ready enough for internal controlled MVP usage:

1. Current Git HEAD and baseline tag are readable.
2. `reports/agent_runs/latest.json` exists and parses.
3. Natural import operator checklist exists.
4. Codex C pending authorization prompt exists.
5. Phase 2.59 second-smoke gate document exists.
6. `scripts/run_local_api.sh` exists.
7. Optional API `/health` is reachable unless skipped.
8. Dangerous authorization env flags are not enabled.
9. Data Steward / DB / NAS activation is not required for this phase.

## Runner

Script:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py --skip-api-health
```

Optional API health check:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py \
  --api-url http://127.0.0.1:8000
```

The runner is read-only. It does not start services, upload files, run Hermes CLI query smoke, write DB/index data, execute repair, or enter rollout.

## Output Policy

The JSON output always includes:

- `dry_run=true`
- `read_only=true`
- `destructive_actions=[]`
- `real_upload_called=false`
- `api_smoke_called=false`
- `cli_smoke_called=false`
- `db_or_index_written=false`
- `production_rollout=false`
- `status=go|pause|no_go`
- `checks[]`
- `known_risks[]`
- `operator_next_steps[]`

If `--output-json` is used, it must be an explicit local path supplied by the operator. The runner does not choose a persistent report path by default.

## Go / Pause / No-Go

### Go

All checks pass. This means internal controlled MVP use may proceed under human operator supervision.

Go does not mean production rollout, automatic tender review, automatic decision making, Data Steward readiness, or authorization to upload arbitrary files.

### Pause

At least one prerequisite is missing or optional API health is unavailable.

The operator should fix prerequisites and rerun the dry-run. The runner must not start services or repair state automatically.

### No-Go

Dangerous authorization signals are enabled, such as cleanup, repair, backfill, reindex, or rollout flags.

The operator must stop and ask for Codex B / human owner review before continuing.

## Non-Goals

- No real upload.
- No second real file smoke.
- No Hermes CLI query smoke.
- No service startup.
- No DB / facts / document_versions / audit_logs writes.
- No OpenSearch / Qdrant / MinIO writes.
- No cleanup, delete, repair, backfill, reindex, or migration.
- No DB / NAS / Data Steward / BIM / TB file pool implementation.
- No production rollout.
- No retrieval contract, facts contract, version governance, or memory kernel architecture changes.

## Current Result

Phase 2.60 implementation is complete and awaiting Codex B review.

Validation:

- `uv run python -m py_compile scripts/phase260_mvp_local_readiness_pack.py`
- `uv run pytest tests/test_phase260_mvp_local_readiness_pack.py tests/test_phase257a_natural_import_evidence_template.py -q`
- `git diff --check`
- `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase260_check.json`

Offline dry-run:

- `uv run python scripts/phase260_mvp_local_readiness_pack.py --skip-api-health`

No API/CLI smoke, upload, DB/index write, repair, backfill, reindex, or rollout was executed.
