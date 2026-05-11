# DB-4B Readonly Connector Shell

日期：2026-05-09

## 目标

DB-4B 在没有共享 dev / staging 账号前，先建立 disabled-by-default readonly connector shell。它只负责生成受控只读 SQL、调用外部注入的 DB-API 形状 connection factory、把 rows 交给 DB-4A preflight validator。

本阶段不内置 MySQL driver，不打开真实连接，不读取真实样本。

## 为什么需要共享 dev 只读账号

共享 dev 只读账号的作用是把企业 Agent 的数据库能力限制在最小范围：

1. 只允许读取四个稳定 View。
2. 不允许读取业务底表。
3. 不允许写平台数据库。
4. 不复用本机应用主账号。
5. 让 staging / 共享 dev 的网络、权限、schema、样本暴露策略提前暴露问题。

本机 dev 适合个人本地验证，但它不是团队联调的权限边界。共享 dev / staging 账号必须由平台/运维提供，并且密码不能写入仓库或文档。

## 当前实现

新增 `AssetCatalogReadonlyConnectorShell`：

1. 默认 `enabled=false`，disabled 时不会调用 connection factory。
2. 只支持四个 source View：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
3. 默认 `sample_mode=structure_only`，生成：
   - `SELECT * FROM <View> WHERE 1 = 0`
4. 显式 `sample_mode=limit` 时生成：
   - `SELECT * FROM <View> LIMIT <limit>`
5. `sample_limit` 最大为 `30`。
6. 未知 View 会被拒绝。
7. 查询结果只转成 rows，并复用 DB-4A preflight validator。

## 配置

新增或沿用配置：

1. `platform_asset_readonly_db_enabled = false`
2. `platform_asset_readonly_db_dsn = None`
3. `platform_asset_readonly_db_user = None`
4. `platform_asset_readonly_db_password = None`
5. `platform_asset_readonly_db_contract_version = delivery_platform.asset_views.v1`
6. `platform_asset_readonly_db_sample_mode = structure_only`
7. `platform_asset_readonly_db_sample_limit = 30`

密码只能通过环境变量或安全渠道注入，不写入 repo、日志或文档。

## 禁止范围

DB-4B connector shell 仍不做：

1. 不 import MySQL / SQLAlchemy / PyMySQL driver。
2. 不自动连接真实 MySQL。
3. 不写 migration。
4. 不写 `external_asset_catalog`。
5. 不扫描 NAS。
6. 不触发 REST。
7. 不写 `documents` / `chunks`。
8. 不写 OpenSearch / Qdrant。
9. 不进入真实 retrieval/indexing。

## 进入 live smoke 的门槛

下一步 live smoke 必须等：

1. 用户单独授权。
2. 平台/运维提供共享 dev 或 staging DSN。
3. 提供企业 Agent 专用只读账号。
4. 明确目标环境 sample policy：
   - `STRUCTURE_ONLY`
   - 或 `ALLOW_LIMIT_30`
5. 明确真实项目名 / NAS 路径是否允许出现在本地日志和测试输出。

live smoke 仍只允许小样本 SELECT + preflight，不允许写库、migration、NAS、索引或真实 retrieval。
