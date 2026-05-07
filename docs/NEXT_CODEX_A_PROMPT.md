# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已 review Phase 2.51b Minimal Mac Mini Operator Command Sheet Artifact，结论：通过。下一轮只允许做 docs-only Git baseline，收口 Phase 2.52 route planning 与 Phase 2.51b command sheet。

## 本轮目标

Phase 2.51b Minimal Mac Mini Operator Command Sheet Git Baseline。

只做 selective staging / commit / tag / push；不进入 Phase 2.51a、Phase 2.50b、真实 Mac Mini deployment、API / CLI smoke、repair、rollout 或 Data Steward。

## Codex B Review 结论

通过，理由：

1. `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md` 明确是 internal controlled MVP operator sheet，不是 production rollout / 客户交付 / 自动审标 / 自动投标 / 自动经营决策。
2. command sheet 覆盖 pre-check、repo state、hot update、health checks、daily run record、Phase 2.49 review command、rollback、stop conditions 与 never-do。
3. canonical run record 口径正确：`reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`。
4. optional Markdown notes 口径正确：`reports/internal_mvp_runs/<YYYYMMDD>_<session>_notes.md`，且不得作为 Phase 2.49 bridge input。
5. 文档明确命令只是模板；本阶段未执行真实命令、未启动服务、未读取真实 run record、未写 DB / index、未 repair、未 rollout。
6. 轻量校验已通过：`git diff --check`、`latest.json` JSON check、ignored report path checks。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
git check-ignore -v reports/deployment_records/example.json
git check-ignore -v reports/deployment_records/example.md
```

## 允许 stage 的文件

只允许 stage 以下文件：

1. `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`
2. `docs/PHASE252_POST_RUNBOOK_ROUTE_PLAN.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

## 必须排除 / 不得 stage

以下文件不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`
5. 任何 `reports/internal_mvp_runs/**/*.json`
6. 任何 `reports/internal_mvp_runs/**/*.md`
7. 任何 `reports/internal_mvp_runs/latest.*`
8. 任何 `reports/deployment_records/**/*.json`
9. 任何 `reports/deployment_records/**/*.md`
10. 任何真实 reports / reviews / run records。

## Baseline 操作

只在 staged 文件完全等于白名单时继续。

```bash
cd /Users/Weishengsu/Hermes_memory
git add docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md \
  docs/PHASE252_POST_RUNBOOK_ROUTE_PLAN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git diff --cached --name-only
```

确认 staged 仅上述 9 个文件后：

```bash
git commit -m "docs: baseline phase 2.51b mac mini operator command sheet"
git tag phase-2.51b-mac-mini-operator-command-sheet-baseline
git push origin main
git push origin phase-2.51b-mac-mini-operator-command-sheet-baseline
```

## Baseline 后复核

```bash
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
```

允许最终仍显示 out-of-scope dirty / untracked only if 它们是：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`

如果出现其他 dirty，停止并写交接。

## 硬禁止

1. 不写功能代码。
2. 不新增 / 修改 scripts 或 tests。
3. 不执行真实 Mac Mini deployment。
4. 不启动 / 停止服务。
5. 不运行 API / CLI smoke。
6. 不读取真实 reports / run records。
7. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
8. 不执行 repair / backfill / reindex / cleanup / delete / migration。
9. 不进入 production rollout。
10. 不进入 Data Steward / BIM 实现。
11. 不修改 retrieval contract。
12. 不修改 memory kernel 主架构。
13. baseline 后不得自动进入 Phase 2.51a / 2.50b / 2.53。

## 完成后状态

更新 `reports/agent_runs/latest.json`（ignored）：

1. `phase=Phase 2.51b Minimal Mac Mini Operator Command Sheet Git Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push 结果。
4. `needs_codex_b_review=false`
5. `needs_codex_c_validation=false`
6. 下一步建议：进入下一阶段规划，优先在 Phase 2.51a fake deployment record dry-run smoke、Phase 2.50b evidence pack planning、或继续内部 MVP operator evidence 之间择一；仍不进入 rollout。

完成后停止，等待 Codex B / 用户检查。
