# Next Codex A Prompt

这是 Codex A 的下一轮固定任务入口。请读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.31 internal controlled MVP Pilot operations + Nightly Sprint launcher docs baseline。

Codex B 已复核 Phase 2.31 文档方向正确：

1. 内部受控 MVP Pilot 操作规划已完成。
2. 使用者指南、反馈模板、known risks checklist 已完成。
3. 本轮仍不进入 production rollout。
4. Nightly Sprint 原问题已定位：协议文件不会自己唤醒 Codex A；需要固定启动入口。
5. 本轮已新增 `docs/NIGHTLY_CODEX_A_PROMPT.md` 并更新队列。

本轮只做 Git baseline，不写功能代码。

## 必须先读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_CODEX_A_PROMPT.md`
3. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_PROTOCOL.md`
4. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
9. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
10. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## Stage 白名单

只允许 stage 以下文件：

1. `docs/PHASE231_INTERNAL_MVP_PILOT_OPERATIONS_PLAN.md`
2. `docs/MVP_PILOT_USER_GUIDE.md`
3. `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md`
4. `docs/MVP_PILOT_KNOWN_RISKS.md`
5. `docs/NIGHTLY_CODEX_A_PROMPT.md`
6. `docs/NIGHTLY_SPRINT_PROTOCOL.md`
7. `docs/NIGHTLY_SPRINT_QUEUE.md`
8. `docs/AGENT_OPERATING_PROTOCOL.md`
9. `docs/ACTIVE_PHASE.md`
10. `docs/HANDOFF_LOG.md`
11. `docs/PHASE_BACKLOG.md`
12. `docs/NEXT_CODEX_A_PROMPT.md`
13. `docs/TODO.md`
14. `docs/DEV_LOG.md`

不得 stage：

1. `reports/agent_runs/latest.json`
2. `reports/nightly_runs/*.json`
3. 任何代码、脚本、测试、真实 report、真实 review record。

## 验证要求

运行：

```bash
git status --short
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/nightly_runs/test.json
```

不运行 pytest，本轮为 docs-only baseline。

## Git baseline

如果 dirty 仅包含白名单文件：

```bash
git add <white-listed files only>
git commit -m "docs: baseline pilot ops and nightly launcher"
git tag phase-2.31-pilot-ops-nightly-launcher-baseline
git push origin main
git push origin phase-2.31-pilot-ops-nightly-launcher-baseline
```

baseline 后必须更新：

1. `docs/ACTIVE_PHASE.md`
2. `docs/HANDOFF_LOG.md`
3. `docs/PHASE_BACKLOG.md`
4. `reports/agent_runs/latest.json`

如从 `docs/NIGHTLY_CODEX_A_PROMPT.md` 启动，且 `NIGHTLY_SPRINT_QUEUE.md` 当前 Item 1 明确 `continue_after_success=true`，baseline 成功后可以继续执行 Item 2：Phase 2.32 MVP Pilot feedback intake planning。

如果不是 Nightly Sprint 启动，baseline 后停止，等待 Codex B。

## 硬禁止

1. 不写代码。
2. 不改 API / retrieval / ingestion / facts。
3. 不写业务 DB。
4. 不修改 OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / cleanup / delete。
6. 不进入 production rollout。
7. 不创建 production cron / scheduler。
8. 不自动进入不在 `NIGHTLY_SPRINT_QUEUE.md` 中的阶段。

## 返回报告

返回：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 是否继续执行 Nightly Sprint Item 2。
6. 是否需要 Codex B / Codex C。
