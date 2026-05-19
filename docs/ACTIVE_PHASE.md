# Active Phase

- 当前 phase：Phase 2.103a Capability Handoff Wording Fix。
- 背景：Phase 2.102b baseline 已完成：commit `5c37661`，tag `phase-2.102b-metric-scoring-pack-baseline`，pushed=true；测试机当前已在 Phase 2.102a 并通过 read-only Gateway / catalog-only smoke。
- 本轮目标：修复 Codex B review blocker，移除 `existing memory evidence` 这类可能混淆 catalog metadata、low-sensitive memory references 与 governed content evidence 的表述。
- 计划修改文件：`docs/PHASE2103_TEST_MACHINE_UPDATE_AND_CAPABILITY_HANDOFF.md`、`docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 当前完成内容：已将含混的 memory evidence 表述改为：catalog questions 来自 safe catalog metadata；low-sensitive memory references 仅用于 continuity；content-level answers 必须有 separately governed retrieval / full-text / parser / component evidence；`related_file_ids` 不代表 Hermes 已读取或记住文件正文。
- 测试结果：危险短语检查通过；`git diff --check` 通过；latest JSON parse 通过；latest ignore check 通过；`git status --short --untracked-files=all` 已复核。
- live smoke 结果：不适用；本阶段只做 docs / handoff，不运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2.103a wording fix 已完成，等待 Codex B re-review；测试机可按受控 prompt 更新到 Phase 2.102b baseline；平台可继续 read-only catalog integration；Phase 2 closeout readiness 仍为否。
- 阻塞点 / 风险点：Phase 2 仍缺 PRD 100+ / Roadmap 300+ eval cases、reviewed result JSON、真实 Top5 / citation scoring、structured fact manual spot-check；不能把 catalog-only 能力包装成 DWG/RVT/BIM 内容理解。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；先完成 handoff pack。
- 下一轮建议：Codex B re-review Phase 2.103a wording fix；通过后用户可授权 selective docs baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段不运行真实 runtime。
- 当前仍禁止：runtime code、测试修改、API / CLI / Gateway / DB / NAS smoke、真实 DB / NAS 连接、raw row / NAS path / storage path / secret 输出、parser、scratch copy、writer smoke、DB / OpenSearch / Qdrant / MinIO / Gateway / platform DB / Hermes memory 写入、Agent DB CRUD、Agent SQL、DWG/RVT/BIM 内容理解、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
