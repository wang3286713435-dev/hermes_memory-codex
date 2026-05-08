# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。请只做 Phase 2.55 Internal MVP Real Upload Smoke Planning docs-only Git baseline。不要进入 Phase 2.55a，不要执行真实 upload，不要运行 API / CLI smoke。

## 1. 背景

Phase 2.55 docs-only planning 已完成并通过 Codex B review。

新增规划文档：

`/Users/Weishengsu/Hermes_memory/docs/PHASE255_INTERNAL_MVP_REAL_UPLOAD_SMOKE_PLAN.md`

Codex B review 结论：

1. 规划方向正确：从已有文件验收推进到小型非敏感单文件真实导入 smoke。
2. 边界清楚：本轮没有执行 upload、API / CLI smoke、DB / index 写入。
3. Phase 2.55a 授权门槛清楚：必须由用户提供非敏感文件路径并显式授权。
4. Data Steward / BIM / NAS / TB 文件池明确后置。
5. 不影响当前内部 MVP 主线。

## 2. 本轮目标

执行 Phase 2.55 docs-only Git baseline。

建议 commit message：

`docs: plan phase 2.55 internal mvp upload smoke`

建议 tag：

`phase-2.55-internal-mvp-upload-smoke-plan-baseline`

## 3. 允许 stage / commit 的文件

只允许 stage 以下 Hermes_memory 文件：

1. `docs/PHASE255_INTERNAL_MVP_REAL_UPLOAD_SMOKE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/NEXT_CODEX_C_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

`reports/agent_runs/latest.json` 是 ignored 本地状态，只更新，不 stage。

## 4. 禁止 stage / 修改的既有 dirty

禁止纳入：

- `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

如果 staged 文件超出白名单，必须停止并 reset staged，不要 commit。

## 5. baseline 前检查

在 `/Users/Weishengsu/Hermes_memory` 运行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

本轮 docs-only，不运行 pytest，不运行 API / CLI smoke，不启动服务，不上传文件。

## 6. Git 操作

1. 只 stage 白名单文件。
2. commit。
3. tag `phase-2.55-internal-mvp-upload-smoke-plan-baseline`。
4. push 当前分支到 `origin`。
5. push tag 到 `origin`。

## 7. 完成后更新 ignored latest

更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `status=baseline`
2. 写入 commit hash。
3. 写入 tag。
4. 写入 push 结果。
5. 写入最终 git status。
6. `needs_codex_b_review=false`
7. `needs_codex_c_validation=false`

仍不要 stage `latest.json`。

## 8. 完成后输出

请输出：

1. staged 文件。
2. 检查结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 是否建议进入下一阶段。

完成 baseline 后停止。不要进入 Phase 2.55a；Phase 2.55a 必须等待用户提供小型非敏感文件路径并明确授权。
