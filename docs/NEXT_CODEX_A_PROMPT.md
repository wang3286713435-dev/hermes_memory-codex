# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`

## 当前状态

Phase 2.37a Pilot issue intake dry-run 最小实现已完成。

已完成内容：

1. 新增 `scripts/phase237a_pilot_issue_intake.py`。
2. 新增 `tests/test_phase237a_pilot_issue_intake.py`。
3. 支持 `--print-template`、`--input`、`--input-dir`、`--strict`。
4. 输出 local triage summary JSON，包含 total、priority / issue type counts、P0/P1 counts、Go / Pause recommendation 与 invalid records。
5. 保持 dry-run 边界：不写 DB、不创建外部 issue、不 repair、不 rollout。

验证结果：

1. `uv run python -m py_compile scripts/phase237a_pilot_issue_intake.py` passed。
2. `uv run pytest tests/test_phase237a_pilot_issue_intake.py -q` passed：`9 passed`。
3. 临时目录 dry-run smoke 通过。

## 下一轮目标

Phase 2.37a Git baseline。

执行条件：

1. Codex B 已审核并确认可以 baseline（2026-05-01 review passed）。
2. 用户明确授权执行 baseline。

## Baseline 文件白名单

只允许 stage / commit 以下文件：

1. `scripts/phase237a_pilot_issue_intake.py`
2. `tests/test_phase237a_pilot_issue_intake.py`
3. `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. `docs/NEXT_CODEX_A_PROMPT.md`

不得 stage / commit：

1. `reports/agent_runs/latest.json`
2. 任何真实 reports JSON
3. 任何真实 review JSON / Markdown
4. 无关代码或文档 dirty

## 必须复跑

```bash
uv run python -m py_compile scripts/phase237a_pilot_issue_intake.py
uv run pytest tests/test_phase237a_pilot_issue_intake.py -q
```

## Git 建议

commit message:

```text
chore: add phase 2.37a pilot issue intake dry-run
```

tag:

```text
phase-2.37a-pilot-issue-intake-baseline
```

## 硬边界

1. 不写业务 DB / facts / document_versions。
2. 不修改 OpenSearch / Qdrant 数据。
3. 不执行 repair / backfill / reindex / cleanup / delete。
4. 不运行真实 API / CLI smoke。
5. 不自动创建 Linear / GitHub issue。
6. 不做自动审标结论。
7. 不修改 retrieval contract。
8. 不修改 memory kernel 主架构。
9. 不进入 production rollout。
10. 不纳入无关 dirty。

## 输出要求

返回精简报告：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. final git status。
7. 是否存在 ignored latest.json / reports 被 staged。
8. 是否建议进入下一阶段。
