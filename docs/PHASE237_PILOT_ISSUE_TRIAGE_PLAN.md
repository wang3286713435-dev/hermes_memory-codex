# Phase 2.37 Pilot Issue Intake / Triage Plan

## 1. Goal

Phase 2.37 defines a lightweight issue intake and triage loop for MVP Pilot feedback.

The goal is to turn Day-1 Pilot findings, Codex C terminal validation, and user trial feedback into structured issue records before starting more fixes.

This phase is planning-only. It does not write feature code, mutate business data, update facts, update document versions, modify OpenSearch / Qdrant, run repair / backfill / reindex, enter rollout, or create automatic tender-review conclusions.

## 2. Current Context

Phase 2.36c is baselined:

1. Commit: `d491a44`.
2. Tag: `phase-2.36c-tender-deep-field-diagnostics-baseline`.
3. Phase 2.36c confirmed that diagnostics and Missing Evidence are semantically consistent.
4. Deep-field recall is still partial: highest bid limit amount, concrete qualification level / category, performance requirements, and personnel quantity still need evidence or manual review.

The next step should not blindly tune retrieval for one tender file. The safer next step is to capture pilot findings as structured issues and route them by priority.

## 3. Candidate Direction Review

| Option | Value | Risk | Recommendation |
| --- | --- | --- | --- |
| A. Pilot Issue Intake / triage | Creates a repeatable loop for Day-1, Codex C, and user feedback; supports P0/P1/P2/P3 routing. | Requires discipline to avoid turning intake into automatic repair. | Recommend as Phase 2.37a. |
| B. Tender deep-field recall continued fix | Directly attacks highest bid limit, qualification, performance, and personnel gaps. | High overfitting risk; source documents may lack fields; without intake, fixes are hard to prioritize. | Defer behind intake. |
| C. Pilot Run Report / daily summary | Good management artifact and daily review view. | Without issue schema, summaries are hard to convert into actionable fixes. | Build after intake schema. |
| D. Hermes CLI / API stability runbook | Useful for repeatable pilot operation and environment diagnosis. | Does not directly capture P1/P2 product issues. | Route as P2 / ops issue type. |
| E. Automatic tender-review enhancement | Could increase perceived capability. | Current evidence is insufficient; high risk of overclaiming or automation boundary violations. | Not recommended. |

## 4. Recommended Phase 2.37a

Recommended Phase 2.37a: issue intake record dry-run + triage schema.

Minimum scope:

1. Define an issue record schema.
2. Provide a local JSON / Markdown intake template.
3. Provide a no-mutation dry-run validator or script if implementation is approved later.
4. Classify issues as P0/P1/P2/P3.
5. Generate a triage summary for human review.
6. Do not auto-create repair tasks, DB records, Linear issues, or GitHub issues.

## 5. Issue Record Schema

Minimum fields:

1. `issue_id`.
2. `source`.
3. `source_phase`.
4. `reported_at`.
5. `reporter`.
6. `query`.
7. `aliases`.
8. `expected_behavior`.
9. `actual_behavior`.
10. `document_ids`.
11. `version_ids`.
12. `citations`.
13. `trace_flags`.
14. `issue_type`.
15. `priority`.
16. `safety_boundary`.
17. `human_review_required`.
18. `suggested_next_action`.
19. `status`.
20. `notes`.

Recommended `status` values:

1. `new`.
2. `triaged`.
3. `needs_codex_b_review`.
4. `needs_codex_c_validation`.
5. `accepted_backlog`.
6. `deferred`.
7. `closed_expected_missing_evidence`.

## 6. Issue Types

Minimum `issue_type` values:

1. `retrieval_recall`.
2. `trace_ux`.
3. `latency`.
4. `alias_session`.
5. `contamination_false_positive`.
6. `missing_evidence_expected`.
7. `answer_boundary`.
8. `environment`.
9. `documentation`.

## 7. Priority Rules

P0:

1. Fabricated answer presented as evidence-backed.
2. Facts or transcript replacing retrieval evidence.
3. Cross-document contamination in final evidence.
4. Permission / tenant leakage.
5. Automatic business, tender, legal, or repair decision beyond boundary.

P1:

1. Key field recall failure that blocks pilot use.
2. Trace contradicts answer boundary.
3. Alias / session failure that blocks retrieval.
4. Citation missing for a core answer.

P2:

1. Latency or long output that slows pilot use but does not corrupt evidence.
2. Display is confusing but trace / evidence remain safe.
3. Non-critical field remains partial.

P3:

1. Copy, prompt, or documentation polish.
2. Low-risk formatting issue.
3. Nice-to-have runbook enhancement.

## 8. Go / Pause Rules

Continue pilot when:

1. P0 count is `0`.
2. P1 items are documented and can be handled by Missing Evidence / manual review.
3. Users understand output is evidence-assisted, not automatic tender review.

Pause or narrow pilot when:

1. Any P0 appears.
2. Repeated P1 blocks the same core workflow without a manual workaround.
3. Alias/session or contamination issues recur after baseline fixes.
4. Users request automatic decisions, repair, rollout, or unsupported facts extraction.

## 9. Non-goals

Phase 2.37 / 2.37a must not:

1. Implement a repair executor.
2. Automatically fix issues.
3. Write business DB, facts, or document_versions.
4. Modify OpenSearch / Qdrant data.
5. Run repair / backfill / reindex.
6. Enter rollout.
7. Create automatic tender-review conclusions.
8. Modify retrieval contract.
9. Modify memory kernel main architecture.
10. Auto-create Linear / GitHub issues unless separately planned and approved.

## 10. Validation Plan

Planning validation:

1. Verify this document keeps issue intake separate from automatic fixes.
2. Verify P0/P1/P2/P3 rules preserve evidence and safety boundaries.
3. Verify Phase 2.36c partial recall items become intake candidates rather than hidden risks.

Future Phase 2.37a validation:

1. Schema validation with sample issue records.
2. Triage summary generation from sample records.
3. No DB write and no repair execution.
4. No real API / CLI smoke required unless the implementation changes terminal behavior.

## 11. Recommendation

Proceed to Phase 2.37a only after Codex B review.

Recommended Phase 2.37a boundary:

1. Local issue intake schema and templates.
2. Optional dry-run validator / summary generator.
3. Sample records for current known issues:
   - highest bid limit amount Missing Evidence.
   - concrete qualification level / category Missing Evidence.
   - performance requirements Missing Evidence.
   - personnel quantity Missing Evidence.
   - long-output latency.
4. No automatic repair and no rollout.
