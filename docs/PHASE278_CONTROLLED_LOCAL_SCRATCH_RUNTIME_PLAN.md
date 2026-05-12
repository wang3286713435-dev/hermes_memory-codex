# Phase 2.78 Controlled Local Scratch Runtime

## 目标

在 Phase 2.76 / 2.77 dry-run copy plan 之后，新增受控本地 scratch runtime 骨架。该 runtime 只处理 dry-run plan 中 `action=would_copy` 的小型本地 fixture 文件，在显式授权和 feature flags 开启时执行本地 copy -> sha256 -> sanitized run record -> cleanup。

本阶段不是测试机真实 NAS smoke，不连接真实 NAS，不解析真实企业文件，不写数据库或索引。

## 本轮实现

新增 `AssetScratchRuntime`：

1. 输入 `AssetScratchCopyPlan`。
2. 只处理 `would_copy` item。
3. 要求 `runtime_authorized=true`。
4. 要求 `scratch_copy_enabled=true` 与 `batch_copy_enabled=true`。
5. 未授权或 flag 未开启时 fail closed，不复制文件。
6. 只接受 `file://` 或本地 fixture path。
7. 复制到 plan 中的 scratch target，计算 copied file sha256。
8. 成功和失败路径都执行 best-effort cleanup。
9. 输出 sanitized run record，不包含 source path / scratch path 原文。
10. 固定 safety flags：不调用 parser，不写 DB / documents / chunks / OpenSearch / Qdrant / MinIO / NAS。

## 安全边界

仍禁止：

1. 连接真实 NAS。
2. 扫描 NAS。
3. 复制真实企业文件。
4. 解析文件正文。
5. 写平台 DB / Hermes DB / `documents` / `chunks`。
6. 写 OpenSearch / Qdrant / MinIO。
7. 默认启用 Data Steward runtime feature flags。
8. mirror migration / selective indexing / repair / cleanup / backfill / reindex / delete。
9. Agent DB / NAS CRUD。
10. 修改 retrieval contract / memory kernel 主架构。
11. production rollout。

## 验证

目标验证：

```bash
uv run python -m py_compile app/services/asset_catalog/scratch_runtime.py app/services/asset_catalog/__init__.py
uv run --extra dev pytest tests/test_data_steward_asset_scratch_copy_plan.py tests/test_data_steward_asset_scratch_runtime.py -q
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_scratch_copy_plan.py tests/test_data_steward_asset_scratch_runtime.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 当前能力边界

Phase 2.78 只能证明本地 fixture copy runtime 的控制语义：

1. explicit authorization gate。
2. feature flag gate。
3. local fixture copy。
4. hash 计算。
5. cleanup。
6. sanitized run record。

它仍不能证明真实 NAS mount、真实企业文件复制、parser 接入、selective indexing 或 Agent 可查询 NAS 文件正文。

## 下一步建议

先由 Codex B review Phase 2.78。若通过，再进入 Phase 2.79 规划小批量真实 smoke：

1. 必须在 Mac mini / 测试机显式授权。
2. 只允许 1-3 个小型非敏感样本。
3. 必须包含 copy -> parse -> cleanup 的 stop conditions。
4. 不允许批量真实 NAS 复制、BIM 大模型复制、DB/index 写入或 rollout。
