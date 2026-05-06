# Phase 2.43 Internal MVP Pilot Launch Candidate Plan

## 1. Planning Conclusion

Phase 2.43 plans the internal MVP Pilot launch candidate.

Current conclusion: Hermes Memory can prepare an internal controlled MVP Pilot launch candidate, but this is not production rollout, customer delivery approval, automatic tender review, automatic bidding, automatic business decision-making, repair authorization, or Data Steward implementation.

The launch candidate can proceed only through supervised human review, explicit evidence capture, and Go / Pause / No-Go gates.

## 2. Pilot Goals

The internal MVP Pilot should validate three business-facing workflows:

1. Tender review assistance: extract tender requirements, risks, Missing Evidence, and citations for human review.
2. File content extraction and source location: retrieve document evidence with `document_id`, `version_id`, chunk / sheet / cell / slide / meeting citation.
3. Company direction analysis support: separate Evidence, Interpretation, Recommendation, Risk, and Missing Evidence while keeping all recommendations as human-decision inputs.

The Pilot should also validate whether current runbooks, user guides, feedback templates, and dry-run review artifacts are usable by a supervised internal team.

## 3. Pilot Non-goals

The internal MVP Pilot does not authorize:

1. Production rollout.
2. Automatic tender review replacing human judgment.
3. Automatic bidding or proposal submission.
4. Automatic business or management decisions.
5. Repair executor, cleanup, delete, backfill, or reindex.
6. DB / facts / document_versions / OpenSearch / Qdrant mutation.
7. Data Steward / BIM asset catalog implementation.
8. Facts automatic extraction.
9. Complete RBAC / ABAC, production audit reporting, or admin UI.
10. Retrieval contract or memory kernel main architecture changes.

## 4. Launch Preconditions

Before a supervised Pilot session starts, the team must confirm:

1. Hermes_memory API `/health` is available.
2. Hermes CLI can start a session.
3. Target files are already ingested; no new upload is required for the launch candidate run.
4. Alias binding flow is known and can be checked in-session.
5. Reviewer, recorder, user, and technical support roles are assigned.
6. Participants have read:
   - `docs/MVP_PILOT_RUNBOOK.md`
   - `docs/MVP_PILOT_USER_GUIDE.md`
   - `docs/MVP_PILOT_KNOWN_RISKS.md`
7. The team accepts that all Missing Evidence and all business recommendations require human review.
8. No repair, rollout, migration, reindex, cleanup, or Data Steward implementation command is part of the session.

## 5. Required Artifacts

The launch candidate depends on these artifacts:

1. `docs/MVP_PILOT_RUNBOOK.md`
2. `docs/MVP_PILOT_USER_GUIDE.md`
3. `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
4. `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md`
5. `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`
6. `docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md`
7. `docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`
8. `docs/PRD_ACCEPTANCE_MATRIX.md`

Supporting artifacts:

1. `scripts/phase242a_mvp_pilot_review_dry_run.py`
2. `reports/mvp_pilot_reviews/README.md`
3. `reports/pilot_issues/README.md`

Real report JSON / Markdown remains ignored and local unless a later phase explicitly changes storage policy.

## 6. Go / Pause / No-Go Gate

### Go

`go` only means the team may continue an internal controlled MVP Pilot.

Go requires:

1. P0 count is `0`.
2. `facts_as_answer=false`.
3. `transcript_as_fact=false`.
4. `snapshot_as_answer=false`.
5. Missing Evidence is visible and manually reviewable.
6. Citation / `document_id` / `version_id` are manually checkable for core answers.
7. Users understand outputs are auxiliary and not final business decisions.

### Pause

`pause` means stop expansion and continue bounded issue triage or manual review.

Pause triggers:

1. Missing Evidence blocks core Pilot tasks.
2. Alias / session instability blocks normal use.
3. Citation or trace is too weak for human checking.
4. P1 issues repeat across core queries.
5. Users are unclear about auxiliary-output boundaries.

### No-Go

`no_go` means the launch candidate must stop.

No-Go triggers:

1. Any P0 item.
2. Facts, transcript, or snapshot replaces retrieval evidence.
3. Missing Evidence is hidden or rewritten as certainty.
4. Permission leakage or real third-document contamination appears.
5. Output implies automatic tender review, automatic bidding, production rollout, repair authorization, or automatic business decision-making.
6. Repair / cleanup / delete / reindex / data mutation is triggered.

## 7. Pilot Day Flow

The supervised Pilot Day should follow this sequence:

1. Environment check: API health, CLI startup, file pool readiness.
2. Role confirmation: user, reviewer, recorder, technical support.
3. Alias binding: bind required working files and save alias status.
4. Day-1 query execution: use `docs/MVP_PILOT_DAY1_RUN_SHEET.md`.
5. Raw output capture: save prompt, response, document/version/citation, safety flags, and pass / partial / fail.
6. Issue intake: use `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md` or the existing Pilot issue intake tooling.
7. Evidence review: use `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`.
8. Dry-run report: prepare sanitized input and run the Phase 2.42a generator.
9. Codex B review: review Go / Pause / No-Go and next bounded phase.
10. Codex C follow-up: only if real terminal behavior must be revalidated.

## 8. Required Recording Fields

For each query, the recorder should capture:

1. query text.
2. raw answer.
3. `document_id`.
4. `version_id`.
5. citation fields.
6. `facts_as_answer`.
7. `transcript_as_fact`.
8. `snapshot_as_answer`, if available.
9. `contamination_flags`.
10. Missing Evidence.
11. pass / partial / fail.
12. P0 / P1 / P2 / P3 priority.
13. manual review note.

For analysis or recommendation prompts, the recorder must also check that recommendations are clearly marked as human-decision inputs.

## 9. Deferred Items

Deferred beyond Phase 2.43:

1. Production rollout.
2. Repair executor.
3. Data Steward / BIM asset catalog implementation.
4. Facts automatic extraction.
5. Complete RBAC / ABAC.
6. Automatic tender review.
7. Automatic bidding.
8. Automatic business decision-making.
9. Production scheduler / cron.
10. Full admin UI.

## 10. Next Phase Candidates

Codex B may choose one bounded follow-up after reviewing this plan:

1. Phase 2.43a launch packet / operator checklist artifact.
2. Phase 2.43b Codex C pre-flight terminal smoke prompt.
3. Phase 2.43c first supervised internal Pilot run review.

None of these candidates should be started automatically from this planning phase.

## 11. Phase 2.43 Validation

This planning artifact should be validated with:

1. `git diff --check`.
2. Keyword review for production rollout, repair, Data Steward, Missing Evidence, `facts_as_answer`, `transcript_as_fact`, No-Go, Go, and Pause.
3. `git status --short`.

No API / CLI smoke, pytest, DB-backed test, report generation, or data mutation is required for Phase 2.43 planning.
