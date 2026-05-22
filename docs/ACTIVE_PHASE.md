# Active Phase

- 当前 phase：Phase 2.113a Self-Awareness Live Validation Go。
- 本轮目标：记录测试机 / OpenWebUI / 8642 对 Phase 2.113a runtime candidate 的真实验收结果。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/kernel.py`、`agent/memory_kernel/session_document_scope.py`、`tests/agent/test_session_document_scope.py`、`tests/agent/test_structured_citation_context.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：收窄 file-discovery intent，只在明确找候选文件时 suppress retrieval；普通内容查询不再被 `找一下 / 帮我找` 误伤；扩展 kernel capability trigger 到“管理文件 / 管理公司文件 / 使用记忆库”等自然问法。
- 测试结果：Codex B 复核通过；Hermes 主仓库 py_compile 通过；`tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py` 为 `102 passed`；直接 probe 确认普通内容查询不再被 file-discovery 抑制，明确找候选文件仍 fail-closed。
- live smoke 结果：测试机 Go；8642 health pass、Hermes Memory health pass、self-awareness pass、ordinary retrieval guard pass、fuzzy file discovery pass；未授权 natural import，因此 import feedback case skipped。
- 当前结论：Phase 2.113a P0 self-awareness / ordinary retrieval guard / fuzzy discovery live gate 已通过。自然导入增强反馈本轮未重复导入，仍不得把 import diagnostics / alias / workspace refs 当 retrieval evidence。
- 阻塞点 / 风险点：本轮未执行新导入；Phase 2 final closeout 仍需单独确认 eval / coverage / freeze checklist，不等同 production rollout。
- 是否建议 baseline：允许 Hermes_memory live-validation handoff baseline；runtime final stable tag 是否推进由下一轮 closeout gate 决定。
- 是否建议进入下一阶段：可以进入 Phase 2.113 closeout / Phase 2 final freeze checklist 更新，不需要 Codex A 继续修 2.113a。
- 下一轮建议：Codex B 更新 Phase 2.113 closeout 与 Phase 2 final freeze checklist；如用户要继续开发，再开新的 bounded phase。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C / 测试机验收：已完成本轮要求；natural import optional case因未授权导入而跳过。
- commit/tag if any：Hermes agent `a12d378e0` / `phase-2.113a-self-awareness-runtime-test-candidate` 已推送；Hermes_memory live-validation baseline 待本轮提交。
