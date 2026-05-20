# Active Phase

- 当前 phase：Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack Codex B Review。
- 背景：Phase 2.110 baseline 已完成并推送：commit `1a07e42`，tag `phase-2.110-full-closeout-return-baseline`；full Phase 2 closeout 已被正式打回，其中 natural-language import usability 仍缺 committed live metric evidence。
- 本轮目标：创建 natural-language import / MVP closeout gap closure pack，把 proven、partial、missing live evidence、requires authorization、candidate exception 分清。
- 修改文件：`docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`、`eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`、`docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 natural import closeout pack、gap matrix、Codex C future smoke prompt。
- 测试结果：`git diff --check` passed；natural import matrix JSON parse passed；evidence template py_compile passed；`tests/test_phase257a_natural_import_evidence_template.py` 14 passed；latest JSON parse passed；latest ignore check passed；`git status --short` reviewed。
- live smoke 结果：未执行；本阶段只准备未来授权 smoke，不运行真实自然语言导入、不上传、不连接 API / DB / NAS / Gateway。
- 当前结论：Codex B review 通过；Phase 2.111 docs / matrix 可 baseline。natural-language import 技术路径有证明，但 full Phase 2 closeout 仍需要新的 accepted Hermes CLI natural-language import smoke，或用户显式例外移出 Phase 2。
- 阻塞点 / 风险点：direct API upload 不能替代 natural-language import；planning / mocked evidence 不能替代 live usability evidence；真实 smoke 需要用户授权具体小型非敏感文件。
- 是否建议 baseline：是，执行 selective docs / matrix baseline；不 stage 无关 `docs/digital-delivery-standards/`。
- 是否建议进入 Phase 3：否。
- 下一轮建议：baseline 后等待用户二选一：授权具体小型非敏感文件给 Codex C 做自然语言导入 acceptance smoke，或显式将 natural import usability 移出 Phase 2 closeout。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要；只有用户授权具体文件后才执行 `docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md`。
- 当前仍禁止：runtime code、测试修改、真实自然语言导入 smoke、上传文件、平台 repo 修改、DB / NAS / Gateway / API 连接、SQL 执行、Hermes memory 写入、facts 写入、documents/chunks 写入、parser / writer / repair / backfill / reindex / delete / migration / rollout、raw path / raw row / raw answer / secret 输出、production rollout、无关 `docs/digital-delivery-standards/` staging。
