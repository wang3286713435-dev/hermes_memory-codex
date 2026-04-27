# Phase Backlog

## 当前优先级

1. Phase 2.29b readiness freeze baseline decision planning：基于 freeze report 判定是否进入 MVP candidate。
2. Phase 2.29b 最小实现候选：只生成 decision record / no-go reason，不进入 rollout。
3. linkage summary 继续仅作为 Phase 2.29 人工验收项；如需代码接入，只能显式参数化读取 summary。

## 后置项

1. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
2. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
3. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
4. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
5. rollout readiness：后置，当前仍不进入生产 rollout。
6. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。
7. repair executor：继续后置，除非 freeze 报告与人工评审明确批准。

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
