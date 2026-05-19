# Active Phase

- 当前 phase：Phase 2.104 Platform Layered Capability Plan。
- 背景：Phase 2.103 baseline 已完成：commit `3c38a06`，tag `phase-2.103-test-machine-capability-handoff-baseline`，pushed=true。
- 本轮目标：把平台接入从 `catalog-only` 说明推进到 `Catalog / Evidence / Memory / Orchestration` 分层能力设计，避免 Hermes 被误接成路径问答 AI。
- 修改文件：`docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 Phase 2.104 分层能力计划；已核对 Hermes repo docs 与共享 `DigitalDeliveryProject` 契约文件；已记录 Catalog current、Evidence/Memory next、Orchestration later 的边界。
- 测试结果：`git diff --check` passed；latest JSON parse passed；latest ignore check passed；`git status --short --untracked-files=all` reviewed。
- live smoke 结果：不适用；本阶段只做 docs / contract planning，不运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2.104 docs-only 计划已实现并通过轻量校验，等待 Codex B review；不是 runtime implementation。
- 阻塞点 / 风险点：Evidence Layer / Memory Layer / Orchestration Layer 不能写成 current；低敏 memory references 不能解释为 file content evidence；共享文档后续如改合同 wording 需单独同步。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.104a。
- 下一轮建议：Codex B review `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`；通过后由用户显式授权 docs baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段不运行真实 runtime。
- 当前仍禁止：runtime code、测试修改、新工具实现、API / CLI / Gateway / DB / NAS smoke、真实 DB / NAS 连接、raw row / NAS path / storage path / secret 输出、parser、scratch copy、writer smoke、DB / OpenSearch / Qdrant / MinIO / Gateway / platform DB / Hermes memory 写入、Agent DB CRUD、Agent SQL、DWG/RVT/BIM 内容理解、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
