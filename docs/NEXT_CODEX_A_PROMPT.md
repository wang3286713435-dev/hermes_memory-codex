# NEXT_CODEX_A_PROMPT

## Phase 2.80 Docs Baseline Task

Codex B review 通过 Phase 2.80 Controlled Scratch Parser Dry-run Planning。

Review 结论：

1. Phase 2.79a small batch NAS scratch-copy smoke `Go` 已记录。
2. Phase 2.80 只做 parser dry-run planning，未执行 parser。
3. 规划继续限定 1-3 个小型非敏感样本。
4. Parser dry-run 只允许后续 Phase 2.80a 显式授权后执行。
5. Parser preview 只能输出 sanitized preview / manifest。
6. 不写 `documents`、`chunks`、OpenSearch、Qdrant、MinIO、platform DB 或 Hermes DB。
7. 不接入 Agent final answer。
8. 不输出 secret、raw row、真实 NAS 路径、真实文件名、正文原文或敏感业务数据。

当前允许 Codex A 只做 Phase 2.80 docs selective Git baseline，不进入 Phase 2.80a。

## 必读文件

1. `docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md`
2. `docs/PHASE279A_SMALL_BATCH_NAS_SMOKE_RESULT.md`
3. `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md`
4. `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

## Baseline 前验证

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
```

## 只允许 stage 的文件

```text
docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md
docs/PHASE279A_SMALL_BATCH_NAS_SMOKE_RESULT.md
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
git add docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md \
  docs/PHASE279A_SMALL_BATCH_NAS_SMOKE_RESULT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git commit -m "docs: plan phase 2.80 scratch parser dry-run"
git tag phase-2.80-scratch-parser-dry-run-plan-baseline
git push origin main
git push origin phase-2.80-scratch-parser-dry-run-plan-baseline
```

完成 baseline 后停止，更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。

## 硬边界

禁止：

1. 执行 parser。
2. 复制真实文件。
3. 读取真实文件内容。
4. 写平台 DB / Hermes DB / `documents` / `chunks`。
5. 写 OpenSearch / Qdrant / MinIO。
6. 扫描 NAS。
7. Agent DB / NAS CRUD。
8. repair / cleanup source data / backfill / reindex / delete。
9. production rollout。
10. 进入 Phase 2.80a。

## Baseline 报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 验证命令结果。
6. 明确 Phase 2.80 只是 parser dry-run planning，不是 parser 执行授权。
7. 下一步是否建议进入 Phase 2.80a controlled parser dry-run。
