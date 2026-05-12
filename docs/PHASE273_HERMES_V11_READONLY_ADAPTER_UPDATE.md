# Phase 2.73 Hermes v1.1 Readonly Adapter Contract Update

## 目标

将 Hermes 侧 Data Steward / asset catalog 只读契约从 `delivery_platform.asset_views.v1` 对齐到 `delivery_platform.asset_views.v1.1`，但不启用真实 DB runtime、mirror、indexing 或 Agent CRUD。

## 本轮完成

1. `DB4A_READONLY_CONTRACT_VERSION` 与默认 `platform_asset_readonly_db_contract_version` 更新为 `delivery_platform.asset_views.v1.1`。
2. readonly preflight 必填字段增加：
   - `permission_tags`
   - `confidentiality_level`
   - `last_seen_at`
   - `lifecycle_status`
   - `index_eligibility`
   - `ModelAssetView.project_id`
3. fake adapter contract version 更新为 v1.1，并补齐 v1.1 governance tags 的规范化输出。
4. catalog metadata DTO 透出 v1.1 字段，但仍保持 `content_evidence_available=false`。
5. readonly preflight 对真实 DB rows 继续 fail-closed：即使 `permission_tags` 存在，缺少 REST/API Key `project_scope` 证明时仍 `would_deny / missing_permission_contract`。

## 安全边界

- 未连接真实 DB。
- 未读取真实行。
- 未扫描 NAS。
- 未写 `documents` / `chunks`。
- 未写 OpenSearch / Qdrant / MinIO。
- 未启用 Data Steward runtime feature。
- 未做 mirror migration、indexing、Agent CRUD 或 production rollout。

## 验证

- `uv run python -m py_compile app/services/asset_catalog/*.py app/core/config.py`
- `uv run pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py -q`
- 结果：`73 passed`

## 当前结论

Hermes 侧 v1.1 readonly adapter / fake adapter / DTO / contract tests 已对齐真实 DB v1.1 字段形态。完整 Data Steward 耦合仍未完成；下一步应继续保持 feature flags 默认 off，并在受控测试机部署 reviewed ref 后再做 v1.1 structure / redacted smoke 复验。
