# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后必须停止等待 Codex B。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### 1. Phase 2.29c docs drift cleanup

- 类型：Green Lane
- 状态：completed
- 目标：清理 TODO 与 Nightly Sprint Queue 中过时的 Phase 2.2 / 2.9 / 2.27b 状态描述。
- 允许：
  - 更新 `docs/TODO.md`。
  - 更新 `docs/NIGHTLY_SPRINT_QUEUE.md`。
  - 更新 `docs/DEV_LOG.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`。
  - 更新 ignored 的 `reports/agent_runs/latest.json`。
- 禁止：
  - 修改业务代码、脚本或测试。
  - 写 DB / `audit_logs`。
  - 执行 repair / backfill / reindex / cleanup / delete。
  - 默认扫描真实 reports / reviews。
  - 进入 rollout。
- 完成后：停止并等待 Codex B 审核是否 baseline。

### 2. Phase 2.29c docs drift cleanup baseline

- 类型：Yellow Lane
- 状态：completed by explicit user command
- 条件：Codex B 审核通过后才执行。
- 默认：不自动执行。
- 目标：提交 Phase 2.29c docs drift cleanup 文档变更并打 tag。
- 禁止：
  - 混入无关 dirty。
  - 修改代码、脚本或测试。
  - 写业务 DB。
  - 执行 repair。
  - 自动进入 release candidate 或 rollout。

### 3. Phase 2.29d release candidate checklist planning

- 类型：Green Lane
- 状态：next
- 目标：规划 MVP freeze candidate 人工复核 / release candidate checklist。
- 允许：
  - 新增规划文档。
  - 同步 TODO / DEV_LOG / ACTIVE / HANDOFF / latest。
- 禁止：
  - 生成 production rollout artifact。
  - 执行 repair executor。
  - 默认扫描真实 reports / reviews。
  - 写 DB / `audit_logs`。
  - 让 facts 替代 retrieval evidence。

## Archived Queue

### Phase 2.27b audit preview / dry-run 最小实现

- 类型：Green Lane
- 状态：completed
- 结果：已实现 sanitized audit payload preview；不写 `audit_logs`，不写 DB。

### Phase 2.27b Git baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：已 baseline；后续进入 Phase 2.27c / 2.27d。

### Phase 2.27c route planning

- 类型：Green Lane
- 状态：completed
- 结果：已规划 report-level sanitized audit opt-in 写入；默认 preview-only。

### Phase 2.29b decision record dry-run baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `f888aa7`，tag `phase-2.29b-freeze-decision-dry-run-baseline`。

## Red Lane

夜间禁止：

1. production rollout。
2. repair executor。
3. DB mutation。
4. default real reports / reviews scan。
5. facts 自动抽取。
6. facts 替代 retrieval evidence 或 final answer。
7. migration。
8. retrieval contract 修改。
9. memory kernel 主架构修改。
10. production cron / scheduler。
