# DB-3C Missing Evidence Response DTO

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-3C 最小实现；DTO only；未接真实 MySQL / NAS / OpenSearch / Qdrant

## 1. 本阶段目标

DB-3C 只把 catalog retrieval guard 的 Missing Evidence decision 转成稳定 response object。

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
AssetCatalogMissingEvidenceResponse
```

位置：

```text
app/services/asset_catalog/response.py
```

导出：

```python
from app.services.asset_catalog import AssetCatalogMissingEvidenceResponse
```

## 3. 行为合同

`AssetCatalogMissingEvidenceResponse.from_decision(request, decision)` 只接受：

1. `decision.missing_evidence is True`
2. `decision.missing_evidence_reason` 非空
3. `decision.prompt_items` 为空
4. write flags 全 false

否则抛出 `ValueError`，避免把普通 catalog lookup 包装成 Missing Evidence。

稳定字段：

1. `response_kind="missing_evidence"`
2. `query`
3. `intent`
4. `missing_evidence=True`
5. `reason`
6. `catalog_items`
7. `prompt_items`
8. `writes_documents=False`
9. `writes_chunks=False`
10. `writes_opensearch=False`
11. `writes_qdrant=False`

当前确认 reason：

1. `asset_catalog_only`
2. `permission_scope_required`
3. `no_authorized_catalog_metadata`

## 4. 边界

DTO 不生成回答、不生成 citation、不生成 prompt context。

`prompt_items` 必须保持为空。catalog-only 资产仍不能作为正文 evidence。

## 5. 验收

测试覆盖：

1. catalog-only content answer 生成 `asset_catalog_only` response。
2. 缺项目权限范围生成 `permission_scope_required` response。
3. 无授权 catalog metadata 生成 `no_authorized_catalog_metadata` response。
4. 非 Missing Evidence decision 被拒绝。
5. 含 `prompt_items` 的 Missing Evidence decision 被拒绝。
6. `to_dict()` 输出稳定字段，且 write flags 全 false。

## 6. 下一步

DB-3D 候选：

1. response DTO 与 temp DB backed guard 组合 smoke。
2. project scope / permission scope response case 扩展。
3. 用户可见 Missing Evidence 文案模板。

真实 MySQL / migration / NAS / OpenSearch / Qdrant 仍需单独授权。
