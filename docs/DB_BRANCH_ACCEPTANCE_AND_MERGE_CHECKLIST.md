# DB Branch Acceptance And Merge Checklist

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：历史 checklist；当前 closeout 以 `docs/DB_BRANCH_CLOSEOUT_AND_MERGE_READINESS.md` 为准

> 2026-05-11 closeout note：本文件创建于 DB-1 baseline 前，保留为历史验收约束。当前 DB 支线已推进至 DB-4D readonly local live smoke interface baseline；最终合回主线判断请优先查看 `docs/DB_BRANCH_CLOSEOUT_AND_MERGE_READINESS.md`。

## 1. 目的

本 checklist 用于 DB 分支 baseline / review / 合回主线前检查。它不启动 DB-2 实现，不授权真实 MySQL / NAS / REST / index 写入，也不改变现有 retrieval contract 或 memory kernel 主架构。

当前允许范围：

1. DB-1 fake View fixtures。
2. DB-1 read-only fake adapter。
3. DB-1 contract tests。
4. DB-2 / DB-3 验收条件文档化。

当前禁止范围：

1. DB-2 `external_asset_catalog` mirror 实现。
2. DB migration。
3. 真实 MySQL 连接。
4. 真实 NAS 扫描，包括 `/Volumes/zyzn/卓羽智能项目`。
5. 真实 REST 写入或平台审计写入。
6. 写 `documents` / `chunks`。
7. 写 OpenSearch / Qdrant。
8. 正文解析、全量 BIM / CAD / 点云解析。
9. retrieval contract 或 memory kernel 主架构修改。
10. production scheduler / rollout。

## 2. 全局 Baseline Gate

任何 DB baseline 前必须满足：

1. `git status --short` 已复核，dirty 范围只包含本阶段白名单文件。
2. 当前分支仍为 `codex/data-steward-db0-contract`。
3. 所有新增 DB / NAS / Data Steward 能力默认 feature flag off。
4. fake adapter 与未来真实平台 client 的边界清晰。
5. catalog-only evidence 与 document content evidence 分层清晰。
6. `permission_tags` 缺失默认 deny。
7. 不依赖平台底表，只依赖稳定 View / 后续 REST contract。
8. 不把 MCP 工具层当作 memory kernel 主证据链替代品。
9. Codex B review 通过后才允许 baseline。
10. 不自动进入下一 DB phase。

## 3. DB-1 Acceptance

DB-1 目标是 fake View Adapter。DB-1 baseline 前必须满足：

1. fake JSON fixtures 覆盖四个 View：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
2. fixtures 覆盖三个项目：
   - `101-C塔`
   - `98-深圳口岸项目`
   - `99-丰图既有建模项目`
3. fake adapter 只读，不连接真实 MySQL / NAS / REST。
4. fake adapter 支持 pagination / `limit` / cursor。
5. fake adapter 绑定并返回 `contract_version`。
6. fake adapter 生成并校验 `asset_uid = source_system + ":" + source_id`。
7. `permission_tags` 缺失时返回 deny，不进入 prompt-ready evidence。
8. stale / moved / missing / checksum missing 状态被 fixture 和测试覆盖。
9. 异常状态保持 catalog-only / metadata-only，不伪造正文 evidence。
10. `AuditEventView` checkpoint 优先使用 `event_id`，并有 contract test 覆盖。
11. 测试不需要外部服务，不触碰真实企业 DB / NAS。
12. 不写 `documents` / `chunks` / OpenSearch / Qdrant。
13. 不做正文解析。
14. 不改 retrieval contract。
15. 不改 memory kernel 主架构。

DB-1 required checks：

```bash
uv run --extra dev pytest tests/test_data_steward_fake_adapter.py -q
uv run --extra dev ruff check app/services/asset_catalog tests/test_data_steward_fake_adapter.py app/core/config.py
git diff --check
```

DB-1 baseline 白名单：

1. `app/core/config.py`
2. `app/services/asset_catalog/**`
3. `tests/test_data_steward_fake_adapter.py`
4. DB 分支交接 / 状态文档。

DB-1 不允许纳入：

1. migrations。
2. `app/models/**` DB schema 变更。
3. `app/services/retrieval/**` retrieval contract 变更。
4. `app/memory_kernel/**` 主架构变更。
5. 真实报告、真实 NAS scan output、真实平台 credential 或 audit output。

## 4. DB-2 Acceptance

DB-2 目标是 Asset Catalog Mirror。本文只定义未来验收条件；当前不得进入 DB-2 实现。

DB-2 进入条件：

1. DB-1 已 baseline。
2. 用户显式授权进入 DB-2。
3. Codex B review 通过 DB-2 implementation prompt。
4. 明确 DB-2 是否允许 migration；未授权前不得写 migration。
5. 仍不连接真实 MySQL / NAS / REST。

DB-2 未来实现完成条件：

