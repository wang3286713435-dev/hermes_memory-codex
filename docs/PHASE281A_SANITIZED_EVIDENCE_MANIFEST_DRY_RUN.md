# Phase 2.81a Sanitized Evidence Manifest Dry-run

## Summary

Phase 2.81a implements the first local sanitized evidence manifest dry-run.

This phase does not parse files, copy files, connect to NAS, write databases, write indexes, write object storage, or connect NAS-derived content to Agent final answers.

## Implemented

1. Added `app/services/asset_catalog/evidence_manifest.py`.
2. Added `scripts/phase281a_sanitized_evidence_manifest.py`.
3. Added `tests/test_data_steward_sanitized_evidence_manifest.py`.
4. Added ignored local manifest policy under `reports/nas_evidence_manifests/`.

The manifest builder reads sanitized parser-preview metadata and emits `nas_evidence_manifest.v0`.

## Manifest Boundary

The manifest may include:

1. Redacted / hashed asset reference.
2. Source view.
3. Project scope proof status.
4. File type and size buckets.
5. Parser status and sanitized parser identifier.
6. Structure count buckets.
7. Sanitized warning codes.
8. Safety flags.
9. Scratch / preview cleanup status.
10. Go / Pause / No-Go decision fields.

The manifest must not include:

1. Raw extracted text.
2. True filenames.
3. True NAS paths.
4. Raw DB rows.
5. Secrets, tokens, passwords, or API keys.
6. Sensitive business values.
7. Prompt-ready document evidence.

## Safety Behavior

The builder rejects previews containing forbidden fields such as `raw_text`, `true_filename`, `nas_path`, `source_path`, `scratch_path`, `raw_row`, `secret`, `token`, `password`, or `api_key`.

If sanitized safety flags indicate any write or Agent answer integration, the manifest is marked `no_go` instead of `ready_for_review`.

## Local Artifact Policy

Future manifest artifacts are written only under ignored local storage:

```text
reports/nas_evidence_manifests/*.json
reports/nas_evidence_manifests/*.md
```

The tracked files in that directory are only:

1. `reports/nas_evidence_manifests/.gitignore`
2. `reports/nas_evidence_manifests/README.md`

## Validation

Completed:

1. Red test observed with missing `app.services.asset_catalog.evidence_manifest`.
2. Red test observed with missing `scripts/phase281a_sanitized_evidence_manifest.py`.
3. Target tests passed after implementation: `uv run --extra dev pytest tests/test_data_steward_sanitized_evidence_manifest.py -q`.

Pending final validation before baseline:

1. `uv run python -m py_compile app/services/asset_catalog/evidence_manifest.py scripts/phase281a_sanitized_evidence_manifest.py`
2. `uv run --extra dev pytest tests/test_data_steward_sanitized_evidence_manifest.py -q`
3. Existing Data Steward regression target.
4. `git diff --check`
5. `uv run python -m json.tool reports/agent_runs/latest.json`
6. `git check-ignore reports/nas_evidence_manifests/example.json`

## Still Forbidden

1. Parser execution.
2. Real file copy.
3. Reading raw file contents.
4. Writing `documents` or `chunks`.
5. Writing OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB.
6. Connecting manifest to Agent final answer.
7. Scanning NAS.
8. Agent DB / NAS CRUD.
9. Repair, backfill, reindex, delete, migration, cleanup source data, or rollout.

## Next

After Codex B review and validation, Phase 2.81a can be baselined.

The next capability after baseline should be planning only: evidence-write eligibility review. It must not write `documents/chunks` or indexes without a separate explicit phase.

