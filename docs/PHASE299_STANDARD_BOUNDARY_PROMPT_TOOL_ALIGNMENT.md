# Phase 2.99 Standard Boundary Prompt / Tool Description Alignment

## Goal

Convert Phase 2.98 and shared Digital Delivery Standard boundary findings into a minimal Hermes-side, locally testable response-boundary artifact.

This phase does not expand Hermes runtime capability. It only adds pure-Python classification and templates for catalog-only / Missing Evidence / lineage-only answer boundaries.

Previous baseline:

- Commit: `40f71b9`
- Tag: `phase-2.98-standard-agent-boundary-review-baseline`
- Pushed: true

## Files Changed

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
11. ignored `reports/agent_runs/latest.json`

## Implemented Findings

Implemented as a small pure-Python Data Steward boundary module:

1. DWG layer/title block/xref/block/coordinate/drawing-content questions require `dwg_parse_evidence`.
2. RVT Level/Grid/Sheet/View/Family/Type/model-internal questions require `rvt_parse_evidence`.
3. BIM component / parameter / LOD / LOI questions require `component_evidence` or `manual_evidence`.
4. PDF / Office full-text content questions require `full_text_evidence`.
5. Catalog / filename / redacted-path lineage answers use the required phrase: `目录/文件名/脱敏路径线索显示……`.
6. `A004-A010` are treated as `sometimes` / lineage-only candidates and not as strong facts or compliance conclusions.
7. Memory references such as `related_file_ids`, `query_id`, `project_id`, and `feedback_labels` are represented as low-sensitive references only, not proof of NAS file content reading.
8. Boundary templates include side-effect flags showing no writes to documents, chunks, OpenSearch, or Qdrant.

## Phase 2.99a Review Fix

Codex B review found one blocking coverage gap: `docx` and `xlsx` content questions were falling through to `current_lineage`.

Fixed in Phase 2.99a:

1. `docx` content questions now return `missing_evidence` with `full_text_evidence`.
2. `xlsx` content questions now return `missing_evidence` with `full_text_evidence`.
3. Existing `pptx` and `pdf` behavior remains `missing_evidence` with `full_text_evidence`.
4. True catalog / filename / redacted-path lineage questions remain `current_lineage`.

## Explicit Non-goals

This phase did not:

1. connect to DB / NAS / platform API / Hermes API
2. run frontend / Gateway smoke
3. modify shared standard files
4. invoke parser, scratch copy, writer smoke, backfill, reindex, repair, cleanup, delete, or migration
5. read DWG / RVT / NWD / IFC content
6. write `documents`, `document_versions`, `chunks`, `citations`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes long-term memory
7. implement Agent answer integration
8. enter production rollout

## Tests Run

TDD was used:

1. RED observed:
   - `UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_standard_answer_boundary.py -q`
   - failure: `ModuleNotFoundError: No module named 'app.services.asset_catalog.standard_answer_boundary'`
2. GREEN observed:
   - `UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_standard_answer_boundary.py -q`
   - result: `9 passed`
3. Phase 2.99a RED observed:
   - `docx` and `xlsx` regression tests failed as `current_lineage`.
4. Phase 2.99a GREEN observed:
   - `UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_standard_answer_boundary.py -q`
   - result: `11 passed`
5. Explicit Office/PDF probe:
   - `docx`, `xlsx`, `pptx`, and `pdf` content queries all return `missing_evidence ('full_text_evidence',)`.

Final validation is recorded in `ACTIVE_PHASE.md` and `reports/agent_runs/latest.json`.

## Remaining Risks

1. This is a local boundary artifact, not production prompt deployment.
2. Shared docs still need future official-name cleanup where `Hermes / Jarvis` appears.
3. Runtime Gateway / Agent integration still requires a separate reviewed phase.
4. The classifier is intentionally conservative and should not be treated as semantic parsing.

## Boundary Confirmation

Phase 2.99 is not production rollout and not DB/NAS runtime authorization.

The added module only returns boundary classifications, templates, and side-effect flags. It performs no IO and no external service calls.
