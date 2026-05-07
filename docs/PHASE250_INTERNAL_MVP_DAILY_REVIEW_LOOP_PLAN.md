# Phase 2.50 Internal MVP Daily Review Loop Runbook Artifact

## Positioning

Phase 2.50 defines the internal controlled MVP daily review loop. It is not a production rollout, customer delivery approval, automatic bidding workflow, Data Steward implementation, or repair executor.

The goal is to make the operator flow repeatable:

1. Run bounded internal MVP queries.
2. Fill an ignored run record from the approved template.
3. Generate a sanitized review payload / review dry-run.
4. Route pause / no-go findings into issue intake.
5. Keep human responsibility explicit for business decisions.

This document is a runbook artifact only. It does not execute a real Pilot, read real run records, write DB state, or approve rollout.

## Daily Inputs

The daily input is a manually filled run record based on:

- `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`

Real run records must remain local and ignored by Git:

- `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`

The operator must not paste raw customer-sensitive content into tracked docs. If a record needs to be shared, prepare a sanitized example or summary first.

## Daily Command Template

Use an explicit input path only. Do not scan `reports/` by default.

```bash
uv run python scripts/phase249_internal_mvp_run_record_review.py \
  --input-run-record reports/internal_mvp_runs/<YYYYMMDD>_<session>.json \
  --review-report \
  --output-dir reports/internal_mvp_runs/<YYYYMMDD>_review
```

The `<YYYYMMDD>_<session>` placeholder must be replaced by the local ignored run record prepared by the operator.

## Output Interpretation

- `decision_hint=go` means the internal controlled MVP can continue under the same evidence and human-review boundaries. It is not production release approval.
- `decision_hint=pause` means the operator should stop the current loop and request human review or Codex B issue intake.
- `decision_hint=no_go` means the current Pilot operation must stop and P0/P1 handling should begin.

Any `go` result remains scoped to internal controlled MVP continuation. It must not be converted into customer delivery, automatic procurement, automatic bidding, automatic review, repair authorization, or rollout approval.

## Issue Intake Trigger

Use Phase 2.37 issue intake conventions when the review report surfaces defects.

| Signal | Intake priority | Issue direction |
|---|---:|---|
| `facts_as_answer=true` | P0 | evidence_policy_violation |
| `transcript_as_fact=true` | P0 | evidence_policy_violation |
| `snapshot_as_answer=true` | P0 | evidence_policy_violation |
| Third document contamination | P0 | cross_document_contamination |
| Hidden Missing Evidence | P1 | missing_evidence_hidden |
| Alias/session blocker | P1 | alias_session |
| Retrieval suppressed without clear user intent | P1 | retrieval_suppressed_unexpected |
| Latency or trace display tail | P2/P3 | latency / trace_ux |

P0 must pause the Pilot. P1 enters triage by default. P2/P3 are tracked as tail items and do not block by default unless they hide evidence risk or operator safety problems.

## Human Responsibility Boundary

Hermes output is evidence-assisted support only.

The following actions always require a human owner:

- Tender, bid, contract, procurement, customer communication, and business-operation decisions.
- Data Steward ownership decisions and enterprise data governance actions.
- Any repair, delete, cleanup, backfill, reindex, or migration.
- Any production rollout, deployment promotion, or customer-facing enablement.

If a query needs a business owner but no owner confirms the action, the correct outcome is pause / manual review, not automatic continuation.

## Storage And Privacy

Default storage rules:

- Real run records remain in ignored `reports/internal_mvp_runs/`.
- Real review JSON / Markdown remains ignored.
- Real reports, latest pointers, and local manifests are not committed.
- Only sanitized examples, templates, README files, and planning docs may be committed.

Before any baseline, verify no real `reports/**/*.json`, `reports/**/*.md`, `latest.json`, or local run artifact is staged.

## Stop Conditions

Stop the daily loop if any of these occur:

1. Hermes_memory API or Hermes CLI is unavailable.
2. Alias/session state blocks the intended file scope.
3. Facts, transcript metadata, or metadata snapshot replaces retrieval evidence.
4. A third document contaminates a scoped or compare answer.
5. Missing Evidence is hidden, softened, or converted into a fabricated answer.
6. The workflow starts drifting toward repair, delete, cleanup, backfill, reindex, migration, or rollout.
7. A decision requires a tender / contract / procurement / business owner and no owner confirms.
8. The operator cannot identify the source run record, session, or evidence IDs.

## Nightly Sprint Boundary

Allowed at night:

- Docs / read-only planning.
- Ignored local state updates.
- Read-only diagnostics.
- Targeted unit tests.
- Temporary-directory smoke with fake data.

Prohibited at night:

- Real Pilot execution.
- Reading real business run records.
- Writing business DB, audit logs, facts, document versions, OpenSearch, or Qdrant.
- Repair, delete, cleanup, backfill, reindex, migration, rollout, cron, or scheduler creation.
- Automatic baseline unless `NEXT_CODEX_A_PROMPT.md` explicitly authorizes it and the task is not Red Lane.

Nightly Sprint output must still update `ACTIVE_PHASE.md`, `HANDOFF_LOG.md`, `reports/agent_runs/latest.json`, and `reports/nightly_runs/<timestamp>.json`.

## Future Candidates

1. Phase 2.50a: fake run record runbook smoke using temporary data only.
2. Phase 2.50b: internal MVP evidence pack that summarizes run records, issue intake, review dry-runs, and stop conditions.
3. Phase 2.51: Mac Mini internal MVP operator checklist / hot update runbook.

None of these candidates imply production rollout, Data Steward implementation, repair execution, or automatic business decisions.
