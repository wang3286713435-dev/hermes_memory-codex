# Phase Backlog

## 当前优先级

1. Phase 2.28 Agent Operating Protocol baseline。
2. Phase 2.27b 最小实现：report review audit preview / dry-run。
3. Phase 2.27c 候选：真实写 `audit_logs` 的独立规划。

## 后置项

1. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
2. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
3. report review 写业务 DB：后置，当前只允许 preview / dry-run。
4. rollout readiness：后置，当前仍不进入生产 rollout。

## 永久边界

1. 不擅自修改 retrieval contract。
2. 不擅自修改 memory kernel 主架构。
3. 不执行 destructive repair / delete / cleanup。
4. 不让 facts 自动替代 retrieval evidence。
5. 不创建生产 cron / 定时任务。
6. 每轮开始读取 ACTIVE_PHASE 与 PHASE_BACKLOG。
7. 每轮结束更新 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json。
8. planning / implementation / validation / baseline 分阶段推进。
9. baseline 前默认需要 Codex B 审核，除非用户明确授权。
