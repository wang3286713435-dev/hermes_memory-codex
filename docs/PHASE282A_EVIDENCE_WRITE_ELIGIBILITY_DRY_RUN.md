# Phase 2.82a Evidence Write Eligibility Dry-run

## Summary

Phase 2.82a implements a local dry-run eligibility evaluator for sanitized NAS evidence manifests.

The evaluator reads an ignored local `nas_evidence_manifest.v0` JSON and writes an ignored local `nas_evidence_write_eligibility.v0` report. It does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not run parser, copy files, read raw content, connect to NAS, or connect manifests to Agent final answers.

## Implemented

1. Added `app/services/asset_catalog/evidence_eligibility.py`.
2. Added `scripts/phase282a_evidence_write_eligibility.py`.
3. Added target tests in `tests/test_data_steward_evidence_write_eligibility.py`.
4. Added ignored local report policy under `reports/nas_evidence_eligibility/`.

## Eligibility States

The dry-run report classifies a manifest as:

1. `not_eligible`
2. `eligible_for_human_review`
3. `eligible_for_evidence_write_planning`
4. `no_go`

No state authorizes actual writes.

## Required Gates

`eligible_for_evidence_write_planning` requires:

1. Supported manifest version.
2. `decision.manifest_status=ready_for_review`.
3. `source.project_scope_proven=true`.
4. `source.permission_proof_status=valid`.
5. `source.storage_locator_present=true`.
6. Parser status `parsed`.
7. Non-empty / non-unknown text length bucket.
8. Scratch and preview cleanup both `all_deleted`.
9. All safety write / answer flags are false.
10. No forbidden raw fields.
11. `index_eligibility_status=eligible_for_preview`.
12. `confidentiality_status=known`.
13. `lifecycle_status=active`.
14. Supported text-capable file type.
15. Human review decision `approve_for_evidence_write_planning`.

Missing proof defaults to `DENIED`.

## CLI

Example:

```bash
uv run python scripts/phase282a_evidence_write_eligibility.py \
  --manifest-json reports/nas_evidence_manifests/redacted-run-001.json \
  --output-dir reports/nas_evidence_eligibility \
  --human-review-decision approve_for_evidence_write_planning
```

The generated report remains an ignored local artifact.

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
11. Treating manifest or eligibility report as document evidence.
12. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## TDD / Validation

Observed red:

1. Initial target pytest failed with missing `app.services.asset_catalog.evidence_eligibility`.

Target green:

1. `uv run --extra dev pytest tests/test_data_steward_evidence_write_eligibility.py -q` passed with `6 passed`.

Final validation:

1. `uv run python -m py_compile app/services/asset_catalog/evidence_eligibility.py scripts/phase282a_evidence_write_eligibility.py` passed.
2. `uv run --extra dev pytest tests/test_data_steward_evidence_write_eligibility.py -q` passed with `6 passed`.
3. `uv run --extra dev pytest tests/test_data_steward_*.py -q` passed with `98 passed`.
4. `git diff --check` passed.
5. `uv run python -m json.tool reports/agent_runs/latest.json >/dev/null` passed.
6. `git check-ignore reports/agent_runs/latest.json` passed.
7. `git check-ignore reports/nas_evidence_eligibility/example.json` passed.

## Current Conclusion

Phase 2.82a creates the review gate between sanitized parser preview manifests and a future evidence-write planning phase.

It still does not make NAS content answerable by the Agent.
