# Active Phase

- 当前 phase：DB-4C Readonly Live Smoke Runner
- 当前分支：`codex/data-steward-db0-contract`
- 当前 baseline：
  - DB-4B readonly connector shell baseline：commit `afadb8d`，tag `phase-db4b-readonly-connector-shell-baseline`
  - DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`
  - DB-3D Temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`
- 本轮授权：继续 DB-4C，但不直接消费真实数据；真实数据 smoke 必须等 DB 分支回归主线并更新数据库团队电脑上的企业 Agent 版本后再显式授权。
- 本轮目标：新增 readonly live smoke runner 关闭态骨架，支持 `structure_only` 字段握手，并把 `LIMIT 30` 真实样本置于主线更新和显式授权双门禁后。

## 本轮修改文件

1. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_live_smoke.py`
2. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_connector.py`
3. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/__init__.py`
4. `/Users/Weishengsu/Hermes_memory_db0/app/core/config.py`
5. `/Users/Weishengsu/Hermes_memory_db0/tests/test_data_steward_asset_catalog_readonly_live_smoke.py`
6. `/Users/Weishengsu/Hermes_memory_db0/docs/DB4C_READONLY_LIVE_SMOKE_RUNNER.md`
7. `/Users/Weishengsu/Hermes_memory_db0/package.json`
8. phase handoff docs

## 完成内容

1. 新增 `AssetCatalogReadonlyLiveSmokeRunner`。
2. runner 默认 disabled，disabled 时不会调用 connector。
3. `structure_only` 模式可验证 cursor column description，不读取真实 rows。
4. 缺 required column 会产生 `missing_required_column` finding。
5. `limit` 模式必须同时满足 `mainline_agent_updated=true` 与 `allow_real_sample_data=true`。
6. rows 仍只进入 DB-4A preflight validator。
7. 新增 live smoke 相关配置，默认均为 false。

## 当前验证状态

1. TDD RED：`uv run --extra dev pytest tests/test_data_steward_asset_catalog_readonly_live_smoke.py -q` 初始因缺少 `AssetCatalogReadonlyLiveSmokeRunner` 失败。
2. TDD GREEN：同一目标测试当前为 `6 passed`。
3. `npm test`：`66 passed`。
4. `npm run lint`：`All checks passed!`。
5. py_compile：passed。
6. `git diff --check`：passed。
7. boundary grep：DB-4C 代码无真实 MySQL driver / DB connect / NAS / REST / documents / chunks / OpenSearch / Qdrant / DML / DDL 路径；命中仅为文档禁止项与 false write flag 字段。

## 当前结论

DB-4C 当前仍是 live smoke runner shell，不代表已经连接真实数据库，也不代表已经读取真实样本。后续真实数据联调必须等 DB 分支回归主线、更新企业 Agent 版本，并单独授权。

## 继续禁止

1. 不自动连接真实 MySQL。
2. 不读取真实样本。
3. 不使用应用主账号。
4. 不创建 production migration。
5. 不写 `external_asset_catalog`。
6. 不扫描真实 NAS。
7. 不读取真实文件正文。
8. 不触发真实 REST 动作。
9. 不写 `documents` / `chunks`。
10. 不写 OpenSearch / Qdrant。
11. 不进入真实 retrieval/indexing。
