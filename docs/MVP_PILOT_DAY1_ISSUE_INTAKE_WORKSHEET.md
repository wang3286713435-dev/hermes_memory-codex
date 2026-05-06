# MVP Pilot Day-1 Issue Intake Worksheet

## 1. Use Conditions

This worksheet is for internal controlled MVP Pilot issue intake only.

It is not:

1. production rollout approval.
2. a repair request.
3. an external issue creation request.
4. an automatic tender review result.
5. permission to write DB / facts / document_versions / OpenSearch / Qdrant.

Use it to turn human-reviewed Pilot findings into sanitized local issue records that can later be validated with the Phase 2.37a dry-run tool.

## 2. Required Fields

For each Pilot issue, record:

| field | required | note |
|---|---:|---|
| `issue_id` | yes | Use `pilot-issue-YYYYMMDD-001` style. |
| `source` | yes | Example: `codex_c_terminal_validation`, `user_pilot_feedback`, `reviewer_observation`. |
| `source_phase` | yes | Example: `Phase 2.44a`. |
| `reported_at` | yes | ISO timestamp with timezone. |
| `reporter` | yes | Use a role or sanitized name. |
| `query` | yes | Keep the exact user query when safe; otherwise sanitize. |
| `aliases` | yes | Example: `@主标书`, `@硬件清单`. |
| `expected_behavior` | yes | What Hermes should have done. |
| `actual_behavior` | yes | What happened, without raw sensitive output unless approved. |
| `document_ids` | yes | Use placeholders in committed samples; real IDs stay in ignored local records. |
| `version_ids` | yes | Use placeholders in committed samples; real IDs stay in ignored local records. |
| `citations` | yes | Chunk / sheet / cell / slide / transcript location if available. |
| `trace_flags` | yes | Include evidence and safety flags when visible. |
| `issue_type` | yes | Must use the current validator enum. See mapping below. |
| `priority` | yes | `P0` / `P1` / `P2` / `P3`. |
| `safety_boundary` | yes | Use validator-supported safety boundary values. |
| `human_review_required` | yes | `true` for all business-impacting Pilot issues. |
| `suggested_next_action` | yes | Must be triage / review / bounded planning, not repair or rollout. |
| `status` | yes | Start with `new`. |
| `notes` | yes | State that this is not repair / rollout approval. |

## 3. Validator-compatible Issue Type Mapping

The Phase 2.37a validator currently accepts:

`retrieval_recall`, `trace_ux`, `latency`, `alias_session`, `contamination_false_positive`, `missing_evidence_expected`, `answer_boundary`, `environment`, `documentation`.

Use this mapping for Day-1 labels:

| Day-1 label | validator `issue_type` | priority |
|---|---|---|
| `retrieval_recall`: 主标书限价 Missing Evidence | `retrieval_recall` | P1 |
| `manual_review_required`: 主标书深层字段人工复核 | `missing_evidence_expected` or `answer_boundary` | P1 |
| `structured_citation_ux`: Excel citation 降级 | `trace_ux` | P1 |
| `strategy_human_review`: 公司方向人工决策 | `answer_boundary` | P1/P2 |
| `trace_display_ux`: 会议 / strategy trace 展示 | `trace_ux` | P2 |

Keep the Day-1 label in `notes` if useful, but keep `issue_type` validator-compatible.

## 4. Day-1 Candidate Quick-fill

### 4.1 Main Tender Price Ceiling Missing Evidence

- issue label: `day1-p1-price-ceiling-missing`
- priority: `P1`
- issue_type: `retrieval_recall`
- aliases: `@主标书`
- expected_behavior: return cited concrete amount or explicit Missing Evidence.
- actual_behavior: highest bid limit / tender control price / bid cap remained Missing Evidence.
- safety_boundary: `missing_evidence`, `evidence_required`, `no_fabrication`
- human_review_required: `true`
- suggested_next_action: record for manual triage before any bounded retrieval fix planning.

### 4.2 Main Tender Deep Fields Need Human Review

