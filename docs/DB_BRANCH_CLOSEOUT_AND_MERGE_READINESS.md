# DB Branch Closeout And Merge Readiness

日期：2026-05-11
分支：`codex/data-steward-db0-contract`
当前 baseline：`39cda74` / `phase-db4d-readonly-local-live-smoke-interface-baseline`

## 1. Closeout 结论

DB 支线当前建议停止扩功能，进入合回主线准备。

本分支已经完成从 DB-0 到 DB-4D 的资产治理前置工作：契约、fake adapter、mirror proof、catalog retrieval guard、Missing Evidence response、readonly DB preflight、readonly connector shell、测试机同机 live smoke 接口与脱敏报告。

当前不继续进入新的 DB-5 / DB-6 实现。DB-5 selective indexing、DB-6 operation plan / approval、真实数据库读取、真实 NAS、真实 OpenSearch / Qdrant 写入，都应在主线合回后按单独授权阶段推进。

## 2. 已完成范围

### DB-0 / DB-1

1. 数据管家定位已明确：Hermes 企业 Agent 产品名；DB / NAS / BIM 是资产治理模块。
2. fake fixtures 覆盖：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
3. fake adapter 只读，支持 pagination / cursor / filter / contract version。
4. unknown filters fail closed。
5. cursor 包含 filter context，跨 filter 复用会拒绝。
6. malformed cursor 安全转为 cursor-specific `ValueError`。
7. `asset_uid` 规则已采用：

```text
source_system + ":" + source_view + ":" + source_id
```

### DB-2

1. fake-adapter dry-run preview 已完成。
2. temporary DB proof-of-contract 已完成。
3. schema contract freeze 已完成。
4. `external_asset_catalog` 与 `external_asset_sync_checkpoint` 合同已文档化。
5. `permission_status` 默认 `DENIED`。
6. `permission_tags` / `project_scope` 缺失时 fail closed。
7. catalog-only 不写 `documents` / `chunks` / OpenSearch / Qdrant。
8. 真实 migration 未执行，仍需单独授权。

### DB-3

1. catalog retrieval guard 已完成。
2. temporary DB backed guard 已完成。
3. Missing Evidence response DTO 已完成。
4. temporary DB Missing Evidence response smoke 已完成。
5. catalog metadata 不进入 `prompt_items`。
6. 正文请求对 catalog-only 资产返回 `asset_catalog_only`。
7. 缺权限 scope 返回 `permission_scope_required`。
8. denied / moved / stale / missing / human-review rows 不进入 catalog result。

### DB-4

1. readonly DB preflight skeleton 已完成。
2. readonly connector shell 已完成。
3. readonly live smoke runner shell 已完成。
4. DB-4D 测试机同机 readonly live smoke interface 已完成。
5. `LIMIT 30` 真实样本被显式 gate 保护。
6. DB-4D 输出只允许脱敏 summary，不输出真实项目名、文件名、NAS 路径、`asset_uid`、`source_id`、raw row、stderr 或密码。
7. 当前开发机无真实 DB 环境；真实 DB smoke 等 Hermes Memory 安装到测试机后执行。

## 3. 当前明确未做

1. 未连接真实 MySQL。
2. 未扫描真实 NAS。
3. 未读取真实文件正文。
4. 未创建 production migration。
5. 未写 `external_asset_catalog` 真实表。
6. 未写平台 DB。
7. 未触发平台 REST。
8. 未写 `documents` / `chunks`。
9. 未写 OpenSearch / Qdrant。
10. 未创建 embedding。
11. 未进入真实 retrieval/indexing。
12. 未实现 DB-5 selective indexing。
13. 未实现 DB-6 operation plan / approval 写入。

## 4. Feature Flag 和默认安全态

合回主线前必须保持：

1. `platform_asset_catalog_enabled = false`
2. `platform_asset_sync_write_enabled = false`
3. `platform_asset_mcp_enabled = false`
4. `platform_asset_semantic_index_enabled = false`
5. `platform_asset_readonly_db_enabled = false`
6. `platform_asset_readonly_live_smoke_enabled = false`
7. `platform_asset_readonly_mainline_agent_updated = false`
8. `platform_asset_readonly_allow_real_sample_data = false`
9. `platform_asset_readonly_same_machine_local_dev_authorized = false`

默认状态下，主线不会自动连接 DB、不会读取样本、不会写 mirror、不会进入 retrieval/indexing。

## 5. 合回主线条件

合回主线前必须满足：

1. QA 对 DB-4D 无 P0/P1/P2 open finding。
2. `npm test` 通过。
3. `npm run lint` 通过。
4. `git diff --check` 通过。
5. 当前分支无 tracked dirty。
6. 临时 QA probe 文件不得纳入提交。
7. 仓库不包含真实 DB 密码、真实样本、真实 NAS scan output 或平台审计输出。
8. catalog-only 与 document content evidence 分层清晰。
9. Missing Evidence 支持 `asset_catalog_only`。
10. 权限缺失默认 deny。
11. 真实 DB smoke 被明确标注为测试机部署后事项。
12. 用户确认执行合回或创建 PR。

## 6. 测试机后续对接门槛

Hermes Memory 安装到测试机后，真实 DB smoke 仍需单独授权，并需要以下信息：

1. 测试机 Hermes Memory 安装路径与启动方式。
2. 测试机访问 `delivery-mysql` 的 host / port / database。
3. `hermes_agent_ro` 凭证的安全传递方式。
4. 数据库团队确认四个 View 字段合同仍为 `delivery_platform.asset_views.v1`。
5. 是否允许执行 `LIMIT 30` 脱敏 smoke。
6. 业务底表拒绝访问验证策略。

测试机真实 DB smoke 只能输出脱敏 summary，不得外发真实项目名、文件名或 NAS 路径。

## 7. 合回后建议路线

1. 先把 DB 支线合回主线，使 Hermes Memory 代码具备 readonly coupling interface。
2. 在测试机更新 Hermes Memory 版本。
3. 先执行 `structure_only` 字段握手。
4. 再按用户授权执行 `LIMIT 30` 脱敏 smoke。
5. 若 smoke 通过，再讨论真实 mirror migration 或 DB-5 selective indexing。
6. DB-5 / DB-6 均需独立 planning、独立授权、独立 QA。

## 8. 当前判定

从 DB 支线开发角度，当前代码与文档可以进入 closeout / merge readiness。

不建议继续在本分支扩大功能。下一步应由用户选择：

1. 保留分支等待后续测试机部署。
2. 创建 PR / 合回主线。
3. 在主线合回后开启测试机真实 DB smoke 小阶段。
