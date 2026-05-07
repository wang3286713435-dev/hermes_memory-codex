# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.45c health-check dry-run implementation baseline

- lane：Yellow Lane
- 状态：codex_b_approved_next_prompt_ready
- 目标：只提交 Phase 2.45c 脚本 / 测试 / 文档 baseline；本轮不新增功能、不运行真实 API / CLI。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 复跑 py_compile、目标 pytest、默认 `--json` dry-run、json.tool、git diff check。
  - 只 stage Phase 2.45c 白名单文件。
  - commit / tag / push Phase 2.45c baseline。
  - 更新 ignored latest 状态。
- 禁止动作：
  - 不修改 / stage `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
  - 不修改 app / migrations / Hermes 主仓库。
  - 不执行真实 Mac mini 部署。
  - 不新增 deployment script。
  - 不运行真实 API / CLI smoke。
  - 不自动 restart / migrate / repair / backfill / reindex / cleanup / delete。
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不启动 Data Steward 实现、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。
  - 不修改 retrieval contract 或 memory kernel 主架构。
  - 不自动发起 Codex C。
- 完成后：停止等待 Codex B baseline confirmation，不得进入 Phase 2.45d。
- baseline 规则：允许 Codex A 执行一次 Git baseline；完成 commit / tag / push 后必须停止。
- 当前结果：等待 Codex A 执行 baseline。

### Item 2：Phase 2.45d Mac mini real-machine deployment record planning

- lane：Green Lane
- 状态：blocked_until_phase_2_45c_baseline_and_user_authorization
- 条件：Phase 2.45c baseline 完成，且用户明确授权后才允许写下一步 prompt。
- 目标：规划 Mac mini real-machine deployment record；默认不执行部署。
- 禁止动作：
  - 不进入 Phase 2.45d。
  - 不执行真实部署。
  - 不新增 deployment script。
  - 不运行真实 API / CLI smoke，除非后续 prompt 明确授权。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：不适用；当前 blocked。

## Archived Queue

### Phase 2.45c Read-only Health-check Script Minimal Implementation

- 类型：Green Lane
- 状态：completed_codex_b_review_passed
- 结果：implementation dirty 已完成，Codex B review 通过，等待 Git baseline。
- 备注：新增只读 runner 与测试；未运行真实 API / CLI smoke，未执行真实部署，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.45b Health-check / Deploy-smoke Dry-run Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `d70497c`，tag `phase-2.45b-health-check-dry-run-plan-baseline`。
- 备注：health-check / deploy-smoke dry-run planning 已 baseline；未新增 health-check script、未运行真实 API / CLI、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.45a Mac mini MVP Deployment Runbook Artifact

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `585d534`，tag `phase-2.45a-mac-mini-deployment-runbook-baseline`。
- 备注：Mac mini deployment runbook artifact 已 baseline；未执行真实部署、未新增 deployment script、未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.45 Mac mini MVP Server Deployment Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `fa6aff4`，tag `phase-2.45-mac-mini-mvp-server-plan-baseline`。
- 备注：Mac mini MVP server deployment planning 已 baseline；未执行真实部署、未新增 deployment script、未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.44d Explicit Local Issue Dry-run Route Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `dcdb7b4`，tag `phase-2.44d-explicit-local-issue-dry-run-plan-baseline`。
- 备注：explicit ignored local issue input dry-run route planning 已 baseline；未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.44c Fake-data Sanitized Issue Intake Dry-run Artifact

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `cb29ed4`，tag `phase-2.44c-fake-issue-intake-dry-run-baseline`。
- 备注：fake-data issue intake dry-run artifact 已 baseline；未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.44b Sanitized Issue Intake Dry-run / Recorder Workflow Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `0241c4d`，tag `phase-2.44b-sanitized-issue-intake-dry-run-plan-baseline`。
- 备注：sanitized issue intake dry-run / recorder workflow planning 已 baseline；未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.44a MVP Pilot Issue Intake Worksheet / Template Artifact

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `14c5640`，tag `phase-2.44a-pilot-issue-intake-worksheet-baseline`。
- 备注：worksheet 与 sanitized JSON template 已 baseline；未生成真实 issue records / Pilot report，未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.43d Main Tender Alias / Session Git Baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `d62852b`；Hermes 主仓库 commit `9e8e5667`；tag `phase-2.43d-main-tender-alias-session-baseline`。
- 备注：`@主标书` alias/session Day-1 Pause blocker 已解除；Codex C continuation 结果为 Go，P0 为 0。
