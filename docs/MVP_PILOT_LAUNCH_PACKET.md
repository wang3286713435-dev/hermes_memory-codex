# MVP Pilot Launch Packet

## 1. Cover Conclusion

This packet is the operator checklist for an internal controlled MVP Pilot.

It is not:

1. production rollout approval.
2. automatic tender review authorization.
3. automatic bidding or proposal submission authorization.
4. automatic business decision authorization.
5. repair, cleanup, delete, backfill, reindex, or data mutation authorization.
6. Data Steward / BIM product implementation approval.

Hermes output in this Pilot is auxiliary. Tender conclusions, business recommendations, and risk judgments must remain human decisions.

## 2. Roles

| role | responsibility |
|---|---|
| Pilot User | Runs the session prompts and flags confusing output. |
| Evidence Reviewer | Checks citation, source location, `document_id`, `version_id`, Missing Evidence, and evidence policy flags. |
| Recorder | Saves raw answers, metadata, pass / partial / fail results, and P0 / P1 / P2 / P3 issue labels. |
| Technical Support | Watches API / CLI availability, alias/session behavior, trace flags, contamination flags, and runtime blockers. |
| Codex B follow-up owner | Reviews the sanitized packet, dry-run report, issue list, and next bounded phase recommendation. |
| Codex C follow-up owner | Revalidates only when real terminal behavior needs confirmation. |

One person may hold multiple roles, but Evidence Reviewer and Recorder must be explicit before the session starts.

## 3. Pre-start 15-minute Checklist

Complete this before any business prompt is run.

| item | required check | result |
|---|---|---|
| API health | Hermes_memory `/health` is available. | pass / fail |
| CLI health | Hermes CLI can start a session. | pass / fail |
| file pool | Target files already exist in the known Pilot pool; no new upload is needed. | pass / fail |
| alias commands | Alias binding commands and target documents are visible to Pilot User and Technical Support. | pass / fail |
| recording template | `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md` is ready. | pass / fail |
| evidence checklist | `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md` is ready. | pass / fail |
| dry-run input template | `docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json` is available for sanitized manual input. | pass / fail |
| run sheet | `docs/MVP_PILOT_DAY1_RUN_SHEET.md` is the query source. | pass / fail |
| known risks | All participants have read `docs/MVP_PILOT_KNOWN_RISKS.md`. | pass / fail |
| boundaries | Everyone understands this is not production rollout, repair, or automatic decision-making. | pass / fail |

If any required check fails, stop and record `Pause`.

## 4. Session Execution Checklist

1. Create a fresh Hermes session and record `session_id`.
2. Bind the required aliases in the same session.
3. For each alias, record:
   - `alias_resolution.status`
   - `resolved_document_id`
   - `resolved_version_id` or `version_id`
   - `alias_missing`
   - `retrieval_suppressed`
4. Run the Day-1 query set from `docs/MVP_PILOT_DAY1_RUN_SHEET.md`.
5. Save each raw answer without rewriting it.
6. Save `citation`, `document_id`, `version_id`, source location, and trace flags.
7. Mark each query as `pass`, `partial`, or `fail`.
8. Assign P0 / P1 / P2 / P3 priority.
9. Keep all Missing Evidence visible.
10. Stop immediately if a P0 or stop condition appears.

## 5. Evidence Review Checklist

For every reviewed answer, Evidence Reviewer must check:

| evidence policy | required value |
|---|---|
| `facts_as_answer` | `false` |
| `transcript_as_fact` | `false` |
| `snapshot_as_answer` | `false` |
| Missing Evidence hidden | `false` |
| Missing Evidence rewritten as certainty | `false` |
| final answer replaces human decision | `false` |

Citation / source review must confirm:

1. `document_id` is present for document-backed answers.
2. `version_id` is present where version governance matters.
3. citation or source location can be manually checked.
4. Excel answers include `sheet_name` and `cell_range` where available.
5. PPTX answers include `slide_number` and `slide_title` where available.
6. meeting answers preserve meeting source location and keep `transcript_as_fact=false`.
7. compare answers do not contain real third-document contamination.

## 6. Go / Pause / No-Go Quick Decision

### Go

`Go` only means the team may continue the internal controlled MVP Pilot.

All conditions must hold:

1. P0 count is `0`.
2. P1 issues are manually manageable or already captured for bounded follow-up.
3. Missing Evidence is visible and recordable.
4. citation / source location can be manually checked.
5. `facts_as_answer=false`, `transcript_as_fact=false`, and `snapshot_as_answer=false`.
6. Users understand outputs are auxiliary and require human decision.

### Pause

Choose `Pause` when:

1. P1 blocks a core workflow.
2. citation cannot be manually checked.
3. alias/session behavior is unstable.
4. Missing Evidence frequency blocks the Pilot task.
5. users appear to treat Hermes output as final business decision.

### No-Go

Choose `No-Go` immediately when:

1. any P0 appears.
2. Hermes fabricates amount, qualification, performance, personnel count, or business conclusion.
3. facts, transcript, or snapshot replaces retrieval evidence.
4. permission leakage appears.
5. real third-document contamination enters the final answer.
6. output implies automatic tender review, automatic bidding, production rollout, repair, or automatic business decision-making.
7. repair / cleanup / delete / backfill / reindex / data mutation is triggered or requested as part of the Pilot.

## 7. Output Archival

1. Do not commit real Pilot reports.
2. Store real report JSON / Markdown only in ignored local report paths.
3. Use sanitized input before running the dry-run report generator.
4. Do not paste confidential excerpts, real customer content, sensitive prices, personal data, real session ids, real fact ids, or private business judgments into committed templates.
5. Use `docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md` before creating any dry-run report.

## 8. Human Decision Declaration

The Recorder must preserve this declaration in the final Pilot notes:

1. Tender answers are review assistance only and cannot be auto-submitted.
2. Company direction recommendations are auxiliary inputs and require human decision.
3. Missing Evidence means the system did not provide enough current evidence.
4. `Go` is not production rollout.
5. `approved_for_manual_action` in any review workflow is not executed repair.

## 9. Stop Conditions

Stop the session when any condition appears:

1. P0.
2. user requests automatic tender review, automatic bidding, or automatic business decision.
3. the next step would require repair, rollout, DB write, OpenSearch write, Qdrant write, facts write, document_versions write, backfill, reindex, cleanup, or delete.
4. the session needs new file upload or real data mutation.
5. citation cannot be checked for a core answer.
6. alias/session instability prevents normal use.

## 10. Follow-up Flow

1. Recorder organizes raw answers and feedback rows.
2. Evidence Reviewer completes `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`.
3. Recorder prepares sanitized dry-run report input if needed.
4. Codex B reviews the issue list, checklist, and dry-run report.
5. Codex B decides the next bounded phase or asks Codex C for terminal revalidation.
6. Codex C only revalidates real terminal behavior; Codex C does not start repair, rollout, DB writes, or Data Steward implementation.

## 11. Operator Sign-off

| field | value |
|---|---|
| pilot_round |  |
| session_id |  |
| Pilot User |  |
| Evidence Reviewer |  |
| Recorder |  |
| Technical Support |  |
| Codex B follow-up owner |  |
| Codex C follow-up needed | yes / no |
| decision | Go / Pause / No-Go |
| decision_reason |  |
