# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
7. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
8. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 本轮目标

Phase 2.27d report-level sanitized review audit write MVP 收口与 Git baseline。

这是 Yellow Lane baseline 任务。只允许固化已经完成并通过验证的 Phase 2.27d 变更；不得继续进入 Phase 2.27e 或其他新实现。

## 当前已验证事实

Codex B 已复核当前交接与轻量验证：

1. `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`：通过。
2. `uv run pytest tests/test_phase227b_review_audit_preview.py -q`：`15 passed`。
3. `reports/agent_runs/latest.json` 被 `.gitignore` 命中。
4. `reports/nightly_runs/*.json` 被 `.gitignore` 命中。
5. 当前实现只在显式 `--write-audit` 时写入 report-level sanitized `audit_logs`。
6. 默认 preview-only，不写 DB。
7. 临时 SQLite smoke 已通过；未写生产 / 真实业务 DB。
8. 未修改 facts、document_versions、OpenSearch、Qdrant。
9. 未执行 repair、backfill、reindex、cleanup、delete、rollout。

## 允许纳入 baseline 的文件

只能 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/scripts/phase227b_review_audit_preview.py`
2. `/Users/Weishengsu/Hermes_memory/tests/test_phase227b_review_audit_preview.py`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
7. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

不得 stage：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/Hermes_memory/reports/nightly_runs/*.json`
3. 任何真实 report / review JSON 产物
4. 任何未列入上方白名单的文件

## Baseline 前复核

执行：

```bash
git status --short
uv run python -m py_compile scripts/phase227b_review_audit_preview.py
uv run pytest tests/test_phase227b_review_audit_preview.py -q
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 范围仅限 Phase 2.27d 允许文件与 ignored local state。
2. 测试仍为 `15 passed`。
3. `latest.json` 仍 ignored。
4. 无真实 reports / reviews JSON 被追踪或 staged。
5. 无生产 / 真实业务 DB 写入。
6. 无 facts / document_versions / OpenSearch / Qdrant mutation。
7. 无 repair / backfill / reindex / cleanup / delete / rollout。

## Git 操作

如果复核通过：

```bash
git add \
  scripts/phase227b_review_audit_preview.py \
  tests/test_phase227b_review_audit_preview.py \
  docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git diff --cached --name-only
git commit -m "chore: add phase 2.27d review audit write mvp"
git tag phase-2.27d-review-audit-write-baseline
git push origin main
git push origin phase-2.27d-review-audit-write-baseline
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
  "phase": "Phase 2.27d Report-level Review Audit Write MVP",
  "status": "baseline",
  "git": {
    "commit": "<actual_commit_hash>",
    "tag": "phase-2.27d-review-audit-write-baseline",
    "pushed": true
  },
  "next_recommendation": "Return to Codex B for Phase 2.27e route planning. Do not auto-enter the next phase."
}
```

## 停止条件

完成 baseline 后必须停止，不得继续执行 Nightly Sprint 下一个 item。

必须停止并报告的情况：

1. dirty 文件超出白名单。
2. 测试失败。
3. `latest.json` 或 nightly run JSON 准备被 staged。
4. 需要写真实业务 DB。
5. 需要 repair / backfill / reindex / cleanup / delete。
6. 需要进入 rollout。
7. 需要修改 facts / document_versions / OpenSearch / Qdrant。
8. 需要进入 Phase 2.27e 或其他新阶段实现。

## 返回报告格式

请返回精简报告：

1. 修改文件
2. 测试结果
3. commit hash
4. tag
5. push 结果
6. 最终 `git status --short`
7. 是否仍有阻塞 / 风险
8. 是否建议进入 Phase 2.27e 规划

不要执行 repair executor、rollout、真实业务数据修改或自动下一阶段开发。
