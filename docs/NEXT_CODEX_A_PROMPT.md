# NEXT_CODEX_A_PROMPT

## Phase 2.99a Codex B Review And Selective Baseline Preparation

You are Codex A. This prompt is for the next handoff state after completing the Phase 2.99a review fix.

Do not modify runtime behavior beyond the reviewed boundary artifact. Do not connect to DB / NAS / platform API / Hermes API. Do not run frontend / Gateway smoke. Do not enter the next phase before Codex B review.

## Background

Phase 2.99a fixed the Codex B review blocker:

1. `docx` content questions now return `missing_evidence` with `full_text_evidence`.
2. `xlsx` content questions now return `missing_evidence` with `full_text_evidence`.
3. Existing `pptx` and `pdf` Missing Evidence behavior remains intact.
4. True catalog / filename / redacted-path lineage behavior remains unchanged.

Previous baseline:

1. commit: `40f71b9`
2. tag: `phase-2.98-standard-agent-boundary-review-baseline`
3. pushed: true

## Codex B Review Scope

Codex B should review:

1. `app/services/asset_catalog/standard_answer_boundary.py`
2. `tests/test_data_steward_standard_answer_boundary.py`
3. `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`
8. `docs/HANDOFF_LOG.md`
9. ignored `reports/agent_runs/latest.json`

Review must confirm:

1. `docx`, `xlsx`, `pptx`, and `pdf` content questions return `missing_evidence` with `full_text_evidence`.
2. Catalog / filename / redacted-path lineage questions still return `current_lineage`.
3. No shared standard files were modified.
4. No DB / NAS / API / Gateway / parser / writer / index / memory / rollout work was done.

## If Review Passes

Prepare a selective baseline only after Codex B approval.

Expected staged files:

1. `app/services/asset_catalog/standard_answer_boundary.py`
2. `app/services/asset_catalog/__init__.py`
3. `tests/test_data_steward_standard_answer_boundary.py`
4. `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`
5. `docs/NEXT_CODEX_A_PROMPT.md`
6. `docs/ACTIVE_PHASE.md`
7. `docs/PHASE_BACKLOG.md`
8. `docs/HANDOFF_LOG.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

Do not stage:

1. `reports/agent_runs/latest.json`
2. any real reports JSON
3. any shared standard files
4. any DB / NAS / API runtime artifacts

Suggested commit message:

```text
feat: add standard answer boundary templates
```

Suggested tag:

```text
phase-2.99-standard-boundary-alignment-baseline
```

## Validation Before Baseline

Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_standard_answer_boundary.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/*.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_asset_catalog_query_preview.py tests/test_data_steward_asset_catalog_missing_evidence_response.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

Also run the explicit Office/PDF probe from Phase 2.99a.

Do not run real Gateway smoke or DB/NAS live smoke.

## Hard Boundaries

Still forbidden:

1. connecting to real DB / NAS / platform API / Hermes API
2. running frontend / Gateway smoke
3. modifying shared docs directly
4. Agent DB CRUD
5. Agent-generated SQL
6. NAS scan/copy
7. parser invocation
8. scratch copy
9. writer smoke against real DB
10. writing `documents`, `document_versions`, `chunks`, `citations`
11. writing OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
12. reading DWG / RVT / NWD / IFC content
13. exposing true `storage_path`, raw row, NAS path, raw content, secret, token, bearer, or credential material
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout

## Stop Condition

Stop after Codex B review or selective baseline.

Do not enter the next phase automatically.
