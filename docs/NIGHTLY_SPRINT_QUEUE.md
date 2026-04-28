# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

当前无可自动执行的下一项。

Phase 2.31 baseline 与 Phase 2.32 planning 已完成，等待 Codex B review。不得自动继续进入 baseline、rollout 或新功能实现。

## Archived Queue

### Phase 2.32 MVP Pilot feedback intake planning

- 类型：Green Lane
- 状态：completed
- 结果：已规划 MVP Pilot feedback intake / triage loop，包含来源、字段、P0/P1/P2/P3、Go / No-Go 与非目标。
- 备注：本轮 docs-only，未写代码、未提交 Git、未进入 rollout。

### Phase 2.31 Pilot ops + Nightly launcher docs baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `184533a`，tag `phase-2.31-pilot-ops-nightly-launcher-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；因 `continue_after_success=true`，成功后继续执行了 Phase 2.32 Green Lane planning。

### Phase 2.31 internal MVP pilot operations planning

- 类型：Green Lane
- 状态：completed
- 结果：已新增内部受控 MVP Pilot 操作规划、使用指南、反馈模板与 known risks 文档。
- 备注：本轮 docs-only，未写代码、未运行测试、未进入 rollout。

### Phase 2.30a / 2.30b Practical MVP Pilot baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `15e05d4`，Hermes 主仓库 commit `13097693`，tag `phase-2.30b-practical-mvp-pilot-baseline`。
- 备注：完成后已按 Yellow Lane 规则停止，未自动进入 Phase 2.31。

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
