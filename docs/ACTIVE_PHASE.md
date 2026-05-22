# Active Phase

- 当前 phase：Phase 2.113a Self-Awareness Review Fix。
- 本轮目标：Codex B review Phase 2.113 runtime fix，发现 fuzzy file-discovery guard 过宽，需打回 Codex A 做最小修复。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/context_builder.py`、`agent/memory_kernel/kernel.py`、`agent/memory_kernel/session_document_scope.py`、`agent/memory_kernel/natural_file_import_runtime.py`、`tests/agent/test_natural_file_import_runtime.py`、`tests/agent/test_structured_citation_context.py`、`tests/agent/test_session_document_scope.py`；Hermes_memory `docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`；Hermes 主仓库 `docs/TODO.md`、`docs/DEV_LOG.md`。
- 完成内容：复核确认 2.113 方向正确，但本地 probe 发现 `帮我找一下工程地点`、`帮我找一下主标书里的工期要求` 等普通 retrieval 问题被误判为 `file_discovery_no_safe_candidate` 并 suppress retrieval；已写入 2.113a 修复交接。
- 测试结果：Codex B 复跑 Hermes 主仓库目标测试 `99 passed`；额外 probe 发现 file-discovery routing regression。
- live smoke 结果：本轮未执行真实 OpenWebUI / 8642 / API / CLI 验收，未上传文件。
- 当前结论：不建议 baseline；Phase 2.113 打回修复。必须先区分“找候选文件”和“在文件内容里找答案”。
- 阻塞点 / 风险点：过宽的 `帮我找/找一下` 规则会把正常内容检索误转成 Missing Evidence；self-awareness trigger 也需覆盖更自然的“你可以帮我管理文件吗”等问法。
- 是否建议 baseline：否。
- 是否建议进入下一阶段：否；先执行 2.113a fix。
- 下一轮建议：Codex A 按 `docs/NEXT_CODEX_A_PROMPT.md` 修复 fuzzy file discovery 与 self-awareness trigger，并补 regression tests。
- 是否需要 Codex B 审核：需要。
- 是否需要 Codex C / 测试机验收：需要。
- commit/tag if any：none。
