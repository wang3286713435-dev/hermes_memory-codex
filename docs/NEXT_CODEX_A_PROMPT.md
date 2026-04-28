# Next Codex A Prompt

这是 Codex A 的下一轮固定任务入口。请读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.33 Internal MVP Pilot Day-1 Execution Packet docs baseline。

Codex B 已审核 Phase 2.33 Day-1 run sheet：

1. `docs/MVP_PILOT_DAY1_RUN_SHEET.md` 已覆盖 Day-1 目标、角色、时间表、alias 绑定、10 条最小 query set、输出保存字段、人工复核、问题分级与 Go / Pause。
2. 本阶段未写代码、未写 DB、未改索引、未进入 repair 或 rollout。
3. 文档符合当前内部受控 MVP Pilot 边界。

本轮只做 Git baseline，不写功能代码。

## 必须先读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
6. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_DAY1_RUN_SHEET.md`
7. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
8. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
9. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## Stage 白名单

只允许 stage 以下文件：

1. `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/HANDOFF_LOG.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage：

1. `reports/agent_runs/latest.json`
2. `reports/nightly_runs/*.json`
3. 任何代码、脚本、测试、真实 report、真实 review record。

## 验证要求

运行：

```bash
git status --short
git diff --check
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/nightly_runs/test.json
```

不运行 pytest，本轮为 docs-only baseline。

## Git baseline

如果 dirty 仅包含白名单文件：

```bash
git add <white-listed files only>
git commit -m "docs: baseline pilot day1 run sheet"
git tag phase-2.33-pilot-day1-run-sheet-baseline
git push origin main
git push origin phase-2.33-pilot-day1-run-sheet-baseline
```

baseline 后必须更新：

1. `docs/ACTIVE_PHASE.md`
2. `docs/HANDOFF_LOG.md`
3. `docs/PHASE_BACKLOG.md`
4. `reports/agent_runs/latest.json`

baseline 后停止，等待 Codex B。不得自动进入 Phase 2.34 或 production rollout。

## 硬禁止

1. 不写代码。
2. 不改 API / retrieval / ingestion / facts。
3. 不写业务 DB。
4. 不修改 OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / cleanup / delete。
6. 不进入 production rollout。
7. 不创建 production cron / scheduler。
8. 不自动创建 Linear / GitHub issue。
9. 不自动继续下一阶段。

## 返回报告

返回：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 是否需要 Codex B / Codex C。
