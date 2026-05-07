# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.45a Mac mini MVP deployment runbook artifact review，并批准进入 **docs-only Git baseline**。

## 当前状态

Phase 2.45a runbook artifact 已完成并通过 Codex B review：

1. `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md` 已新增。
2. Runbook 覆盖 Day-0 准备、目录创建、env / secrets、repo checkout、服务启动顺序、部署 / 热更新、minimum smoke、备份 / 回滚、stop conditions 与 operator sign-off。
3. Runbook 明确这是人工部署 checklist，不是 production rollout，不是自动部署工具。
4. 本阶段未写功能代码，未新增 deployment script，未运行 API / CLI，未执行真实部署。
5. 本阶段未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。

Codex B review 结论：

1. Runbook 边界正确。
2. 可进入 Phase 2.45a docs-only Git baseline。
3. 不允许进入 Phase 2.45b。
4. 不允许执行真实 Mac mini 部署或新增部署脚本。

## 本轮目标

只做 Phase 2.45a docs-only Git baseline。

不得新增规划、不得写代码、不得新增脚本、不得运行 API / CLI、不得执行真实部署、不得进入下一 phase。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`
8. `reports/agent_runs/latest.json`

## Baseline 前检查

运行：

```bash
git status --short
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 只包含 Phase 2.45a 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/agent_runs/latest.json` 被 Git ignore 命中。
3. 不存在 deployment script、真实 API / CLI 输出、真实部署记录、DB/index/data 产物被 staged。

## 允许 stage 的文件

只能 stage 以下文件：

1. `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

必须显式排除：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`
3. `app/**`
4. `scripts/**`
5. `tests/**`
6. `migrations/**`
7. Hermes 主仓库文件

stage 后必须运行：

```bash
git diff --cached --name-only
git diff --cached --check
```

如果 staged 文件超出白名单，立即 unstage 并停止。

## Commit / Tag / Push

commit message：

```text
docs: add phase 2.45a mac mini deployment runbook
```

tag：

```text
phase-2.45a-mac-mini-deployment-runbook-baseline
```

执行：

```bash
git commit -m "docs: add phase 2.45a mac mini deployment runbook"
git tag phase-2.45a-mac-mini-deployment-runbook-baseline
git push origin main
git push origin phase-2.45a-mac-mini-deployment-runbook-baseline
```

## 硬边界

本轮禁止：

1. 进入 Phase 2.45b。
2. 新增 deployment script。
3. 执行真实 Mac mini 部署。
4. 运行 API / CLI smoke。
5. 写 DB / facts / document_versions。
6. 修改 OpenSearch / Qdrant。
7. repair / backfill / reindex / cleanup / delete。
8. production rollout。
9. Data Steward / BIM 实现。
10. 创建 production scheduler / cron。
11. 修改 retrieval contract 或 memory kernel 主架构。

## 完成后

更新 ignored `reports/agent_runs/latest.json`：

1. `status=baseline`
2. 记录 commit hash、tag、pushed=true。
3. 下一步建议只写为：等待 Codex B 确认 baseline 后，再由用户决定是否进入 Phase 2.45b health-check / deploy-smoke dry-run planning。

最终输出必须包含：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 确认未 stage / commit `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
6. 确认未新增 deployment script、未执行真实部署。

完成 baseline 后停止，不得继续下一阶段。
