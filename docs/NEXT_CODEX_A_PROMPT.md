# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.29b 最小实现：readiness freeze decision record dry-run。

本轮只生成 decision record，不执行 rollout，不执行 repair，不写业务 DB。

## 当前基线

Phase 2.29b planning 已完成并准备 baseline：

1. `docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md` 已定义 pass/warn/fail 映射。
2. `warn` 必须人工确认，不能自动进入 MVP candidate。
3. `fail` 必须 No-Go。
4. `pass` 只允许进入 MVP freeze candidate，不等于 production ready。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 建议新增脚本

`/Users/Weishengsu/Hermes_memory/scripts/phase229b_freeze_decision_dry_run.py`

## 建议新增测试

`/Users/Weishengsu/Hermes_memory/tests/test_phase229b_freeze_decision_dry_run.py`

## 功能要求

1. 读取显式传入的 Phase 2.29a freeze report JSON。
2. 生成 decision record JSON。
3. `freeze_report.status=pass` 映射为 `approved_for_mvp_freeze_candidate`。
4. `freeze_report.status=warn` 映射为 `needs_manual_review`。
5. `freeze_report.status=fail` 映射为 `no_go`。
6. 输出必须恒定：
   - `dry_run=true`
   - `production_rollout=false`
   - `repair_approved=false`
   - `destructive_actions=[]`
7. 如果 freeze report 包含 `production_rollout=true`、`repair_executed=true` 或非空 `destructive_actions`，必须 No-Go。
8. 不执行任何 action。

## CLI 建议

1. `--freeze-report <path>`
2. `--reviewer <name>` 可选。
3. `--notes <text>` 可选，但不得包含敏感原文。
4. `--json`
5. `--output-file <path>` 可选。
6. `--dry-run-preview` 可选，不写文件。

## 测试要求

1. pass -> approved_for_mvp_freeze_candidate。
2. warn -> needs_manual_review。
3. fail -> no_go。
4. unsafe rollout / repair / destructive_actions -> no_go。
5. dry_run / production_rollout / repair_approved / destructive_actions 恒定。
6. dry-run-preview 不写文件。

## Live smoke 要求

1. `uv run python -m py_compile scripts/phase229b_freeze_decision_dry_run.py`
2. `uv run pytest tests/test_phase229b_freeze_decision_dry_run.py -q`
3. 使用临时目录 fake freeze report JSON 执行 pass / warn / fail dry-run。
4. 不读取真实 reports / reviews。
5. 不写 DB。
6. 不生成 rollout / repair 产物。

## 文档同步

更新：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 硬边界

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts。
4. 不修改 document_versions。
5. 不修改 OpenSearch / Qdrant。
6. 不读取真实 reports / reviews 目录。
7. 不默认运行 full eval。
8. 不执行 repair / backfill / reindex / cleanup / delete。
9. 不进入 rollout。
10. 不进入 repair executor。
11. 不做 facts 自动抽取。
12. 不让 facts 替代 retrieval evidence。
13. 不改 retrieval contract。
14. 不改 memory kernel 主架构。

## Git 规则

本轮不提交 Git。完成后停止，等待 review / baseline 指令。

## 返回报告

1. 修改文件
2. 实现内容
3. 测试结果
4. live smoke 结果
5. 是否写 DB
6. 是否生成 rollout / repair 产物
7. 是否建议 Git baseline
