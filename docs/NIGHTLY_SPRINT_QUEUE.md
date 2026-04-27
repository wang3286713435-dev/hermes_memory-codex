# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后必须停止等待 Codex B。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### 1. Phase 2.30a / 2.30b Practical MVP Pilot baseline

- 类型：Yellow Lane
- 状态：next，已由用户与 Codex B 授权。
- 目标：在 Codex C 真实终端复验 `10/12 pass, 2 partial, 0 failed` 后，提交 Phase 2.30a Pilot 文档与 Phase 2.30b alias/session 修复。
- 入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许：
  - 复跑指定轻量测试。
  - 只 stage `NEXT_CODEX_A_PROMPT.md` 白名单内的文件。
  - 双仓库 commit / tag / push。
  - 更新 ignored 的 `reports/agent_runs/latest.json`。
  - 写入 ignored 的 `reports/nightly_runs/<timestamp>.json`。
- 禁止：
  - 混入无关 dirty。
  - stage Hermes 主仓库 `uv.lock`、`PHASE211E...` 或 adapter reload 测试。
  - 修改业务 DB、facts、document_versions、OpenSearch、Qdrant。
  - 执行 repair / backfill / reindex / cleanup / delete。
  - 进入 production rollout。
  - 自动继续 Phase 2.31。
- 完成后：必须停止等待 Codex B / 用户审核。

### 2. Phase 2.31 internal MVP pilot operations planning

- 类型：Green Lane
- 状态：blocked until Phase 2.30 baseline reviewed。
- 目标：规划内部受控 MVP Pilot 试用操作流程、用户反馈表、known risk checklist 与人工复核节奏。
- 默认：不得在 Phase 2.30 baseline 后自动执行。
- 禁止：
  - production rollout。
  - repair executor。
  - DB mutation。
  - 新 API / 新 ingestion / facts 自动抽取。
  - 让 facts 替代 retrieval evidence。

## Archived Queue

### Phase 2.29c docs drift cleanup

- 类型：Green Lane
- 状态：completed
- 结果：已清理 TODO 与 Nightly Sprint Queue 中过时的 Phase 2.2 / 2.9 / 2.27b 状态描述。

### Phase 2.29c docs drift cleanup baseline

- 类型：Yellow Lane
- 状态：completed by explicit user command
- 结果：已 baseline。

### Phase 2.29d release candidate checklist planning

- 类型：Green Lane
- 状态：completed
- 结果：已规划 MVP freeze candidate 人工复核 / release candidate checklist。

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
