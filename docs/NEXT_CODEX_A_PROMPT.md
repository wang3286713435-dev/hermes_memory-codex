# NEXT_CODEX_A_PROMPT

当前 DB-4B Readonly Connector Shell 已进入本地实现验证阶段。下一步建议 full validation、Codex review、baseline，然后交给测试 agent 独立复测。

## 已完成 baseline / review 事实

1. DB-3A catalog retrieval guard baseline：commit `fda6c87`，tag `phase-db3a-catalog-retrieval-guard-baseline`。
2. DB-3B temporary DB backed guard baseline：commit `8fd46a3`，tag `phase-db3b-temp-db-backed-guard-baseline`。
3. DB-3C Missing Evidence response review-fix baseline：commit `84e718a`，tag `phase-db3c-missing-evidence-response-review-fix-baseline`。
4. DB-3D temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`。
5. DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`。

## 当前 DB-4B 允许范围

1. disabled-by-default readonly connector shell。
2. 只生成四个 View 的白名单 SELECT。
3. 默认 `structure_only`，只生成 `WHERE 1 = 0` 字段握手 SQL。
4. 显式 `limit` 模式最多 `LIMIT 30`。
5. 只通过注入的 fake / DB-API 形状 connection factory 加载 rows。
6. rows 只进入 DB-4A preflight validator。

## 当前 DB-4B 禁止范围

1. 不 import MySQL / SQLAlchemy / PyMySQL driver。
2. 不自动连接真实 MySQL。
3. 不写 migration。
4. 不写 `external_asset_catalog`。
5. 不扫描真实 NAS。
6. 不读取真实文件正文。
7. 不触发真实 REST。
8. 不写 `documents` / `chunks`。
9. 不写 OpenSearch / Qdrant。
10. 不创建 embedding。
11. 不进入真实 retrieval/indexing。

## 本轮需要 review

1. `app/services/asset_catalog/readonly_connector.py`
2. `app/services/asset_catalog/__init__.py`
3. `app/core/config.py`
4. `tests/test_data_steward_asset_catalog_readonly_connector.py`
5. `docs/DB4B_READONLY_CONNECTOR_SHELL.md`
6. `package.json`

## 验证命令

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/services/asset_catalog/readonly_preflight.py app/services/asset_catalog/readonly_connector.py app/core/config.py`
4. `git diff --check`

## Review checklist

1. connector shell 不得创建真实 DB client。
2. connector shell 不得 import SQLAlchemy / pymysql / mysql connector / requests / httpx。
3. disabled 时不得调用 connection factory。
4. 只允许四个 View。
5. 默认必须是 `WHERE 1 = 0` structure-only。
6. `LIMIT` 模式必须显式开启，且最大 30。
7. 不得出现 DML / DDL / 业务底表。
8. rows 只进入 DB-4A preflight，不进入 prompt / retrieval / indexing。

## 下一步候选

共享 dev / staging 账号到位后，才允许进入 DB-4C live smoke。DB-4C 仍必须单独授权，且只允许真实只读小样本或 structure-only 字段握手。
