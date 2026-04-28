# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Waiting：Phase 2.34 compare false-positive Git baseline

- lane：Yellow Lane
- 目标：提交 Phase 2.34 compare false-positive 修复与复验文档基线。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 仅 stage `docs/NEXT_CODEX_A_PROMPT.md` 白名单中的双仓文件。
  - 提交 Hermes 主仓库当前可写远端 `backup2` 与 Hermes_memory `origin/main`。
  - 打 tag `phase-2.34-compare-contamination-baseline`。
- 禁止动作：
  - 不扩大到主标书深层字段召回实现。
  - 不扩大到 latency 优化实现。
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 production rollout。
  - 不强推。
- 默认：需要用户明确执行；baseline 后停止等待 Codex B。

## Archived Queue

### Phase 2.34 compare false-positive fix

- 类型：Yellow Lane
- 状态：validated
- 结果：最终 evidence 在 compare 文档集合内时输出 `third_document_mixed=false`；真实第三文件 evidence 仍保留污染标记。
- 备注：Codex C 真实终端复验已通过；等待 Git baseline。

### Phase 2.33 MVP Pilot Day-1 run sheet baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；未写代码、未进入 rollout。

### Phase 2.33 MVP Pilot Day-1 execution packet planning

- 类型：Green Lane
- 状态：completed
- 结果：已新增 `docs/MVP_PILOT_DAY1_RUN_SHEET.md`，覆盖 Day-1 目标、角色、时间表、最小 query set、输出保存字段与 Go / Pause。
- 备注：docs-only planning；未写代码、未提交 Git、未进入 rollout。

### Phase 2.32 MVP Pilot feedback intake planning baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `160ce62`，tag `phase-2.32-feedback-intake-plan-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；未写代码、未进入 rollout。

### Phase 2.31 Pilot ops + Nightly launcher docs baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `184533a`，tag `phase-2.31-pilot-ops-nightly-launcher-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；因 `continue_after_success=true`，成功后继续执行了 Phase 2.32 Green Lane planning。

### Phase 2.30a / 2.30b Practical MVP Pilot baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `15e05d4`，Hermes 主仓库 commit `13097693`，tag `phase-2.30b-practical-mvp-pilot-baseline`。
- 备注：完成后已按 Yellow Lane 规则停止，未自动进入 Phase 2.31。

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
