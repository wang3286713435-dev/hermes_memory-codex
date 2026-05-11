# Phase 2.62 MVP Issue Triage Summary Runner

## 1. Goal

Phase 2.62 adds a local read-only issue triage summary runner for Mac mini internal MVP use.

The goal is to let an operator keep real issue JSON files under ignored local storage and generate a sanitized summary for Codex B review without copying long chat records.

This phase does not create external issues, write DB or index state, execute repair, or enter rollout.

## 2. Inputs

Supported inputs:

1. explicit issue JSON files via repeated `--input-json`.
2. one-level JSON files under a provided `--input-dir`, such as `reports/internal_mvp_issues`.

The runner only reads `.json` files. It does not read Markdown notes, screenshots, logs, Word files, spreadsheets, or images.

## 3. Output

The summary contains:

1. P0 / P1 / P2 / P3 counts.
2. final `ready` / `pause` / `no_go` status.
3. Codex B as next owner.
4. validation errors and invalid JSON files.
5. dangerous boolean field counts.
6. sanitized `issue_refs`.

`issue_refs` intentionally excludes raw query text, notes, expected behavior, actual behavior, full local paths, returned document ids, evidence chunk ids, and customer / project context.

## 4. Status Semantics

1. `ready`: no P0/P1 and no validation blocker.
2. `pause`: P1, ordinary validation error, or invalid JSON.
3. `no_go`: P0 or dangerous evidence / mutation / rollout field.

The runner reuses the Phase 2.61a validator semantics so issue intake and triage summary stay aligned.

## 5. CLI Examples

```bash
uv run python scripts/phase262_mvp_issue_triage_summary.py \
  --input-json reports/internal_mvp_issues/local_issue.json
```

```bash
uv run python scripts/phase262_mvp_issue_triage_summary.py \
  --input-dir reports/internal_mvp_issues \
  --output-json /tmp/hermes_issue_summary.json
```

The runner writes only to stdout by default. `--output-json` must be explicit.

## 6. Non-Goals

Phase 2.62 does not:

1. generate real issue records.
2. create Linear / GitHub / external issues.
3. write DB, facts, document versions, audit logs, OpenSearch, Qdrant, MinIO, or source files.
4. execute cleanup, delete, repair, backfill, reindex, migration, or rollout.
5. enter Data Steward / DB / NAS / BIM / TB file pool work.

## 7. Validation

Required validation:

```bash
uv run python -m py_compile scripts/phase262_mvp_issue_triage_summary.py
uv run pytest tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase262_check.json
```

No API / CLI smoke is required.

## 8. Next Step

Codex B should review the implementation and determine whether to prepare a selective baseline prompt.

Future candidate after baseline: operator daily summary workflow, still local-first and read-only by default.
