# Active Phase

- 当前 phase：Phase 2.105 Hermes Kernel Authority / Platform Alignment Contract。
- 背景：Phase 2.104d baseline 已完成：commit `f0fabc4`，tag `phase-2.104d-feedback-scoring-linkage-contract-baseline`，pushed=true；Phase 2.104 / 2.104a / b / c / d 已完成 Catalog / Evidence / Memory / Feedback 分层契约规划。
- 本轮目标：通过 Hermes 侧 docs / contract / fixture 明确 Hermes 与 Platform 权责边界，防止 Hermes 被降级为平台内单轮智能问答插件。
- 修改文件：`docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`、`docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md`、`eval/phase2_inventory/hermes_platform_authority_alignment_examples.json`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 Hermes Kernel Authority / Platform Alignment contract；已新增 Platform Team handoff；已新增 9 条 sanitized authority-alignment fixture examples；已核对 Hermes repo docs 与共享 `DigitalDeliveryProject` 契约文件。
- 测试结果：`git diff --check` passed；latest JSON parse passed；fixture JSON parse passed；latest ignore check passed；`git status --short --untracked-files=all` reviewed。
- live smoke 结果：不适用；本阶段只做 docs / contract fixtures，不运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2.105 docs / fixture 内容已实现并通过轻量校验，等待 Codex B review；Hermes 是 enterprise agent kernel，Platform 是 UI + Gateway + permission/data surface，Data Steward / Catalog 是 Hermes 能力模块之一。
- 阻塞点 / 风险点：平台若只传 single-turn user message，会把 Hermes 压成 stateless plugin；平台不得拥有 reasoning state；Gateway 权限与 redaction 权威必须保留；Data Steward 不得被等同于 Hermes 全貌。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.106 或 runtime session implementation。
- 下一轮建议：Codex B review Phase 2.105；通过后由用户显式授权 docs / fixture baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段不运行真实 runtime。
- 当前仍禁止：runtime code、测试修改、平台 repo 修改、共享文件直接修改、Gateway/session runtime 实现、DB / NAS / Gateway / API / OpenSearch / Qdrant / MinIO 连接、SQL 执行、API / CLI / Gateway smoke、Hermes memory 写入、facts 写入、documents/chunks 写入、NAS scan/copy/parser、raw path / raw row / raw answer / secret 输出、production rollout、无关 `docs/digital-delivery-standards/` staging。
