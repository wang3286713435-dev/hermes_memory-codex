# Active Phase

- 当前 phase：Phase 2.112f Alias Continuity Restore Fix Review Passed / Test-machine Validation Pending。
- 本轮目标：修复测试机 OpenWebUI / 8642 中 import 已 `alias_continuity_status=stored` 但 follow-up `@alias` 仍 `alias_missing + retrieval_suppressed` 的 owner-scoped restore 断点。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/session_document_scope.py`、`tests/agent/test_session_document_scope.py`、`tests/agent/test_natural_file_import_runtime.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory `docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`reports/agent_runs/latest.json`。
- 完成内容：将 `alias_continuity_*` 与 `stable_owner_missing` 稳定传播到 nested `alias_resolution`；补跨 store reload / 新 agent instance 的 same-owner restore 测试；补 cross-owner denied、missing stable owner、conflict fail-closed 诊断断言。
- 测试结果：Hermes 主仓库 py_compile 通过；`tests/agent/test_natural_file_import_runtime.py tests/agent/test_session_document_scope.py` 为 `77 passed`；gateway stable-owner targeted tests 为 `3 passed`。
- live smoke 结果：未执行真实 upload/import/OpenWebUI/8642；本轮仅做本地代码与单元回归。
- 当前结论：2.112f 已通过 Codex B review；Hermes agent runtime test-candidate 已 baseline 并推送；Phase 2 natural import closeout 仍需测试机 OpenWebUI / 8642 复验。
- 阻塞点 / 风险点：真实 follow-up retrieval + citation 尚未复验；不得恢复 alias-global registry，不得使用 ordinary memory 作为 alias persistence。
- 是否建议 baseline：runtime test-candidate 已完成；full runtime baseline 仍等待测试机 OpenWebUI / 8642 通过。
- 是否建议进入下一阶段：否。
- 下一轮建议：测试机 Codex checkout `phase-2.112f-alias-continuity-restore-runtime-test-candidate`，重启 8642，并执行真实 OpenWebUI import -> follow-up `@建筑类数据样表` retrieval + citation。
- 是否需要 Codex B 审核：runtime candidate 已通过；测试机回传后再做最终 review。
- 是否需要 Codex C / 测试机验收：需要测试机 OpenWebUI / 8642 验收。
- commit/tag if any：Hermes agent `78eb77158` / `phase-2.112f-alias-continuity-restore-runtime-test-candidate`。
