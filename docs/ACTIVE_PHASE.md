# Active Phase

- 当前 phase：Phase 2.112h Explicit Natural Import Alias Preservation Fix passed alias gate / retrieval backend env blocker。
- 本轮目标：修复 natural import 阶段未保留用户显式自然语言 alias，导致测试机 import 后 follow-up `@建筑类数据样表` 仍 alias_missing 的 blocker。
- 修改文件：Hermes 主仓库 `agent/memory_kernel/natural_file_import.py`、`tests/agent/test_natural_file_import.py`、`tests/agent/test_natural_file_import_flow.py`、`tests/agent/test_natural_file_import_runtime.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory 交接文档与 ignored `reports/agent_runs/latest.json`。
- 完成内容：扩展 explicit alias parser，覆盖 `别名 @...`、`别名为 @...`、`别名叫 @...`、`别名设为 @...`、`设定别名为 @...`、`我想叫它 @...`；用户请求 alias 优先于 generated alias；malformed alias 继续 fail-closed / not requested；补 follow-up restore 测试证明 `@建筑类数据样表` 可恢复 document/version scoped filters。
- 测试结果：targeted parser / flow / runtime tests `15 passed`；py_compile 通过；natural import / upload client / session scope regression `124 passed`。
- live smoke 结果：未执行真实 OpenWebUI / 8642 upload/import；本轮只做本地最小代码修复与回归验证。
- 当前结论：Phase 2.112h 已通过 Codex B development-machine review；测试机复验已证明 explicit requested alias import 与 follow-up alias restore 均通过；当前 blocker 已从 alias continuity 转为 Hermes_memory retrieval backend 环境问题。
- 阻塞点 / 风险点：follow-up 已 `alias_resolved` 且 `alias_missing=false`，但 retrieval 被 `retrieval_backend_failed_postgres_hostname_unresolved` 抑制；需要修复测试机 Hermes_memory API / DB hostname 环境后重跑 retrieval + citation。不得恢复 alias-global registry 或 ordinary memory alias persistence。
- 是否建议 baseline：runtime test-candidate 已完成；alias gate 已通过；full natural import closeout 仍等待测试机修复 retrieval backend DB hostname 后通过 evidence/citation。
- 是否建议进入下一阶段：否。
- 下一轮建议：测试机 Codex 不再打回 alias 代码；先修复 Hermes_memory retrieval backend 的 `postgres` hostname unresolved 环境问题，再重跑 follow-up retrieval + citation。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C / 测试机验收：是，OpenWebUI / 8642 必须复验。
- commit/tag if any：Hermes agent `e1d38e1ec` / `phase-2.112h-explicit-import-alias-runtime-test-candidate`。