1. mirror 与现有 `documents` / `chunks` 完全分离。
2. catalog-only 资产不得写入 `documents` / `chunks`。
3. catalog-only 资产不得写入 OpenSearch / Qdrant。
4. mirror 记录保留 `source_system`、`source_id`、`asset_uid`、`source_view`、`contract_version`。
5. mirror 记录保留 `project_id`、`project_scope`、`permission_tags`。
6. `permission_tags` 缺失默认 deny。
7. checkpoint 优先使用 `AuditEventView.event_id`。
8. `updated_at` 只能作为辅助字段，不作为唯一增量依据。
9. moved / stale / missing / checksum missing 状态可被保存和查询。
10. sync preview 可输出将要 upsert / skip / deny 的结果。
11. dry-run 默认不写 DB。
12. 如 future phase 允许写本地 mirror，只能写 Hermes_memory 自有 catalog mirror，不写平台 DB。
13. fixture DB / temporary DB tests 覆盖 upsert 幂等、checkpoint、permission deny、异常状态。
14. 不做 selective indexing。
15. 不进入 DB-3 catalog retrieval。

DB-2 合回主线前额外条件：

1. migration 如存在，必须独立、可回滚、只新增 catalog mirror，不触碰现有 retrieval 表语义。
2. 所有 DB-2 写路径必须受 `PLATFORM_ASSET_SYNC_WRITE_ENABLED=false` 默认关闭保护。
3. 真实平台连接配置必须缺省为空或 disabled。
4. test suite 不依赖真实 MySQL / NAS。
5. Codex B review 确认没有把 catalog mirror 混入 document evidence。

## 5. DB-3 Acceptance

DB-3 目标是 Catalog Retrieval。本文只定义未来验收条件；当前不得进入 DB-3 实现。

DB-3 进入条件：

1. DB-2 已 baseline。
2. 用户显式授权进入 DB-3。
3. Codex B review 通过 DB-3 implementation prompt。
4. DB-3 retrieval provider 与现有 document retrieval contract 的边界已设计清楚。

DB-3 未来实现完成条件：

1. 只回答目录类问题，例如项目文件清单、模型登记状态、文件路径、大小、checksum、更新时间、项目归属、index 状态。
2. 对正文内容、文件结论、条款解释、图纸内容、模型语义分析返回 Missing Evidence。
3. Missing Evidence 可区分 `asset_catalog_only`。
4. context 明确区分：
   - `asset_catalog_evidence`
   - `document_content_evidence`
   - `semantic_index_evidence`
5. pre-model 权限过滤先于任何 context 注入。
6. 无权限、无 `permission_tags`、项目不匹配、异常状态资产不得进入 prompt。
7. 无权限时不得返回敏感路径、正文片段或可推断内容。
8. citation_status 保持 `metadata_only`，除非后续 selective indexing phase 明确授权并完成。
9. 不改变现有 retrieval request / response contract 语义。
10. 不让 catalog retrieval 替代 document content retrieval。
11. tests 覆盖 allowed catalog query、asset_catalog_only Missing Evidence、permission denied、abnormal sync status。

DB-3 合回主线前额外条件：

1. DB-3 默认 feature flag off。
2. DB-3 可在 flag off 时完全不影响现有 retrieval。
3. DB-3 trace 字段不破坏既有 trace 消费方。
4. Codex B review 确认没有把 metadata 当正文 evidence。
5. 至少完成 DB-1 / DB-2 / DB-3 组合 contract tests。

## 6. 主线合回 Checklist

DB 分支合回主线前必须全部满足：

1. 当前 DB phase 已 baseline，且没有未完成 review blockers。
2. 所有 DB / NAS / Data Steward feature flags 默认 off。
3. fake adapter 与真实平台 client 分离。
4. 没有真实 MySQL / NAS / REST credential、scan output 或审计写入产物进入仓库。
5. 没有写入 `documents` / `chunks` 的 catalog-only 资产。
6. 没有 OpenSearch / Qdrant 写入路径默认开启。
7. catalog-only evidence 和 document content evidence 分层清晰。
8. Missing Evidence 支持或规划支持 `asset_catalog_only`，且不会误报为正文 evidence。
9. `permission_tags` 缺失默认 deny。
10. 主线 MVP 的既有 retrieval / ingestion / memory kernel tests 不因 DB 分支回归。
11. `git diff --check` 通过。
12. DB 阶段目标 tests 通过。
13. Codex B review 通过。
14. 用户确认可以合回主线。

## 7. Hard Stop Conditions

出现以下任一情况必须停止，等待用户重新授权：

1. 需要连接真实 MySQL。
2. 需要扫描真实 NAS。
3. 需要读取或写入 `/Volumes/zyzn/卓羽智能项目`。
4. 需要写平台 REST / audit / operation plan。
5. 需要新增 DB migration，但当前 prompt 未授权。
6. 需要写 `documents` / `chunks`。
7. 需要写 OpenSearch / Qdrant。
8. 需要做 selective indexing。
9. 需要改 retrieval contract。
10. 需要改 memory kernel 主架构。
11. 需要进入 DB-2 或 DB-3 实现。
12. 需要 production scheduler / rollout。
