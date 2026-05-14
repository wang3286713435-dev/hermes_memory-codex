# Phase 2.83a Evidence Write Payload Dry-run

## Summary

Phase 2.83a implements a local dry-run payload builder for sanitized NAS evidence-write planning.

The builder reads an ignored local `nas_evidence_write_eligibility.v0` JSON and writes an ignored local `nas_evidence_write_payload.v0` JSON. It does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not run parser, copy files, read raw content, scan NAS, or connect payloads to Agent final answers.

## Implemented

1. Added `app/services/asset_catalog/evidence_payload.py`.
2. Added `scripts/phase283a_evidence_write_payload.py`.
3. Added target tests in `tests/test_data_steward_evidence_write_payload.py`.
4. Added ignored local report policy under `reports/nas_evidence_payloads/`.

## Payload States

The dry-run payload builder classifies an item as:

1. `payload_not_allowed`
2. `payload_ready_for_human_review`
3. `payload_ready_for_write_dry_run`
4. `payload_no_go`

No state authorizes actual writes.

## Required Gates

`payload_ready_for_write_dry_run` requires:

1. Supported eligibility report version.
2. Eligibility state `eligible_for_evidence_write_planning`.
3. Eligibility report write / answer flags all false.
4. No forbidden raw fields.
5. Project scope proven.
6. Permission proof valid.
7. Storage locator present.
8. Citation contract can be satisfied.
9. Human review decision `approve_for_payload_dry_run_planning`.

Missing proof defaults to `DENIED`.

## CLI

Example:

```bash
uv run python scripts/phase283a_evidence_write_payload.py \
  --eligibility-json reports/nas_evidence_eligibility/redacted-run-001-eligibility.json \
  --output-dir reports/nas_evidence_payloads \
  --human-review-decision approve_for_payload_dry_run_planning
```

The generated payload remains an ignored local artifact.

## Safety Boundary

Still forbidden:

1. Writing `documents`.
2. Writing `chunks`.
3. Writing OpenSearch, Qdrant, or MinIO.
4. Writing platform DB or Hermes DB.
5. Running parser.
6. Copying real files.
7. Reading raw file contents.
8. Scanning NAS.
9. Agent DB / NAS CRUD.
10. Agent final answer integration.
11. Treating manifest, eligibility report, or payload plan as document evidence.
12. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## TDD / Validation

Observed red:

1. Initial target pytest failed with missing `app.services.asset_catalog.evidence_payload`.

Target green:

1. `uv run --extra dev pytest tests/test_data_steward_evidence_write_payload.py -q` passed with `6 passed`.

Final validation:

1. `uv run python -m py_compile app/services/asset_catalog/evidence_payload.py scripts/phase283a_evidence_write_payload.py` passed.
2. `uv run --extra dev pytest tests/test_data_steward_evidence_write_payload.py -q` passed with `6 passed`.
3. `uv run --extra dev pytest tests/test_data_steward_*.py -q` passed with `104 passed`.
4. `git diff --check` passed.
5. `uv run python -m json.tool reports/agent_runs/latest.json >/dev/null` passed.
6. `git check-ignore reports/agent_runs/latest.json` passed.
7. `git check-ignore reports/nas_evidence_payloads/example.json` passed.

## Current Conclusion

Phase 2.83a creates a local payload dry-run layer after eligibility review.

It still does not make NAS content answerable by the Agent.
