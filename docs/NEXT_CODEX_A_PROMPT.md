# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做一个 bounded step，完成后停止，等待 Codex B 审核。

## 必读文件

执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
7. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`
9. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.41a MVP Pilot Evidence Review Checklist Artifact 已完成，Codex B review 通过，可以进入 docs-only baseline。

当前基线：

1. HEAD：`40f8380`
2. tag：`phase-2.41-mvp-pilot-evidence-review-plan-baseline`
3. `origin/main` 已对齐。

当前工作区允许存在一个遗留无关 dirty：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

该 Phase 2.38 文件不属于本轮范围，必须保留原状，不得 stage、commit、清理或改写。

## Baseline Gate 判定

本轮允许 baseline，因为 5 条 gate 已满足：

1. 当前 phase 有明确验收结果：新增 `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`，可人工填写 Go / Pause / No-Go、P0 / P1、evidence policy、citation、governance、human review 与 not-claimable。
2. Codex B review 已通过：checklist 没有批准 production rollout、repair executor、自动审标、自动经营决策或 Data Steward 实现。
3. 目标静态检查通过：`git diff --check` 与 Phase 2.41a 关键词 `rg` 复核通过。
4. 文档状态已同步：ACTIVE_PHASE、HANDOFF_LOG、TODO、DEV_LOG、PHASE_BACKLOG、latest 已同步 Phase 2.41a。
5. 下一步将切换 phase 或扩大范围：baseline 后才允许规划 Pilot evidence review dry-run report 或实际内部 Pilot review 流程。

小修不 baseline 规则仍有效；本轮不是 prompt wording / 状态文件小改，而是完整 Phase 2.41a checklist artifact 收口。

## 本轮目标

Phase 2.41a MVP Pilot Evidence Review Checklist Artifact docs-only Git baseline。

只提交 Phase 2.41a checklist 与交接文档；不进入下一阶段实现，不新增代码，不扩展能力。

## 允许 stage / commit 的文件白名单

只允许 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
6. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

`/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新，但不得提交。

## 禁止 stage / commit 的文件

明确禁止 stage / commit：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. 任意代码文件
3. 任意脚本文件
4. 任意测试文件
5. 任意 migration / schema 文件
6. 任意 reports / reviews 真实 JSON 产物
7. Hermes 主仓库任意文件

## 硬边界

1. 不写功能代码。
2. 不新增脚本、测试、migration、schema。
3. 不写 DB / facts / document_versions。
4. 不修改 OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / cleanup / delete。
6. 不进入 rollout。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。
9. 不启动 Data Steward 实现。
10. 不新增 Neo4j / PostGIS / scheduler / DB schema。
11. 不运行 pytest。
12. 不修改 Hermes 主仓库。
13. 不自动进入下一阶段。

## Baseline 前检查

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git status --short
git diff --check
rg -n "MVP Pilot Evidence Review Checklist|reviewer|reviewed_at|go|pause|no_go|P0|P1|facts_as_answer=false|transcript_as_fact=false|snapshot_as_answer=false|Missing Evidence|人工复核|production ready|自动审标|Data Steward" docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md docs/TODO.md docs/DEV_LOG.md docs/PHASE_BACKLOG.md docs/ACTIVE_PHASE.md
```

本轮为 docs-only baseline，不运行 pytest，不跑 API / CLI smoke。

## Git baseline 步骤

只 stage 白名单文件：

```bash
git add docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md docs/TODO.md docs/DEV_LOG.md docs/PHASE_BACKLOG.md docs/ACTIVE_PHASE.md docs/HANDOFF_LOG.md docs/NEXT_CODEX_A_PROMPT.md
git diff --cached --check
git diff --cached --name-only
```

确认 staged 文件只包含上述 7 个文件后提交：

```bash
git commit -m "docs: baseline phase 2.41a mvp pilot evidence review checklist"
git tag phase-2.41a-mvp-pilot-evidence-review-checklist-baseline
git push origin main
git push origin phase-2.41a-mvp-pilot-evidence-review-checklist-baseline
```

## 完成后更新 ignored 本地状态

更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `phase`: `Phase 2.41a MVP Pilot Evidence Review Checklist Artifact`
2. `status`: `baseline`
3. `git.commit`: 当前 commit hash
4. `git.tag`: `phase-2.41a-mvp-pilot-evidence-review-checklist-baseline`
5. `git.pushed`: `true`
6. `needs_codex_b_review`: `true`
7. `next_recommendation`: `Codex B review Phase 2.41a baseline. Next phase should choose one bounded path: Pilot evidence review dry-run report or actual internal Pilot review runbook.`

`latest.json` 仍必须被 ignore，不得 stage。

## 验收标准

1. Commit 只包含 Phase 2.41a docs-only 白名单文件。
2. Tag `phase-2.41a-mvp-pilot-evidence-review-checklist-baseline` 指向当前 HEAD。
3. `origin/main` 与 tag 均推送成功。
4. 未提交 `reports/agent_runs/latest.json`。
5. 未提交 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
6. 未修改代码、脚本、测试、DB、OpenSearch、Qdrant、Hermes 主仓。
7. 最终 `git status --short` 允许只剩无关遗留 dirty：`M docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`；如没有则更好。

## 完成报告必须包含

1. commit hash
2. tag
3. push 结果
4. staged 文件列表
5. final `git status --short`
6. 是否保留无关 dirty
7. 是否建议进入下一阶段规划

## 下一步建议

Baseline 完成后停止。不要自动进入下一阶段。

下一阶段需 Codex B 按 Baseline Gate 再写入新的 `NEXT_CODEX_A_PROMPT.md`。
