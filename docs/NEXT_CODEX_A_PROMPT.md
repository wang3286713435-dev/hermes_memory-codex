# NEXT_CODEX_A_PROMPT

当前 DB-4A Readonly DB Preflight Skeleton 已进入本地实现验证阶段。下一步建议 full validation、Codex review、baseline，然后交给测试 agent 独立复测。

## 已完成 baseline / review 事实

1. DB-2 schema handoff freeze baseline：commit `bd24284`，tag `phase-db2-schema-handoff-freeze-baseline`。
2. DB-3A catalog retrieval guard baseline：commit `fda6c87`，tag `phase-db3a-catalog-retrieval-guard-baseline`。
3. DB-3B temporary DB backed guard baseline：commit `8fd46a3`，tag `phase-db3b-temp-db-backed-guard-baseline`。
4. DB-3C Missing Evidence response review-fix baseline：commit `84e718a`，tag `phase-db3c-missing-evidence-response-review-fix-baseline`。
5. DB-3D temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`。

## 当前 DB-4A 允许范围

1. 基于数据库团队连接合同做本地 readonly preflight skeleton。
2. 只接收内存中的四个 View rows，不打开数据库连接。
3. 校验 View 字段清单和 unsupported View。
4. 输出 `AssetCatalogMirrorPreview`，权限缺失默认 `would_deny`。
5. 固定 `source_system=delivery_platform`。
6. 固定 `source_contract_version=delivery_platform.asset_views.v1`。
7. `AuditEventView.event_id` 只作为 checkpoint candidate。

## 当前 DB-4A 禁止范围

1. 不连接真实 MySQL。
2. 不写 migration。
3. 不写 `external_asset_catalog`。
4. 不扫描真实 NAS。
5. 不读取真实文件正文。
6. 不触发真实 REST。
7. 不写 `documents` / `chunks`。
8. 不写 OpenSearch / Qdrant。
9. 不创建 embedding。
10. 不进入真实 retrieval/indexing。

## 本轮需要 review

1. `app/services/asset_catalog/readonly_preflight.py`
2. `app/services/asset_catalog/__init__.py`
3. `app/core/config.py`
4. `tests/test_data_steward_asset_catalog_readonly_preflight.py`
5. `docs/DB4A_READONLY_DB_PREFLIGHT_PLAN.md`
6. `package.json`

## 验证命令

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/services/asset_catalog/readonly_preflight.py app/core/config.py`
4. `git diff --check`

## Review checklist

1. DB-4A validator 不得调用真实 DB client。
2. DB-4A validator 不得 import SQLAlchemy / pymysql / requests / httpx。
3. 只允许四个 View；未知 View 必须 finding。
4. 缺 required field 必须 finding 且跳过该 row。
5. 权限字段缺失必须 `would_deny`。
6. `prompt_items` / retrieval / indexing 不得出现。
7. 所有 write flags 必须保持 false。

## DB-4B 候选

DB-4B 才允许讨论真实只读 staging/dev smoke，但仍必须单独授权。进入 DB-4B 前需要：

1. 用户明确授权 DB-4B。
2. 平台/运维提供 staging 或 dev 联调 DSN。
3. 提供企业 Agent 专用只读账号，不使用应用主账号。
4. 只读账号仅有四个 View 的 SELECT 权限。
5. 明确样例中真实项目名 / NAS 路径是否可暴露。
6. DB-4A baseline 和测试 agent 独立复测通过。

DB-4B 仍不允许 migration、mirror write、NAS scan、documents/chunks、OpenSearch/Qdrant、selective indexing 或真实 Agent 写操作。
