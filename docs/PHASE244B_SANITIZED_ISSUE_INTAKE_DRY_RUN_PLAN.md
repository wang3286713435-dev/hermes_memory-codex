# Phase 2.44b Sanitized Issue Intake Dry-run / Recorder Workflow Plan

## 1. Goal

Phase 2.44b plans how Pilot recorder output should move from human-reviewed Day-1 findings into sanitized local issue intake dry-run inputs.

This phase is planning-only. It does not create real issue records, run the dry-run on real records, fix retrieval, or approve rollout.

The output of this plan is a bounded workflow for a future explicit phase.

## 2. Non-goals

Phase 2.44b does not:

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

## 3. Inputs and Sanitization

Future dry-run input should be manually prepared from:

1. Day-1 raw Hermes output.
2. reviewer judgment.
3. recorder worksheet rows.
4. visible trace fields.
5. available citations and document/version identifiers.

Sanitize or replace before committing any artifact:

| source value | local ignored issue record | committed artifact |
|---|---|---|
| raw answer | allowed only in ignored local record if approved | omit or summarize |
| real `document_id` | allowed only in ignored local record | use `example-document-id` |
| real `version_id` | allowed only in ignored local record | use `example-version-id` |
| real citation / chunk / cell / slide | allowed only in ignored local record | use placeholder |
| session_id | allowed only in ignored local record if needed | omit |
| reviewer / user names | use role or sanitized name | use role |
| business decision notes | summarize conservatively | do not include sensitive judgment |

Never place secrets, customer-private raw text, unreviewed legal/tender conclusions, or production credentials into committed examples.

## 4. Recorder Workflow

Recommended future workflow:

1. Save Day-1 raw output in an ignored local evidence bundle if needed.
2. Complete `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_WORKSHEET.md` for each finding.
3. Select the validator-compatible `issue_type`.
4. Assign P0 / P1 / P2 / P3.
5. Mark `human_review_required=true` for all business-impacting findings.
6. Copy the sanitized issue into a local ignored JSON file under `reports/pilot_issues/`.
7. Run strict validation with the Phase 2.37a tool.
8. If valid, include the issue in a local triage summary.
9. Let Codex B / user decide whether a later bounded fix phase is warranted.

Recorder must not:

1. mark any issue as repair-approved.
2. create external Linear / GitHub issues automatically.
3. treat `continue_with_manual_review` as rollout approval.
4. hide Missing Evidence.
5. change priorities to avoid review.

## 5. Dry-run Validation Commands

Validate one local ignored issue record:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input reports/pilot_issues/example.json --strict
```

Validate all local ignored issue records:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

Print a validator-compatible template:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --print-template
```

Interpretation:

1. `invalid_count > 0` means the recorder must fix the local issue input before review.
2. `go_pause_recommendation=pause` means at least one P0 is present.
3. `go_pause_recommendation=continue_with_manual_review` means P1 exists and human review is required.
4. `go_pause_recommendation=continue` is not production rollout approval.

## 6. Issue Type / Priority Mapping

Use current validator-compatible `issue_type` values.

| Day-1 finding | issue_type | priority | review note |
|---|---|---|---|
| 主标书限价 / 招标控制价 Missing Evidence | `retrieval_recall` | P1 | Do not fabricate; manual source review required. |
| 主标书资质 / 项目经理 / 联合体 / 业绩 / 人员 partial | `missing_evidence_expected` or `answer_boundary` | P1 | Split by field only after reviewer checks citations. |
| Excel cell citation degraded to row / range | `trace_ux` | P1 | Keep sheet / source location. |
| 公司方向建议需人工决策 | `answer_boundary` | P1/P2 | Must retain `no_automatic_decision`. |
| 会议 / strategy trace display polish | `trace_ux` | P2 | Record if auditability is affected. |

If future issue taxonomy needs `structured_citation_ux`, `manual_review_required`, or `strategy_human_review`, expand the validator in a separate bounded phase. Do not overload this planning phase into a schema change.

## 7. Local Storage and Git Policy

1. Real issue records stay under ignored local paths such as `reports/pilot_issues/*.json`.
2. Raw output bundles remain ignored.
3. Real Pilot reports remain ignored.
4. Only sanitized templates, runbooks, and reviewed examples may be committed.
5. `reports/agent_runs/latest.json` remains ignored local agent state.
6. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` is unrelated legacy dirty and must not be staged with Phase 2.44b.

## 8. Review / Baseline Gate

Before any future implementation or baseline:

1. Codex B reviews the workflow plan.
2. Static checks pass.
3. No real issue records or Pilot reports are generated.
4. No DB / index / facts / document_versions writes occur.
5. No repair, rollout, or Data Steward work is started.
6. Next phase remains explicitly bounded.

Phase 2.44b planning does not require Codex C validation because it does not touch API / CLI behavior.

## 9. Risks and Stop Conditions

Risks:

1. Recorder may accidentally include raw business output in a committed artifact.
2. Day-1 labels may not match current validator enum values.
3. P1 findings may be mistaken for fix authorization.
4. `continue_with_manual_review` may be misread as rollout approval.

Stop immediately if:

1. a task requires real issue generation.
2. a task requires scanning real reports.
3. a task requires DB / facts / versions / OpenSearch / Qdrant writes.
4. a task tries to repair, backfill, reindex, cleanup, or delete.
5. a task attempts production rollout or Data Steward implementation.
6. a task asks facts, transcript, or recommendations to replace retrieval evidence.

## 10. Next Recommendation

Proceed to Codex B review of this plan.

If approved, the next bounded phase can be one of:

1. Phase 2.44b docs-only Git baseline.
2. Phase 2.44c sanitized issue intake dry-run implementation using fake / temp data only.
3. Phase 2.44c recorder workflow runbook artifact.

Do not enter retrieval fixes, real issue generation, repair, rollout, or Data Steward work from this planning phase.
