# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.43b MVP Pilot Pre-flight Smoke Prompt / Runbook Git baseline，完成后停止，等待 Codex B 审核。不要启动真实 Pilot，不要运行 API / CLI smoke，不要进入 Phase 2.43c，不要进入 production rollout、repair、Data Steward 实现或任何业务数据写入。

## 必读文件

执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
8. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`
10. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_LAUNCH_PACKET.md`
11. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.43b MVP Pilot Pre-flight Smoke Prompt / Runbook artifact 已完成并通过 Codex B review。

Codex B 已复核：

1. `docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md` 是交给 Codex C 的真实终端预飞行验收提示词，不是 Pilot 启动授权。
2. Prompt 覆盖 API / CLI、fresh session、alias 绑定、主标书 evidence / Missing Evidence、Excel / PPTX structured citation、会议纪要 transcript boundary、confirmed facts boundary 与 optional compare smoke。
3. Prompt 明确输出结构化报告：API / CLI 状态、`session_id`、alias table、query table、P0 / P1 / P2 / P3、evidence policy flags、Missing Evidence、third-document contamination 与 Go / Pause / No-Go。
4. Prompt 明确 `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`、Missing Evidence 可见、citation / source 可人工核查。
5. Prompt 明确 `Go` 只代表可考虑内部受控 MVP Pilot，不是 production rollout、自动审标、自动投标、自动经营决策、repair 或 Data Steward implementation。
6. 未运行真实 API / CLI smoke，未启动真实 Pilot，未生成真实 report，未写 DB，未进入 rollout / repair / Data Steward 实现。

当前基线：

1. HEAD：`5423497`
2. tag：`phase-2.43a-mvp-pilot-launch-packet-baseline`
3. `origin/main` 已对齐。

当前允许保留一个遗留无关 dirty：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

该 Phase 2.38 文件不属于本轮范围，必须保留原状，不得 stage、commit、清理或改写。

## Baseline Gate 判定

本轮允许 baseline，因为 5 条 gate 已满足：

1. 当前 phase 有明确验收结果：Phase 2.43b pre-flight prompt / runbook artifact 已完成。
2. Codex B review 已通过：未发现偏离 PRD、MVP Pilot 边界或 Data Steward 后置边界。
3. 目标验证通过：`git diff --check`、新增 prompt diff check、关键词边界检查、`latest.json` JSON 校验与 ignore 检查通过；本阶段无需 Codex C 真实终端验收。
4. 文档状态已同步：ACTIVE_PHASE、PHASE_BACKLOG、NIGHTLY_SPRINT_QUEUE、TODO、DEV_LOG、HANDOFF_LOG 与 ignored latest 均记录 Phase 2.43b 状态。
5. 下一步将扩大到 Codex C 真实终端 pre-flight smoke；baseline 后才允许交给 Codex C 执行。

小修不 baseline 规则仍有效；本轮不是小修，而是 Phase 2.43b artifact 阶段收口。

## 本轮目标

Phase 2.43b MVP Pilot Pre-flight Smoke Prompt / Runbook Git baseline。

只提交 Phase 2.43b 白名单文件；不进入下一阶段，不运行真实 API / CLI，不启动真实 Pilot，不生成真实 report，不写 DB，不做 rollout 或 repair。

## 允许 stage / commit 的文件白名单

只允许 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
6. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
8. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

`/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新，但不得提交。

## 禁止 stage / commit 的文件

明确禁止 stage / commit：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. 任意业务服务代码文件。
3. 任意脚本文件。
4. 任意测试文件。
5. 任意 migration / schema 文件。
6. 任意真实 reports / reviews JSON 或 Markdown 产物。
7. Hermes 主仓库任意文件。
8. 任意 DB / OpenSearch / Qdrant / facts / document_versions 相关数据产物。

## 验证命令

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git diff --check
git diff --check --no-index /dev/null docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md || test $? -eq 1
rg -n "Codex C|pre-flight|API|CLI|alias|facts_as_answer|transcript_as_fact|snapshot_as_answer|Missing Evidence|No-Go|Go|Pause|P0|P1|citation|document_id|version_id|no upload|no DB|no report|production rollout|repair|Data Steward" docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md docs/TODO.md docs/DEV_LOG.md docs/PHASE_BACKLOG.md docs/ACTIVE_PHASE.md docs/NIGHTLY_SPRINT_QUEUE.md
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

不运行 API / CLI smoke，不运行 pytest，不生成真实 report。

## Git 操作

确认 dirty 仅包含白名单文件与允许保留的 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 后执行：

```bash
git add docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md

git diff --cached --name-only
git diff --cached --check
git commit -m "docs: add phase 2.43b mvp pilot preflight smoke prompt"
git tag phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline
git push origin main
git push origin phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline
```

## 完成后必须检查

1. `git status --short`
2. HEAD commit hash
3. tag 是否指向 HEAD
4. `origin/main` push 是否成功
5. tag push 是否成功
6. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 是否仍未 staged / 未提交

如果最终只剩 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty，可以报告为遗留无关 dirty；不要清理它。

## 硬边界

1. 不写业务 DB / facts / document_versions。
2. 不修改 OpenSearch / Qdrant。
3. 不执行 repair / backfill / reindex / cleanup / delete。
4. 不进入 production rollout。
5. 不生成真实 MVP Pilot report。
6. 不默认扫描真实 reports / reviews。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。
9. 不启动 Data Steward 实现。
10. 不新增 Neo4j / PostGIS / scheduler / DB schema。
11. 不运行 API / CLI smoke。
12. 不修改 Hermes 主仓库。
13. baseline 后必须停止，不得自动进入下一 phase，不得自动发起 Codex C。

## 完成报告必须包含

1. 修改文件。
2. 验证命令与结果。
3. staged 文件白名单复核结果。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 `git status --short`。
8. 是否保留 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 遗留 dirty。
9. 是否进入真实 Pilot / rollout / repair / Data Steward 实现（必须为否）。
10. 是否自动发起 Codex C（必须为否）。
