# Phase 2.46d Mac Mini Local MVP Smoke Result

## 1. Purpose

This document records a sanitized summary of the Codex C Mac mini local MVP smoke result.

It does not contain raw transcripts, secret values, `.env` values, complete terminal logs, or sensitive business content.

This result supports internal controlled MVP continuation only. It is not production rollout approval.

## 2. Boundary

Phase 2.46d does not:

1. run smoke.
2. start, stop, or modify services.
3. execute Mac mini setup.
4. run Phase 2.45c health-check runner.
5. generate raw evidence artifacts.
6. read or generate secret values.
7. write DB, facts, document_versions, audit_logs, OpenSearch, or Qdrant.
8. run repair, backfill, reindex, cleanup, delete, or migration.
9. approve production rollout.
10. authorize Data Steward / BIM implementation.
11. authorize automatic tender review, automatic bidding, automatic business decisions, contract decisions, procurement decisions, or customer communication.

## 3. Smoke Summary

| field | value |
|---|---|
| phase | Phase 2.46d Mac mini local MVP smoke result intake |
| session_id | `20260507_170043_729824` |
| API `/health` | pass, `200 OK` |
| Hermes CLI | pass |
| decision | Go |
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| production rollout | false |
| repair authorized | false |
| Data Steward authorized | false |

`Go` means internal controlled MVP smoke may continue. It does not mean production rollout, deployment approval, automatic business decision approval, repair authorization, or customer-facing approval.

## 4. Alias Binding Result

| alias | status | document_id | version_id | alias_missing | retrieval_suppressed |
|---|---|---|---|---|---|
| `@主标书` | alias_bound | `869d4684-0a98-4825-bc72-ada65c15cfc9` | `43558ba9-2813-42ff-b11b-3fbb4448a5bb` | false | false |
| `@会议纪要` | alias_bound | `92051cc6-56b5-4930-bdf0-119163c83a75` | `e3b422e3-35e2-4d89-8136-66a558e8cfbe` | false | false |
| `@硬件清单` | alias_bound | `402657e8-2ea8-48b7-8266-85aab45bbc41` | `f1c43bfd-6b1b-4ec1-99a6-c0650e2e2e14` | false | false |
| `@C塔方案` | alias_bound | `a52e75b3-fec9-4e08-8c0d-03b0e55cf21d` | `2e0adc17-f8ea-4ac3-b944-a788c1980616` | false | false |

## 5. Query Result Summary

| query | result | priority | sanitized finding |
|---|---|---|---|
| Q1 主标书基础字段 | pass | none | only `@主标书` evidence; citation visible; limit / control price Missing Evidence visible; no contamination |
| Q2 Excel citation | pass | P2 | only `@硬件清单` evidence; `sheet_name=开始`; `cell_range=A3:P24` + Row 7; row/range citation is human-checkable but not exact single-cell |
| Q3 PPTX citation | pass | none | only `@C塔方案` evidence; `slide_number=1`; `slide_title=卓羽智能` |
| Q4 会议纪要边界 | partial | P2 | only `@会议纪要` evidence; `transcript_as_fact` not explicitly printed, but content did not treat transcript as confirmed facts |
| Q5 公司方向分析 | pass | P2 | four target aliases cited; recommendations marked human-decision-required; Missing Evidence visible; no automatic business decision |

## 6. Findings

### P0

None.

### P1

None.

### P2

1. Excel citation is human-checkable but remains row/range level rather than exact single-cell.
2. Meeting transcript boundary content was correct, but `transcript_as_fact=false` was not explicitly printed in one sampled output.
3. Company direction analysis passed the human-decision boundary but should remain under reviewer supervision.

### P3

None recorded in the sanitized summary.

## 7. Decision

| decision field | result |
|---|---|
| Go / Pause / No-Go | Go |
| internal controlled MVP continuation | allowed |
| production rollout | forbidden |
| repair / backfill / reindex / cleanup / delete | forbidden |
| automatic tender / bidding / business decision | forbidden |
| customer-facing decision / communication | requires human owner confirmation |
| Data Steward implementation | not authorized |

## 8. Follow-up Recommendations

1. Continue internal controlled MVP operating loop planning.
2. Track P2 display tails:
   - Excel exact cell citation display.
   - explicit `transcript_as_fact=false` display in meeting outputs.
3. Keep all tender, business, contract, procurement, and customer communication decisions under human owner confirmation.
4. Do not enter production rollout without a separate readiness / approval phase.
5. Do not start repair executor or Data Steward implementation from this smoke result.

## 9. Current Conclusion

Codex C smoke returned `Go` with `P0=0` and `P1=0`.

The result supports internal controlled MVP continuation only. It does not authorize production rollout, automatic decisions, repair execution, DB / index writes, or Data Steward implementation.
