# NEXT_CODEX_A_PROMPT

## Phase 2.81a Git Baseline Task

Phase 2.81a sanitized evidence manifest dry-run implementation is complete and Codex B review has passed.

This baseline must only capture the local ignored-manifest dry-run implementation. Do not enter the next phase.

## Summary

Implemented:

1. `app/services/asset_catalog/evidence_manifest.py`
2. `scripts/phase281a_sanitized_evidence_manifest.py`
3. `tests/test_data_steward_sanitized_evidence_manifest.py`
4. `reports/nas_evidence_manifests/.gitignore`
5. `reports/nas_evidence_manifests/README.md`
6. `docs/PHASE281A_SANITIZED_EVIDENCE_MANIFEST_DRY_RUN.md`

Capability:

1. Read sanitized parser-preview metadata from explicit JSON input.
2. Reject forbidden raw fields such as `raw_text`, `true_filename`, `nas_path`, `source_path`, `scratch_path`, `raw_row`, `secret`, `token`, `password`, and `api_key`.
3. Generate `nas_evidence_manifest.v0`.
4. Mark manifests `no_go` if write or Agent answer safety flags are true.
5. Write manifest JSON only into ignored local artifact storage.

## Allowed Stage Files

Only stage these files:

1. `app/services/asset_catalog/evidence_manifest.py`
2. `app/services/asset_catalog/__init__.py`
3. `scripts/phase281a_sanitized_evidence_manifest.py`
4. `tests/test_data_steward_sanitized_evidence_manifest.py`
5. `reports/nas_evidence_manifests/.gitignore`
6. `reports/nas_evidence_manifests/README.md`
7. `docs/PHASE281A_SANITIZED_EVIDENCE_MANIFEST_DRY_RUN.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.
Do not stage real files under `reports/nas_evidence_manifests/*.json` or `*.md`.

## Validation Commands

Run:

```bash
uv run python -m py_compile app/services/asset_catalog/evidence_manifest.py scripts/phase281a_sanitized_evidence_manifest.py
uv run --extra dev pytest tests/test_data_steward_sanitized_evidence_manifest.py -q
uv run --extra dev pytest tests/test_data_steward_*.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/nas_evidence_manifests/example.json
```

## Hard Boundaries

Forbidden:

1. Execute parser.
2. Copy real files.
3. Read raw file contents.
4. Write platform DB / Hermes DB / `documents` / `chunks`.
5. Write OpenSearch / Qdrant / MinIO.
6. Scan NAS.
7. Agent DB / NAS CRUD.
8. Agent final answer integration.
9. Treat manifest as document evidence.
10. Commit ignored manifest artifacts.
11. Repair / cleanup source data / backfill / reindex / delete / migration.
12. Production rollout.

## Baseline Steps

1. Confirm dirty set contains only allowed files.
2. Run validation commands above.
3. Selective stage allowed files only.
4. Commit message:
   - `chore: add phase 2.81a sanitized evidence manifest dry-run`
5. Tag:
   - `phase-2.81a-sanitized-evidence-manifest-dry-run-baseline`
6. Push `origin/main` and tag.
7. Stop. Do not enter evidence-write planning or Agent answer integration.

## Acceptance Criteria

1. Final `git status --short` clean.
2. Commit includes only allowed files.
3. `reports/agent_runs/latest.json` is ignored and not committed.
4. No real manifest artifact is committed.
5. No parser / file copy / DB / index / object-store / Agent answer side effect occurred.
