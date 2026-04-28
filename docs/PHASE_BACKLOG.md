# Phase Backlog

## 当前优先级

1. Phase 2.34 baseline：Codex C 复验已通过，下一步只做双仓 Git baseline。
2. Phase 2.34 post-baseline review：Codex B 检查 commit/tag/push 与剩余 dirty。
3. Phase 2.35 候选：根据 Day-1 P1/P2 决定是否规划深层召回专项、latency polish 或继续 Pilot feedback report；不得直接 rollout。

## Day-1 Pilot 已知问题

1. P1 retrieval recall：`@主标书` 基础信息中最高投标限价未被当前召回覆盖。
2. P1 retrieval recall：`@主标书` 资质等级、业绩、人员数量等深层字段需人工复核。
3. P1 contamination / UX：`@会议纪要 vs @主标书` 实际 evidence 仅两份目标文档，但输出层误报 `third_document_mixed=true`。
4. P2 latency：会议纪要决策 / 风险与公司方向分析长输出偏慢。
5. Pilot 期间所有经营建议必须保留人工决策声明，不得当成自动经营决策。
6. Phase 2.34 已最小修复 Q8 输出层误报，Codex C 真实终端复验通过，建议 baseline。

## 后置项

1. 主标书深层字段召回专项：需单独 Phase 规划，不在 Phase 2.34 中顺手扩做。
2. 长输出 query 延迟优化：需先收集更多 Pilot 样本，不在 Phase 2.34 中扩大。
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
