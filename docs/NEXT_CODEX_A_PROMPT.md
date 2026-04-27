# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 本轮目标

Phase 2.27e Review Audit Eval Route Planning 收口与 Git baseline。

本轮只做规划文档基线固化，不写功能代码，不写 DB，不执行 eval，不执行 repair。

## 当前已确认事实

1. Phase 2.27e 规划已完成。
2. 新增规划文档：`docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`。
3. 推荐路线：优先做 deterministic eval / unit test 安全断言，以及 readiness audit 只读检查。
4. archive / review / audit 关联诊断为第二优先级。
5. item-level audit summary、完整 review record 入库、repair executor 与 rollout 继续后置。
6. 本轮未修改 Python 代码。
7. 本轮未写 `audit_logs`。
8. 本轮未写真实业务 DB。
9. 本轮未修改 facts、document_versions、OpenSearch、Qdrant。

## 只允许 stage 以下文件

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

不得 stage：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/Hermes_memory/reports/nightly_runs/*.json`
3. 任何真实 report / review JSON
4. 任何业务代码文件
5. 任何未列入白名单的文件

## Baseline 前复核

执行：

```bash
git status --short
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 范围仅为 Phase 2.27e 规划文档、交接文档与 ignored local state。
2. `reports/agent_runs/latest.json` 仍被 ignored。
3. 无 Python 代码变更。
4. 无真实 report / review / nightly JSON 被 staged。
5. 无 DB / index / facts / version 数据变更。
6. 无 repair / backfill / reindex / cleanup / delete / rollout。

本轮不需要运行 pytest；如运行，必须说明原因。

## Git 操作

如果复核通过：

```bash
git add \
  docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git diff --cached --name-only
git commit -m "docs: plan phase 2.27e review audit eval"
git tag phase-2.27e-review-audit-eval-plan-baseline
git push origin main
git push origin phase-2.27e-review-audit-eval-plan-baseline
```

## 交接更新

baseline 成功后更新：

1. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
2. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

`latest.json` 写入：

```json
{
  "phase": "Phase 2.27e Review Audit Eval Route Planning",
  "status": "baseline",
  "git": {
    "commit": "<actual_commit_hash>",
    "tag": "phase-2.27e-review-audit-eval-plan-baseline",
    "pushed": true
  },
  "next_recommendation": "Return to Codex B for Phase 2.27e minimal implementation prompt. Do not auto-enter implementation."
}
```

## 停止条件

完成 baseline 后必须停止，不得进入实现。

必须停止并报告：

1. dirty 文件超出白名单。
2. 需要修改 Python 代码。
3. 需要写 `audit_logs`。
4. 需要写真实业务 DB。
5. 需要运行 repair / backfill / reindex / cleanup / delete。
6. 需要修改 facts、document_versions、OpenSearch、Qdrant。
7. 需要进入 rollout。
8. 需要自动进入 Phase 2.27e 实现。

## 返回报告格式

请返回精简报告：

1. 修改文件
2. 测试与验证结果
3. commit hash
4. tag
5. push 结果
6. 最终 `git status --short`
7. 是否仍有阻塞 / 风险
8. 是否建议进入 Phase 2.27e 最小实现

不要执行 repair executor、rollout、真实业务数据修改或自动下一阶段开发。
