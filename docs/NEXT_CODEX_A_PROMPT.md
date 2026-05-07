# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.45d Mac mini Real-machine Deployment Record Planning review，并批准进入 **docs-only Git baseline**。

## 当前状态

Phase 2.45d planning 已完成并通过 Codex B review：

1. 新增 `docs/PHASE245D_MAC_MINI_DEPLOYMENT_RECORD_PLAN.md`。
2. Planning 覆盖 real-machine deployment record inputs、output schema、operator checklist、stop conditions、storage policy、Phase 2.45c runner relationship 与 future phase candidates。
3. 规划明确 deployment record 是人工记录 / operator sign-off 模板，不是 deployment script。
4. 真实部署、真实 API / CLI smoke、Phase 2.45c runner、service restart、migration、repair / backfill / reindex / cleanup / delete、DB / facts / document_versions / audit_logs / OpenSearch / Qdrant 写入均未执行。

Codex B review 结论：

1. 文档边界正确。
2. `docs/PHASE245D_MAC_MINI_DEPLOYMENT_RECORD_PLAN.md` 未把 deployment record 误写成真实部署授权。
3. storage policy 明确真实 deployment record JSON / Markdown future local ignored。
4. stop conditions 覆盖 health-check fail、Qdrant/env 错误、secret exposure、unknown dirty、evidence P0、repair/reindex/write DB/rollout 请求。
5. 可进入 Phase 2.45d docs-only Git baseline。
6. 不允许进入 Phase 2.45e。

## 本轮目标

只做 Phase 2.45d docs-only Git baseline。

不得新增功能、不得新增 deployment script、不得运行 Phase 2.45c runner、不得运行真实 API / CLI smoke、不得执行真实 Mac mini deployment、不得进入 Phase 2.45e。

## 必须复跑

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 只包含 Phase 2.45d 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/agent_runs/latest.json` 被 Git ignore 命中。
3. 没有 scripts / tests / app / migrations / real reports / `.env` 被 staged。
4. 没有真实 deployment record JSON / Markdown 被 staged。

不得运行：

1. pytest。
2. Phase 2.45c runner。
3. API / CLI smoke。
4. Hermes CLI chat。
5. real deployment commands。

## 允许 stage 的文件

只能 stage 以下文件：

1. `docs/PHASE245D_MAC_MINI_DEPLOYMENT_RECORD_PLAN.md`
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
3. `scripts/**`
4. `tests/**`
5. `app/**`
6. `migrations/**`
7. Hermes 主仓库
8. 真实 reports / reviews / run JSON
9. `.env` 或 secret-bearing 文件

## Commit / Tag / Push

如果且仅如果 staged 文件完全匹配白名单，则执行：

```bash
git add docs/PHASE245D_MAC_MINI_DEPLOYMENT_RECORD_PLAN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md
git commit -m "docs: plan phase 2.45d deployment record"
git tag phase-2.45d-deployment-record-plan-baseline
git push origin main
git push origin phase-2.45d-deployment-record-plan-baseline
```

## 硬边界

1. 不进入 Phase 2.45e。
2. 不执行真实部署。
3. 不运行 Phase 2.45c runner。
4. 不运行真实 API / CLI smoke。
5. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
6. 不执行 repair / backfill / reindex / cleanup / delete。
7. 不新增 deployment script。
8. 不进入 rollout / Data Steward。
9. 不修改 retrieval contract。
10. 不修改 memory kernel 主架构。

## Baseline 后更新

baseline 成功后更新 ignored `reports/agent_runs/latest.json`：

1. `phase=Phase 2.45d Mac mini Real-machine Deployment Record Planning Baseline`
2. `status=baseline`
3. `git.commit=<new_commit>`
4. `git.tag=phase-2.45d-deployment-record-plan-baseline`
5. `git.pushed=true`
6. `needs_codex_b_review=false`
7. `next_recommendation=进入 Phase 2.45e 前先由 Codex B 检查 baseline 状态；不自动进入下一阶段。`

## 返回要求

返回精简报告：

1. 修改文件。
2. 验证结果。
3. commit hash / tag / push 结果。
4. final `git status --short`。
5. 是否进入下一阶段：否，baseline 后停止等待 Codex B / 用户。
