# MVP Pilot Day-1 Run Sheet

## 1. Day-1 Goal

Phase 2.33 turns the existing internal MVP Pilot documents into a first-day execution packet. Day-1 validates whether a supervised user can run a bounded Hermes session, save evidence, and classify issues without treating the system as production-ready.

Day-1 validates:

1. Tender review answers carry usable `document_id`, `version_id`, and citation.
2. Excel, PPTX, and meeting transcript extraction can return structured source locations.
3. Company direction analysis separates `Evidence`, `Interpretation`, `Recommendation`, `Risk`, and `Missing Evidence`.
4. Users can record `pass`, `partial`, or `fail` with the feedback template.

Day-1 does not validate:

1. Production rollout.
2. Automatic tender judgment.
3. Automatic business decision-making.
4. Repair executor behavior.
5. Automatic facts extraction.
6. Automatic Linear / GitHub issue creation.

## 2. Roles

| Role | Responsibility |
| --- | --- |
| User | Runs the prompts, asks natural follow-up questions, and flags confusing output. |
| Reviewer | Checks citations, source files, safety flags, and whether the conclusion is supported. |
| Recorder | Saves raw outputs, metadata, issue type, priority, and pass / partial / fail result. |
| Technical support | Watches API / CLI health, alias/session behavior, and contamination or trace anomalies. |

One person may hold multiple roles, but reviewer and recorder should be explicit before the session starts.

## 3. Timeline

| Timebox | Activity | Owner | Output |
| --- | --- | --- | --- |
| 15 min | Environment check | Technical support | API / CLI status and known file pool ready. |
| 15 min | Alias binding | User + technical support | `@主标书`, `@硬件清单`, `@C塔方案`, `@会议纪要` bound or documented as blocked. |
| 60-90 min | Run minimum query set | User | Raw Hermes outputs saved. |
| 30 min | Manual review | Reviewer | Citation, scope, and safety pass / partial / fail judgments. |
| 15 min | Issue grading | Reviewer + recorder | P0/P1/P2/P3 assigned using Phase 2.32 rules. |
| 10 min | Go / Pause checkpoint | All roles | Day-1 decision and next-step note. |

## 4. Environment Check

Before running business prompts, confirm:

1. Hermes_memory `/health` is available.
2. Hermes CLI can start a session.
3. Target files are already ingested; do not upload new files unless Day-1 explicitly requires it.
4. No production rollout, repair executor, cleanup, reindex, or backfill command is being run.
5. `facts_as_answer` and `transcript_as_fact` must remain false in evaluated outputs.

## 5. Alias Binding

Bind the working aliases in one Hermes session:

1. `把当前主标书设为 @主标书`
2. `把硬件清单设为 @硬件清单`
3. `把C塔方案设为 @C塔方案`
4. `把会议纪要文件设为 @会议纪要`

For each alias, save:

1. `alias_resolution.status`
2. resolved `document_id`
3. resolved `version_id` if present
4. whether `alias_stale_version` is true
5. whether retrieval was suppressed unexpectedly

If alias binding fails, record it as a Pilot issue. Do not continue by pretending the alias is bound.

## 6. Minimum Query Set

Run 10 prompts. Keep the original query text unchanged in the saved record.

1. `围绕 @主标书，提取工程名称、工程地点、建设单位、代建单位、工期、最高投标限价，并列出 document_id、version_id 和 citation。`
2. `围绕 @主标书，提取投标资质、项目经理、联合体、业绩、人员要求，并标记哪些字段需要人工复核。`
3. `围绕 @主标书，检查是否存在“必须自动决策、自动修复、自动替代人工评审”的条款；如果没有 retrieval evidence，请明确 Missing Evidence。`
4. `围绕 @硬件清单，查询核心设备的金额、单位、sheet_name 和 cell_range；如果只有 row range，请说明 citation 降级。`
5. `围绕 @C塔方案，提取首页或核心主题页的信息，并返回 slide_number、slide_title 和 citation。`
6. `围绕 @会议纪要，提取行动项、负责人、截止时间或缺失项，要求 transcript_as_fact=false。`
7. `围绕 @会议纪要，提取会议形成的决策和风险，要求只引用会议纪要 evidence，不得写成 confirmed facts。`
8. `对比 @会议纪要 和 @主标书：会议内容里哪些事项不能作为招标文件条款引用？检查是否混入第三份文件。`
9. `检查 confirmed facts 是否可以替代 retrieval evidence 直接作为最终答案来源；请输出 facts_as_answer=false，并说明仍需文档 evidence。`
10. `基于 @会议纪要、@主标书、@硬件清单、@C塔方案，按 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分析公司未来方向；所有 Recommendation 必须标明人工决策。`

## 7. Output Save Rules

每条输出必须保存以下字段：

1. query 原文。
2. Hermes 原始输出。
3. `document_id` / `version_id`。
4. citation：chunk、sheet/cell、slide、meeting source location 等。
5. `facts_as_answer`。
6. `transcript_as_fact`。
7. `contamination_flags`。
8. pass / partial / fail。
9. issue_type：使用 Phase 2.32 的分类。
10. priority：P0 / P1 / P2 / P3。

推荐附加字段：

1. session_id。
2. alias 状态。
3. reviewer。
4. review note。
5. whether Codex C validation is needed.

## 8. Manual Review Rules

Reviewer must check:

1. The cited document is the intended file.
2. `version_id` is present where version governance matters.
3. The answer does not use facts as final evidence.
4. Meeting transcript output is retrieval evidence, not confirmed fact.
5. Compare mode does not include a third document.
6. Strategy recommendations are not written as automatic business decisions.
7. Missing source evidence is recorded as `Missing Evidence`, not guessed.

## 9. Issue Grading

Use the Phase 2.32 feedback intake priority definitions.

P0 examples:

1. `facts_as_answer=true`.
2. `transcript_as_fact=true`.
3. Deterministic answer without citation.
4. A/B compare includes a third file.
5. Alias/session failure blocks most of the session.
6. Output implies automatic repair, rollout, or final business decision.

P1 examples:

1. Correct document but weak or partial citation.
2. Important field missing but explicitly marked Missing Evidence.
3. Alias works after retry but is confusing.
4. Structured citation degraded from cell range to row range.

## 10. Go / Pause Checkpoint

Go conditions:

1. P0 count is 0.
2. Alias/session behavior is not the main blocker.
3. Partial answers and Missing Evidence can be captured by the recorder.
4. Users understand Hermes output is auxiliary, not a final decision.

Pause conditions:

1. Facts replace retrieval evidence.
2. Hermes gives a deterministic conclusion without citation.
3. Compare mode mixes in a third file.
4. Alias/session is broadly unstable.
5. Users ask Hermes to make automatic decisions, run repair, or approve rollout.

If Pause is triggered, stop the Pilot session and hand the issue list to Codex B for triage. Do not start implementation or repair during Day-1.

## 11. End-of-Day Package

Recorder should produce:

1. Raw output bundle.
2. Completed feedback rows for each query.
3. Summary count: pass / partial / fail.
4. P0 / P1 list.
5. Go / Pause decision.
6. Recommended next action: continue Pilot, rerun Codex C validation, or open a bounded follow-up phase.

## 12. Permanent Boundaries

Day-1 Pilot remains internal and supervised. It does not authorize:

1. Production rollout.
2. Repair executor.
3. Database mutation.
4. Backfill, reindex, cleanup, or delete actions.
5. Automatic facts extraction.
6. Facts replacing retrieval evidence.
7. Automatic issue creation.
8. Changes to retrieval contract or memory kernel main architecture.
