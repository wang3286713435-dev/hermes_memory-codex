# Active Phase

- 当前 phase：Phase 2.65 Mac mini MVP Landing Pack Git Baseline。
- 背景：Phase 2.64b baseline 已完成：commit `da84197`，tag `phase-2.64b-data-steward-selective-integration-baseline`；Codex B review 指出 Phase 2.65 唯一阻塞是 hermes-agent ref 仍为占位符。
- 本轮目标：把 Mac mini install/update 文档和 manifest 示例中的 hermes-agent ref pin 到 reviewed tag `phase-2.56e-natural-import-real-upload-smoke-baseline`。
- 修改文件：`docs/PHASE265_MAC_MINI_MVP_LANDING_PLAN.md`、`docs/MAC_MINI_MVP_INSTALL_UPDATE_QUICKSTART.md`、`docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`、`docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`、`tests/test_phase265_mvp_release_manifest.py`、交接文档和 ignored `reports/agent_runs/latest.json`。
- 完成内容：reviewed hermes-agent ref 已替换；新增测试确认 reviewed tag manifest 为 `ready_for_operator_review`，placeholder ref 仍为 `pause`。
- 测试结果：`uv run python -m py_compile scripts/phase265_mvp_release_manifest.py` 通过；目标 pytest `41 passed`；reviewed-ref manifest 为 `ready_for_operator_review` 且无 pause reasons；placeholder manifest 仍为 `pause` 且包含 `missing_reviewed_hermes_agent_ref`；`git diff --check` 通过；`latest.json` JSON 校验通过。
- live smoke 结果：未运行真实 Mac mini deployment，未启动 Docker，未运行 API / CLI smoke，未连接真实 DB，未扫描 NAS。
- 当前结论：Codex B review 通过。Phase 2.65 landing pack 与 reviewed-ref fix 已满足 selective Git baseline 条件。
- 阻塞点 / 风险点：Mac mini secrets、真实 DB/NAS/Data Steward smoke 仍需后续授权；baseline 必须排除历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty。
- 是否建议 baseline：是；Codex A 应执行 `docs/NEXT_CODEX_A_PROMPT.md` 的 selective Git baseline。
- 是否建议进入下一阶段：否，当前应停在 Phase 2.65 review / baseline gate。
- 下一轮建议：Codex A 执行 Phase 2.65 selective Git baseline；baseline 后停止，交给 Codex B 检查。
- 是否需要 Codex B 审核：已完成；baseline 后需要最终状态检查。
- 是否需要 Codex C 真实终端验收：本阶段不需要；Mac mini 实机安装时再执行。
