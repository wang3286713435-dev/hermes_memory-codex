# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.50 Internal MVP Daily Review Loop Runbook Artifact

- lane：Green Lane
- 状态：codex_b_review_passed_baseline_in_progress
- 目标：把内部受控 MVP 每日 operator 流程串成 runbook artifact，连接 run query、ignored run record、review dry-run 与 issue intake。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE250_INTERNAL_MVP_DAILY_REVIEW_LOOP_PLAN.md`。
  - 更新 Phase 2.50 交接文档与 ignored latest 状态。
  - 运行 docs / JSON / ignore 轻量检查。
- 禁止动作：
  - 不写业务功能代码、scripts 或 tests。
  - 不读取真实 internal MVP run record。
  - 不运行真实 Pilot。
  - 不运行 API / CLI smoke。
  - 不启动 / 停止服务。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不进入 rollout、repair 或 Data Steward 实现。
  - 不 stage / commit / tag / push。
- 完成后：执行 Phase 2.50 docs-only Git baseline 后停下。
- baseline 规则：Yellow Lane，默认夜间不可自动执行；需要 Codex B 明确授权。
- 前置状态：Phase 2.49 Git baseline 已完成，commit `f23f248`，tag `phase-2.49-internal-mvp-run-record-review-baseline`。

### Item 1：Phase 2.46 Mac mini Day-0 Real-machine Setup Planning

- lane：Green Lane
- 状态：completed_baseline
- 目标：规划 Mac mini 到货后的 Day-0 real-machine setup / internal MVP application prep；本轮不执行真实部署、不运行 health-check runner、不运行 API / CLI。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE246_MAC_MINI_DAY0_SETUP_PLAN.md`。
  - 更新 Phase 2.46 交接文档与 ignored latest 状态。
  - 运行 `git diff --check`、latest JSON 校验与 `git status --short`。
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
- 完成后：Codex B review 已通过；下一步只允许执行 Item 2 docs-only baseline，不得进入 Phase 2.46a。
- baseline 规则：本 item 不 baseline；baseline 由 Item 2 执行。
- 当前结果：Git baseline 已完成，commit `13e2206`，tag `phase-2.46-mac-mini-day0-setup-plan-baseline`。

### Item 2：Phase 2.46 Day-0 setup planning baseline

- lane：Yellow Lane
- 状态：completed
- 条件：Codex B review 已通过；Codex A 必须严格按 `docs/NEXT_CODEX_A_PROMPT.md` 白名单执行。
- 目标：只提交 Phase 2.46 planning / handoff 文档 baseline。
- 禁止动作：
  - 不进入 Phase 2.46a。
  - 不执行真实部署。
  - 不新增 deployment script。
  - 不运行真实 API / CLI smoke，除非后续 prompt 明确授权。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要 Codex B 明确授权。

### Item 3：Phase 2.46a Day-0 setup checklist artifact

- lane：Green Lane
- 状态：completed_codex_b_review_passed
- 目标：新增可人工填写的 Mac mini Day-0 setup checklist artifact。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/MAC_MINI_DAY0_SETUP_CHECKLIST.md`。
  - 更新 Phase 2.46a 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不执行真实 Mac mini setup。
  - 不运行 health-check runner。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不新增 deployment script / scheduler / cron。
  - 不进入 rollout 或 Data Steward 实现。
  - 不 stage / commit / tag / push。
- 完成后：Codex B review 已通过；下一步只允许执行 Item 4 docs-only baseline，不得进入 Phase 2.46b。
- 当前结果：Codex A 已完成 `docs/MAC_MINI_DAY0_SETUP_CHECKLIST.md`；Codex B review 已通过。

### Item 4：Phase 2.46a Day-0 setup checklist artifact baseline

- lane：Yellow Lane
- 状态：completed
- 条件：Codex B review 已通过；Codex A 必须严格按 `docs/NEXT_CODEX_A_PROMPT.md` 白名单执行。
- 目标：只提交 Phase 2.46a checklist artifact / handoff 文档 baseline。
- 禁止动作：
  - 不进入 Phase 2.46b。
  - 不执行真实 setup。
  - 不运行 health-check runner。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要 Codex B 明确授权。

### Item 5：Phase 2.46b human-run evidence attachment planning

- lane：Green Lane
- 状态：completed_codex_b_review_passed
- 目标：规划 Mac mini 人工运行后的证据挂接 / 归档 / 引用方式。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE246B_MAC_MINI_EVIDENCE_ATTACHMENT_PLAN.md`。
  - 更新 Phase 2.46b 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不生成真实 health-check report、deployment record 或 smoke report。
  - 不执行真实 Mac mini setup。
  - 不运行 health-check runner。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不新增 deployment script / scheduler / cron。
  - 不进入 rollout 或 Data Steward 实现。
  - 不 stage / commit / tag / push。
