# Active Phase

- 当前 phase：DB-4A Readonly DB Preflight Skeleton
- 当前分支：`codex/data-steward-db0-contract`
- 当前 baseline：
  - DB-3D Temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`
  - DB-3C Missing Evidence response review-fix baseline：commit `84e718a`，tag `phase-db3c-missing-evidence-response-review-fix-baseline`
  - DB-3B temporary DB backed guard baseline：commit `8fd46a3`，tag `phase-db3b-temp-db-backed-guard-baseline`
  - DB-3A catalog retrieval guard baseline：commit `fda6c87`，tag `phase-db3a-catalog-retrieval-guard-baseline`
  - DB-2 schema handoff freeze baseline：commit `bd24284`，tag `phase-db2-schema-handoff-freeze-baseline`
- 本轮授权：基于数据库团队连接合同继续 DB-4A，只做本地只读预检骨架；不连接真实 MySQL，不写 migration，不扫 NAS，不触发 REST，不写 documents/chunks/OpenSearch/Qdrant，不进入真实 retrieval/indexing。
- 本轮目标：把四个稳定 SQL View 的字段合同、`source_system=delivery_platform`、`source_contract_version=delivery_platform.asset_views.v1`、权限缺失默认 deny 和 `event_id` checkpoint candidate 固化成本地 preflight validator。

## 本轮修改文件

1. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/readonly_preflight.py`
2. `/Users/Weishengsu/Hermes_memory_db0/app/services/asset_catalog/__init__.py`
3. `/Users/Weishengsu/Hermes_memory_db0/app/core/config.py`
4. `/Users/Weishengsu/Hermes_memory_db0/tests/test_data_steward_asset_catalog_readonly_preflight.py`
5. `/Users/Weishengsu/Hermes_memory_db0/docs/DB4A_READONLY_DB_PREFLIGHT_PLAN.md`
6. `/Users/Weishengsu/Hermes_memory_db0/package.json`
7. `/Users/Weishengsu/Hermes_memory_db0/docs/ACTIVE_PHASE.md`
8. `/Users/Weishengsu/Hermes_memory_db0/docs/DEV_LOG.md`
9. `/Users/Weishengsu/Hermes_memory_db0/docs/HANDOFF_LOG.md`
10. `/Users/Weishengsu/Hermes_memory_db0/docs/NEXT_CODEX_A_PROMPT.md`
11. `/Users/Weishengsu/Hermes_memory_db0/docs/PHASE_BACKLOG.md`
12. `/Users/Weishengsu/Hermes_memory_db0/docs/TODO.md`

## 完成内容

1. 新增 `AssetCatalogReadonlyPreflightValidator`，只接收内存 rows，不打开数据库连接。
2. 支持四个约定 View：`ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView`。
3. 校验每个 View 的数据库团队确认字段清单。
4. unsupported View 会产生 `unsupported_source_view` finding，防止绕过 contract review。
5. 缺 required field 会产生 `missing_required_field` finding，并跳过该 row 的 preview。
6. 归一化 `asset_uid = delivery_platform + ":" + source_view + ":" + source_id`。
7. 权限字段缺失默认 `permission_status=denied`、`action=would_deny`、`reason=missing_permission_contract`。
8. `AuditEventView.event_id` 只作为 `last_event_id_candidate`，不写 checkpoint。
9. 新增只读 DB 配置开关，默认 off，DSN/user 默认空。
10. 新增 DB-4A handoff 文档，明确 DB-4B 真实只读 smoke 的前置条件。

## 当前验证状态

1. TDD RED：`uv run --extra dev pytest tests/test_data_steward_asset_catalog_readonly_preflight.py -q` 初始因缺少 DB-4A exports/config 失败。
2. TDD RED：unsupported View 测试初始失败，因为未知 View 被忽略。
3. TDD GREEN：同一目标测试当前为 `5 passed`。
4. `npm test`：`53 passed`。
5. `npm run lint`：`All checks passed!`。
6. py_compile：passed。
7. `git diff --check`：passed。
8. boundary grep：DB-4A 代码无真实 MySQL / NAS / REST / OpenSearch / Qdrant / documents / chunks 写路径；命中仅为文档禁止项与 false write flag 字段。

## 当前结论

DB-4A 当前仍是本地 contract/preflight 骨架，不代表已接入真实数据库。真实数据库只读 smoke 可以作为 DB-4B 候选，但必须等用户单独授权，并由平台/运维提供企业 Agent 专用只读 DSN 与账号。

## 继续禁止

1. 不连接真实 MySQL。
2. 不创建 production migration。
3. 不写 `external_asset_catalog`。
4. 不扫描真实 NAS。
5. 不读取真实文件正文。
6. 不触发真实 REST 动作。
7. 不写 `documents` / `chunks`。
8. 不写 OpenSearch / Qdrant。
9. 不进入 DB-3/DB-4 后续真实 retrieval/indexing。
