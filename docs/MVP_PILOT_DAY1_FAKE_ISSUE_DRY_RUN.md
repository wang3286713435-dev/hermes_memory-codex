# MVP Pilot Day-1 Fake Issue Dry-run

## 1. Purpose

This document proves the Phase 2.44b sanitized issue intake workflow can be exercised with committed fake data.

It is not a real Pilot issue record, Pilot report, repair request, rollout decision, or retrieval fix.

## 2. Input

Committed fake input:

```text
docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json
```

The input contains two placeholder records:

1. P1 `retrieval_recall` / Missing Evidence example.
2. P1 `trace_ux` / structured citation display example.

The records use fake aliases, fake document IDs, fake version IDs, fake citations, fake source locations, and sanitized behavior descriptions. They do not contain real raw answers, real customer data, real amounts, real tender judgments, real session IDs, or real business recommendations.

## 3. Commands

Validate JSON shape:

```bash
uv run python -m json.tool docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_input_check.json
```

Run strict validator:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json --strict >/tmp/day1_fake_issue_intake_validate.json
```

Generate dry-run summary:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_intake_summary.json
```

## 4. Expected Output

Expected validator result:

1. `total=2`.
2. `valid_records=2`.
3. `invalid_count=0`.
4. `by_priority.P1=2`.
5. `go_pause_recommendation=continue_with_manual_review`.

Interpretation:

1. The fake records are structurally valid for the existing Phase 2.37a local issue intake validator.
2. `continue_with_manual_review` means the fake records contain P1-style issues and require human review.
3. It is not production rollout approval.
4. It is not authorization to repair, reindex, backfill, delete, write DB, or create external issues.

## 5. Git and Storage Boundary

Committed artifacts may include:

1. this runbook.
2. the fake input JSON.

Real artifacts must remain ignored local files:

1. real `reports/pilot_issues/*.json`.
2. real Pilot reports.
3. raw Hermes output bundles.
4. real session IDs, document IDs, version IDs, citations, and raw answers.

## 6. Stop Conditions

Stop and ask for a new bounded phase if a task requires:

1. real issue record generation.
2. scanning real `reports/` or `reviews/`.
3. API / CLI smoke.
4. DB / facts / document_versions / OpenSearch / Qdrant writes.
5. repair, cleanup, delete, backfill, or reindex.
6. production rollout.
7. Data Steward implementation.

## 7. Phase 2.44c Result

Executed validation result:

1. `uv run python -m json.tool docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_input_check.json`: passed.
2. `uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json --strict >/tmp/day1_fake_issue_intake_validate.json`: passed.
3. `uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_intake_summary.json`: passed.

Summary:

1. `total=2`.
2. `valid_records=2`.
3. `invalid_count=0`.
4. `by_issue_type.retrieval_recall=1`.
5. `by_issue_type.trace_ux=1`.
6. `by_priority.P1=2`.
7. `go_pause_recommendation=continue_with_manual_review`.
8. `writes_db=false`.
9. `creates_external_issue=false`.
10. `repairs_issue=false`.
11. `destructive_actions=[]`.

Phase 2.44c only validates fake-data workflow readiness. It does not resolve Day-1 P1 / P2 findings.

Next step after Codex A completion is Codex B review. Git baseline should wait until that review passes.
