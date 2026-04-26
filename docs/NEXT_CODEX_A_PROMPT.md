# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。

当用户要求“执行 `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`”时，Codex A 必须读取本文件中的完整任务说明，而不是依赖聊天窗口中的长 prompt。

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

除非本文件明确要求 baseline，否则不要提交 Git。

## 本轮目标

Phase 2.27b 最小实现：review record sanitized audit payload preview / dry-run。

## 背景

Phase 2.27b 规划已完成：

1. 推荐先做 report-level sanitized audit payload preview。
2. 不直接写 `audit_logs`。
3. 不写 notes。
4. 不写 reasons。
5. 不写 `approved_action`。
6. 不写完整 `item_decisions`。
7. 不写 report 原文。
8. 不写本机绝对路径。
9. `executable=false` 必须稳定保留。
10. `approved_for_manual_action` 仍不等于 executed。

## 建议新增脚本

`/Users/Weishengsu/Hermes_memory/scripts/phase227b_review_audit_preview.py`

## 建议新增测试

`/Users/Weishengsu/Hermes_memory/tests/test_phase227b_review_audit_preview.py`

## 功能要求

1. 输入本地 review record JSON。
2. 输出 sanitized audit payload JSON。
3. 只做 preview / dry-run。
4. 不写 `audit_logs`。
5. 不写业务 DB。
6. 不修改 review record。
7. 不执行 repair。

输入 review record 可来自 Phase 2.27a 格式：

1. `review_id`
2. `report_path`
3. `report_type`
4. `report_hash`
5. `reviewer`
6. `reviewed_at`
7. `status`
8. `notes`
9. `item_decisions`
10. `executable=false`
11. `dry_run=true`
12. `destructive_actions=[]`

## 输出 audit payload 字段

```json
{
  "dry_run": true,
  "event_type": "report.review.created",
  "review_id": "...",
  "report_hash": "...",
  "report_type": "...",
  "review_status": "...",
  "reviewer": "...",
  "reviewed_at": "...",
  "summary": {
    "items_total": 0,
    "approved_count": 0,
    "rejected_count": 0,
    "deferred_count": 0,
    "needs_review_count": 0
  },
  "executable": false,
  "would_write_audit_logs": false
}
```

## 必须排除字段

1. `notes`
2. `reason`
3. `approved_action`
4. 完整 `item_decisions`
5. report 原文
6. `report_path` 的本机绝对路径
7. source `document_id` / `fact_id` 等 item-level entity details

## CLI 建议

1. `--review-record <path>`
2. `--json`
3. `--fail-on-unsafe-field`
4. `--dry-run-preview` 默认 true
5. `--output-file <path>` 可选，但默认只 stdout

如果支持 `--output-file`：

1. 输出文件也必须视为本地产物，不入 Git。
2. 不得默认写入 repo tracked 路径。

## 安全校验

1. payload 中出现 `notes` / `reason` / `approved_action` / `item_decisions` 时失败。
2. `report_path` 是绝对路径时不得进入 payload。
3. review record `executable=true` 时失败。
4. review record `dry_run=false` 时失败。
5. `destructive_actions` 非空时失败。

## 测试要求

1. sanitized payload shape。
2. `notes` / `reason` / `approved_action` 不进入 payload。
3. 完整 `item_decisions` 不进入 payload。
4. 本机绝对 `report_path` 不进入 payload。
5. `executable=false`、`dry_run=true`、`would_write_audit_logs=false`。
6. unsafe review record 被拒绝。
7. `approved_for_manual_action` 不被描述为 executed。

## Live Smoke

1. `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`
2. `uv run pytest tests/test_phase227b_review_audit_preview.py -q`
3. 使用临时目录 fake review record 执行 preview。
4. 确认 stdout payload 不含 `notes` / `reason` / `approved_action` / `item_decisions` / 绝对路径。
5. 不写 DB。
6. 不生成真实 audit payload 文件，除非在 tmp 目录。

## 硬边界

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts。
4. 不修改 `document_versions`。
5. 不修改 OpenSearch。
6. 不修改 Qdrant。
7. 不执行 repair / backfill / reindex。
8. 不进入 rollout。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。

## 文档同步

更新：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE227B_REVIEW_AUDIT_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 执行要求

1. 不提交 Git，除非本文件明确要求 baseline。
2. 不写 `audit_logs`。
3. 不写业务 DB。
4. 不修改 facts。
5. 不修改 `document_versions`。
6. 不修改 OpenSearch。
7. 不修改 Qdrant。
8. 不执行 repair / backfill / reindex。
9. 不进入 rollout。
10. 返回精简摘要。
11. 必须更新交接文件。
