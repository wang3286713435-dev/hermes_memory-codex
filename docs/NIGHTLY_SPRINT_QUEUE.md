# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.45e Sanitized Deployment Record Template Artifact

- lane：Green Lane
- 状态：completed_codex_b_review_passed
- 目标：新增 sanitized deployment record template 与 ignored local storage policy；本轮不执行真实部署、不运行 health-check runner、不运行 API / CLI。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/MAC_MINI_DEPLOYMENT_RECORD_TEMPLATE.md`。
  - 新增 `reports/deployment_records/.gitignore` 与 `reports/deployment_records/README.md`。
  - 更新 Phase 2.45e 交接文档与 ignored latest 状态。
  - 运行 `git diff --check`、deployment record ignore 检查、latest JSON 校验与 `git status --short`。
- 禁止动作：
  - 不修改 / stage `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
  - 不修改 scripts / tests / app / migrations / Hermes 主仓库。
  - 不运行 Phase 2.45c runner。
  - 不执行真实 Mac mini 部署。
  - 不新增 deployment script。
  - 不运行真实 API / CLI smoke。
  - 不自动 restart / migrate / repair / backfill / reindex / cleanup / delete。
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不启动 Data Steward 实现、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。
  - 不修改 retrieval contract 或 memory kernel 主架构。
  - 不自动发起 Codex C。
- 完成后：已通过 Codex B review；下一步只能进入 Item 2 docs-only baseline，不得进入 Phase 2.46。
- baseline 规则：本 item 不 baseline；仅交付 template artifact dirty。
- 当前结果：Codex A 已新增 sanitized template 与 `reports/deployment_records/` ignore / README 策略；目标验证通过，Codex B review 通过。

### Item 2：Phase 2.45e template artifact baseline

- lane：Yellow Lane
- 状态：ready_for_codex_a_baseline
- 条件：Codex B review 已通过；Codex A 可按 `docs/NEXT_CODEX_A_PROMPT.md` 做 selective docs-only baseline。
- 目标：只提交 Phase 2.45e template artifact / handoff 文档 baseline。
- 禁止动作：
  - 不进入 Phase 2.46。
  - 不执行真实部署。
  - 不新增 deployment script。
  - 不运行真实 API / CLI smoke，除非后续 prompt 明确授权。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要 Codex B 明确授权。

## Archived Queue

### Phase 2.45d Mac mini Real-machine Deployment Record Planning

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `e12f82a`，tag `phase-2.45d-deployment-record-plan-baseline`。
- 备注：deployment record planning 已 baseline；未执行真实部署、未运行 health-check runner、未运行 API / CLI smoke、未写 DB / facts / document_versions / OpenSearch / Qdrant。

### Phase 2.45c Read-only Health-check Script Baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `fbad94f`，tag `phase-2.45c-health-check-dry-run-baseline`。
- 备注：health-check dry-run runner 已 baseline；未运行真实 API / CLI smoke、未执行真实部署、未写 DB / facts / document_versions / OpenSearch / Qdrant。

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
