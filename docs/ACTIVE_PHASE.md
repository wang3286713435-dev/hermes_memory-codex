# Active Phase

- 当前 phase：Phase 2.112h Explicit Natural Import Alias Preservation Fix Handoff。
- 本轮目标：打回 2.112g，要求 Codex A 修复自然语言导入阶段未保留用户指定 `@建筑类数据样表` alias 的问题。
- 最新测试机结论：Pause。2.112g 已 checkout 且 8642 重启；import 成功并绑定了某个 alias，但不是用户请求的 `@建筑类数据样表`；follow-up `@建筑类数据样表` 仍 `alias_missing=true`、`retrieval_suppressed=true`。
- Codex B 判断：2.112g stable-owner path 大概率已解决；新 blocker 是 natural import explicit alias parsing / preservation。当前 `_ALIAS_RE` 只支持较窄的 `绑定为/命名为/叫 @alias` 表达，真实自然语言的 `别名 @...`、`别名为 @...`、`设定别名为 @...` 等可能被漏掉并触发 generated alias。
- 修改文件：Hermes_memory 交接文档与 NEXT prompt；不修改 runtime 代码。
- 当前结论：需 Codex A 执行 Phase 2.112h bounded fix；full natural import closeout 继续 blocked。
- 是否建议进入下一阶段：否。
- 是否需要 Codex B 审核：Codex A 修复后需要。
- 是否需要测试机验收：Codex B review 后仍必须测试机 OpenWebUI / 8642 复验 import requested alias -> follow-up retrieval + citation。

- 当前 phase：Phase 2.112g Header-only Stable Owner Restore Fix Review Passed / Test-machine Validation Pending。
- 本轮目标：修复 OpenWebUI / 8642 follow-up 只有 `X-Hermes-Session-Id` header 时 stable owner 未恢复，导致 natural import `@alias` continuity restore 失败。
- 修改文件：Hermes 主仓库 `gateway/platforms/api_server.py`、`tests/gateway/test_api_server.py`、`docs/TODO.md`、`docs/DEV_LOG.md`；Hermes_memory `docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`reports/agent_runs/latest.json`。
- 完成内容：`X-Hermes-Session-Id` 已加入 gateway stable owner fallback headers；accepted import turn 与 header-only follow-up 会生成同一 safe owner；补 header-only owner、owner equivalence、alias continuity restore scoped filters 与 no `stable_owner_missing` 测试。
- 测试结果：py_compile 通过；新增 gateway targeted tests `3 passed`；natural import / upload client / session scope regression `109 passed`；完整 `tests/gateway/test_api_server.py` 在当前主仓 `.venv` 因缺 async pytest 插件 false-fail existing async tests。
- live smoke 结果：未执行真实 upload/import/OpenWebUI/8642；本轮仅做本地最小代码修复与回归验证。
- 当前结论：Phase 2.112g 已通过 Codex B review；Hermes agent runtime test-candidate 已 baseline 并推送；仍需测试机 OpenWebUI / 8642 复验。
- 阻塞点 / 风险点：本机完整 gateway async suite 环境不可用；真实 follow-up retrieval + citation 尚未复验；不得恢复 alias-global registry 或 ordinary memory alias persistence。
- 是否建议 baseline：runtime test-candidate 已完成；full runtime baseline 仍等待测试机 OpenWebUI / 8642 通过。
- 是否建议进入下一阶段：否。
- 下一轮建议：测试机 Codex checkout `phase-2.112g-header-owner-restore-runtime-test-candidate`，重启 8642，并执行真实 OpenWebUI import -> follow-up `@建筑类数据样表` retrieval + citation。
- 是否需要 Codex B 审核：runtime candidate 已通过；测试机回传后再做最终 review。
- 是否需要 Codex C / 测试机验收：是，OpenWebUI / 8642 必须复验。
- commit/tag if any：Hermes agent `20d9fb561` / `phase-2.112g-header-owner-restore-runtime-test-candidate`。
