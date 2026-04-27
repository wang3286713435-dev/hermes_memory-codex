# Phase Backlog

## 当前优先级

1. Phase 2.27f baseline review：Codex B 审核 archive / review / audit 关联诊断规划 baseline，确认不读取敏感原文、不扩大 DB 写入。
2. Phase 2.27f 最小实现候选：只读 linkage summary，使用 fake manifest / fake review / fake audit event 单元测试和临时目录 smoke。
3. Phase 2.27f implementation prompt：仅在 Codex B 审核通过后生成，不自动进入实现。
4. Phase 2.28c 后续：Nightly Sprint 队列继续保持，但不自动执行 Yellow Lane。

## 后置项

1. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
2. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
3. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
4. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
5. rollout readiness：后置，当前仍不进入生产 rollout。
6. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。

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
