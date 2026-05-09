# DB-3D Temp DB Missing Evidence Response Smoke

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-3D 最小实现；temporary DB backed guard + Missing Evidence response DTO；未接真实 MySQL / NAS / OpenSearch / Qdrant

## 1. 本阶段目标

DB-3D 只验证 DB-3B 的 SQLite memory temporary mirror rows 可以通过 DB-3A guard，再由 DB-3C DTO 生成稳定 Missing Evidence response。

它不做：

1. 真实 MySQL 连接。
2. migration。
3. NAS scan。
4. documents / chunks 写入。
5. OpenSearch / Qdrant 写入。
6. embedding / semantic index。
7. 真实 retrieval / indexing。

## 2. 已实现

新增：

```python
AssetCatalogMissingEvidenceResponse.from_preview(preview, request)
```

行为：

1. 使用 `AssetCatalogRetrievalGuard` evaluate preview。
2. 复用 `from_decision()` 包装 Missing Evidence decision。
3. catalog lookup 的非 Missing Evidence decision 仍被拒绝。

## 3. 验收

新增测试：

```text
tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py
```

覆盖：

1. SQLite memory temp DB rows + content answer 生成 `asset_catalog_only` response。
2. 缺项目权限 scope 生成 `permission_scope_required` response。
3. 授权 catalog lookup 不会被包装成 Missing Evidence response。
4. `prompt_items` 为空。
5. write flags 全 false。

## 4. 真实数据库接入门槛

DB-3D 通过后，可以考虑进入真实数据库接入前置阶段，但只能先做 staging / dev 环境的只读连接预检。

真实数据库接入的下一步建议：

1. DB-4A：真实数据库只读 preflight adapter。
2. 只读账号，只访问平台确认的 View 或 mirror 表。
3. 不创建 migration。
4. 不写真实数据库。
5. 不扫描 NAS。
6. 不写 documents / chunks / OpenSearch / Qdrant。
7. 只把真实 rows 规范化为 `AssetCatalogMirrorPreview` 或等价只读 DTO。

生产 migration、mirror 写入、NAS 扫描、OpenSearch / Qdrant indexing 仍需单独授权。
