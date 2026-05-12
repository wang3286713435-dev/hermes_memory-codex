# Phase 2.75 Data Steward Catalog Query Preview

## 目标

在 Phase 2.74 测试机 v1.1 adapter smoke 已完成 core Go 后，继续推进 Data Steward 与 Hermes 主线的低耦合接入：新增只读 catalog query preview，让企业 Agent 可以在受控权限范围内查看资产目录元数据，同时继续禁止把 DB / NAS catalog 当成文档正文 evidence。

本阶段不是完整 DB / NAS / BIM 耦合，也不是 Agent CRUD。

## 当前 2.74 能力边界

Phase 2.74 已证明：

1. 测试机可在 reviewed ref 上识别 `delivery_platform.asset_views.v1.1`。
2. 四个 View 可做 structure-only 校验。
3. `LIMIT 30` 脱敏统计 smoke 已通过，且未输出 raw row / secret / 真实业务明细。
4. Hermes 侧 fake adapter / readonly DTO / preflight 与 v1.1 字段对齐。
5. Data Steward feature flags 仍默认关闭。

Phase 2.74 尚未证明：

1. 企业 Agent 能直接检索 NAS 文件正文。
2. DB catalog 能作为 retrieval evidence 进入回答。
3. Hermes 已完成 mirror / selective indexing / NAS content extraction。
4. Agent 能对数据库或 NAS 执行增删改查。
5. `permission_tags` 已等同最终授权。

结论：Phase 2.74 是“真实 DB v1.1 结构 + 脱敏统计 + Hermes adapter contract”级别耦合，不是完整 Data Steward 运行时耦合。

## 本轮实现

新增 `AssetCatalogQueryPreviewer`：

1. 复用 `AssetCatalogRetrievalGuard` 的 fail-closed 判断。
2. 对 `catalog_lookup` 返回只读 catalog metadata preview。
3. 对 `content_answer` 返回 `asset_catalog_only` Missing Evidence。
4. 永远不生成 prompt evidence。
5. 永远不写 `documents` / `chunks` / OpenSearch / Qdrant。
6. 不连接真实 DB、不执行 SQL、不扫描 NAS。
7. 不输出 `storage_path` / raw row。

## 安全语义

1. `asset_catalog_only=true`：返回的是资产目录元数据，不是文件正文。
2. `content_evidence_available=false`：当前没有 NAS / BIM 文件正文 evidence。
3. `permission_fail_closed=true`：缺少 REST/API Key project scope 时默认拒绝。
4. `content_answer_blocked=true`：用户要求回答文件正文时，必须返回 Missing Evidence。
5. `index_eligibility=catalog_only`：不得自动进入 full-text / semantic indexing。

## 当前仍禁止

1. 连接真实 DB 运行生产查询。
2. 扫描 NAS。
3. mirror migration。
4. 写 Hermes Memory DB、`documents`、`chunks`、OpenSearch、Qdrant、MinIO。
5. DB CRUD / Agent 直接改 MySQL 或 NAS。
6. 将 catalog metadata 当作 document retrieval evidence。
7. production rollout。

## 验证

目标测试：

```bash
uv run --extra dev pytest tests/test_data_steward_asset_catalog_query_preview.py -q
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py -q
```

## 下一步建议

Phase 2.75 通过后，下一步不应直接启用 runtime。建议进入 Phase 2.76：

1. 规划 REST/API Key `project_scope` 权限证明接入。
2. 明确 catalog preview 如何被 Hermes 主仓展示为“资产目录结果”，而非文档证据。
3. 继续保持 feature flags 默认 off。
4. 等权限证明、preview UX、只读审计都稳定后，再讨论 selective indexing / NAS content extraction。
