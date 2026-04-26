# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件中的完整任务说明，而不是依赖聊天窗口中的长 prompt。

执行前必须读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PRD.md`
5. `/Users/Weishengsu/Hermes_memory/docs/ROADMAP.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TECHNICAL_DESIGN.md`
7. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
8. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

执行结束必须更新：

1. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
2. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 本轮目标

Phase 2.27b review audit payload preview / dry-run 收口与 Git baseline。

## 背景

Phase 2.27b 最小实现已由文件化 prompt 交接成功完成：

1. 新增 `scripts/phase227b_review_audit_preview.py`。
2. 新增 `tests/test_phase227b_review_audit_preview.py`。
3. sanitized audit payload preview 只输出 report-level summary。
4. 固定 `dry_run=true`、`executable=false`、`would_write_audit_logs=false`。
5. 已排除 `notes`、`reason`、`approved_action`、完整 `item_decisions`、report 原文、本机绝对路径与 item-level entity details。
6. unsafe review record 会被拒绝：`executable=true`、`dry_run=false`、`destructive_actions` 非空均失败。

已通过验证：

1. `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`
2. `uv run pytest tests/test_phase227b_review_audit_preview.py -q`
3. 测试结果：`10 passed`
4. 临时目录 fake review record preview 通过。
5. stdout payload 未包含敏感字段、绝对路径、entity id 或 `executed`。
6. 未写 DB。
7. 未写 `audit_logs`。
8. 未生成真实 audit payload 文件。

## 当前应提交文件

只允许 stage 以下 Phase 2.27b 相关文件：

1. `/Users/Weishengsu/Hermes_memory/scripts/phase227b_review_audit_preview.py`
2. `/Users/Weishengsu/Hermes_memory/tests/test_phase227b_review_audit_preview.py`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE227B_REVIEW_AUDIT_PLAN.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
7. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

## 不得提交

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. 任何真实 audit payload JSON
3. 任何真实 review JSON / Markdown
4. 任何 `reports/nightly_runs/*.json`
5. 任何无关业务代码或运行产物

## 必须复跑

```bash
cd /Users/Weishengsu/Hermes_memory
uv run python -m py_compile scripts/phase227b_review_audit_preview.py
uv run pytest tests/test_phase227b_review_audit_preview.py -q
```

## 必须复核

1. `git status --short` 只包含 Phase 2.27b baseline 相关文件。
2. `reports/agent_runs/latest.json` 仍被 `git check-ignore` 命中。
3. 无真实运行产物被 staged。
4. 未写 `audit_logs`。
5. 未写业务 DB。
6. 未执行 repair / backfill / reindex。
7. `approved_for_manual_action` 未被描述为 executed。

## Git 要求

1. 只 stage “当前应提交文件”列表中的文件。
2. commit message：
   `chore: add phase 2.27b review audit preview`
3. tag：
   `phase-2.27b-review-audit-preview-baseline`
4. push `origin/main`。
5. push tag。

## 硬边界

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts。
4. 不修改 `document_versions`。
5. 不修改 OpenSearch。
6. 不修改 Qdrant。
7. 不执行 repair / backfill / reindex。
8. 不进入 rollout。
9. 不提交 `latest.json` 或真实运行产物。
10. 不自动进入 Phase 2.27c。

## 返回报告

请返回精简摘要：

1. 修改文件
2. 测试结果
3. commit hash
4. tag
5. push 结果
6. final git status
7. `latest.json` 是否 ignored
8. 是否存在真实运行产物 staged
9. 是否建议进入下一阶段规划
