# Active Phase

- 当前 phase：Phase 2.115 Workspace Context Inference / Auto Alias / Fuzzy File Discovery。
- 本轮目标：实现自然语言导入的 workspace_context 自动推断、安全 alias 生成 / 绑定、同会话 fuzzy file discovery，并发布 Hermes 主仓 runtime test-candidate。
- 修改文件：Hermes 主仓 `natural_file_import.py`、`natural_file_import_flow.py`、`natural_file_import_runtime.py`、`session_document_scope.py`、`run_agent.py`、相关 tests 与 docs；Hermes_memory 侧更新交接 / TODO / DEV_LOG / NEXT prompt / latest 状态。
- 完成内容：无 `PROJECT_CONTEXT` / 显式 alias 时可从安全文件名 / folder label / query 推断 workspace；生成 `@C塔人力成本测算表` 类安全 alias；alias binding 持久化 workspace metadata；fuzzy discovery 可按 workspace/category/alias 安全候选检索；响应稳定声明 diagnostics 不是 retrieval evidence 且不展示 raw path。
- 测试结果：Hermes 主仓 `git diff --check` 通过；py_compile 通过；natural import / runtime / session scope regression `129 passed`。
- live smoke 结果：本轮未执行真实 OpenWebUI / 8642 upload/import；等待测试机按 runtime candidate 复验无手填 `PROJECT_CONTEXT/ALIAS` 的自然导入流。
- 当前结论：Phase 2.115 本地实现候选已通过 Codex B review；是否收口取决于 Codex C / 测试机真实复验。
- 阻塞点 / 风险点：测试机仍需证明 import -> generated alias -> same-session retrieval/citation -> fuzzy discovery；不得把 workspace metadata 当 content evidence。P2 UX 尾项：低置信度 workspace 应在用户侧更明确请求确认。
- 是否建议 baseline：Hermes 主仓 runtime test-candidate 已可交测试机；不建议 Phase 2.115 总收口。
- 是否建议进入下一阶段：否，先做 test-machine validation gate。
- 下一轮建议：Codex C checkout `phase-2.115-workspace-auto-alias-runtime-test-candidate`，验证无 alias / 无 project context 的自然导入与 fuzzy discovery。
- 是否需要 Codex B 审核：已完成，本地 review pass。
- 是否需要 Codex C / 测试机验收：需要。
- commit/tag if any：Hermes 主仓 `1ac8099e4` / `phase-2.115-workspace-auto-alias-runtime-test-candidate`，已推送 `backup2` 当前语义分支与 tag。
