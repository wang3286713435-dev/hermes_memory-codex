# Phase 2.44d Explicit Local Issue Dry-run Route Plan

## 1. Goal

Phase 2.44d plans whether a later bounded phase may use explicit, manually prepared, ignored local issue input to dry-run the real Pilot recorder workflow.

This phase is planning-only. It does not create real issue records, scan real reports, fix retrieval, approve rollout, or execute repair.

The goal is to define the conditions, sanitization rules, validation commands, review gates, and stop conditions for any future explicit local dry-run.

## 2. Non-goals

Phase 2.44d does not:

1. generate real `reports/pilot_issues/*.json`.
2. generate a real Pilot report.
3. scan real `reports/` or `reviews/` by default.
4. run API / CLI smoke.
5. write DB / facts / document_versions.
6. modify OpenSearch or Qdrant.
7. repair, backfill, reindex, cleanup, or delete.
8. create Linear / GitHub issues automatically.
9. implement Data Steward / BIM functionality.
10. change retrieval contract or memory kernel main architecture.
11. fix Day-1 P1 / P2 findings.

## 3. Preconditions for Explicit Local Input

A future phase may use real recorder input only when all conditions are met:

1. The user explicitly authorizes use of local ignored issue input for a named phase.
2. Input is manually prepared by a recorder or reviewer; it is not auto-generated from a broad report scan.
3. The input path is explicit, usually under `reports/pilot_issues/`.
4. The file is confirmed ignored by Git before validation.
5. Raw output bundles, raw answers, screenshots, and business-sensitive notes remain local-only.
6. Codex A does not infer missing business judgment or change issue priority to make validation pass.
7. Each issue keeps `human_review_required=true` when business-impacting.
8. P0 / P1 / P2 / P3 priority remains reviewer-visible.

If any condition is not met, stop and return to planning.

## 4. Sanitization and Local-only Fields

Real local ignored issue records may contain fields that committed examples must not contain.

| field / content | ignored local input | committed docs / examples |
|---|---|---|
| real `document_id` | allowed if needed for review | placeholder only |
| real `version_id` | allowed if needed for review | placeholder only |
| real citation / chunk / cell / slide | allowed if needed for review | placeholder only |
| raw answer text | allowed only after human approval | omit or summarize |
| session_id | allowed if needed for debugging | omit |
| customer / project private details | only if required and local ignored | omit or sanitize |
| tender/legal/business judgment | local-only, reviewer owned | summarize without sensitive detail |
| reviewer notes | local-only unless sanitized | role-level summary only |
| credentials / secrets | never allowed | never allowed |

Committed artifacts may include runbooks, fake inputs, and sanitized templates. They must not contain real raw answers, real business-sensitive judgments, or production credentials.

## 5. Recorder Workflow

Recommended future explicit local workflow:

1. Recorder gathers the specific Day-1 finding approved for local intake.
2. Recorder fills the worksheet from `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_WORKSHEET.md`.
3. Recorder maps labels to validator-compatible `issue_type`.
4. Recorder saves one or more issue records to an ignored local file, for example:

```text
reports/pilot_issues/day1-local-recorder-input.json
```

5. Recorder verifies the path is ignored:

```bash
git check-ignore -v reports/pilot_issues/day1-local-recorder-input.json
```

6. Recorder runs strict validation.
7. Codex B / user reviews the summary.
8. Only after review may a separate bounded phase plan a P1 / P2 fix or trace polish.

Recorder must not:

1. mark any issue as repair-approved.
2. create external Linear / GitHub issues automatically.
3. treat `continue_with_manual_review` as rollout approval.
4. hide Missing Evidence.
5. downgrade priority to avoid review.
6. convert issue intake into retrieval code changes.

## 6. Validation Commands

Validate one explicitly authorized ignored local input:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input reports/pilot_issues/day1-local-recorder-input.json --strict
```

Validate all explicitly authorized local issue records:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

Print a validator-compatible template:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --print-template
```

Interpretation:

1. `invalid_count > 0` means the local input must be fixed before review.
2. `go_pause_recommendation=pause` means at least one P0 is present.
3. `go_pause_recommendation=continue_with_manual_review` means P1 exists and human review is required.
4. `go_pause_recommendation=continue` is not production rollout approval.

## 7. Review / Decision Gate

Codex B / user review should decide:

1. Whether each issue is valid and sufficiently sanitized.
2. Whether the priority is credible.
3. Whether the issue belongs to retrieval recall, trace UX, answer boundary, alias/session, latency, environment, or documentation.
4. Whether a P1 / P2 fix planning phase is warranted.
5. Whether Codex C terminal validation is needed later.

Review outcomes:

| outcome | meaning |
|---|---|
| continue_with_manual_review | human review continues; not rollout approval |
| bounded_fix_planning_candidate | a future phase may plan a narrow fix |
| backlog | keep for later triage |
| pause | P0 or blocking P1 requires stopping Pilot flow |
| no_go | unacceptable safety / evidence boundary issue |

No outcome in this plan authorizes repair, production rollout, DB writes, index mutation, Data Steward implementation, or external issue creation.

## 8. Git and Storage Policy

1. Real issue records stay ignored under local paths such as `reports/pilot_issues/*.json`.
2. Raw output bundles remain ignored.
3. Real Pilot reports remain ignored.
4. Only sanitized templates, fake inputs, runbooks, and reviewed examples may be committed.
5. `reports/agent_runs/latest.json` remains ignored local agent state.
6. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` is unrelated legacy dirty and must not be staged with Phase 2.44d.

Before any future real local dry-run, run:

```bash
git check-ignore -v reports/pilot_issues/<file>.json
```

If the file is not ignored, stop.

## 9. Risks and Stop Conditions

Risks:

1. Recorder may accidentally include raw business output in a committed artifact.
2. P1 findings may be mistaken for fix authorization.
3. `continue_with_manual_review` may be misread as rollout approval.
4. Real local input may contain sensitive business judgments that should not enter Git.
5. Issue taxonomy may not match all Day-1 labels.

Stop immediately if:

1. a task requires real issue generation in a tracked file.
2. a task requires default scanning of real `reports/` or `reviews/`.
3. a task requires DB / facts / document_versions / OpenSearch / Qdrant writes.
4. a task tries to repair, backfill, reindex, cleanup, or delete.
5. a task attempts production rollout or Data Steward implementation.
6. a task asks facts, transcript, snapshot, or recommendations to replace retrieval evidence.
7. a task asks Codex A to make tender, legal, business, or operating decisions without human owner review.

## 10. Next Recommendation

Proceed to Codex B review of this plan.

If approved, the next bounded phase can be one of:

1. Phase 2.44d docs-only Git baseline.
2. Phase 2.44e explicit ignored local issue dry-run using a user-specified local input file.
3. Phase 2.44e recorder workflow runbook refinement.

Do not enter retrieval fixes, real tracked issue generation, repair, rollout, Data Steward work, or external issue creation from this planning phase.
