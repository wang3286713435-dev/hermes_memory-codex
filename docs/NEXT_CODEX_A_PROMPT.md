# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.42 docs-only Git baseline，完成后停止，等待 Codex B 审核。

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
9. `/Users/Weishengsu/Hermes_memory/docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
10. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.42 MVP Pilot Review Dry-run Report Planning 已完成，Codex B review 通过。

Phase 2.42 docs sync review-fix 已完成，Codex B review 通过：

1. `docs/TODO.md` 当前状态不再停留在 Phase 2.39 正在收口。
2. `docs/NIGHTLY_SPRINT_QUEUE.md` Current Queue 不再指向旧 Phase 2.37 baseline。
3. Phase 2.42 baseline 仍属于 Yellow Lane，必须单独执行，本轮即为单独 baseline task。

当前基线：

1. HEAD：`a2e1042`
2. tag：`phase-2.41a-mvp-pilot-evidence-review-checklist-baseline`
3. `origin/main` 已对齐。

当前允许保留一个遗留无关 dirty：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

该 Phase 2.38 文件不属于本轮范围，必须保留原状，不得 stage、commit、清理或改写。

## Baseline Gate 判定

本轮允许 baseline，因为 5 条 gate 已满足：

1. 当前 phase 有明确验收结果：Phase 2.42 dry-run report planning 已完成，覆盖输入、输出、decision schema、P0/P1/P2/P3 aggregation、evidence policy、citation summary、Missing Evidence summary 与 storage policy。
2. Codex B review 已通过：规划未进入 production rollout、repair、DB 写入、OpenSearch / Qdrant mutation、Data Steward 实现或自动审标。
3. 目标静态检查通过：`git diff --check` 与 Phase 2.42 / Nightly queue 关键词 `rg` 复核通过。
4. 文档状态已同步：TODO 当前状态与 Nightly Current Queue 已修正，ACTIVE_PHASE、PHASE_BACKLOG、HANDOFF_LOG、DEV_LOG、latest 已同步 Phase 2.42。
5. 下一步将切换 phase 或扩大范围：baseline 后才允许规划 Phase 2.42a local ignored review report artifact / generator。

小修不 baseline 规则仍有效；本轮不是小修本身，而是 Phase 2.42 planning + docs sync review-fix 的阶段收口 baseline。

## 本轮目标

Phase 2.42 MVP Pilot Review Dry-run Report Planning docs-only Git baseline。

只提交 Phase 2.42 planning、docs sync review-fix 与交接文档；不进入 Phase 2.42a，不新增代码，不生成真实 report。

## 允许 stage / commit 的文件白名单

只允许 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
6. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
8. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`

`/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新，但不得提交。

## 禁止 stage / commit 的文件

明确禁止 stage / commit：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. 任意代码文件
3. 任意脚本文件
4. 任意测试文件
5. 任意 migration / schema 文件
6. 任意 reports / reviews 真实 JSON 或 Markdown 产物
7. Hermes 主仓库任意文件

## 硬边界

1. 不写功能代码。
2. 不新增脚本、测试、migration、schema。
3. 不生成真实 MVP Pilot review report。
4. 不写 DB / facts / document_versions。
5. 不修改 OpenSearch / Qdrant。
6. 不执行 repair / backfill / reindex / cleanup / delete。
7. 不进入 production rollout。
8. 不改 retrieval contract。
9. 不改 memory kernel 主架构。
10. 不启动 Data Steward 实现。
11. 不新增 Neo4j / PostGIS / scheduler / DB schema。
12. 不运行 pytest。
13. 不运行 API / CLI smoke。
14. 不修改 Hermes 主仓库。
15. Baseline 后停止，不自动进入 Phase 2.42a。

## Baseline 前检查

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git status --short
git diff --check
rg -n "Phase 2.42|MVP Pilot Review Dry-run|go|pause|no_go|P0|P1|facts_as_answer=false|transcript_as_fact=false|snapshot_as_answer=false|Missing Evidence|人工复核|production rollout|Data Steward|repair|Green Lane|Yellow Lane|小修不 baseline" docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md docs/TODO.md docs/DEV_LOG.md docs/PHASE_BACKLOG.md docs/ACTIVE_PHASE.md docs/NIGHTLY_SPRINT_QUEUE.md
```

本轮为 docs-only baseline，不运行 pytest，不跑 API / CLI smoke。

## Git baseline 步骤

只 stage 白名单文件：

```bash
git add docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md docs/TODO.md docs/DEV_LOG.md docs/PHASE_BACKLOG.md docs/ACTIVE_PHASE.md docs/HANDOFF_LOG.md docs/NEXT_CODEX_A_PROMPT.md docs/NIGHTLY_SPRINT_QUEUE.md
git diff --cached --check
git diff --cached --name-only
```

确认 staged 文件只包含上述 8 个文件后提交：

```bash
git commit -m "docs: baseline phase 2.42 mvp pilot review dry-run plan"
git tag phase-2.42-mvp-pilot-review-dry-run-plan-baseline
git push origin main
git push origin phase-2.42-mvp-pilot-review-dry-run-plan-baseline
```

## 完成后更新 ignored 本地状态

更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `phase`: `Phase 2.42 MVP Pilot Review Dry-run Report Planning`
2. `status`: `baseline`
3. `git.commit`: 当前 commit hash
4. `git.tag`: `phase-2.42-mvp-pilot-review-dry-run-plan-baseline`
5. `git.pushed`: `true`
6. `needs_codex_b_review`: `true`
7. `needs_codex_c_validation`: `false`
8. `next_recommendation`: `Codex B review Phase 2.42 baseline. Next phase candidate: Phase 2.42a local ignored MVP Pilot review dry-run report artifact or generator planning; do not start rollout.`

`latest.json` 仍必须被 ignore，不得 stage。

## 验收标准

1. Commit 只包含 Phase 2.42 docs-only 白名单文件。
2. Tag `phase-2.42-mvp-pilot-review-dry-run-plan-baseline` 指向当前 HEAD。
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

Baseline 完成后停止。不要自动进入 Phase 2.42a。

下一阶段需 Codex B 按 Baseline Gate 再写入新的 `NEXT_CODEX_A_PROMPT.md`。
