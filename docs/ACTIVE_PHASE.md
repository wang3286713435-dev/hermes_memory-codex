# Active Phase

- 当前 phase：Phase 2.112b Natural Import Alias Binding / Retrieval Blocker Fix prompt。
- 本轮目标：根据测试机 OpenWebUI / 8642 Pause 报告，交接 Codex A 修复 import 成功后 `alias_bind_failed`、follow-up `alias_missing=true`、`retrieval_suppressed=true` 的最小阻塞点。
- 修改文件：Hermes_memory 交接文档；新增测试机专用验证 prompt；未修改 Hermes runtime code。
- 已确认结果：测试机真实导入已成功返回 `document_id=6e89bbe8-599f-47e3-9cca-d8e7b7ae4f1b`、`version_id=0df440d0-9f2b-4fd5-8a84-19435fdd1b2f`、`chunk_count=6`、`indexed_count=6`。
- 当前阻塞点：标题/别名绑定返回 `alias_bind_failed`；同会话 `@建筑类数据样表` follow-up 返回 `alias_missing=true` 与 `retrieval_suppressed=true`，citation 无法验收。
- 角色边界：Codex A 负责开发修复；Codex C 是开发机测试代码/验证支持会话；测试机 Codex 才负责 Mac mini / OpenWebUI / 8642 真实环境验收。
- 当前结论：Phase 2.112 不能 baseline；必须先完成 Phase 2.112b runtime fix，再由 Codex B review，随后由测试机 Codex 执行真实验证。
- 是否建议 baseline：否。
- 是否建议进入下一阶段：否。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；测试机验收使用 `docs/CODEX_TEST_MACHINE_PHASE2112_NATURAL_IMPORT_VALIDATION_PROMPT.md`，不是 `docs/NEXT_CODEX_C_PROMPT.md`。
- 当前仍禁止：production rollout、NAS scan、DB CRUD/SQL、Gateway/平台 contract 修改、direct API upload 替代 evidence、import diagnostics 当 retrieval evidence、raw path/secret/file content 输出、repair/backfill/reindex/delete/migration。
- commit/tag if any: none.
