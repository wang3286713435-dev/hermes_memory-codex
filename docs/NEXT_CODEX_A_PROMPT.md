# NEXT_CODEX_A_PROMPT

当前 DB-4C Readonly Live Smoke Runner 已进入本地实现验证阶段。下一步建议 full validation、Codex review、baseline，然后交给测试 agent 独立复测。

## 已完成 baseline / review 事实

1. DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`。
2. DB-4B readonly connector shell baseline：commit `afadb8d`，tag `phase-db4b-readonly-connector-shell-baseline`。

## 当前 DB-4C 允许范围

1. readonly live smoke runner shell。
2. 默认 disabled。
3. `structure_only` 字段握手。
4. cursor column description required-column validation。
5. rows 只进入 DB-4A preflight validator。
6. `LIMIT 30` 真实样本必须等待主线企业 Agent 版本更新和显式授权。

## 当前 DB-4C 禁止范围

1. 不自动连接真实 MySQL。
2. 不读取真实样本。
3. 不使用应用主账号。
4. 不写 migration。
5. 不写 `external_asset_catalog`。
6. 不扫描真实 NAS。
7. 不读取真实文件正文。
8. 不触发真实 REST。
9. 不写 `documents` / `chunks`。
10. 不写 OpenSearch / Qdrant。
11. 不创建 embedding。
12. 不进入真实 retrieval/indexing。

## 本轮需要 review

1. `app/services/asset_catalog/readonly_live_smoke.py`
2. `app/services/asset_catalog/readonly_connector.py`
3. `app/services/asset_catalog/__init__.py`
4. `app/core/config.py`
5. `tests/test_data_steward_asset_catalog_readonly_live_smoke.py`
6. `docs/DB4C_READONLY_LIVE_SMOKE_RUNNER.md`
7. `package.json`

## 验证命令

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/services/asset_catalog/readonly_preflight.py app/services/asset_catalog/readonly_connector.py app/services/asset_catalog/readonly_live_smoke.py app/core/config.py`
4. `git diff --check`

## Review checklist

1. disabled runner 不得调用 connector。
2. `structure_only` 不得读取真实 rows。
3. required columns 缺失必须产生 finding。
4. `limit` 模式必须要求 `mainline_agent_updated` 和 `allow_real_sample_data` 同时为 true。
5. rows 只进入 DB-4A preflight，不进入 prompt / retrieval / indexing。
6. 不得出现 DML / DDL / 业务底表 / MySQL driver / NAS / REST / documents/chunks / OpenSearch/Qdrant 路径。

## 下一步候选

DB-4C 复测通过后，可以进入 DB-4D docs-only 主线回归与数据库团队电脑更新 runbook。真实数据 smoke 必须等主线版本更新完成后再单独授权。
