# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.42b Git baseline，完成后停止，等待 Codex B 审核。不要进入 Phase 2.42c / 2.43，不要启动真实 Pilot、production rollout、repair 或 Data Steward 实现。

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
10. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`
11. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md`
12. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.42b MVP Pilot Review Dry-run Input Template / Runbook artifact 已完成实现并通过 Codex B review。

Codex B 已复核：

1. Template 是合法 JSON。
2. Template 只含 sanitized placeholders，未包含真实客户数据、真实 session_id、真实 document_id、真实 fact_id、真实人员姓名、真实金额或敏感判断。
3. Template 可被 2.42a generator 读取，输出安全 dry-run report。
4. 输出固定保持 dry-run / no rollout / no repair / no destructive action / no data mutation / facts-transcript-snapshot not answer。
5. Template 当前 decision 为 `pause`，原因是 Missing Evidence 未人工复核，符合预期。
6. Runbook 明确不是 production rollout approval、不是 repair authorization，不是自动审标、自动投标或自动经营决策。

当前基线：

1. HEAD：`4c60b28`
2. tag：`phase-2.42a-mvp-pilot-review-dry-run-generator-baseline`
3. `origin/main` 已对齐。

当前允许保留一个遗留无关 dirty：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

该 Phase 2.38 文件不属于本轮范围，必须保留原状，不得 stage、commit、清理或改写。

## Baseline Gate 判定

本轮允许 baseline，因为 5 条 gate 已满足：

1. 当前 phase 有明确验收结果：Phase 2.42b template / runbook artifact 已完成，dry-run 输出 decision 为 `pause` 且安全字段通过断言。
2. Codex B review 已通过：artifact 未进入 rollout、repair、DB 写入、OpenSearch / Qdrant mutation、API / CLI smoke、Data Steward 实现或主架构变更。
3. 目标验证通过：JSON parse、generator dry-run、safety assertions、`git diff --check` 均通过。
4. 文档状态已同步：ACTIVE_PHASE、PHASE_BACKLOG、HANDOFF_LOG、TODO、DEV_LOG、PHASE242 plan 与 ignored latest 均记录 Phase 2.42b 状态。
5. 下一步将切换 phase 或扩大范围：baseline 后才允许规划 Phase 2.42c / 2.43。

小修不 baseline 规则仍有效；本轮不是小修，而是 Phase 2.42b artifact 阶段收口。

## 本轮目标

Phase 2.42b MVP Pilot Review Dry-run Input Template / Runbook Git baseline。

只提交 Phase 2.42b 白名单文件；不进入下一阶段，不生成真实 report，不运行 API / CLI，不写 DB，不做 rollout 或 repair。

## 允许 stage / commit 的文件白名单

只允许 stage 以下文件：

1. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`
2. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
8. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

`/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新，但不得提交。

## 禁止 stage / commit 的文件

明确禁止 stage / commit：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`，除非只为本 baseline 做必要状态同步且 Codex A 能解释原因
3. 任意业务服务代码文件
4. 任意脚本文件，包括 `scripts/phase242a_mvp_pilot_review_dry_run.py`
5. 任意测试文件
6. 任意 migration / schema 文件
7. 任意真实 reports / reviews JSON 或 Markdown 产物
8. Hermes 主仓库任意文件
9. 任意 DB / OpenSearch / Qdrant / facts / document_versions 相关数据产物

## 验证命令

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
uv run python -m json.tool docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json >/tmp/phase242b_template_check.json
uv run python scripts/phase242a_mvp_pilot_review_dry_run.py --input docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json --json >/tmp/phase242b_report_check.json
uv run python - <<'PY'
import json
from pathlib import Path
report = json.loads(Path('/tmp/phase242b_report_check.json').read_text())
assert report['dry_run'] is True
assert report['production_rollout'] is False
assert report['repair_authorized'] is False
assert report['destructive_actions'] == []
assert report['facts_as_answer'] is False
assert report['transcript_as_fact'] is False
assert report['snapshot_as_answer'] is False
assert report['decision'] in {'go', 'pause', 'no_go'}
print(report['decision'])
PY
git diff --check
git status --short
```

不运行 API / CLI smoke，不运行 DB-backed tests。

## Git 操作

确认 dirty 仅包含白名单文件与允许保留的 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 后执行：

```bash
git add docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json \
  docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md \
  docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git diff --cached --name-only
git diff --cached --check
git commit -m "docs: add phase 2.42b mvp pilot review dry-run template"
git tag phase-2.42b-mvp-pilot-review-dry-run-template-baseline
git push origin main
git push origin phase-2.42b-mvp-pilot-review-dry-run-template-baseline
```

如果必须同步 `docs/NIGHTLY_SPRINT_QUEUE.md`，必须先确认它只包含 Phase 2.42b baseline queue 变更，再单独说明；否则不要 stage。

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
2. 验证命令与结果
3. staged 文件白名单复核结果
4. commit hash
5. tag
6. push 结果
7. final `git status --short`
8. 是否仍有遗留无关 dirty
9. 是否建议进入下一阶段
