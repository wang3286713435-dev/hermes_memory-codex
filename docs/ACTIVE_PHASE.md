# Active Phase

- 当前 phase：Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation。
- 本轮目标：将用户真实使用中暴露的 P0 blocker 纳入主线：Hermes 不能只会调用外置记忆库，而必须在 8642 / OpenWebUI 用户侧明确知道并使用自己的 memory / workspace / retrieval / evidence kernel。
- 修改文件：`docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`docs/HANDOFF_LOG.md`、ignored `reports/agent_runs/latest.json`；未修改 runtime 代码。
- 完成内容：已把 Phase 2.113 定义为 Codex A P0 runtime handoff，要求补齐 Hermes 自我认知、自然导入成功反馈、自动/推荐别名、模糊找文件候选、低敏 memory/workspace 边界和 overclaim 防护。
- 测试结果：本轮为 docs / handoff baseline；未运行 runtime/API/CLI/import 测试。
- 当前结论：Phase 2.112i 的 scoped natural import Go 仍有效，但 Phase 2 不能收口；Hermes Memory Self-Awareness / Kernel Activation 是新的 P0 blocker，必须由 Codex A 修复后再由 Codex B review 与测试机 / 8642 验证。
- PRD 偏离自查：除 2.113 P0 外，仍存在 eval scale、Top5/citation metrics、structured fact spot-check、parser/source coverage、tender deep-field、version lifecycle、RBAC/ABAC、knowledge admin/human validation、platform native session/evidence/memory unlock 等 P1/closeout 缺口。
- 阻塞点 / 风险点：不要把 memory/workspace metadata 当 content evidence；不要把自然导入 scoped pass 写成 unrestricted production-ready；不要将 Hermes 降级为平台路径问答插件。
- 是否建议 baseline：建议仅对 Phase 2.113 交接文档 baseline。
- 是否建议进入下一阶段：进入 Codex A Phase 2.113 runtime fix；不进入 Phase 3，不宣布 Phase 2 complete。
- 下一轮建议：Codex A 按 `docs/NEXT_CODEX_A_PROMPT.md` 实现最小 runtime fix，并补 targeted tests；完成后交 Codex B review。
- 是否需要 Codex B 审核：需要。
- 是否需要 Codex C / 测试机验收：Codex A 修复后需要测试机 / OpenWebUI / 8642 验证。
- commit/tag if any：pending。
