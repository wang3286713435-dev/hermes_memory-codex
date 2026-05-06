# Phase 2.44 MVP Pilot Continuation / Issue Intake Plan

## 1. Goal

Phase 2.44 converts the Phase 2.43d baseline and Codex C Day-1 continuation result into a bounded plan for continued internal MVP Pilot use and issue intake.

Day-1 continuation result:

1. Decision: `Go` for internal controlled MVP Pilot continuation.
2. Query summary: `6 pass / 4 partial / 0 fail`.
3. P0 count: `0`.
4. `@主标书` alias/session blocker: resolved.
5. `@主标书` Q1-Q2: `alias_resolved`, `alias_missing=false`, `retrieval_suppressed=false`.

This plan does not approve production rollout.

## 2. Non-goals

Phase 2.44 does not:

1. create real Pilot issue records.
2. generate a real Pilot review report.
3. run API / CLI smoke.
4. fix retrieval recall.
5. write DB / facts / document_versions.
6. modify OpenSearch or Qdrant.
7. run repair, backfill, reindex, cleanup, or delete.
8. create Linear / GitHub issues automatically.
9. implement Data Steward, BIM schema, Neo4j, PostGIS, spatial index, or scheduler.
10. change retrieval contract or memory kernel main architecture.

## 3. Current Continuation Decision

The project may continue the internal controlled MVP Pilot under supervision.

Required constraints:

1. Every business-impacting output remains auxiliary.
2. Tender review fields with Missing Evidence or partial citations require human review.
3. Company direction recommendations require human decision.
4. P1 / P2 findings must be captured through issue intake before any fix phase is planned.
5. `Go` means "continue internal Pilot", not "production ready".

## 4. Day-1 Issue Intake Candidate Table

| id | priority | issue_type | source query / area | observed behavior | recommended intake action | immediate fix? |
|---|---|---|---|---|---|---|
| `day1-p1-price-ceiling-missing` | P1 | `retrieval_recall` | `@主标书` 工程基础信息 | 最高投标限价 / 招标控制价 / 投标报价上限仍为 Missing Evidence | Create sanitized local issue candidate with query, expected field, actual Missing Evidence, document_id, citations if any, and human review required | no |
| `day1-p1-tender-deep-fields-manual-review` | P1 | `manual_review_required` | `@主标书` 资质 / 项目经理 / 联合体 / 业绩 / 人员 | 相关字段仍 partial，需人工复核 | Group into one issue or split by field after reviewer checks raw outputs | no |
| `day1-p1-excel-citation-degraded` | P1 | `structured_citation_ux` | `@硬件清单` Excel citation | 部分 cell citation 降级为 row / range | Record sheet / row-range degradation and affected query | no |
| `day1-p1-strategy-human-review` | P1/P2 | `strategy_human_review` | 公司未来方向分析 | 可辅助分析，但经营建议 / 风险 / 行业判断必须人工决策 | Record as human-decision boundary issue if output wording is unclear | no |
| `day1-p2-trace-display-ux` | P2 | `trace_display_ux` | 会议风险解释 / strategy trace | 部分 trace 展示仍需 polish | Record only if reviewer cannot audit evidence efficiently | no |

## 5. Record-now vs Fix-now Policy

Record now:

1. Missing Evidence fields.
2. partial citation quality.
3. human-review-required business or tender fields.
4. trace display friction.
5. any repeatable Pilot UX confusion.

Do not fix now:

1. price ceiling recall.
2. qualification / project manager / performance / personnel deep-field recall.
3. Excel cell-range reconstruction.
4. strategy reasoning or business recommendation wording.
5. trace display polish.

Fix planning requires a separate bounded Phase after issue records are reviewed.

## 6. Recommended Next Phase

Recommended: Phase 2.44a sanitized local issue records / issue intake summary dry-run.

Minimum boundary:

1. Read a manually prepared sanitized Day-1 continuation input file.
2. Generate local issue record skeletons or summary preview.
3. Do not scan real `reports/` by default.
4. Do not write real issue JSON unless explicitly instructed.
5. Do not create external issues.
6. Do not repair or tune retrieval.

Alternative: Phase 2.44a Pilot continuation run packet / recorder worksheet.

Use this alternative if the team wants one more manually guided Pilot continuation before generating issue records.

## 7. Go / Pause / No-Go Rules for Next Pilot Continuation

Go:

1. P0 remains `0`.
2. alias/session remains stable for target aliases.
3. Missing Evidence is visible and recordable.
4. P1 issues are captured for bounded follow-up.
5. users understand outputs are auxiliary.

Pause:

1. a P1 blocks the session flow.
2. alias/session instability returns.
3. citation cannot be manually checked for a core answer.
4. Missing Evidence frequency makes the task unusable.
5. user behavior drifts toward automatic decision-making.

No-Go:

1. any P0 appears.
2. facts / transcript / snapshot replaces retrieval evidence.
3. third-document contamination enters final evidence.
4. Hermes fabricates price, qualification, performance, personnel, or business conclusion.
5. any repair, cleanup, delete, reindex, backfill, rollout, or DB write is triggered.

## 8. Human Review Responsibilities

Reviewer must save or confirm:

1. raw query.
2. raw answer.
3. document_id.
4. version_id.
5. citation / source location.
6. pass / partial / fail.
7. issue_type.
8. priority.
9. human_review_required.
10. evidence policy flags when available.
11. reviewer note.

Recorder must keep real issue records local and ignored unless a sanitized artifact is explicitly approved for commit.

## 9. Storage and Git Policy

1. Real Pilot issue records belong under ignored local paths such as `reports/pilot_issues/*.json`.
2. Real Pilot review reports remain ignored local artifacts.
3. No real raw output bundle should be committed.
4. Templates, runbooks, and sanitized examples may be committed only after review.
5. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` is unrelated legacy dirty and must not be staged as part of Phase 2.44.

## 10. Next Recommendation

Proceed to Codex B review of this plan.

If approved, Phase 2.44a should be either:

1. sanitized local issue records / issue intake summary dry-run, or
2. Pilot continuation recorder worksheet.

Do not enter implementation, retrieval tuning, repair, rollout, or Data Steward work from this planning phase.
