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

Phase 2.27c Review Audit Write Route Planning 收口与 Git baseline。

## 背景

Phase 2.27c 已由 Nightly Sprint Green Lane 完成规划：

1. 评审是否将 report review 事件真实写入 `audit_logs`。
2. 推荐路线：后续可进入 report-level sanitized audit 写入 MVP。
3. 真实写 `audit_logs` 属于 Yellow Lane，不能夜间自动实现。
4. Phase 2.27c 本轮只做规划与文档同步，未写功能代码。
5. 未写 DB、未写 `audit_logs`、未执行 repair / backfill / reindex。
6. 已写入 nightly run 记录：`reports/nightly_runs/20260427_024050.json`，该文件为 ignored 本地运行产物，不得提交。

## 当前应提交文件

只允许 stage 以下 Phase 2.27c planning 相关文件：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

## 不得提交

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/Hermes_memory/reports/nightly_runs/20260427_024050.json`
3. 任何 `reports/nightly_runs/*.json`
4. 任何真实 reports JSON
5. 任何真实 reviews JSON / Markdown
6. 任何业务代码变更

## 必须复核

1. `git status --short` 只包含 Phase 2.27c planning / handoff 相关文件。
2. `reports/agent_runs/latest.json` 仍被 `git check-ignore` 命中。
3. `reports/nightly_runs/*.json` 仍被 `git check-ignore` 命中。
4. 无真实运行产物被 staged。
5. 未写 `audit_logs`。
6. 未写业务 DB。
7. 未执行 repair / backfill / reindex。
8. Phase 2.27c 是 planning baseline，不是 audit write implementation。

## Git 要求

1. 只 stage “当前应提交文件”列表中的文件。
2. commit message：
   `docs: plan phase 2.27c review audit write route`
3. tag：
   `phase-2.27c-review-audit-write-route-baseline`
4. push `origin/main`。
5. push tag。

## 硬边界

1. 不实现 Phase 2.27d。
2. 不写 `audit_logs`。
3. 不写业务 DB。
4. 不修改 facts。
5. 不修改 `document_versions`。
6. 不修改 OpenSearch。
7. 不修改 Qdrant。
8. 不执行 repair / backfill / reindex。
9. 不进入 rollout。
10. 不提交 `latest.json` 或 nightly run JSON。

## 返回报告

请返回精简摘要：

1. 修改文件
2. commit hash
3. tag
4. push 结果
5. final git status
6. `latest.json` 是否 ignored
7. nightly run JSON 是否 ignored
8. 是否存在真实运行产物 staged
9. 是否建议进入 Phase 2.27d 实现
