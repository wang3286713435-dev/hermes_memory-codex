# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.44a MVP Pilot Issue Intake Worksheet / Template Artifact

- lane：Green Lane
- 状态：implemented_waiting_codex_b_review
- 目标：为 Day-1 continuation P1/P2 尾项提供人工 worksheet 与 sanitized JSON template，便于后续 dry-run 校验。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_WORKSHEET.md`。
  - 新增 `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_TEMPLATE.json`。
  - 更新 Phase 2.44a 交接文档与 ignored latest 状态。
  - 运行 `git diff --check`、模板 JSON 校验、Phase 2.37a template 输出检查、`latest.json` JSON 校验、ignore 检查与 `git status --short`。
- 禁止动作：
  - 不修改 / stage `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
  - 不修改代码、脚本、测试、migration 或 Hermes 主仓库。
  - 不修改 Hermes_memory retrieval / indexing / facts / version governance / migration / schema。
  - 不默认扫描真实 `reports/` 或 `reviews/` 目录。
  - 不生成真实 MVP Pilot report。
  - 不生成真实 `reports/pilot_issues/*.json` issue record。
  - 不生成 production rollout approval。
  - 不授权 repair / cleanup / delete / reindex。
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不运行新的 API / CLI smoke。
  - 不启动 Data Steward 实现、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。
  - 不修改 retrieval contract 或 memory kernel 主架构。
  - 不自动发起 Codex C。
- 完成后：已停止等待 Codex B review，不得进入 Phase 2.44b。
- baseline 规则：本 item 不 baseline；仅交付 planning dirty。
- 当前结果：docs/template artifact 已完成，新增 worksheet 与 sanitized JSON template；未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Item 2：Phase 2.44a docs-only artifact baseline

- lane：Yellow Lane
- 状态：blocked_until_codex_b_review
- 条件：Codex B review 明确通过 Phase 2.44a artifact 后才允许执行。
- 目标：只提交 Phase 2.44a worksheet / template / handoff 文档 baseline。
- 禁止动作：
  - 不进入 Phase 2.44b。
  - 不生成真实 issue records / Pilot report。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要用户或 Codex B 明确授权。

## Archived Queue

### Phase 2.43d Main Tender Alias / Session Git Baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `d62852b`；Hermes 主仓库 commit `9e8e5667`；tag `phase-2.43d-main-tender-alias-session-baseline`。
- 备注：`@主标书` alias/session Day-1 Pause blocker 已解除；Codex C continuation 结果为 Go，P0 为 0。

### Phase 2.43b MVP Pilot Pre-flight Smoke Prompt Artifact

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `ef2e43f`，tag `phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline`。
- 备注：pre-flight smoke prompt / runbook 已 baseline；Codex C pre-flight 返回 Go，但 Day-1 Pilot 后续触发 `@主标书` alias/session Pause。

### Phase 2.43a MVP Pilot Launch Packet Git Baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `5423497`，tag `phase-2.43a-mvp-pilot-launch-packet-baseline`。
- 备注：只固化 launch packet / operator checklist；未启动真实 Pilot，未生成真实 report，未进入 rollout / repair / Data Steward。

### Phase 2.43 Internal MVP Pilot Launch Candidate Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `5141bb5`，tag `phase-2.43-mvp-pilot-launch-candidate-plan-baseline`。
- 备注：只做 docs-only planning；未启动真实 Pilot，未生成真实 report，未进入 rollout / repair / Data Steward。

### Phase 2.42b MVP Pilot review dry-run input template / runbook

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `edd0e08`，tag `phase-2.42b-mvp-pilot-review-dry-run-template-baseline`。
- 备注：sanitized input template 与 runbook 已 baseline；未生成真实 MVP Pilot report，未进入 rollout / repair。

### Phase 2.37 planning Git baseline

- 类型：Yellow Lane
- 状态：completed / stale archived
- 结果：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
- 备注：旧 Current Queue 已归档；不得再作为夜间当前任务。

### Phase 2.36c tender deep-field diagnostics baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。
- 备注：diagnostics 与 Missing Evidence 语义一致性已收口；deep-field recall 仍 partial。

### Phase 2.35c Git baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `ec77c96`；Hermes 主仓库 commit `ead4e899`；tag `phase-2.35c-alias-session-baseline`。
- 备注：alias/session 修复已收口；deep-field recall 仍 partial。

### Phase 2.35 main tender deep-field retrieval implementation

- 类型：Yellow Lane
- 状态：implemented / validated partial
- 结果：目标测试 `22 passed`；Codex C 复验安全边界通过，但最高投标限价和具体资质等级仍未命中。
- 备注：不 baseline，进入 Phase 2.35b 小修 / 诊断。

### Phase 2.34 compare false-positive baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `789ed22`；Hermes 主仓库 commit `5de49bf5`；tag `phase-2.34-compare-contamination-baseline`。
- 备注：已通过 Codex C 复验；未进入 rollout。

### Phase 2.33 MVP Pilot Day-1 run sheet baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；未写代码、未进入 rollout。

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
