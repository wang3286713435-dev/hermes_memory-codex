# Active Phase

- 当前 phase：Phase 2.81 Codex B Review / Baseline Prompt。
- 背景：Phase 2.80 baseline 已完成：commit `93cbb18`，tag `phase-2.80-scratch-parser-dry-run-plan-baseline`，pushed=true。Phase 2.80a Mac mini / 测试机 controlled scratch parser dry-run 已返回 `go`。
- 本轮目标：规划 sanitized evidence manifest；本轮不生成 manifest artifact。
- 修改文件：`docs/PHASE281_SANITIZED_EVIDENCE_MANIFEST_PLAN.md`、`docs/PHASE280A_CONTROLLED_SCRATCH_PARSER_DRY_RUN_RESULT.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md` 与 ignored `reports/agent_runs/latest.json`。
- 完成内容：已完成 Phase 2.81 planning，明确 manifest 只能从 sanitized parser preview 派生，只能做 ignored local artifact，不包含 raw text / 真实文件名 / 真实 NAS 路径 / raw DB row / secret / 敏感业务数据。
- 测试结果：`git diff --check` 通过；`uv run python -m json.tool reports/agent_runs/latest.json >/dev/null` 通过。
- live smoke 结果：本轮不运行 API / CLI smoke，不连接 DB / NAS；上一轮测试机返回 `decision=go`、`parsed_preview_count=3`、`cleanup_status=all_deleted`。
- 当前结论：Phase 2.81 planning 已完成，Codex B review 已通过；尚未实现 manifest runner，尚未写 `documents/chunks`、index 或 Agent answer。
- 阻塞点 / 风险点：Phase 2.81a 若进入 manifest runner，必须仍是 ignored local dry-run，不得把 manifest 接入 Agent final answer。
- 是否建议 baseline：是；建议先完成 Phase 2.81 docs baseline。
- 是否建议进入下一阶段：否；Phase 2.81a sanitized evidence manifest dry-run implementation 需单独授权。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中的 selective docs baseline，baseline 后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要；Phase 2.81 先规划 manifest。
