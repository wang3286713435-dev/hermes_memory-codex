# Active Phase

- 当前 phase：Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack Handoff。
- 背景：Phase 2.110 baseline 已完成并推送：commit `1a07e42`，tag `phase-2.110-full-closeout-return-baseline`；full Phase 2 closeout 已被正式打回，原因之一是 natural-language import usability 未形成 committed live metric evidence。
- 本轮目标：写入 Codex A 文件化任务，让 Codex A 创建 natural-language import / MVP closeout gap closure pack，而不是由 Codex B 直接实现功能代码。
- 修改文件：`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- Codex A 预期产物：`docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`、`eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`，可选 `docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md`。
- 当前结论：下一步应先整理自然语言导入验收矩阵和真实 smoke 授权门槛；不得直接宣布 full Phase 2 complete。
- 阻塞点 / 风险点：不得把历史 planning / mocked flow / direct API upload 当作完整自然语言导入验收；真实 smoke 仍需用户授权具体文件和执行环境。
- 是否建议 baseline：是，建议 selective prompt/docs baseline；不 stage 无关 `docs/digital-delivery-standards/`。
- 是否建议进入 Phase 3：否，先让 Codex A 完成 Phase 2.111 gap closure pack。
- 是否需要 Codex B 审核：Codex A 完成后需要 Codex B 审核。
- 是否需要 Codex C 真实终端验收：当前不需要；若 Codex A 创建 Codex C smoke prompt，也只能在用户明确授权后执行。
- 当前仍禁止：runtime code、测试修改、平台 repo 修改、DB / NAS / Gateway / API 连接、SQL 执行、Hermes memory 写入、facts 写入、documents/chunks 写入、NAS scan/copy/parser、真实自然语言导入 smoke、raw path / raw row / raw answer / secret 输出、production rollout、无关 `docs/digital-delivery-standards/` staging。
