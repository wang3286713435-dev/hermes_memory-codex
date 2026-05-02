# Phase 2.37c Pilot Issue Triage Summary Plan

## 1. Goal

Phase 2.37c plans the daily or per-round human triage summary for MVP Pilot issue records.

The goal is to turn local issue records under `reports/pilot_issues/*.json` into a human-reviewable summary that helps decide which P1 / P2 findings should enter later bounded fix planning.

This phase is planning-only. It does not create real issue records, fix issues, write business data, create external issues, run repair, or enter rollout.

## 2. Current Inputs

Planned input:

```text
reports/pilot_issues/*.json
```

These input records follow the Phase 2.37a schema and are validated with:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

This planning phase does not create real `reports/pilot_issues/*.json` files.

## 3. Planned Outputs

Future Phase 2.37d may generate local triage summary artifacts such as:

1. `reports/pilot_triage/YYYYMMDD_summary.json`
2. `reports/pilot_triage/YYYYMMDD_summary.md`

Real summary artifacts should be ignored by Git by default because they may contain sensitive trial findings.

The summary should include:

1. Total issue count.
2. Counts by priority.
3. Counts by issue type.
4. P0 / P1 list for human review.
5. Repeated workflow blockers.
6. Missing Evidence items.
7. Suggested bounded next action.
8. Explicit Go / Pause recommendation.

## 4. Triage Rules

P0:

1. Immediately pause or narrow the pilot.
2. Require Codex B and user review.
3. Do not enter automatic repair.
4. Do not continue rollout.

P1:

1. Candidate for bounded fix planning.
2. Must include evidence, citation, document_id / version_id, and reproduction query.
3. Must preserve Missing Evidence when the source does not support a claim.
4. Requires human review before implementation.

P2:

1. Candidate for backlog, runbook, UX, latency, or quality polish.
2. Does not block pilot if evidence boundary remains safe.
3. Can be batched into later planning.

P3:

1. Documentation, copy, prompt, or low-risk formatting polish.
2. Does not block pilot.

## 5. Known First-Batch Candidates

Known candidates from Day-1 / Codex C validation:

1. P1 retrieval recall: `@主标书` highest bid limit / tender control price / bid ceiling amount remains Missing Evidence.
2. P1 retrieval recall: `@主标书` concrete tender qualification level / category remains Missing Evidence.
3. P1 / partial: project manager, consortium, performance, and personnel requirements have nearby evidence but need manual review.
4. P2 latency: long-form meeting decision / risk / company direction analysis can be slow.

These are issue candidates only. They are not automatic repair tasks.

## 6. Go / Pause Rules

The Go / Pause meaning must stay aligned with Phase 2.37a:

1. Any P0: `pause`.
2. No P0 but at least one P1: `continue_with_manual_review`.
3. Only P2 / P3: `continue`.

`continue_with_manual_review` does not mean production rollout approval.

## 7. PRD Alignment

Every issue and triage summary must retain the PRD evidence boundary:

1. Preserve citation and document/version references when available.
2. Preserve `Missing Evidence` when the source does not support a field.
3. Preserve human review for business interpretation.
4. Do not turn issue intake into automatic tender-review conclusions.
5. Do not let facts, transcript, or summaries replace retrieval evidence.

## 8. BIM Relationship

BIM Data Steward is now a later PRD planning direction.

Phase 2.37c does not handle BIM asset catalog, BIM model parsing, BIM file governance, online viewing, clash detection, or quantity takeoff.

If BIM-related findings appear during MVP Pilot, route them as planning feedback only and do not mix them into current MVP Pilot fixes.

## 9. Non-goals

Phase 2.37c does not:

1. Fix issues.
2. Create real issue records.
3. Create Linear or GitHub issues.
4. Write DB, facts, document_versions, OpenSearch, or Qdrant.
5. Run repair, backfill, reindex, cleanup, or delete.
6. Run real API / CLI smoke.
7. Enter rollout.
8. Produce automatic tender-review conclusions.
9. Modify retrieval contract.
10. Modify memory kernel main architecture.

## 10. Recommended Next Step

After Phase 2.37c baseline, choose one:

1. Phase 2.37d minimal implementation: local triage summary generator that reads existing local issue records and writes ignored summary output.
2. Manual first-batch issue recording: create sanitized local issue records for known P1/P2 candidates, then run the Phase 2.37a validator.

Recommended default: implement Phase 2.37d local triage summary generator only after Codex B review.
