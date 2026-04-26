# Phase Backlog

## 当前优先级

1. Phase 2.27b Git baseline：sanitized audit payload preview / dry-run。
2. Phase 2.27c 候选：真实写 `audit_logs` 的独立规划。
3. Phase 2.28c 后续：Nightly Sprint 队列继续保持，但不自动执行 Yellow Lane。

## 后置项

1. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
2. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
3. report review 写业务 DB：后置，当前只允许 sanitized preview / dry-run。
4. rollout readiness：后置，当前仍不进入生产 rollout。
5. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。

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
