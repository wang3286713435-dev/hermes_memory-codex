# Phase Backlog

## 当前优先级

1. Phase 2.32 review：Codex B 审核 MVP Pilot feedback intake / triage loop。
2. Phase 2.32 baseline：审核通过后只提交文档 baseline，不写功能代码。
3. Phase 2.32 后置：根据真实试用反馈决定是否进入召回质量专项或 UX / prompt polish，不直接 rollout。

## 后置项

1. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
2. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
3. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
4. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
5. rollout readiness：后置，当前仍不进入生产 rollout。
6. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。
7. repair executor：继续后置，除非 freeze 报告与人工评审明确批准。
8. docs drift cleanup 已完成 baseline；下一步仍不得直接进入 release candidate execution 或 rollout。
9. production rollout 继续后置；MVP freeze candidate checklist 不得被解释为 production ready。
10. Phase 2.29e 若实现，也只能输出 dry-run checklist JSON，不得写 DB、执行 repair 或默认扫描真实 reports / reviews。
11. Phase 2.30a Pilot 仍是内部受控试运行，不等于生产发布或自动决策。
12. Phase 2.30b 只修 alias / session stability，不处理深层召回质量尾项或 production rollout。
13. Phase 2.30b 代码层最小修复与 runbook prompt follow-up 已通过 Codex C 真实终端复验。
14. Phase 2.31 只能规划内部受控试用，不得解释为生产发布。
15. Phase 2.31 已完成 docs-only planning；下一步只能 review / baseline，不得自动进入 rollout 或新功能实现。
16. Nightly Sprint 只能在 Codex A 被启动后执行；`docs/NIGHTLY_CODEX_A_PROMPT.md` 是睡前启动入口，不是系统定时器。
17. Phase 2.32 已完成 docs-only planning；下一步只能 review / baseline，不得自动创建 issue、写 DB、repair 或 rollout。

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
