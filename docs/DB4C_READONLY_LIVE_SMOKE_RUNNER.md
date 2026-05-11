# DB-4C Readonly Live Smoke Runner

日期：2026-05-11

## 目标

DB-4C 新增 live smoke runner 的关闭态骨架。它把 DB-4B connector shell 包起来，允许未来做真实只读字段握手，但当前不会自动连接真实数据库，也不会读取真实样本。

本阶段核心边界：真实数据必须等 DB 分支开发完成、回归主线，并通过更新企业 Agent 版本部署到数据库团队电脑后，才允许进入真实样本 smoke。

## 当前实现

新增 `AssetCatalogReadonlyLiveSmokeRunner`：

1. 默认 disabled。
2. disabled 时不会调用 connector 或 connection factory。
3. `structure_only` 模式只执行字段结构握手，不读取真实 rows。
4. runner 会用 cursor column description 校验四个 View 的 required columns。
5. rows 仍只进入 DB-4A preflight validator。
6. 所有 write flags 仍为 `false`。

## 真实样本门禁

`LIMIT 30` 真实样本模式必须同时满足：

1. `mainline_agent_updated = true`
2. `allow_real_sample_data = true`

否则 runner 会拒绝执行，并提示真实样本需要主线企业 Agent 更新和显式授权。

这条门禁对应当前产品节奏：DB 分支完成前，不用本分支直接消费真实业务样本；后续需要先把 DB 分支合回主线，再更新数据库团队电脑上的企业 Agent 版本。

## 配置

新增配置默认值：

1. `platform_asset_readonly_live_smoke_enabled = false`
2. `platform_asset_readonly_mainline_agent_updated = false`
3. `platform_asset_readonly_allow_real_sample_data = false`

默认配置不会连接真实数据库，也不会读取真实样本。

## 继续禁止

DB-4C 当前仍不做：

1. 不自动连接真实 MySQL。
2. 不读取真实样本。
3. 不写 migration。
4. 不写 `external_asset_catalog`。
5. 不扫描 NAS。
6. 不触发 REST。
7. 不写 `documents` / `chunks`。
8. 不写 OpenSearch / Qdrant。
9. 不进入真实 retrieval/indexing。
10. 不把 catalog-only 资产送入 prompt/evidence/answer。

## 后续需要数据库团队提供的信息

进入真实环境前仍需要：

1. shared dev / staging DSN。
2. shared dev / staging 只读账号和密码。
3. 四个 View 正向验证结果。
4. 业务底表反向拒绝验证结果。
5. 样本读取策略确认：`STRUCTURE_ONLY` 或 `ALLOW_LIMIT_30`。
6. 如允许 `LIMIT 30`，需确认真实项目名、文件名、NAS 路径是否可出现在本地测试输出中。
