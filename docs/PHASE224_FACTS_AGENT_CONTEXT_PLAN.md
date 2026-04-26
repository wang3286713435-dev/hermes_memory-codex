# Phase 2.24 Facts Agent Context Plan

## 1. 目标

Phase 2.24 只做 confirmed facts 是否进入 Agent 上下文的路线裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构。

## 2. 当前基线

Phase 2.21a / 2.21b / 2.22a / 2.23a 已完成：

1. evidence-backed facts。
2. facts eval。
3. facts 查询权限过滤。
4. fact query audit。
5. confirm / reject 人工确认。
6. facts 管理查询。
7. confirmed facts 只读检索与 source citation 回链。

当前边界：

1. facts 仍不进入 Agent final answer。
2. facts 不自动抽取。
3. confirmed facts 已可作为只读结构化记录查询。

## 3. 候选方向评审

| 方向 | 企业落地价值 | 技术风险 | 当前依赖 | 是否会放大风险 | 是否适合下一阶段 |
| --- | --- | --- | --- | --- | --- |
| A. confirmed facts 作为辅助上下文进入 Agent，但不得替代 retrieval evidence | 高。可让 Agent 看到已确认结构化事实，提高上下文稳定性。 | 中。若边界清晰，风险可控；若误作答案则风险升高。 | confirmed facts 查询、citation、stale、权限、audit 已具备。 | 中。需要强制 `facts_as_answer=false` 和 evidence required。 | 推荐。 |
| B. confirmed facts 直接参与 Agent final answer | 高。可提升回答效率。 | 高。容易绕过 retrieval evidence，造成过期或冲突事实被直接输出。 | 只读 facts 已具备，但 answer policy 尚未完成。 | 高。会放大 stale / conflict / permission 风险。 | 暂不推荐。 |
| C. facts 自动抽取 | 高。可扩大覆盖。 | 很高。会批量制造待确认事实。 | evidence-backed 创建具备，但抽取、审核、冲突处理不足。 | 很高。会增加治理压力。 | 不推荐。 |
| D. facts UI / 管理后台 | 高。企业落地需要人工操作入口。 | 中。涉及产品形态、权限、审计与前端。 | API 已具备雏形。 | 中。流程未稳定前不宜固化 UI。 | 可后续规划。 |
| E. 继续强化 facts eval / permissions | 中高。提升可信度。 | 低中。偏治理增强。 | eval、soft policy 已具备。 | 低。可作为 A 的配套验证。 | 适合配套推进。 |

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.24a：confirmed facts 作为 Agent 辅助上下文。**

推荐原因：

1. confirmed facts 已完成只读检索、source citation、stale 诊断、权限过滤与 audit。
2. 进入辅助上下文能提升 Agent 对已确认企业事实的可见性。
3. 本阶段仍不允许 facts 替代 retrieval evidence，可避免过早把 facts 当最终答案。
4. 相比直接进入 final answer，该路线更适合渐进验证。

## 5. Phase 2.24a 最小边界

最小规则：

1. 只允许 `verification_status=confirmed` 的 facts 进入 Agent context。
2. trace 必须输出 `facts_context_used=true`。
3. trace 必须输出 `facts_as_answer=false`。
4. 每条 fact 必须显示 `source_document_id`、`source_version_id`、`source_chunk_id`。
5. `stale_source_version=true` 时必须在 context 中提示，不得静默使用。
6. facts 查询必须继承 source document soft policy；deny 后不得进入 Agent context。
7. audit 必须记录 `facts_context_fact_ids`。
8. Agent 最终回答仍必须由本轮 retrieval evidence 支撑。
9. 如果 retrieval evidence 为空，不允许只靠 facts 生成文档型最终答案。

最小 context 语义：

1. confirmed facts 只能作为“辅助结构化上下文”。
2. facts citation 只能帮助用户回到 source chunk。
3. facts 不替代 retrieval citation。
4. facts 与 retrieval evidence 冲突时，必须优先提示冲突，而不是直接采信 fact。

## 6. 最小验收建议

Phase 2.24a 后续实现应至少验证：

1. confirmed fact 可进入 Agent context。
2. unverified / rejected fact 不进入 Agent context。
3. denied fact 不进入 Agent context。
4. stale source fact 进入 context 时有明确 warning。
5. `facts_context_used=true` 且 `facts_as_answer=false`。
6. `facts_context_fact_ids` 写入 audit / trace。
7. retrieval evidence 为空时，Agent 不得只靠 facts 假装有文档证据。

## 7. 非目标

Phase 2.24a 不做：

1. 自动抽取 facts。
2. facts 直接替代文档证据。
3. facts 直接参与 Agent final answer。
4. 复杂知识图谱。
5. UI / 管理后台。
6. rollout。
7. retrieval contract 重构。
8. memory kernel 主架构重构。