- 完成后：Codex B review 已通过；下一步只允许执行 Item 6 docs-only baseline，不得进入 Phase 2.46c。
- 当前结果：Codex A 已完成 `docs/PHASE246B_MAC_MINI_EVIDENCE_ATTACHMENT_PLAN.md`；Codex B review 已通过。

### Item 6：Phase 2.46b evidence attachment planning baseline

- lane：Yellow Lane
- 状态：completed
- 条件：Codex B review 已通过；Codex A 必须严格按 `docs/NEXT_CODEX_A_PROMPT.md` 白名单执行。
- 目标：只提交 Phase 2.46b evidence attachment planning / handoff 文档 baseline。
- 禁止动作：
  - 不进入 Phase 2.46c。
  - 不生成真实 evidence。
  - 不执行真实 setup。
  - 不运行 health-check runner。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要 Codex B 明确授权。

### Item 7：Phase 2.46c Codex C local MVP smoke prompt artifact

- lane：Green Lane
- 状态：completed_codex_b_review_passed
- 目标：新增给 Codex C 的 Mac mini local MVP smoke prompt artifact。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md`。
  - 更新 Phase 2.46c 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不运行真实 smoke。
  - 不启动服务。
  - 不运行 health-check runner。
  - 不生成真实 evidence / deployment record / smoke report。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不新增 deployment script / scheduler / cron。
  - 不进入 rollout 或 Data Steward 实现。
  - 不 stage / commit / tag / push。
- 完成后：Codex B review 已通过；下一步只允许执行 Item 8 docs-only baseline，不得发起 Codex C。
- 当前结果：Codex A 已完成 `docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md`；Codex B review 已通过。

### Item 8：Phase 2.46c Codex C smoke prompt artifact baseline

- lane：Yellow Lane
- 状态：completed
- 条件：Codex B review 已通过；Codex A 必须严格按 `docs/NEXT_CODEX_A_PROMPT.md` 白名单执行。
- 目标：只提交 Phase 2.46c prompt artifact / handoff 文档 baseline。
- 禁止动作：
  - 不实际运行 Codex C smoke。
  - 不启动服务。
  - 不生成真实 evidence / deployment record / smoke report。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：默认夜间不可自动执行；需要 Codex B 明确授权。

### Item 9：Phase 2.46d local MVP smoke result intake baseline

- lane：Yellow Lane
- 状态：completed
- 条件：Codex C smoke returned Go; Codex B reviewed and provided sanitized result summary.
- 目标：记录 sanitized Mac mini local MVP smoke result，并做 docs-only Git baseline。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE246D_MAC_MINI_LOCAL_MVP_SMOKE_RESULT.md`。
  - 更新 Phase 2.46d 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
  - 按白名单做 docs-only baseline。
- 禁止动作：
  - 不重跑 smoke。
  - 不启动服务。
  - 不生成真实 evidence / deployment record / smoke report。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 rollout / Data Steward。
- baseline 规则：本轮仅允许提交 sanitized result 文档与交接文件。
- 当前结果：Git baseline 已完成，commit `255c2e97fa6d644c2d83655e7ac919c8401f54f2`，tag `phase-2.46d-mac-mini-local-mvp-smoke-result-baseline`。

### Item 10：Phase 2.47 internal controlled MVP operating loop planning

- lane：Green Lane
- 状态：completed_codex_b_reviewed
- 目标：把 Mac mini smoke `Go` 结果转化为内部受控 MVP 的运营闭环计划。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md`。
  - 更新 Phase 2.47 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不运行真实 smoke。
  - 不启动服务。
  - 不运行 health-check runner。
  - 不生成真实 evidence / deployment record / pilot run record。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 production rollout 或 Data Steward 实现。
  - 不 stage / commit / tag / push，除非后续 prompt 明确授权 baseline。
- 完成后：Codex B review 已通过；下一步执行 Item 11 daily operator checklist artifact。
- baseline 规则：按低人工干预策略，docs-only planning 可先不单独 baseline；形成 reusable checklist / template 后再由 Codex B 决定是否合并 baseline。

### Item 11：Phase 2.47a daily operator checklist artifact

- lane：Green Lane
- 状态：completed_codex_b_reviewed
- 目标：将 Phase 2.47 operating loop 转成每日 operator checklist artifact。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md`。
  - 更新 Phase 2.47a 交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不执行真实 operation。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不进入 production rollout。
- 完成后：Codex B review 已通过；下一步执行 Item 12 local ignored pilot run record template。
- baseline 规则：默认不单独 baseline；由 Codex B 判断是否与 Phase 2.47 planning 合并 baseline。

