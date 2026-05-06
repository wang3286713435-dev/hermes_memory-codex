# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.42a MVP Pilot review dry-run report generator Git baseline

- lane：Yellow Lane
- 状态：ready
- 目标：在 Codex B review 通过后，提交 Phase 2.42a MVP Pilot review dry-run report generator Git baseline。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 运行 py_compile、目标 pytest、git diff --check、ignore 检查。
  - selective staging Phase 2.42a 白名单文件。
  - commit、tag、push `origin/main` 与 tag。
- 禁止动作：
  - 不 stage / commit `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
  - 不默认扫描真实 `reports/` 或 `reviews/` 目录。
  - 不生成 production rollout approval。
  - 不授权 repair / cleanup / delete / reindex。
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不运行 API / CLI smoke。
  - 不启动 Data Steward 实现、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。
  - 不修改 retrieval contract 或 memory kernel 主架构。
  - baseline 后不得自动进入下一 phase。
- 完成后：必须停止等待 Codex B review。
- baseline 规则：本 item 已由 Codex B 写入 baseline prompt；仅可执行本次 baseline，不得连跑下一阶段。

## Archived Queue

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
