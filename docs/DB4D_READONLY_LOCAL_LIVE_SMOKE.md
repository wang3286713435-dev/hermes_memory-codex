# DB-4D Readonly Local Live Smoke

日期：2026-05-11

## 目标

DB-4D 在 DB-4C runner shell 基础上，新增同机部署场景的只读 live smoke 执行层。目标运行环境是后续测试机：Hermes Memory 与 `delivery-mysql` 在同一台 Mac 上运行，用 `hermes_agent_ro` 访问四个稳定 View，并把 `LIMIT 30` 样本读取限制在测试机本机进程内。

本阶段不是 production migration，也不是真实 retrieval/indexing 接入。

当前开发机没有真实数据库环境，因此 DB-4D 当前只冻结耦合接口、门禁、脱敏报告和运行方式；真实 DB smoke 等 Hermes Memory 安装到测试机后再执行。

## 当前实现

新增 `app.services.asset_catalog.readonly_local_live_smoke`：

1. 通过 Docker MySQL CLI 执行只读查询，不在命令参数中携带密码。
2. 密码只从环境变量 `MYSQL_PWD` 读取；仓库、测试和文档不保存密码。
3. 复用 DB-4B `AssetCatalogReadonlyConnectorShell`。
4. 复用 DB-4C `AssetCatalogReadonlyLiveSmokeRunner`。
5. 复用 DB-4A `AssetCatalogReadonlyPreflightValidator`。
6. 真实 rows 只在进程内转为 preflight preview，并立即汇总为脱敏 JSON。
7. 输出不包含 `asset_uid`、`source_id`、项目名、文件名、NAS 路径、raw row、stderr 或密码。

## 新增门禁

DB-4C 原门禁保留：`LIMIT 30` 必须显式授权真实样本。

DB-4D 增加同机本地 dev 例外门禁：

1. `allow_real_sample_data = true`
2. `same_machine_local_dev_authorized = true`

这只适用于测试机上 Hermes Memory 与 `delivery-mysql` 同机运行的本地 dev / shared-dev 临时联调。staging、production 仍不得使用该例外。

新增配置默认值：

```text
platform_asset_readonly_same_machine_local_dev_authorized = false
```

默认仍不会读取真实样本。

## 脱敏输出

DB-4D 输出只允许包含：

1. sample mode。
2. 是否使用真实样本。
3. 检查过的 View 名。
4. 每个 View 的字段数量。
5. missing-column finding。
6. 每个 View 的 row count。
7. preflight item / denied / review count。
8. 是否存在 checkpoint candidate，不输出具体 event id。
9. write flags。
10. 业务底表是否被拒绝读取。

禁止输出：

1. 项目名。
2. 文件名。
3. NAS 路径。
4. source id。
5. asset uid。
6. raw row。
7. SQL stderr。
8. 密码。

## 测试机执行方式

执行前由调用方在当前进程环境里设置 `MYSQL_PWD`，不要写入 `.env`、代码、文档、命令行参数或日志。

```bash
uv run python -m app.services.asset_catalog.readonly_local_live_smoke \
  --sample-mode limit \
  --allow-real-sample-data \
  --same-machine-local-dev-authorized \
  --forbidden-table-probe
```

## 当前 smoke 状态

当前开发机没有真实 `delivery-mysql` 数据库环境，不能把开发机连接结果作为 DB-4D 验收结果。DB-4D 当前状态：

```text
status: interface_ready_waiting_for_test_machine
real_db_smoke_executed: false
real_rows_read: false
sample_values_persisted: false
```

等 Hermes Memory 安装到测试机后，再由测试机环境执行 `structure_only` 或授权后的 `LIMIT 30` 脱敏 smoke。复核前不能声称真实 DB live smoke 已通过。

## 测试机对接时需要的信息

进入真实 DB smoke 前需要用户或数据库团队提供：

1. 测试机上 Hermes Memory 的安装路径和启动方式。
2. 测试机访问 `delivery-mysql` 的 host / port / database。
3. `hermes_agent_ro` 凭证的安全传递方式。
4. 是否允许在测试机执行 `LIMIT 30` 脱敏 smoke。
5. 数据库团队确认四个 View 的字段合同没有变化。

## 继续禁止

1. 不使用 `delivery` 应用账号。
2. 不使用 root 账号作为企业 Agent 连接账号。
3. 不读取业务底表，业务底表只允许做拒绝访问验证。
4. 不写 migration。
5. 不写 `external_asset_catalog`。
6. 不扫描真实 NAS。
7. 不读取真实文件正文。
8. 不触发真实 REST。
9. 不写 `documents` / `chunks`。
10. 不写 OpenSearch / Qdrant。
11. 不创建 embedding。
12. 不进入真实 retrieval/indexing。
