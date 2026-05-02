# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md`

## 当前状态

Phase 2.37b Pilot issue intake runbook / local storage convention 已完成。

已完成内容：

1. 新增 `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md`。
2. 新增 `reports/pilot_issues/.gitignore`。
3. 新增 `reports/pilot_issues/README.md`。
4. 真实 Pilot issue JSON / Markdown 默认 ignored，不入 Git。
5. 本轮未修改 intake 脚本、测试、业务代码、DB、facts、versions、OpenSearch 或 Qdrant。

验证结果：

1. `git diff --check` passed。
2. `uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237b_issue_template.json` passed。
3. `uv run python scripts/phase237a_pilot_issue_intake.py --input /tmp/phase237b_issue_template.json --strict` passed。
4. `git check-ignore -v reports/pilot_issues/example.json` passed。

## 下一轮目标

Phase 2.37b docs baseline。

执行条件：

1. Codex B 已审核并确认可以 baseline（2026-05-02 review passed）。
2. 用户明确授权执行 baseline。

## Baseline 文件白名单

只允许 stage / commit 以下文件：

1. `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md`
2. `reports/pilot_issues/.gitignore`
3. `reports/pilot_issues/README.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. `docs/NEXT_CODEX_A_PROMPT.md`

不得 stage / commit：

1. `reports/agent_runs/latest.json`
2. `reports/pilot_issues/*.json`
3. `reports/pilot_issues/*.md` except `README.md`
4. `scripts/phase237a_pilot_issue_intake.py`
5. `tests/test_phase237a_pilot_issue_intake.py`
6. 任何业务代码、DB、retrieval、indexing、facts、OpenSearch、Qdrant 相关文件。

## 必须复跑

```bash
git diff --check
uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237b_issue_template.json
uv run python scripts/phase237a_pilot_issue_intake.py --input /tmp/phase237b_issue_template.json --strict
git check-ignore -v reports/pilot_issues/example.json
```

不运行 pytest，除非脚本或测试被修改。

## Git 建议

commit message:

```text
docs: add phase 2.37b pilot issue intake runbook
```

tag:

```text
phase-2.37b-pilot-issue-intake-runbook-baseline
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
10. 不实现 BIM asset catalog。
11. 不纳入无关 dirty。

## 输出要求

返回精简报告：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. final git status。
7. 是否存在 ignored latest.json / pilot issue records 被 staged。
8. 是否建议进入下一阶段。
