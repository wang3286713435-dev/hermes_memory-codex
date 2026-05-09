# DB-3A Catalog Retrieval Guard

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-3A 最小实现；fake preview only；未接真实 MySQL / NAS / OpenSearch / Qdrant

## 1. 本阶段目标

DB-3A 只实现 catalog-only retrieval guard。

它的作用是把 DB-2 的资产目录 metadata 和未来正文 evidence 清楚分开：

1. 项目级授权通过时，可以返回 catalog metadata lookup 结果。
2. catalog metadata 不能变成 prompt-ready 正文 evidence。
3. 用户请求正文内容时，必须返回 Missing Evidence。
4. 权限范围缺失时 fail closed。

## 2. 已实现

新增：

1. `app/services/asset_catalog/retrieval_guard.py`
2. `tests/test_data_steward_asset_catalog_retrieval_guard.py`

导出：

1. `AssetCatalogRetrievalGuard`
2. `AssetCatalogRetrievalRequest`
3. `AssetCatalogRetrievalDecision`
4. `AssetCatalogMetadataItem`

## 3. 行为合同

`AssetCatalogRetrievalGuard.evaluate(preview, request)` 当前只接受 DB-2 fake preview 结果。

`intent="catalog_lookup"`：

1. 只返回 `would_upsert`、`permission_status=allowed`、项目在 `allowed_project_ids` 内的 metadata rows。
2. `prompt_items` 永远为空。
3. 不写 `documents` / `chunks` / OpenSearch / Qdrant。

`intent="content_answer"`：

1. 不返回 catalog metadata 作为回答上下文。
2. `prompt_items` 永远为空。
3. 如果有可见 catalog metadata，返回 `missing_evidence_reason=asset_catalog_only`。
4. 如果没有授权 catalog metadata，返回 `missing_evidence_reason=no_authorized_catalog_metadata`。

缺 `allowed_project_ids`：

1. 返回 `missing_evidence_reason=permission_scope_required`。
2. 不返回 catalog metadata。
3. 不返回 prompt items。

## 4. 禁止范围

DB-3A 仍禁止：

1. 真实 MySQL 连接。
2. 真实 NAS 扫描。
3. 真实 REST 动作。
4. 读取真实文件正文。
5. 写 `documents` / `chunks`。
6. 写 OpenSearch / Qdrant。
7. 生成 chunk。
8. 创建 embedding。
9. 接真实权限系统。
10. 企业 Agent 自动写 NAS / 业务库 / 文件系统。

## 5. 验收

当前测试覆盖：

1. catalog lookup 只返回授权 metadata。
2. catalog metadata 不进入 prompt items。
3. content answer 返回 `asset_catalog_only` Missing Evidence。
4. 缺项目 scope 返回 `permission_scope_required`。
5. denied / moved / stale / missing / human-review rows 不成为 catalog result。
6. `denied_count` 只统计用户项目范围内的 denied rows，不泄露范围外资产轮廓。

## 6. 下一步

DB-3B 候选：

1. 增加 temporary DB backed guard，只读 `external_asset_catalog_contract`。
2. 增加更明确的 Missing Evidence response DTO。
3. 增加 permission scope / project scope 组合测试。

DB-3B 仍不应接真实 MySQL。真实数据库接入需要单独授权 migration、连接信息、账号权限和数据库团队确认。
