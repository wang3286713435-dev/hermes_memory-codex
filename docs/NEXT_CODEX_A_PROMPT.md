# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.42a Git baseline，完成后停止，等待 Codex B 审核。不要进入 Phase 2.42b / Phase 2.43。

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

Phase 2.42a MVP Pilot Review Dry-run Report Generator 已完成实现并通过 Codex B review。

Codex B 已复核：

1. 实现只读取显式 `--input` JSON，不默认扫描真实 `reports/` / `reviews/`。
2. 输出固定包含 `dry_run=true`、`production_rollout=false`、`repair_authorized=false`、`destructive_actions=[]`、`data_mutation=false`、`facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`。
3. P0 / unsafe evidence policy / rollout / repair / destructive action / data mutation 均会进入 `no_go`。
4. Missing Evidence 未人工复核会进入 `pause`。
5. Markdown 输出明确不是 production rollout approval、不是 repair authorization，并要求 human review。
6. 真实 MVP Pilot review report JSON / Markdown 默认 ignored。

当前基线：

1. HEAD：`0e0d208`
2. tag：`phase-2.42-mvp-pilot-review-dry-run-plan-baseline`
3. `origin/main` 已对齐。

当前允许保留一个遗留无关 dirty：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

该 Phase 2.38 文件不属于本轮范围，必须保留原状，不得 stage、commit、清理或改写。

## Baseline Gate 判定

本轮允许 baseline，因为 5 条 gate 已满足：

1. 当前 phase 有明确验收结果：Phase 2.42a generator 已实现，目标测试 `7 passed`。
2. Codex B review 已通过：实现未进入 rollout、repair、DB 写入、OpenSearch / Qdrant mutation、API / CLI smoke、Data Steward 实现或主架构变更。
3. 目标验证通过：`py_compile`、目标 pytest、`git diff --check`、`git check-ignore` 均通过。
4. 文档状态已同步：ACTIVE_PHASE、PHASE_BACKLOG、HANDOFF_LOG、TODO、DEV_LOG、PHASE242 plan 与 ignored latest 均记录 Phase 2.42a 状态。
5. 下一步将切换 phase 或扩大范围：baseline 后才允许规划 Phase 2.42b / 2.43。

小修不 baseline 规则仍有效；本轮不是小修，而是 Phase 2.42a 最小实现阶段收口。

## 本轮目标

Phase 2.42a MVP Pilot Review Dry-run Report Generator Git baseline。

只提交 Phase 2.42a 白名单文件；不进入下一阶段，不生成真实 report，不运行 API / CLI，不写 DB，不做 rollout 或 repair。

## 允许 stage / commit 的文件白名单

只允许 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/scripts/phase242a_mvp_pilot_review_dry_run.py`
2. `/Users/Weishengsu/Hermes_memory/tests/test_phase242a_mvp_pilot_review_dry_run.py`
3. `/Users/Weishengsu/Hermes_memory/reports/mvp_pilot_reviews/.gitignore`
4. `/Users/Weishengsu/Hermes_memory/reports/mvp_pilot_reviews/README.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
7. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
8. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
10. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
11. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
12. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`

`/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新，但不得提交。

## 禁止 stage / commit 的文件

明确禁止 stage / commit：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. 任意业务服务代码文件
3. 任意 migration / schema 文件
4. 任意真实 reports / reviews JSON 或 Markdown 产物
5. Hermes 主仓库任意文件
6. 任意 DB / OpenSearch / Qdrant / facts / document_versions 相关数据产物

## 验证命令

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
uv run python -m py_compile scripts/phase242a_mvp_pilot_review_dry_run.py
uv run pytest tests/test_phase242a_mvp_pilot_review_dry_run.py -q
git diff --check
git check-ignore -v reports/mvp_pilot_reviews/example.json reports/mvp_pilot_reviews/example.md reports/agent_runs/latest.json || true
git status --short
```

不运行 API / CLI smoke。

## Git 操作

确认 dirty 仅包含白名单文件与允许保留的 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 后执行：

```bash
git add scripts/phase242a_mvp_pilot_review_dry_run.py \
  tests/test_phase242a_mvp_pilot_review_dry_run.py \
  reports/mvp_pilot_reviews/.gitignore \
  reports/mvp_pilot_reviews/README.md \
  docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/NIGHTLY_SPRINT_QUEUE.md

git diff --cached --name-only
git commit -m "chore: add phase 2.42a mvp pilot review dry-run generator"
git tag phase-2.42a-mvp-pilot-review-dry-run-generator-baseline
git push origin main
git push origin phase-2.42a-mvp-pilot-review-dry-run-generator-baseline
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
13. baseline 后必须停止，不得自动进入下一 phase。

## 完成报告必须包含

1. 修改文件
2. 测试命令与结果
3. staged 文件白名单复核结果
4. commit hash
5. tag
6. push 结果
7. final `git status --short`
8. 是否仍有遗留无关 dirty
9. 是否建议进入下一阶段
