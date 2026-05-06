# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.44d explicit local issue dry-run route planning review，并批准进入 **docs-only Git baseline**。

## 当前状态

Phase 2.44d planning 已完成并通过 Codex B review：

1. `docs/PHASE244D_EXPLICIT_LOCAL_ISSUE_DRY_RUN_PLAN.md` 已定义 explicit local issue input 的前置条件、local-only 字段、recorder workflow、validation commands、review gate、Git/storage policy 与 stop conditions。
2. 后续真实 recorder workflow dry-run 只能在用户显式授权、人工准备、路径明确、Git ignored 确认后进行。
3. 本阶段未生成真实 issue records，未生成真实 Pilot report，未扫描真实 `reports/` / `reviews/`，未运行 API / CLI。
4. 本阶段未写 DB / facts / document_versions / OpenSearch / Qdrant，未进入 repair、rollout 或 Data Steward。

Codex B review 结论：

1. 规划边界正确。
2. 可进入 Phase 2.44d docs-only Git baseline。
3. 不允许进入 Phase 2.44e。
4. 不允许生成真实 issue records / Pilot report。

## 本轮目标

只做 Phase 2.44d docs-only Git baseline。

不得新增规划、不得写代码、不得运行 API / CLI、不得生成真实 report / issue records、不得进入下一 phase。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/PHASE244D_EXPLICIT_LOCAL_ISSUE_DRY_RUN_PLAN.md`
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

1. dirty 只包含 Phase 2.44d 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/agent_runs/latest.json` 被 Git ignore 命中。
3. 不存在真实 `reports/pilot_issues/*.json`、真实 Pilot report、API / CLI 输出或业务数据产物被 staged。

## 允许 stage 的文件

只能 stage 以下文件：

1. `docs/PHASE244D_EXPLICIT_LOCAL_ISSUE_DRY_RUN_PLAN.md`
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
3. `reports/pilot_issues/*.json`
4. `reports/mvp_pilot_reviews/*.json`
5. `app/**`
6. `scripts/**`
7. `tests/**`
8. `migrations/**`
9. Hermes 主仓库文件

stage 后必须运行：

```bash
git diff --cached --name-only
git diff --cached --check
```

如果 staged 文件超出白名单，立即 unstage 并停止。

## Commit / Tag / Push

commit message：

```text
docs: plan phase 2.44d explicit local issue dry-run
```

tag：

```text
phase-2.44d-explicit-local-issue-dry-run-plan-baseline
```

执行：

```bash
git commit -m "docs: plan phase 2.44d explicit local issue dry-run"
git tag phase-2.44d-explicit-local-issue-dry-run-plan-baseline
git push origin main
git push origin phase-2.44d-explicit-local-issue-dry-run-plan-baseline
```

## 硬边界

本轮禁止：

1. 进入 Phase 2.44e。
2. 生成真实 issue records。
3. 生成真实 Pilot report。
4. 默认扫描真实 `reports/` 或 `reviews/`。
5. 运行 API / CLI smoke。
6. 写 DB / facts / document_versions。
7. 修改 OpenSearch / Qdrant。
8. repair / backfill / reindex / cleanup / delete。
9. production rollout。
10. Data Steward / BIM 实现。
11. 外部 Linear / GitHub issue 创建。
12. 修改 retrieval contract 或 memory kernel 主架构。

## 完成后

更新 ignored `reports/agent_runs/latest.json`：

1. `status=baseline`
2. 记录 commit hash、tag、pushed=true。
3. 下一步建议只写为：等待 Codex B 确认 baseline 后，再由用户决定是否进入 Phase 2.44e explicit ignored local issue dry-run。

最终输出必须包含：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 确认未 stage / commit `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
6. 确认未生成真实 issue records / Pilot report。

完成 baseline 后停止，不得继续下一阶段。
