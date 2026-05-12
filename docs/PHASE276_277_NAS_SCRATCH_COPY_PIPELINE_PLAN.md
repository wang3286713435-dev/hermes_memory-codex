# Phase 2.76 / 2.77 NAS Scratch Copy Pipeline

## 目标

在 Data Steward v1.1 catalog preview 之后，新增 **NAS 只读临时工作副本** 的 dry-run 计划能力。Hermes 根据数据库资产目录与项目权限证明，生成按项目小批量复制计划，但本阶段不连接真实 NAS、不复制文件、不解析正文、不写索引。

## 本轮完成

1. 新增 `AssetScratchCopyPlanner` / `AssetScratchCopyPlanRequest` / `AssetScratchCopyPlanItem` / `AssetScratchCopyPlanSummary`。
2. 新增 feature flags，默认关闭：
   - `PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`
   - `PLATFORM_ASSET_BATCH_COPY_ENABLED=false`
3. planner 只消费 fake asset catalog adapter，生成 dry-run plan。
4. 默认限制：
   - `max_files=10`
   - `max_total_bytes=2GB`
   - `max_single_file_bytes=512MB`
5. 只允许 office / pdf / text / csv 等小型文件候选进入 `would_copy`。
6. RVT / DWG / NWD / IFC / BIM 大模型文件继续 metadata-only，不进入正文复制计划。
7. 输出 reasons：
   - `permission_scope_required`
   - `permission_denied`
   - `catalog_only`
   - `confidentiality_unknown`
   - `unsupported_file_type`
   - `size_limit_exceeded`
   - `lifecycle_not_active`
   - `missing_storage_locator`
   - `batch_limit_exceeded`
   - `total_size_limit_exceeded`

## 安全边界

本阶段不做：

1. 真实 NAS 连接。
2. 文件复制。
3. 文件解析。
4. mirror migration。
5. selective indexing。
6. 写 Hermes Memory DB / `documents` / `chunks` / OpenSearch / Qdrant / MinIO。
7. Agent DB CRUD。
8. 删除、移动、覆盖、改名 NAS 原件。
9. production rollout。

`scratch_path` 只是未来 Mac mini 本地临时副本路径计划，不代表文件已复制。真实复制必须另开 Phase 2.78，并要求测试机 / Mac mini 显式授权。

## 当前能力边界

Phase 2.76 / 2.77 让 Hermes 可以回答“哪些资产理论上可以进入临时复制计划、哪些必须跳过以及为什么”。它仍不能回答 NAS 文件正文内容，也不能把 DB catalog metadata 当作 document evidence。

## 验证

已完成验证：

```bash
uv run python -m py_compile app/services/asset_catalog/scratch_copy_plan.py app/services/asset_catalog/__init__.py app/core/config.py
uv run --extra dev pytest tests/test_data_steward_asset_scratch_copy_plan.py -q  # 5 passed
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_scratch_copy_plan.py -q  # 82 passed
git diff --check
```

## 下一步建议

1. Codex B review Phase 2.76 / 2.77。
2. 若通过，做 selective baseline。
3. Phase 2.78 再规划 Mac mini controlled local scratch runtime，只允许 1-3 个小型非敏感样本真实 copy -> parse -> cleanup smoke。
