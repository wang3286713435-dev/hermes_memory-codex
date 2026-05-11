# Active Phase

- 当前 phase：DB-4D Readonly Local Live Smoke
- 当前分支：`codex/data-steward-db0-contract`
- 当前 baseline：
  - DB-4C readonly live smoke runner baseline：commit `444e562`，tag `phase-db4c-readonly-live-smoke-runner-baseline`
  - DB-4B readonly connector shell baseline：commit `afadb8d`，tag `phase-db4b-readonly-connector-shell-baseline`
  - DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`
  - DB-3D Temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`
- 本轮授权：当前开发机不具备真实数据库环境；DB-4D 只保留后续测试机同机部署时的只读耦合接口、门禁和脱敏 smoke runner。
- 本轮目标：新增 DB-4D 测试机同机只读 live smoke 执行层，支持同机本地 dev 授权门禁、Docker MySQL CLI 只读查询、脱敏 JSON 报告和业务底表拒绝验证。

## 本轮修改文件

1. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_local_live_smoke.py`
2. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_live_smoke.py`
3. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/__init__.py`
4. `/Users/Weishengsu/Hermes_memory_db0/app/core/config.py`
5. `/Users/Weishengsu/Hermes_memory_db0/tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py`
6. `/Users/Weishengsu/Hermes_memory_db0/tests/test_data_steward_asset_catalog_readonly_live_smoke.py`
7. `/Users/Weishengsu/Hermes_memory_db0/docs/DB4D_READONLY_LOCAL_LIVE_SMOKE.md`
8. `/Users/Weishengsu/Hermes_memory_db0/package.json`
9. phase handoff docs

## 完成内容

1. 新增 `DockerMysqlReadonlyQueryRunner`，通过 Docker MySQL CLI 做本机只读查询。
2. 命令参数不携带密码，只读取进程环境变量 `MYSQL_PWD`。
3. 新增 `DockerMysqlDbApiConnection` / cursor 适配层，复用既有 connector shell。
4. 新增 `run_readonly_local_live_smoke()`，输出脱敏 summary。
5. 新增业务底表拒绝验证 `verify_forbidden_table_denials()`，不输出 raw stderr。
6. `LIMIT 30` 可由 `same_machine_local_dev_authorized=true` + `allow_real_sample_data=true` 在测试机同机 dev 明确授权下执行。
7. 默认配置仍全部 fail closed。

## 当前验证状态

1. TDD RED：`uv run --extra dev pytest tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py -q` 初始因缺少 `readonly_local_live_smoke` 模块失败。
2. TDD GREEN：本轮目标测试当前为 `5 passed`。
3. 真实 DB smoke：当前开发机无真实数据库环境，后续等 Hermes Memory 安装到测试机后执行；本轮未读取真实 rows。
4. `npm test`：`71 passed`。
5. `npm run lint`：`All checks passed!`。
6. py_compile：passed。
7. `git diff --check`：passed。

## 当前结论

DB-4D 代码层已准备好测试机同机只读 `LIMIT 30` smoke，但当前开发机不执行真实 DB 验收。下一步做 review / baseline；真实 smoke 等测试机部署后再跑。

## 继续禁止

1. 不自动连接真实 MySQL；仅在测试机上显式运行 DB-4D local smoke 命令时连接同机容器。
2. 不持久化真实样本。
3. 不使用应用主账号。
4. 不创建 production migration。
5. 不写 `external_asset_catalog`。
6. 不扫描真实 NAS。
7. 不读取真实文件正文。
8. 不触发真实 REST 动作。
9. 不写 `documents` / `chunks`。
10. 不写 OpenSearch / Qdrant。
11. 不进入真实 retrieval/indexing。
