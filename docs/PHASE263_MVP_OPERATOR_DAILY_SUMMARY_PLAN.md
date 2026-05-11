# Phase 2.63 Internal MVP Operator Daily Summary Workflow

## Goal

Phase 2.63 turns local internal MVP issue records into an operator-facing daily summary.

The goal is to reduce manual copying and manual triage after Mac mini controlled MVP use. The summary answers whether the day is `ready`, `pause`, or `no_go`, while keeping the output sanitized and read-only.

## Scope

Implemented:

- `scripts/phase263_mvp_operator_daily_summary.py`
- `tests/test_phase263_mvp_operator_daily_summary.py`

The runner can:

1. Read a Phase 2.62 summary with `--issue-summary-json`.
2. Read issue records directly with repeated `--input-json`.
3. Read one-level issue JSON files with `--input-dir`.
4. Reuse `phase262_mvp_issue_triage_summary.build_summary()` for direct issue input.
5. Emit JSON to stdout.
6. Write JSON only when `--output-json` is explicitly provided.
7. Write sanitized Markdown only when `--output-md` is explicitly provided.

## Daily Summary Fields

The JSON output includes:

- `phase`
- `dry_run=true`
- `read_only=true`
- `production_rollout=false`
- `repair_attempted=false`
- `external_issue_created=false`
- `db_or_index_written=false`
- `decision`
- `severity_counts`
- `p0_count`
- `p1_count`
- `operator_summary`
- `codex_b_review_needed`
- `codex_c_validation_needed`
- `recommended_actions`
- `blocked_by`
- `issue_refs`

## Decision Rules

- `no_go`: any P0 or dangerous flag.
- `pause`: any P1, invalid JSON, or validation gap.
- `ready`: only P2/P3 issues or empty issue input.

## Markdown Redaction

Markdown output must not include:

- raw query text
- notes
- expected behavior
- actual behavior
- local full paths
- returned document ids
- evidence chunk ids

Only sanitized issue refs are included.

## Non-goals

Phase 2.63 does not:

- create real issue records
- create external issues
- upload files
- run API / CLI smoke
- write DB, facts, document versions, audit logs, OpenSearch, Qdrant, or MinIO
- execute cleanup, delete, repair, backfill, reindex, or migration
- enter DB / NAS / Data Steward branch intake
- approve rollout

## Verification

Completed:

```bash
uv run python -m py_compile scripts/phase263_mvp_operator_daily_summary.py
uv run pytest tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
```

Result: `28 passed`.

## Current Status

Implementation is complete and waiting for Codex B review. This phase is not baselined yet.
