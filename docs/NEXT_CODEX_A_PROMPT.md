# NEXT_CODEX_A_PROMPT

## Phase 2.76 / 2.77 Selective Git Baseline Task

Codex B 已复核 Phase 2.76 / 2.77 NAS Scratch Copy Pipeline Dry-run：

1. 实现范围只限 dry-run copy plan。
2. `AssetScratchCopyPlanner` 不连接真实 NAS、不复制文件、不调用 parser、不创建 scratch 目录。
3. 缺少 REST/API Key `project_scope` / `allowed_project_ids` 时 fail-closed。
4. `catalog_only`、`UNKNOWN` confidentiality、unsupported file type、size 超限、lifecycle 非 active、missing storage locator 均不会进入 `would_copy`。
5. Office / PDF / text 小文件只有在权限、生命周期、index eligibility、size 与 locator 均满足时才进入计划中的 `would_copy`。
6. BIM 大模型仍 metadata-only / requires review，不自动复制或解析。
7. Feature flags 默认关闭：`PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`、`PLATFORM_ASSET_BATCH_COPY_ENABLED=false`。
8. 不写平台 DB / Hermes DB / `documents` / `chunks` / OpenSearch / Qdrant / MinIO。
9. 不启用 Data Steward runtime、mirror、selective indexing、Agent CRUD 或 production rollout。

当前允许 Codex A 只做 Phase 2.76 / 2.77 selective Git baseline，不进入 Phase 2.78 实现。

## 必读文件

1. `docs/PHASE276_277_NAS_SCRATCH_COPY_PIPELINE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `.env.example`
8. `app/core/config.py`
9. `app/services/asset_catalog/scratch_copy_plan.py`
10. `tests/test_data_steward_asset_scratch_copy_plan.py`

## Baseline 前验证

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
uv run python -m py_compile app/services/asset_catalog/scratch_copy_plan.py app/services/asset_catalog/__init__.py app/core/config.py
uv run --extra dev pytest tests/test_data_steward_asset_scratch_copy_plan.py -q
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_scratch_copy_plan.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 只允许 stage 的文件

```text
.env.example
app/core/config.py
app/services/asset_catalog/__init__.py
app/services/asset_catalog/scratch_copy_plan.py
tests/test_data_steward_asset_scratch_copy_plan.py
docs/PHASE276_277_NAS_SCRATCH_COPY_PIPELINE_PLAN.md
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
git add .env.example \
  app/core/config.py \
  app/services/asset_catalog/__init__.py \
  app/services/asset_catalog/scratch_copy_plan.py \
  tests/test_data_steward_asset_scratch_copy_plan.py \
  docs/PHASE276_277_NAS_SCRATCH_COPY_PIPELINE_PLAN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git commit -m "chore: add phase 2.76 2.77 nas scratch copy dry-run"
git tag phase-2.76-2.77-nas-scratch-copy-dry-run-baseline
git push origin main
git push origin phase-2.76-2.77-nas-scratch-copy-dry-run-baseline
```

完成 baseline 后停止，更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。

## 硬边界

禁止：

1. 进入 Phase 2.78 runtime copy。
2. 连接真实 NAS 或复制真实文件。
3. 解析真实 NAS 文件。
4. 删除、移动、覆盖、重命名 NAS 原件。
5. 写平台 DB / Hermes DB / `documents` / `chunks`。
6. 写 OpenSearch / Qdrant / MinIO。
7. 启用 Data Steward runtime feature flags。
8. 执行 mirror migration、selective indexing、repair、cleanup、backfill、reindex、delete。
9. 实现 Agent DB/NAS CRUD。
10. 修改 retrieval contract / memory kernel 主架构。
11. production rollout。

## Baseline 报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 验证命令结果。
6. 明确说明 2.76 / 2.77 仍不是完整 DB/NAS 内容查询，只是安全 dry-run copy plan。
7. 下一步建议是否进入 Phase 2.78 controlled local scratch runtime。
