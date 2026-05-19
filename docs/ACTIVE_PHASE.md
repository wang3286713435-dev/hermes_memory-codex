# Active Phase

- 当前 phase：Phase 2.104a Evidence Availability Contract Docs + Fixtures。
- 背景：Phase 2.104 baseline 已完成：commit `e2c1d3c`，tag `phase-2.104-platform-layered-capability-plan-baseline`，pushed=true；Phase 2.104 已明确 Catalog Layer=current，Evidence / Memory / Orchestration 仍为 next / future。
- 本轮目标：定义 Evidence Availability Contract 的状态枚举、字段、Missing Evidence 语义和 sanitized fixtures，为 Platform Gateway / Hermes 安全区分 catalog-only 与 future evidence search 做准备。
- 修改文件：`docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`、`eval/phase2_inventory/evidence_availability_contract_examples.json`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 Evidence Availability Contract 文档；已新增 7 条 sanitized fixture examples；已核对 Hermes repo docs 与共享 `DigitalDeliveryProject` 契约文件。
- 测试结果：`git diff --check` passed；latest JSON parse passed；fixture JSON parse passed；latest ignore check passed；`git status --short --untracked-files=all` reviewed。
- live smoke 结果：不适用；本阶段只做 docs / contract fixtures，不运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2.104a docs / fixture 内容已实现并通过轻量校验，等待 Codex B review；不是 runtime implementation。
- 阻塞点 / 风险点：`evidence_indexed` 不能被误解为当前平台已开放 `document_evidence_search`；fixtures 不能包含真实项目名、真实文件名、raw path、raw row、asset_uid、source_id、secret 或业务敏感内容。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.104b。
- 下一轮建议：Codex B review Phase 2.104a；通过后由用户显式授权 docs / fixture baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段不运行真实 runtime。
- 当前仍禁止：runtime code、测试修改、新工具实现、`document_evidence_search` 实现、API / CLI / Gateway / DB / NAS smoke、真实 DB / NAS 连接、SQL 执行、raw row / NAS path / storage path / secret 输出、parser、scratch copy、writer smoke、DB / OpenSearch / Qdrant / MinIO / Gateway / platform DB / Hermes memory 写入、Agent DB CRUD、Agent SQL、DWG/RVT/BIM 内容理解、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
