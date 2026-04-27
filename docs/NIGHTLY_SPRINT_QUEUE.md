# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.31 Pilot ops + Nightly launcher docs baseline

- lane：Yellow Lane
- preapproved_docs_only_baseline：true
- continue_after_success：true
- 目标：提交 Phase 2.31 内部受控 MVP Pilot 操作规划与 Nightly Sprint 启动入口文档基线。
- 允许动作：
  - 复核 dirty 仅包含本 item 白名单文件。
  - stage / commit / tag / push 白名单文件。
  - 更新 `reports/agent_runs/latest.json` 与 `reports/nightly_runs/<timestamp>.json`。
- 禁止动作：
  - 不写代码。
  - 不改脚本或测试。
  - 不写 DB。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 production rollout。
- 文件白名单：
  - `docs/PHASE231_INTERNAL_MVP_PILOT_OPERATIONS_PLAN.md`
  - `docs/MVP_PILOT_USER_GUIDE.md`
  - `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md`
  - `docs/MVP_PILOT_KNOWN_RISKS.md`
  - `docs/NIGHTLY_CODEX_A_PROMPT.md`
  - `docs/NIGHTLY_SPRINT_PROTOCOL.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/AGENT_OPERATING_PROTOCOL.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
- 建议 commit message：`docs: baseline pilot ops and nightly launcher`
- 建议 tag：`phase-2.31-pilot-ops-nightly-launcher-baseline`
- 继续条件：
  - 仅在 baseline 成功、最终 tracked status 干净、未出现非白名单 dirty 时，可继续 Item 2。
  - 若 push / tag / status 任一失败，必须停止等待 Codex B。

### Item 2：Phase 2.32 MVP Pilot feedback intake planning

- lane：Green Lane
- 目标：规划内部 MVP Pilot 反馈收集、分诊和优先级闭环，让试用问题能转化为下一轮可执行队列。
- 允许动作：
  - 新增 `docs/PHASE232_MVP_PILOT_FEEDBACK_INTAKE_PLAN.md`。
  - 同步更新 `docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/NIGHTLY_SPRINT_QUEUE.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`reports/agent_runs/latest.json`。
  - 仅运行 `git status --short` 与 ignore 检查。
- 必须包含：
  - feedback intake 来源：`MVP_PILOT_FEEDBACK_TEMPLATE.md`、真实 Hermes 输出、人工复核结论。
  - triage 字段：场景、pass/partial/fail、问题类型、业务影响、优先级、是否需要 Codex C、是否需要新 phase。
  - P0/P1/P2/P3 定义。
  - 进入下一阶段的 Go/No-Go 规则。
  - 明确不自动修复、不自动写 DB、不自动创建 Linear / GitHub issue。
- 禁止动作：
  - 不写代码。
  - 不提交 Git。
  - 不创建 production cron / scheduler。
  - 不进入 repair executor 或 rollout。
- 完成后停止，等待 Codex B review。

## Archived Queue

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
