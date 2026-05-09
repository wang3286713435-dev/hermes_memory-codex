# Active Phase

- 当前 phase：DB-4B Readonly Connector Shell
- 当前分支：`codex/data-steward-db0-contract`
- 当前 baseline：
  - DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`
  - DB-3D Temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`
  - DB-3C Missing Evidence response review-fix baseline：commit `84e718a`，tag `phase-db3c-missing-evidence-response-review-fix-baseline`
  - DB-3B temporary DB backed guard baseline：commit `8fd46a3`，tag `phase-db3b-temp-db-backed-guard-baseline`
  - DB-3A catalog retrieval guard baseline：commit `fda6c87`，tag `phase-db3a-catalog-retrieval-guard-baseline`
- 本轮授权：在共享 dev / staging 账号到位前，先做 disabled-by-default readonly connector shell；不连接真实 MySQL，不写 migration，不扫 NAS，不触发 REST，不写 documents/chunks/OpenSearch/Qdrant，不进入真实 retrieval/indexing。
- 本轮目标：固化只读 SQL 白名单、`structure_only` 字段握手、显式 `limit 30` 样本模式、默认关闭和 DB-4A preflight 串接。

## 本轮修改文件

1. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_connector.py`
2. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/__init__.py`
3. `/Users/Weishengsu/Hermes_memory_db0/app/core/config.py`
4. `/Users/Weishengsu/Hermes_memory_db0/tests/test_data_steward_asset_catalog_readonly_connector.py`
5. `/Users/Weishengsu/Hermes_memory_db0/docs/DB4B_READONLY_CONNECTOR_SHELL.md`
6. `/Users/Weishengsu/Hermes_memory_db0/package.json`
7. phase handoff docs

## 完成内容

1. 新增 `AssetCatalogReadonlyConnectorShell`。
2. connector 默认 disabled，disabled 时不会调用 connection factory。
3. 默认 `sample_mode=structure_only`，只生成 `WHERE 1 = 0` 字段握手 SQL。
4. 显式 `sample_mode=limit` 才生成 `LIMIT 30` 小样本 SQL。
5. sample limit 最大 30。
6. 未知 View 会被拒绝。
7. fake connection rows 会转成 dict rows 并交给 DB-4A validator。
8. 新增只读 DB password/sample mode/sample limit 配置，默认不含 secret。

## 当前验证状态

1. TDD RED：`uv run --extra dev pytest tests/test_data_steward_asset_catalog_readonly_connector.py -q` 初始因缺少 `AssetCatalogReadonlyConnectorShell` 失败。
2. TDD GREEN：同一目标测试当前为 `7 passed`。
3. Target regression：`uv run --extra dev pytest tests/test_data_steward_asset_catalog_readonly_connector.py tests/test_data_steward_asset_catalog_readonly_preflight.py -q` 为 `12 passed`。
4. `npm test`：`60 passed`。
5. `npm run lint`：`All checks passed!`。
6. py_compile：passed。
7. `git diff --check`：passed。
8. boundary grep：DB-4B 代码无真实 MySQL driver / DB connect / NAS / REST / documents / chunks / OpenSearch / Qdrant / DML / DDL 路径；命中仅为文档禁止项、业务底表拒绝测试和 false write flag 字段。

## 当前结论

DB-4B 当前仍是 connector shell，不代表已连接真实数据库。共享 dev / staging 账号到位后，才能进入单独授权的 live smoke。

## 继续禁止

1. 不自动连接真实 MySQL。
2. 不使用应用主账号。
3. 不创建 production migration。
4. 不写 `external_asset_catalog`。
5. 不扫描真实 NAS。
6. 不读取真实文件正文。
7. 不触发真实 REST 动作。
8. 不写 `documents` / `chunks`。
9. 不写 OpenSearch / Qdrant。
10. 不进入真实 retrieval/indexing。
