# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`

## 当前状态

Phase 2.37 Pilot Issue Intake / Triage planning 已完成并通过 Codex B review。

Codex B review 结论：

1. 规划方向正确：优先建立 issue intake / triage，而不是继续盲修单个 tender deep-field recall 问题。
2. issue schema、issue_type、P0/P1/P2/P3 priority、Go / Pause 规则与非目标边界清晰。
3. 规划没有要求写 DB、facts、document_versions、OpenSearch / Qdrant，也没有进入 repair、rollout 或自动审标。
4. 推荐 Phase 2.37a：local issue intake schema / templates / dry-run validator or summary generator。

## 本轮目标

Phase 2.37 Pilot Issue Intake / Triage planning Git baseline。

只做 docs-only baseline，不写功能代码，不运行 pytest，不运行真实 API / CLI smoke，不进入 Phase 2.37a 实现。

## 允许修改 / 提交文件

仅允许 stage / commit 以下文件：

1. `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/HANDOFF_LOG.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/NIGHTLY_SPRINT_QUEUE.md`

`reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新但不得 staged / committed。

## Baseline 前复核

1. `git status --short`
2. `git diff --check`
3. `git diff --cached --name-only`，确认 staged 前为空或仅白名单文件。
4. 确认无代码、脚本、测试、DB、索引相关文件被修改或 staged。

## Git baseline

若复核通过：

1. stage 仅允许文件。
2. commit message：
   - `docs: plan phase 2.37 pilot issue triage`
3. tag：
   - `phase-2.37-pilot-issue-triage-plan-baseline`
4. push：
   - `origin/main`
   - tag

baseline 后必须停止，不得自动进入 Phase 2.37a。

## 硬边界

1. 不写功能代码。
2. 不运行 pytest，除非误改代码需要证明回退。
3. 不运行真实 API / CLI smoke。
4. 不写业务 DB / facts / document_versions。
5. 不修改 OpenSearch / Qdrant 数据。
6. 不执行 repair / backfill / reindex / cleanup / delete。
7. 不自动创建 Linear / GitHub issue。
8. 不做自动审标结论。
9. 不修改 retrieval contract。
10. 不修改 memory kernel 主架构。
11. 不进入 production rollout。
12. 不纳入无关 dirty。

## 输出要求

返回精简报告：

1. 修改文件。
2. Codex B review 结论是否已写入文档。
3. baseline 前复核结果。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 `git status --short`。
8. 阻塞点 / 风险点。
9. 是否建议进入 Phase 2.37a 规划 / 实现。
