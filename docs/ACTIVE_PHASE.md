# Active Phase

- 当前 phase：Phase 2.113a Self-Awareness Review / Runtime Candidate Handoff。
- 本轮目标：完成 Codex B review，发布 Hermes agent runtime test-candidate，并准备测试机 / OpenWebUI / 8642 验收 prompt。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/kernel.py`、`agent/memory_kernel/session_document_scope.py`、`tests/agent/test_session_document_scope.py`、`tests/agent/test_structured_citation_context.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：收窄 file-discovery intent，只在明确找候选文件时 suppress retrieval；普通内容查询不再被 `找一下 / 帮我找` 误伤；扩展 kernel capability trigger 到“管理文件 / 管理公司文件 / 使用记忆库”等自然问法。
- 测试结果：Codex B 复核通过；Hermes 主仓库 py_compile 通过；`tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py` 为 `102 passed`；直接 probe 确认普通内容查询不再被 file-discovery 抑制，明确找候选文件仍 fail-closed。
- live smoke 结果：本轮未执行 OpenWebUI / 8642 / API / CLI 真实验收，未上传文件。
- 当前结论：Phase 2.113a runtime fix 已通过 Codex B 本地 review；Hermes agent runtime test-candidate 已推送，下一步进入测试机 / OpenWebUI / 8642 验收。
- 阻塞点 / 风险点：用户侧 LLM 表现尚未 live 验证；import diagnostics、aliases、workspace refs 仍必须保持 metadata-only，不得当 retrieval evidence。
- 是否建议 baseline：允许 Hermes_memory docs / handoff baseline；runtime final baseline 仍等待测试机验收。
- 是否建议进入下一阶段：否，先完成 live validation gate。
- 下一轮建议：测试机按 `docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md` 验证 self-awareness、natural import success feedback、fuzzy file discovery candidates、ordinary retrieval not suppressed。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C / 测试机验收：需要。
- commit/tag if any：Hermes agent `a12d378e0` / `phase-2.113a-self-awareness-runtime-test-candidate` 已推送；Hermes_memory docs baseline 待本轮提交。