### Item 12：Phase 2.47b local ignored pilot run record template

- lane：Green Lane
- 状态：completed_baseline
- 目标：新增本地 ignored pilot run record template / storage policy。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`。
  - 新增 `reports/internal_mvp_runs/.gitignore` 与 `reports/internal_mvp_runs/README.md`。
  - 更新 Phase 2.47b 交接文档与 ignored latest 状态。
  - 运行 docs-only / ignore 校验。
- 禁止动作：
  - 不生成真实 pilot run record。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不进入 production rollout。
- 完成后：Phase 2.47 / 2.47a / 2.47b combined docs baseline 已完成；用户可使用 checklist + run record template 开始 Day-0 / Day-1。
- baseline 规则：已 baseline，commit `bfe7981`，tag `phase-2.47-internal-mvp-operating-artifacts-baseline`。

### Item 13：Phase 2.47 combined docs artifact baseline

- lane：Yellow Lane
- 状态：completed
- 目标：合并提交 Phase 2.47 planning、2.47a checklist、2.47b run record template 与交接文档。
- 禁止动作：
  - 不进入 Phase 2.48。
  - 不运行 smoke。
  - 不生成真实 run record。
  - 不写 DB / facts / document_versions / OpenSearch / Qdrant。
  - 不进入 production rollout。
- baseline 规则：已完成，commit `bfe7981`，tag `phase-2.47-internal-mvp-operating-artifacts-baseline`。

### Item 14：Phase 2.48 P2 display tails triage planning

- lane：Green Lane
- 状态：completed_waiting_codex_b_review
- 目标：规划 Excel citation display tail 与 meeting transcript boundary flag tail 的 P2 分诊、候选小修和验收口径。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE248_P2_DISPLAY_TAILS_TRIAGE_PLAN.md`。
  - 更新 Phase 2.48 交接文档与 ignored latest 状态。
  - 运行 docs-only / ignore 校验。
- 禁止动作：
  - 不运行 smoke。
  - 不启动服务。
  - 不生成真实 run record。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 production rollout。
- 完成后：等待 Codex B review；通过后选择 Item 15 或 Item 16。
- baseline 规则：本 item 默认不 baseline；需 Codex B 明确授权。

### Item 15：Phase 2.48a Excel citation display polish

- lane：Green Lane
- 状态：completed_waiting_codex_b_review
- 目标：仅在 renderer / citation summary 层补 Excel citation fallback 展示，例如 `row_range_fallback=true`；不改 parser。
- 禁止动作：
  - 不改 retrieval contract。
  - 不改 memory kernel 主架构。
  - 不改 ingestion / parser / indexing。
  - 不执行 repair / backfill / reindex。
  - 不进入 rollout。
- 完成后：已完成 bounded implementation，等待 Codex B review；必要时由 Codex C targeted smoke。

### Item 16：Phase 2.48b Meeting transcript boundary display polish

- lane：Green Lane
- 状态：completed_codex_b_review_passed
- 目标：仅在 context / trace display 层稳定显示 `transcript_as_fact=false` 或等价 boundary statement。
- 禁止动作：
  - 不改 meeting ingestion contract。
  - 不改 retrieval contract。
  - 不改 memory kernel 主架构。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不进入 rollout。
- 完成后：已完成 bounded implementation，等待 Codex B review；必要时由 Codex C targeted smoke。

### Item 17：Phase 2.48c Codex C targeted smoke prompt

- lane：Green Lane
- 状态：completed_pass
- 目标：为 Codex C 准备 targeted smoke，验证 Excel citation display fallback 与 meeting transcript boundary display。
- 禁止动作：
  - 不重跑 full Day-1，除非 targeted smoke 出现 P1/P0。
  - 不启动 production rollout。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete。
- 完成后：停止等待 Codex B review；由 Codex B 决定是否 baseline。

## Archived Queue

### Phase 2.45e Sanitized Deployment Record Template Artifact

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `8bd7616`，tag `phase-2.45e-deployment-record-template-baseline`。
- 备注：deployment record template 已 baseline；未生成真实 deployment record、未执行真实部署、未运行 health-check runner、未运行 API / CLI smoke、未写 DB / facts / document_versions / OpenSearch / Qdrant。

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

### Item 18：Phase 2.48 combined Git baseline

- lane：Yellow Lane
- 状态：ready_for_codex_a_baseline
- 目标：选择性提交 Phase 2.48 triage、2.48a、2.48b、2.48c 交接与测试结果。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 禁止动作：不进入 Phase 2.49，不运行新 smoke，不写 DB / index，不进入 rollout。
- baseline 规则：Codex B 已授权；必须 selective staging。
