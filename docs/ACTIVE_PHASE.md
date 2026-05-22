# Active Phase

- 当前 phase：Phase 2.114a Natural Import Path Parser Fix。
- 本轮目标：修复 Phase 2.114 final user-flow acceptance 暴露的 natural import parser blocker：中文 prompt 中授权绝对路径未被提取，导致 upload adapter not_called / missing_path。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/natural_file_import.py`、`tests/agent/test_natural_file_import.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory `docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`docs/NEXT_CODEX_A_PROMPT.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：未加引号 path extraction 改为按扩展名捕获，支持 fullwidth colon、中文句号、中文路径和目录空格；目录路径仍可被识别为不支持目录导入；多路径继续 fail-closed。
- 测试结果：新增 parser regression 先失败后修复；Hermes 主仓库 py_compile 通过；`tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py` 为 `54 passed`。
- live smoke 结果：本轮未执行真实 OpenWebUI / 8642 import，未上传文件。
- 当前结论：Phase 2.114a parser blocker 已本地修复，并已发布 runtime test-candidate；需要测试机用一个授权小文件复跑 Phase 2.114 final user-flow acceptance。
- 阻塞点 / 风险点：真实 OpenWebUI / 8642 import 尚未复验；本轮 runtime candidate 不代表 production rollout 或 unrestricted import。
- 是否建议 baseline：已完成 runtime test-candidate；不建议 Phase 2 stable freeze，等待 Phase 2.114 live Go。
- 是否建议进入下一阶段：否；下一步是 Codex C / 测试机复验 Phase 2.114。
- 下一轮建议：测试机 checkout runtime candidate，重启 8642，使用授权小样本验证 import -> alias -> retrieval -> citation -> evidence boundary。
- 是否需要 Codex B 审核：需要。
- 是否需要 Codex C / 测试机验收：需要。
- commit/tag if any：Hermes 主仓库 commit `c8ed29a83c441f58939f64b6b175ae4cac980ea3`；tag `phase-2.114a-natural-import-path-parser-runtime-test-candidate`；已推送 `backup2`。
