# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.45b Health-check / Deploy-smoke Dry-run Planning review，并批准进入 **docs-only Git baseline**。

## 当前状态

Phase 2.45b planning 已完成并通过 Codex B review：

1. 已新增 `docs/PHASE245B_HEALTH_CHECK_DRY_RUN_PLAN.md`。
2. Planning 覆盖 Git / `.env` key-name / NAS / external SSD / Postgres / OpenSearch / Qdrant / API `/health` / Hermes CLI / ignored runtime path 候选检查。
3. Planning 覆盖 MVP smoke candidates、JSON output schema、stop conditions、human-only 与 future bounded script 边界。
4. 本阶段未写功能代码，未新增 health-check script，未新增 deployment script，未运行 API / CLI，未执行真实部署。
5. 本阶段未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。

Codex B review 结论：

1. 规划边界正确。
2. 可进入 Phase 2.45b docs-only Git baseline。
3. 不允许进入 Phase 2.45c。
4. 不允许新增 health-check script、deployment script、真实 smoke 或真实 Mac mini 部署。

## 本轮目标

只做 Phase 2.45b docs-only Git baseline。

不得新增规划、不得写代码、不得新增脚本、不得运行 API / CLI、不得执行真实部署、不得进入下一 phase。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/PHASE245B_HEALTH_CHECK_DRY_RUN_PLAN.md`
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

1. dirty 只包含 Phase 2.45b 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/agent_runs/latest.json` 被 Git ignore 命中。
3. 不存在 health-check script、deployment script、真实 API / CLI 输出、真实部署记录、DB/index/data 产物被 staged。

## 允许 stage 的文件

只能 stage 以下文件：

1. `docs/PHASE245B_HEALTH_CHECK_DRY_RUN_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage：

1. `reports/agent_runs/latest.json`
2. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
3. `app/**`
4. `scripts/**`
5. `tests/**`
6. `migrations/**`
7. Hermes 主仓库
8. 任何真实 reports / reviews / run JSON

## Commit / Tag / Push

如果且仅如果 staged 文件完全匹配白名单，则执行：

```bash
git commit -m "docs: add phase 2.45b health check dry run plan"
git tag phase-2.45b-health-check-dry-run-plan-baseline
git push origin main
git push origin phase-2.45b-health-check-dry-run-plan-baseline
```

## 硬边界

本轮禁止：

1. 进入 Phase 2.45c。
2. 新增 health-check script。
3. 新增 deployment script。
4. 执行真实 Mac mini 部署。
5. 运行 API / CLI smoke。
6. 写 DB / facts / document_versions。
7. 修改 OpenSearch / Qdrant。
8. repair / backfill / reindex / cleanup / delete。
9. production rollout。
10. Data Steward / BIM 实现。
11. 创建 production scheduler / cron。
12. 修改 retrieval contract 或 memory kernel 主架构。

## 完成后

更新 ignored `reports/agent_runs/latest.json`：

1. `status=baseline`
2. 记录 commit hash、tag、pushed=true。
3. 下一步建议只写为：等待 Codex B 确认 baseline 后，再由用户决定是否进入 Phase 2.45c read-only health-check script implementation。

最终输出必须包含：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 确认未 stage / commit `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
6. 确认未新增 health-check script、deployment script，未执行真实部署。

完成 baseline 后停止，不得继续下一阶段。