## 8. 当前结论

建议开始 Phase 2.24a 最小实现。

confirmed facts 可以进入 Agent 辅助上下文，但必须强制 `facts_as_answer=false`，并继续要求 retrieval evidence 支撑最终回答。

## 9. Phase 2.24a 实施结果

本轮已完成 Phase 2.24a 最小实现，主要落在 Hermes 主仓库消费层；Hermes_memory 保持现有 facts API / service 能力，不改 retrieval contract。

已完成：

1. Hermes 主仓库可在显式 facts context hint 下读取 confirmed facts 作为辅助上下文。
2. 仅 `verification_status=confirmed` 的 facts 会进入 Agent context。
3. facts 查询继续继承 source document soft policy；deny 或无 confirmed facts 时不注入。
4. trace 输出 `facts_context_used`、`facts_context_fact_ids`、`facts_as_answer=false`、`stale_fact_source_count`。
5. context block 明确 confirmed facts 只是 auxiliary context，最终回答仍需要本轮 retrieval evidence。
6. stale source fact 会显示 warning，不阻断注入。
7. 无当前 retrieval evidence 时会 suppress facts context，避免 facts 单独支撑文档型回答。

验证结果：

1. 主仓库 direct assertion tests 通过：39 个函数断言通过。
2. live smoke 正向注入通过：retrieval evidence 存在时，`facts_context_used=true`，`facts_as_answer=false`。
3. live smoke stale source 通过：`stale_fact_source_count=1` 且 context 出现 stale warning。
4. live smoke 无 retrieval evidence 通过：`facts_context_suppressed_reason=no_current_retrieval_evidence`。

## 10. Phase 2.24a 终端验收修复记录

真实终端验收暴露两类问题：

1. confirmed facts context 与 meeting transcript metadata 展示混在 session scope 中，模型容易把会议纪要 retrieval chunks 误读为 facts。
2. `stale fact source` 类诊断 query 未稳定触发 confirmed facts stale 检查，导致旧版本 fact warning 未出现。

修复结论：

1. Hermes 主仓库已将 confirmed facts context 改为独立分区：`Confirmed facts auxiliary context`。
2. meeting transcript 仍只作为 retrieval evidence metadata，`transcript_as_fact=false`。
3. facts trace 稳定输出 `facts_context_used`、`facts_context_fact_ids`、`facts_as_answer=false`、`stale_fact_source_count`。
4. stale source 诊断 query 可触发 facts stale 检查，并输出 `latest_version_id`。
5. 若没有 facts context，trace / context 明确显示 `facts_context_used=false`、`facts_as_answer=false`。
6. 复验 Prompt 4 前必须先绑定 `@会议纪要`，因为 alias 是 session-level 状态，新会话不会自动继承。

二次修复补充：

1. 无作用域 `stale fact source` query 不再触发普通文档 retrieval，避免无关文件污染诊断。
2. `phase224a 测试事实是否可以直接作为最终答案来源` 类 fact-answer policy query 会抑制 retrieval，并明确 `no_current_retrieval_evidence`。
3. `facts_context_fact_ids` 只允许 fact id list，禁止混入 `[E]` / `[C]` retrieval chunk 或 citation id。
4. 已知 stale fact `9f98384b-5053-4a8f-9b83-35983b28b38e` 可被 stale scan 检出，并输出 `latest_version_id=76ca95a1-393f-4278-b254-ab66295bb14f`。
5. alias 绑定 / 普通 retrieval-only 场景已稳定渲染 facts diagnostics：`facts_context_used=false`、`facts_context_fact_ids=[]`、`facts_as_answer=false`，confirmed facts 分区仅在 facts context 真正启用时出现。

真实终端复验收口：

1. API 可用，Hermes CLI 可用。
2. `@会议纪要` 预备绑定通过，document_id 为 `92051cc6-56b5-4930-bdf0-119163c83a75`。
3. 预备绑定输出稳定为 `facts_context_used=false`、`facts_context_fact_ids=[]`、`facts_as_answer=false`。
4. 5 条正式验收全部通过。
5. stale fact `9f98384b-5053-4a8f-9b83-35983b28b38e` 已检出，`stale_fact_source_count=1`。
6. stale source version 为 `896a19d7-2b01-4492-9672-bb4fdfbc7921`，latest version 为 `76ca95a1-393f-4278-b254-ab66295bb14f`。
7. 未出现 E/C chunks 写入 `facts_context_fact_ids`、fact-only query 检索无关文档或 facts 替代 retrieval evidence。
8. `facts_as_answer` 全场景保持 false。

仍保留非目标：

1. facts 不进入 Agent final answer。
2. 不自动抽取 facts。
3. 不做复杂知识图谱。
4. 不做 UI / 管理后台。
5. 不进入 rollout。
