# Active Phase

- 当前 phase：Phase 2.104c Governed Document Evidence Search Contract Planning。
- 背景：Phase 2.104b baseline 已完成：commit `d67d7ea`，tag `phase-2.104b-memory-continuity-permission-contract-baseline`，pushed=true；Phase 2.104a / 2.104b 已分别定义 Evidence Availability 与 Memory Continuity Permission Boundary。
- 本轮目标：规划 future-only `document_evidence_search` contract，让 Hermes 后续能从 catalog-only 走向 governed evidence retrieval，但不实现 runtime search。
- 修改文件：`docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md`、`eval/phase2_inventory/document_evidence_search_contract_examples.json`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 governed document evidence search contract plan；已新增 9 条 sanitized fixture examples；已核对 Hermes repo docs 与共享 `DigitalDeliveryProject` 契约文件。
- 测试结果：`git diff --check` passed；latest JSON parse passed；fixture JSON parse passed；latest ignore check passed；`git status --short --untracked-files=all` reviewed。
- live smoke 结果：不适用；本阶段只做 docs / contract fixtures，不运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2.104c docs / fixture 内容已实现并通过轻量校验，等待 Codex B review；不是 runtime implementation。
- 阻塞点 / 风险点：`document_evidence_search` 仍是 future-only；不得被平台误认为当前 runtime capability；memory refs 不能当 evidence；catalog-only / parser-required / unsupported / permission-denied 必须走 Missing Evidence 或安全拒绝。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.104d。
- 下一轮建议：Codex B review Phase 2.104c；通过后由用户显式授权 docs / fixture baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段不运行真实 runtime。
- 当前仍禁止：runtime code、测试修改、`document_evidence_search` 实现、parser/writer/scratch copy/indexing、memory runtime 实现、新工具实现、API / CLI / Gateway / DB / NAS smoke、真实 DB / NAS 连接、SQL 执行、raw row / NAS path / storage path / secret 输出、DB / OpenSearch / Qdrant / MinIO / Gateway / platform DB / Hermes memory 写入、Agent DB CRUD、Agent SQL、DWG/RVT/BIM 内容理解、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
