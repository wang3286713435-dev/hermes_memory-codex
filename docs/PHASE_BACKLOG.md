# Phase Backlog

## 当前优先级

1. Phase 2.35c Git baseline：提交 bounded retrieval + alias/session 修复与阶段文档。
2. baseline 文案必须明确：alias/session 已通过真实终端复验，但 deep-field recall 仍 partial。
3. baseline 后再规划后续 retrieval recall / trace display tail items。

## Day-1 Pilot 已知问题

1. P1 retrieval recall：`@主标书` 最高投标限价 / 招标控制价 / 投标报价上限未召回具体金额。
2. P1 retrieval recall：`@主标书` 投标资质具体等级 / 类别未召回。
3. P1 partial：项目经理、联合体、业绩、人员要求已有相关 evidence，但仍需人工复核。
4. P2 latency：会议纪要决策 / 风险与公司方向分析长输出偏慢。
5. Pilot 期间所有经营建议必须保留人工决策声明，不得当成自动经营决策。

## Phase 2.35 当前状态

1. Phase 2.35 最小实现已完成，目标测试 `22 passed`。
2. Codex C 复验显示安全边界通过：无编造、facts/transcript 均未替代 evidence。
3. Phase 2.35b 已完成 metadata precision 小修：限价需具体金额，资质需具体等级 + 类别。
4. Phase 2.35b 已新增 API trace 顶层 profile 字段：`metadata_guided_query_profile`、`metadata_deep_field_profile`。
5. alias 首次绑定不稳定已在 Codex C 真实 CLI 中复现：bind 成功后正式 Q1/Q2 变为 `alias_missing=true / retrieval_suppressed=true`。
6. Phase 2.35c 已完成主仓库最小修复：`上一轮已锁定的当前文件` 等说法现在会走 current-document bind / current retrieval fallback，不再被误当成标题或历史上下文。
7. Codex C 真实终端复验通过：session `20260429_165301_e3c312` 中正式 Q1/Q2 均为 `alias_resolved`，`alias_missing=false`，`retrieval_suppressed=false`。
8. Phase 2.35c 可进入 Git baseline，但只能声明 alias/session 修复收口；deep-field recall 与 trace 透出仍不完全收口。

## 后置项

1. 完整 AI 审标 / 自动审标：后置，当前只做 retrieval evidence 与 trace 改善。
2. 长输出 query 延迟优化：需先收集更多 Pilot 样本，不在 Phase 2.35b 中扩大。
3. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
4. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
5. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
6. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
7. rollout readiness：后置，当前仍不进入生产 rollout。
8. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。
9. default real reports / reviews scan：后置，除非用户显式指定输入。
10. production rollout 继续后置；MVP Pilot 不得解释为 production ready。

## 永久边界

1. 不擅自修改 retrieval contract。
2. 不擅自修改 memory kernel 主架构。
3. 不执行 destructive repair / delete / cleanup。
4. 不让 facts 自动替代 retrieval evidence。
5. 不创建生产 cron / 定时任务。
6. 每轮开始读取 ACTIVE_PHASE 与 PHASE_BACKLOG。
7. 用户要求执行任务入口时，读取 `docs/NEXT_CODEX_A_PROMPT.md`。
8. 夜间执行时读取 `docs/NIGHTLY_SPRINT_PROTOCOL.md` 与 `docs/NIGHTLY_SPRINT_QUEUE.md`。
9. 每轮结束更新 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json。
10. 夜间 sprint 结束额外写入 ignored 的 `reports/nightly_runs/<timestamp>.json`。
11. planning / implementation / validation / baseline 分阶段推进。
12. baseline 前默认需要 Codex B 审核，除非用户明确授权。
