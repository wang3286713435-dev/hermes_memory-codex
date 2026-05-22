# Active Phase

- 当前 phase：Phase 2.112h Explicit Natural Import Alias Preservation Fix runtime candidate / test-machine validation pending。
- 本轮目标：修复 natural import 阶段未保留用户显式自然语言 alias，导致测试机 import 后 follow-up `@建筑类数据样表` 仍 alias_missing 的 blocker。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/natural_file_import.py`、`tests/agent/test_natural_file_import.py`、`tests/agent/test_natural_file_import_flow.py`、`tests/agent/test_natural_file_import_runtime.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory 交接文档与 ignored `reports/agent_runs/latest.json`。
- 完成内容：扩展 explicit alias parser，覆盖 `别名 @...`、`别名为 @...`、`别名叫 @...`、`别名设为 @...`、`设定别名为 @...`、`我想叫它 @...`；用户请求 alias 优先于 generated alias；malformed alias 继续 fail-closed / not requested；补 follow-up restore 测试证明 `@建筑类数据样表` 可恢复 document/version scoped filters。
- 测试结果：targeted parser / flow / runtime tests `15 passed`；py_compile 通过；natural import / upload client / session scope regression `124 passed`。
- live smoke 结果：未执行真实 OpenWebUI / 8642 upload/import；本轮只做本地最小代码修复与回归验证。
- 当前结论：Phase 2.112h 已通过 Codex B development-machine review；Hermes agent runtime test-candidate 已 baseline 并推送；需要测试机复验 explicit requested alias import -> follow-up retrieval + citation。
- 阻塞点 / 风险点：真实 OpenWebUI / 8642 仍未复验；Phase 2 natural import closeout 继续 blocked；不得恢复 alias-global registry 或 ordinary memory alias persistence。
- 是否建议 baseline：runtime test-candidate 已完成；full natural import closeout 仍等待测试机 OpenWebUI / 8642 通过。
- 是否建议进入下一阶段：否。
- 下一轮建议：测试机 Codex checkout `phase-2.112h-explicit-import-alias-runtime-test-candidate`，重启 8642，复验用户请求 `@建筑类数据样表` 是否被保存且 follow-up scoped retrieval 有 citation。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C / 测试机验收：是，OpenWebUI / 8642 必须复验。
- commit/tag if any：Hermes agent `e1d38e1ec` / `phase-2.112h-explicit-import-alias-runtime-test-candidate`。
