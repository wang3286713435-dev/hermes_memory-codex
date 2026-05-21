# Active Phase

- 当前 phase：Phase 2.112b Natural Import Alias Binding / Retrieval Blocker Fix implemented。
- 本轮目标：修复测试机 OpenWebUI / 8642 暴露的 natural import 成功后 `alias_bind_failed`、follow-up `alias_missing=true`、`retrieval_suppressed=true` 断链。
- 修改文件：Hermes 主仓 `run_agent.py`、`agent/memory_kernel/session_document_scope.py`、`tests/agent/test_natural_file_import_runtime.py`、`tests/agent/test_session_document_scope.py`、主仓 TODO/DEV_LOG；Hermes_memory TODO/DEV_LOG/HANDOFF/PHASE_BACKLOG/ACTIVE_PHASE/latest.json。
- 完成内容：同一 conversation history 中的 natural import diagnostics 可恢复 session alias；已存在导入 alias 的 title rebind 可复用既有 `document_id/version_id`，不再因 resolver miss 失败；import diagnostics 仍不作为 retrieval evidence。
- 测试结果：`py_compile` 通过；`tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py tests/agent/test_session_document_scope.py -q` 结果 `99 passed`。
- live smoke 结果：本轮未重复真实导入、未跑 OpenWebUI / 8642 live smoke。
- 当前结论：Codex B review 通过，开发机侧 blocker fix 可进入测试机真实验收；真实验收仍需测试机 Codex 重跑 alias + retrieval + citation。
- 阻塞点 / 风险点：真实 OpenWebUI / 8642 尚未复验；主仓仍有既存无关 dirty，不得混入后续 baseline。
- 是否建议 baseline：否，需先测试机真实 OpenWebUI / 8642 验收。
- 是否建议进入下一阶段：否。
- 下一轮建议：测试机 Codex 执行 `docs/CODEX_TEST_MACHINE_PHASE2112_NATURAL_IMPORT_VALIDATION_PROMPT.md`。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：否；真实 Mac mini / OpenWebUI / 8642 由测试机 Codex 执行。
- commit/tag if any: none.
