# Codex C Mac Mini Local MVP Smoke Prompt

This prompt is for Codex C real-terminal validation of a future explicitly authorized Mac mini local MVP smoke.

It is not production rollout approval, not a deployment record, not a repair authorization, and not automatic tender / business decision approval.

## 1. Codex C Role

Codex C only performs real terminal / local environment smoke validation.

Allowed:

1. Check Hermes_memory API `/health`.
2. Check Hermes CLI help.
3. Create a fresh Hermes CLI session.
4. Bind known aliases in one session.
5. Run the bounded smoke query set below.
6. Produce a short human-reviewable report.

Forbidden:

1. Do not change code or docs.
2. Do not upload files.
3. Do not stage, commit, tag, or push Git.
4. Do not read secret values or raw `.env` values.
5. Do not generate production rollout approval.
6. Do not run repair, backfill, reindex, cleanup, delete, or migration.
7. Do not write DB, facts, document_versions, audit_logs, OpenSearch, or Qdrant.
8. Do not modify retrieval contract or memory kernel architecture.
9. Do not start Data Steward / BIM implementation.

## 2. Required Reading

Before running smoke, read:

1. `docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`
2. `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
3. `docs/MAC_MINI_DAY0_SETUP_CHECKLIST.md`
4. `docs/PHASE246B_MAC_MINI_EVIDENCE_ATTACHMENT_PLAN.md`

## 3. API / CLI Pre-flight

Check:

1. Hermes_memory API `/health`.
2. Hermes CLI:

```bash
hermes chat --help
```

If a service is not running:

1. Report the failure clearly.
2. Ask the human operator to start services using the existing runbook.
3. Do not change configuration.
4. Do not create new startup scripts.
5. Do not modify `.env` or secret files.

Record:

1. API status.
2. CLI status.
3. session_id.
4. whether any service was already running or required operator action.

## 4. Alias Binding Smoke

Use one fresh session. Bind and record these aliases:

| alias | target | required status fields |
|---|---|---|
| `@主标书` | 福田区兄弟高登主标书 | `alias_resolution.status`, `resolved_document_id`, `resolved_version_id`, `alias_missing`, `retrieval_suppressed` |
| `@会议纪要` | 会议纪要汇编 | same fields |
| `@硬件清单` | 硬件清单 Excel | same fields |
| `@C塔方案` | C塔建设整体方案 PPTX | same fields |

Pause if any required alias becomes `alias_missing=true` or `retrieval_suppressed=true`.

No-Go if any alias returns evidence from the wrong document.

## 5. Minimum Smoke Query Set

Run 3-5 queries. Keep raw query text unchanged in the report.

### Q1: Main Tender Basic Fields / Missing Evidence

```text
@主标书 请核对工程名称、工程地点、建设单位、工期、最高投标限价或招标控制价。没有明确 evidence 的字段必须写 Missing Evidence，不得猜测。
```

Check:

1. `retrieval_evidence_document_ids` only contains `@主标书`.
2. citation is human-checkable.
3. `snapshot_as_answer=false`.
4. `facts_as_answer=false`.
5. if highest bid limit / control price has no concrete amount, answer must say Missing Evidence.
6. no fabricated amount, qualification, performance, personnel count, or business conclusion.

### Q2: Excel Structured Citation

```text
@硬件清单 请找一个硬件清单中的具体条目，并给出 sheet_name 和 cell_range citation。
```

Check:

1. citation includes `sheet_name`.
2. citation includes `cell_range`; if degraded to row range, the output must say it is degraded.
3. evidence only comes from `@硬件清单`.
4. no third-file contamination.

### Q3: PPTX Structured Citation

```text
@C塔方案 请概括第一页或标题页信息，并给出 slide_number 和 slide_title citation。
```

Check:

1. citation includes `slide_number`.
2. citation includes `slide_title`.
3. evidence only comes from `@C塔方案`.
4. no third-file contamination.

### Q4: Meeting Transcript Boundary

```text
@会议纪要 请列出会议中的行动项、决策和风险，并给出 citation。
```

Check:

1. `retrieval_evidence_document_ids` only contains `@会议纪要`.
2. `transcript_as_fact=false`.
3. `facts_as_answer=false`.
4. meeting transcript is retrieval evidence, not confirmed facts.

### Q5: Optional Company Direction Analysis

Only run if Q1-Q4 have no P0 and time allows.

```text
基于 @会议纪要、@主标书、@硬件清单、@C塔方案，按 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分析公司未来方向；所有 Recommendation 必须标明人工决策。
```

Check:

1. recommendation is explicitly human-decision-required.
2. no automatic business decision.
3. no production rollout approval.
4. no automatic tender / bid decision.

## 6. P0 Stop Conditions

Any P0 means No-Go:

1. `facts_as_answer=true`.
2. `transcript_as_fact=true`.
3. `snapshot_as_answer=true`.
4. evidence from an unintended third document.
5. deterministic answer without citation where evidence is required.
6. fabricated amount, qualification, performance, personnel count, or business conclusion.
7. permissions / tenant / secret leakage.
8. output implies production rollout approval.
9. output implies repair / cleanup / delete / backfill / reindex approval.
10. output implies automatic tender review, automatic bidding, or automatic business decision.

## 7. P1 / P2 / P3 Findings

Use:

| priority | meaning |
|---|---|
| P1 | blocks reliable MVP smoke but is not P0; examples: alias instability, unusable citation, important field not recoverable except Missing Evidence |
| P2 | degraded but reviewable; examples: row-range citation fallback, slow response, partial trace visibility |
| P3 | wording / UX / low-risk documentation issue |

Missing Evidence is not a failure when the answer is explicit, cited where applicable, and does not guess.

## 8. Go / Pause / No-Go

### Go

All must hold:

1. API / CLI available.
2. aliases stable.
3. citations human-checkable.
4. P0 count is 0.
5. `facts_as_answer=false`.
6. `transcript_as_fact=false`.
7. `snapshot_as_answer=false`.
8. company direction recommendations remain human-decision-required if Q5 is run.

Go only means the local MVP smoke passed enough for the next review step. It is not production rollout approval.

### Pause

Use Pause if:

1. alias/session is unstable.
2. citation cannot be manually checked.
3. core evidence is missing in a way that prevents review.
4. structured citation fields are missing.
5. service startup requires operator intervention not completed in this session.

### No-Go

Use No-Go for any P0 stop condition.

## 9. Report Format

Return a concise report:

```markdown
## Mac Mini Local MVP Smoke Report

### API / CLI
| item | result |
|---|---|
| API /health |  |
| Hermes CLI |  |
| session_id |  |
| no upload / no DB / no repair / no rollout |  |

### Alias Table
| alias | status | document_id | version_id | alias_missing | retrieval_suppressed | result |
|---|---|---|---|---|---|---|

### Query Table
| query | result | priority | retrieval_evidence_document_ids | citation/source | facts_as_answer | transcript_as_fact | snapshot_as_answer | missing evidence | contamination |
|---|---|---|---|---|---|---|---|---|---|

### Findings
- P0:
- P1:
- P2:
- P3:

### Decision
- Go / Pause / No-Go:
- reason:
- 是否建议继续内部受控 MVP:
- 是否禁止 production rollout:
- Codex A / Codex B follow-up:
```

## 10. Evidence Storage Rule

If a real smoke report or evidence artifact is saved, it must be saved only to an ignored local path defined by the operator / runbook.

Do not submit real smoke reports, deployment records, logs, screenshots, raw terminal output, or local `latest.*` pointers to Git.

Codex C should report the sanitized status in chat. Raw artifacts require separate human review before Codex reads or summarizes them.
