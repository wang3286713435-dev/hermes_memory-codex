# NEXT_CODEX_A_PROMPT

## Phase 2.78 Selective Git Baseline Task

Codex B 已复核 Phase 2.78 Controlled Local Scratch Runtime：

1. 实现范围只限本地 fixture scratch runtime。
2. `AssetScratchRuntime` 要求 explicit `runtime_authorized=true`。
3. `AssetScratchRuntime` 要求 `scratch_copy_enabled=true` 与 `batch_copy_enabled=true`。
4. 未授权或 feature flags 未开启时 fail closed，不复制文件。
5. runtime 只处理 `action=would_copy` item。
6. runtime 只接受 local path / `file://` fixture，不实现 NAS scan。
7. 成功路径执行 copy -> sha256 -> cleanup。
8. 失败路径执行 best-effort cleanup。
9. sanitized run record 不输出 source path / scratch path 原文。
10. parser / DB / documents / chunks / OpenSearch / Qdrant / MinIO / NAS write flags 恒为 false。

当前允许 Codex A 只做 Phase 2.78 selective Git baseline，不进入 Phase 2.79。

## 必读文件

1. `docs/PHASE278_CONTROLLED_LOCAL_SCRATCH_RUNTIME_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `app/services/asset_catalog/scratch_runtime.py`
8. `tests/test_data_steward_asset_scratch_runtime.py`

## Baseline 前验证

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
uv run python -m py_compile app/services/asset_catalog/scratch_runtime.py app/services/asset_catalog/__init__.py
uv run --extra dev pytest tests/test_data_steward_asset_scratch_copy_plan.py tests/test_data_steward_asset_scratch_runtime.py -q
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_scratch_copy_plan.py tests/test_data_steward_asset_scratch_runtime.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 只允许 stage 的文件

```text
app/services/asset_catalog/scratch_runtime.py
app/services/asset_catalog/__init__.py
tests/test_data_steward_asset_scratch_runtime.py
docs/PHASE278_CONTROLLED_LOCAL_SCRATCH_RUNTIME_PLAN.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/TODO.md
docs/DEV_LOG.md
docs/NEXT_CODEX_A_PROMPT.md
```

不要 stage `reports/agent_runs/latest.json`，它是 ignored 本地状态文件。

## Commit / Tag

如验证通过且 dirty 仅为上述白名单文件：

```bash
git add app/services/asset_catalog/scratch_runtime.py \
  app/services/asset_catalog/__init__.py \
  tests/test_data_steward_asset_scratch_runtime.py \
  docs/PHASE278_CONTROLLED_LOCAL_SCRATCH_RUNTIME_PLAN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git commit -m "chore: add phase 2.78 local scratch runtime"
git tag phase-2.78-local-scratch-runtime-baseline
git push origin main
git push origin phase-2.78-local-scratch-runtime-baseline
```

完成 baseline 后停止，更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。

## 硬边界

禁止：

1. 进入 Phase 2.79。
2. 连接真实 NAS。
3. 复制真实企业文件。
4. 调用 parser。
5. 写平台 DB / Hermes DB / `documents` / `chunks`。
6. 写 OpenSearch / Qdrant / MinIO。
7. 启用 runtime feature flags 默认值。
8. 执行 mirror / selective indexing / repair / cleanup / backfill / reindex / delete。
9. 实现 Agent DB / NAS CRUD。
10. 修改 retrieval contract / memory kernel 主架构。
11. production rollout。

## Baseline 报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 验证命令结果。
6. 明确 Phase 2.78 仍只是本地 fixture runtime，不是测试机真实 NAS smoke。
7. 下一步是否建议进入 Phase 2.79 small batch real smoke。
