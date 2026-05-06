# MVP Pilot Review Dry-run Runbook

## Purpose

This runbook explains how to prepare sanitized input for `scripts/phase242a_mvp_pilot_review_dry_run.py`.

The generated report is a local dry-run artifact for internal MVP Pilot review. It is not production rollout approval, not repair authorization, not automatic tender review, and not an automatic business decision.

## Inputs To Collect Manually

Use only sanitized, manually reviewed summaries from:

1. Codex C terminal validation reports.
2. Pilot issue records.
3. `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`.
4. `docs/PRD_ACCEPTANCE_MATRIX.md`.
5. Readiness audit or repair plan dry-run summaries, if explicitly selected.
6. Codex B review notes.

Do not paste confidential excerpts, real customer data, real session ids, real document ids, real fact ids, personal names, sensitive prices, or private business judgments into the template.

## Fill The Template

Start from:

```bash
docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json
```

Keep these safety values unless a separate review explicitly says otherwise:

```json
{
  "facts_as_answer": false,
  "transcript_as_fact": false,
  "snapshot_as_answer": false,
  "missing_evidence_hidden": false,
  "production_rollout_claimed": false
}
```

All Missing Evidence must remain visible and must be manually reviewed. Missing Evidence must not be rewritten as a certain answer.

## Run The Dry-run Generator

Print JSON to stdout:

```bash
uv run python scripts/phase242a_mvp_pilot_review_dry_run.py --input docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json --json
```

If testing file output, use a temporary directory or the ignored local report directory:

```bash
uv run python scripts/phase242a_mvp_pilot_review_dry_run.py --input docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json --output-dir reports/mvp_pilot_reviews --json
```

Real report JSON and Markdown under `reports/mvp_pilot_reviews/` are local artifacts and are ignored by Git.

## Interpret The Decision

### `no_go`

`no_go` means at least one P0 or unsafe policy was found. Common causes:

1. Fabricated amount, qualification, performance, personnel count, or business conclusion.
2. Facts, transcript, or snapshot used as answer evidence.
3. Permission leakage or real third-document contamination.
4. Hidden Missing Evidence.
5. Repair, cleanup, delete, reindex, destructive action, or rollout claim.

### `pause`

`pause` means P0 is absent, but the Pilot should not expand yet. Common causes:

1. Missing Evidence still needs manual review.
2. Blocking P1 exists.
3. Citation or trace is not stable enough for manual checking.
4. Readiness or repair dry-run warnings affect risk judgment.

### `go`

`go` only means the team may continue an internal controlled MVP Pilot. It does not mean production ready, customer delivery ready, automatic tender review ready, or repair authorized.

## Review Checklist

Before using a dry-run report in a phase decision, confirm:

1. P0 count is correct.
2. P1 items are recorded with next-phase or manual-review handling.
3. Citation fields are manually checkable.
4. Missing Evidence is not hidden.
5. Not-claimable capabilities remain not claimed.
6. Codex B has reviewed the dry-run report before any baseline or next-phase prompt.
7. Codex C validation is requested only when real terminal behavior must be verified.

## Non-goals

This runbook does not authorize:

1. Production rollout.
2. Repair executor.
3. Data cleanup, deletion, backfill, or reindex.
4. DB, facts, document_versions, OpenSearch, or Qdrant writes.
5. Automatic tender review.
6. Automatic bidding or business decision-making.
7. Data Steward implementation.
