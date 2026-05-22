# Active Phase

- 当前 phase：Phase 2.115 Workspace Context Inference / Auto Alias / Fuzzy File Discovery。
- 本轮目标：把自然语言导入从测试式 `PROJECT_CONTEXT/ALIAS` 输入升级为 Hermes 自动推断工作区、生成安全别名、写入工作区注册表并支持模糊找文件的企业 Agent 用户流。
- 修改文件：新增 `docs/PHASE2115_WORKSPACE_CONTEXT_AUTO_ALIAS_PLAN.md`；更新 `docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：定义 Phase 2.115 的产品目标、workspace_context 数据边界、auto alias 行为、fuzzy file discovery 行为、测试机验收标准与禁止项。
- 测试结果：docs-only planning；未执行 runtime code、import、DB/index write 或 NAS scan。
- live smoke 结果：上一轮 Phase 2.114a final user-flow acceptance 已 Go；本轮 2.115 尚未实现/验收。
- 当前结论：Phase 2.115 是 Phase 2 stable closeout 前的用户体验补强项，目标是不再要求用户手填 `PROJECT_CONTEXT`。
- 阻塞点 / 风险点：实现前不得宣称自动工作区/自动别名/模糊找文件已完成；仍不得写 raw path/raw content/secret 到 memory。
- 是否建议 baseline：允许 docs-only planning baseline；runtime baseline 等 Codex A 实现与测试机复验。
- 是否建议进入下一阶段：进入 Codex A bounded implementation；不要扩展到平台 Gateway、NAS 全量扫描、DWG/RVT/BIM 内容理解或 production rollout。
- 下一轮建议：Codex A 按 `docs/NEXT_CODEX_A_PROMPT.md` 实现最小 workspace context / auto alias / fuzzy discovery，并发布 runtime test-candidate。
- 是否需要 Codex B 审核：需要，Codex A 完成后 review。
- 是否需要 Codex C / 测试机验收：需要，runtime candidate 后复验无 alias/project context 的自然导入流。
- commit/tag if any：none for this planning update yet。