- issue label: `day1-p1-tender-deep-fields-manual-review`
- priority: `P1`
- issue_type: `missing_evidence_expected` or `answer_boundary`
- aliases: `@主标书`
- fields: qualification, project manager, consortium, performance, personnel.
- safety_boundary: `evidence_required`, `no_fabrication`
- human_review_required: `true`
- suggested_next_action: split by field only after reviewer checks raw outputs and citations.

### 4.3 Excel Citation Degraded to Row / Range

- issue label: `day1-p1-excel-citation-degraded`
- priority: `P1`
- issue_type: `trace_ux`
- aliases: `@硬件清单`
- expected_behavior: stable sheet and cell-range citation when available.
- actual_behavior: some cell citation degraded to row / range.
- safety_boundary: `evidence_required`
- human_review_required: `true`
- suggested_next_action: record affected query, sheet name, and degraded source location.

### 4.4 Strategy Output Requires Human Decision

- issue label: `day1-p1-strategy-human-review`
- priority: `P1` or `P2`
- issue_type: `answer_boundary`
- aliases: strategy query may involve `@会议纪要`, `@主标书`, `@硬件清单`, `@C塔方案`.
- expected_behavior: recommendations are auxiliary and explicitly require human decision.
- actual_behavior: record if wording could be mistaken as an automatic decision.
- safety_boundary: `no_automatic_decision`, `evidence_required`
- human_review_required: `true`
- suggested_next_action: keep as human decision boundary review.

### 4.5 Trace Display UX

- issue label: `day1-p2-trace-display-ux`
- priority: `P2`
- issue_type: `trace_ux`
- expected_behavior: trace display makes evidence and safety flags easy to audit.
- actual_behavior: meeting risk / strategy trace display still needs polish.
- safety_boundary: `evidence_required`
- human_review_required: `true` when business-impacting.
- suggested_next_action: record only if reviewer cannot audit evidence efficiently.

## 5. Priority Rules

P0:

1. fabricated answer presented as evidence-backed.
2. facts or transcript replacing retrieval evidence.
3. cross-document contamination in final evidence.
4. permission or tenant leakage.
5. automatic business, tender, legal, rollout, or repair decision.

P1:

1. key field recall failure that blocks Pilot usefulness.
2. core citation missing or degraded.
3. alias/session failure that blocks retrieval.
4. answer boundary ambiguity around human decisions.

P2:

1. confusing trace or display with safe evidence.
2. latency / verbosity that slows review.
3. non-critical partial field.

P3:

1. wording, formatting, or documentation polish.
2. low-risk template or worksheet improvement.

## 6. Go / Pause / No-Go Interpretation

Go:

1. P0 count is zero.
2. P1 issues are recordable and manually reviewable.
3. users understand Hermes output is auxiliary.

Pause:

1. a P1 blocks the session flow.
2. alias/session instability returns.
3. reviewer cannot audit core citation.
4. Missing Evidence frequency makes the task unusable.

No-Go:

1. any P0 appears.
2. facts / transcript / snapshot replaces retrieval evidence.
3. third-document contamination enters final evidence.
4. Hermes fabricates price, qualification, performance, personnel, or business conclusion.
5. any repair, cleanup, delete, reindex, backfill, rollout, or DB write is triggered.

## 7. Commands

Print the validator template:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --print-template
```

Validate one local issue record:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input reports/pilot_issues/example.json --strict
```

Validate all local issue records:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

## 8. From Worksheet to Ignored Local JSON

1. Copy one completed worksheet row into a local JSON file under `reports/pilot_issues/`.
2. Keep real raw answers, real document IDs, real version IDs, and real citations in ignored local files only.
3. Run the strict validator before using the issue in a triage summary.
4. Do not commit real issue records.
5. Do not create Linear / GitHub issues automatically.

## 9. Permanent Prohibitions

Do not treat this worksheet as:

1. a repair request.
2. production rollout approval.
3. automatic external issue creation.
4. a retrieval fix task.
5. a DB / index mutation task.
6. Data Steward / BIM implementation approval.
