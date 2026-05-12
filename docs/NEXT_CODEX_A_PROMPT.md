# NEXT_CODEX_A_PROMPT

## Phase 2.79 Docs Baseline Task

Codex B 已复核 Phase 2.79 Small Batch Real Smoke Planning：

1. 本阶段只做 docs / prompt planning。
2. `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md` 明确 Phase 2.79a 才能执行真实 smoke。
3. `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md` 只用于后续显式授权的 Mac mini / 测试机任务。
4. 样本范围限制为 1-3 个小型非敏感文件。
5. 文件类型优先 Office / PDF / text / CSV / XLSX。
6. 单文件建议 <= 50MB，总量建议 <= 200MB。
7. RVT / DWG / IFC / NWD / BIM 大模型、整项目目录、NAS scan、bulk copy 均禁止。
8. Parser、ingestion、DB / index write、Agent final answer integration 均禁止。
9. 报告必须 sanitized，不输出 secret、raw row、真实 NAS 路径或真实业务数据。

当前允许 Codex A 只做 Phase 2.79 docs selective Git baseline，不执行 Phase 2.79a。

## 必读文件

1. `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md`
2. `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Baseline 前验证

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 只允许 stage 的文件

```text
docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md
docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md
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
git add docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md \
  docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git commit -m "docs: plan phase 2.79 small batch nas smoke"
git tag phase-2.79-small-batch-nas-smoke-plan-baseline
git push origin main
git push origin phase-2.79-small-batch-nas-smoke-plan-baseline
```

完成 baseline 后停止，更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。

## 硬边界

禁止：

1. 执行真实 NAS copy。
2. 执行 parser。
3. 写平台 DB / Hermes DB / `documents` / `chunks`。
4. 写 OpenSearch / Qdrant / MinIO。
5. 扫描 NAS。
6. 批量复制项目目录。
7. 复制 BIM 大模型。
8. Agent DB / NAS CRUD。
9. repair / cleanup / backfill / reindex / delete。
10. production rollout。
11. 进入 Phase 2.79a。

## Baseline 报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 验证命令结果。
6. 明确 Phase 2.79 只是 planning，不是执行授权。
7. 下一步是否建议进入 Phase 2.79a small batch real smoke。
