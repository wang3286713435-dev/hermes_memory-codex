# Active Phase

- 当前 phase：Phase 2.116 Natural Import User-facing Response Polish。
- 本轮目标：把 Phase 2.115 已打通的自然导入 / workspace / auto alias / fuzzy discovery 从调试输出改成正常用户可读回复。
- 修改文件：新增 `docs/PHASE2116_NATURAL_IMPORT_USER_RESPONSE_POLISH_PLAN.md`；更新 `docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/HANDOFF_LOG.md`、`docs/PHASE_BACKLOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：明确 Phase 2.115 真实 OpenWebUI / 8642 flow 已通过；定义 2.116 只改默认 user-facing renderer，不改 upload / ingestion / retrieval / workspace inference 底层。
- 测试结果：docs-only planning；未运行 runtime code、import、DB/index write 或 NAS scan。
- live smoke 结果：上一轮 2.115 已证明 import -> workspace -> generated alias -> retrieval citation -> fuzzy discovery；但默认响应仍打印 `Natural file import diagnostics` 大段调试信息。
- 当前结论：Phase 2.116 是用户体验收口项；目标是让 Hermes 像企业 Agent 说话，而不是把 trace 甩给用户。
- 阻塞点 / 风险点：实现前仍会出现 diagnostics 大段输出；修复时不得删除测试需要的 diagnostics，只应改变默认渲染。
- 是否建议 baseline：允许 docs-only planning baseline；runtime baseline 等 Codex A 实现与测试机复验。
- 是否建议进入下一阶段：进入 Codex A bounded implementation；不要触碰上传、检索、平台 Gateway 或 NAS。
- 下一轮建议：Codex A 按 `docs/NEXT_CODEX_A_PROMPT.md` 修 natural import / fuzzy discovery 默认回复，并保留 debug diagnostics。
- 是否需要 Codex B 审核：需要，Codex A 完成后 review。
- 是否需要 Codex C / 测试机验收：需要，runtime candidate 后复验普通用户看不到大段 diagnostics。
- commit/tag if any：none for this planning update yet。
