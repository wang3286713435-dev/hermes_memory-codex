# Active Phase

- 当前 phase：Phase 2.108 Standalone Kernel Freeze Contract。
- 背景：稳定平台集成基线已完成并推送：commit `fb3781a`，tag `phase-2-stable-hermes-platform-integration-baseline`；平台 0B Gateway controlled live smoke 已回传 `Go`，但该基线只代表平台安全接入，不代表 Hermes 只能是平台 catalog-only 插件。
- 本轮目标：补齐 Phase 2 收口前的 standalone Hermes kernel freeze contract，明确 Hermes 脱离平台时仍保留企业 Agent 内核、workspace、session/context、memory/evidence/retrieval、文件治理和后续 NAS governance 路线。
- 修改文件：`docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md`、`docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`、`eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、共享 `DigitalDeliveryProject` 契约文件、ignored `reports/agent_runs/latest.json`。
- 完成内容：新增 standalone kernel freeze contract；将平台只读 catalog-only 定义为当前安全表面而非 Hermes 产品上限；保留 Phase 3 对 native session、Evidence Layer、Memory Layer、NAS governance、workspace 的解锁路线。
- 测试结果：待运行 `git diff --check`、JSON parse、latest ignore check 与 shared-doc path check。
- 当前结论：Phase 2 stable tag 可继续作为平台安全集成基线；但 Phase 2 收口前必须记录 Hermes 独立内核能力不会被平台接入方式削弱。
- 阻塞点 / 风险点：runtime session/thread native lifecycle、Evidence Layer、Memory runtime、target-scale metrics、natural import usability 仍为 known risk；Data Steward full product、Agent DB CRUD/SQL、NAS semantic collection、DWG/RVT/BIM 内容理解仍为 Phase 3+。
- 是否建议 baseline：是，建议 selective docs / shared-contract baseline；不 stage 无关 `docs/digital-delivery-standards/`。
- 是否建议进入下一阶段：否；先完成 Phase 2.108 review / baseline，再判断是否进入 Phase 2 final freeze checklist 或 Phase 3 planning。
- 是否需要 Codex B 审核：本轮由 Codex B 执行 standalone kernel freeze contract 收口。
- 是否需要 Codex C 真实终端验收：不需要；本轮为 docs / contract-only，不连接平台、DB、NAS、Gateway 或 API。
- 当前仍禁止：runtime code、测试修改、平台 repo 修改、DB / NAS / Gateway / API 连接、SQL 执行、Hermes memory 写入、facts 写入、documents/chunks 写入、NAS scan/copy/parser、raw path / raw row / raw answer / secret 输出、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
