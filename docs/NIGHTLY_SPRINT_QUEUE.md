# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.54b File Steward UX Runtime Display Integration Baseline

- lane：Yellow Lane
- 状态：codex_b_review_passed_waiting_selective_baseline
- 目标：Phase 2.54b display integration 已通过 review；下一步只做 selective Git baseline。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - Hermes 主仓只 stage `agent/memory_kernel/context_builder.py` 与 `tests/agent/test_session_document_scope.py`。
  - Hermes_memory 只 stage Phase 2.54b 交接文档白名单。
  - 运行 py_compile、target pytest、docs 校验与 selective staged diff 复核。
- 禁止动作：
  - 不真实上传文件。
  - 不调用真实 Hermes_memory API。
  - 不读取真实文件内容。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不修改 retrieval contract 或 memory kernel 主架构。
  - 不修改 `context_builder.py`、`kernel.py`、`orchestrator.py`、`hermes_memory_adapter.py`。
  - 不进入 Data Steward / BIM / NAS / TB 文件池。
  - 不执行 repair / backfill / reindex / cleanup / delete / migration。
  - 不做 production rollout。
  - 不进入 Phase 2.54c 或 Phase 2.53d。
- 当前结果：Codex B review 通过，目标测试 `73 passed`；未真实 upload、未调用 API、未写 DB / index。
- 完成后：baseline 后停止等待 Codex B review；不得自动进入真实 upload smoke。

### Current Item：Phase 2.53a Natural Language File Import Parser / Dry-run Planner

- lane：Yellow Lane
- 状态：completed_baseline
- 目标：Phase 2.53a selective Git baseline 已完成；不接真实 upload。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 Hermes 主仓 `agent/memory_kernel/natural_file_import.py`。
  - 新增 Hermes 主仓 `tests/agent/test_natural_file_import.py`。
  - 更新交接文档与 ignored latest 状态。
  - 运行 py_compile 与目标测试 / direct assertion fallback。
- 禁止动作：
  - 不上传真实文件。
  - 不调用真实 Hermes_memory API。
  - 不修改 adapter / kernel / orchestrator / context_builder / session scope。
  - 不递归扫描目录、NAS、网盘或 TB 级 BIM 文件池。
  - 不生成真实 evidence pack。
  - 不读取真实 reports / run records。
  - 不执行真实 Mac Mini deployment。
  - 不启动 / 停止服务。
  - 不运行 API / CLI smoke。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete / migration。
  - 不进入 production rollout 或 Data Steward。
  - 不 stage / commit / tag / push。
- 完成后：baseline 后停止等待 Codex B review；不得自动进入 Phase 2.53b adapter / kernel integration。
- 前置状态：Phase 2.53 baseline 已完成，commit `f92a342`，tag `phase-2.53-natural-language-file-import-plan-baseline`。
- 当前结果：Codex B review 已通过，已写入 selective baseline prompt；主仓目标测试 `10 passed`；未接真实 upload。

### Next Item：Phase 2.53b Natural Language File Import Adapter / Kernel Integration Planning

- lane：Yellow Lane
- 状态：codex_b_review_passed_waiting_docs_baseline
- 目标：Phase 2.53b planning 已通过 review；下一步只做 docs-only baseline。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 新增 `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`。
  - 更新交接文档与 ignored latest 状态。
  - 运行 docs-only 校验。
- 禁止动作：
  - 不写功能代码。
  - 不修改 Hermes 主仓 `agent/`、`tests/`、`run_agent.py`。
  - 不新增 upload adapter / HTTP client。
  - 不调用真实 Hermes_memory API。
  - 不上传文件。
  - 不读取真实文件内容。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete / migration。
  - 不进入 Data Steward / BIM TB 级管理。
  - 不 stage / commit / tag / push。
- 完成后：baseline 后停止等待 Codex B review；不得自动进入 Phase 2.53c。

### Candidate Next Item：Phase 2.53c Mocked Natural Import Adapter / Kernel Integration

- lane：Green Lane
- 状态：implemented_waiting_codex_b_review
- 目标：使用 mocked upload adapter 验证 parser preflight、alias seed 和 import diagnostics 分离；实现已完成，等待 Codex B review。
- 任务入口：待 Codex B 写入 `docs/NEXT_CODEX_A_PROMPT.md`。
- 允许动作：
  - 仅使用 fake / mocked adapter。
  - 增加 unit tests / direct assertions。
  - 不调用真实 Hermes_memory API。
- 禁止动作：
  - 不上传真实文件。
  - 不读取真实文件内容。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不执行 repair / backfill / reindex / cleanup / delete / migration。
  - 不进入 Data Steward / BIM TB 级管理。
- 完成后：等待 Codex B review；真实 upload smoke 仍必须后置 Phase 2.53d 并由用户显式授权。

### Candidate Next Item：Phase 2.54a File Steward UX

- lane：Green Lane
- 状态：candidate_after_codex_b_review
- 目标：规划或实现 file discovery first、active document continuation、alias failure helper、file-answer metadata display。
- 任务入口：待 Codex B 写入 `docs/NEXT_CODEX_A_PROMPT.md`。
- 禁止动作：
  - 不真实上传文件。
  - 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
  - 不放松 citation / evidence / Missing Evidence 边界。
  - 不进入 Data Steward / BIM / NAS / TB 文件池。

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
