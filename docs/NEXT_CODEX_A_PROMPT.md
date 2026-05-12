# NEXT_CODEX_A_PROMPT

## Phase 2.75 Codex B Review / Baseline Task

Codex B 已复核 Phase 2.75 Data Steward Catalog Query Preview：

1. 实现范围只限只读 catalog query preview。
2. `AssetCatalogQueryPreviewer` 只返回资产目录元数据 preview，不生成 prompt evidence。
3. `content_answer` 场景返回 `asset_catalog_only` Missing Evidence。
4. 缺少 REST/API Key `project_scope` 时 fail-closed。
5. 不连接真实 DB、不执行 SQL、不读取真实行、不扫描 NAS。
6. 不写 `documents` / `chunks` / OpenSearch / Qdrant / MinIO。
7. 不启用 Data Steward runtime、mirror、selective indexing、Agent CRUD 或 production rollout。

当前允许 Codex A 只做 Phase 2.75 selective Git baseline，不进入 Phase 2.76 实现。

## 必读文件

1. `docs/PHASE275_DATA_STEWARD_CATALOG_QUERY_PREVIEW.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`

## Baseline 前验证

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
uv run python -m py_compile app/services/asset_catalog/query_preview.py app/services/asset_catalog/__init__.py
uv run --extra dev pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 只允许 stage 的文件

```text
app/services/asset_catalog/query_preview.py
app/services/asset_catalog/__init__.py
tests/test_data_steward_asset_catalog_query_preview.py
docs/PHASE275_DATA_STEWARD_CATALOG_QUERY_PREVIEW.md
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
git add app/services/asset_catalog/query_preview.py \
  app/services/asset_catalog/__init__.py \
  tests/test_data_steward_asset_catalog_query_preview.py \
  docs/PHASE275_DATA_STEWARD_CATALOG_QUERY_PREVIEW.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git commit -m "chore: add phase 2.75 data steward catalog preview"
git tag phase-2.75-data-steward-catalog-preview-baseline
git push origin main
git push origin phase-2.75-data-steward-catalog-preview-baseline
```

完成 baseline 后停止，更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。

## 硬边界

禁止：

1. 进入 Phase 2.76 实现。
2. 连接真实 DB 或执行 SQL。
3. 读取真实业务行。
4. 扫描 NAS。
5. 写平台 DB / Hermes DB / OpenSearch / Qdrant / MinIO。
6. 写 `documents` / `chunks`。
7. 执行 mirror migration、selective indexing、repair、cleanup、backfill、reindex、delete。
8. 启用 Data Steward runtime feature flags。
9. 实现 Agent DB CRUD。
10. 修改 retrieval contract / memory kernel 主架构。
11. production rollout。

## Baseline 报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 验证命令结果。
6. 明确说明 2.75 仍不是完整 DB/NAS 耦合，企业 Agent 仍不能通过数据库无损查询 NAS 文件正文。
