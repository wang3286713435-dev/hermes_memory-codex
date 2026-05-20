# Active Phase

- 当前 phase：Phase 2 Stable Hermes Platform Baseline Tag。
- 背景：Phase 2.107 baseline 已完成并推送：commit `3ef3966`，tag `phase-2.107-minimal-freeze-blocker-closure-baseline`；平台 0B Gateway hardening 已完成，`EXPECT_HERMES_AGENT_AVAILABLE=true` controlled live smoke 返回 `PASS=14 FAIL=0`。
- 本轮目标：将 `Phase 2 Stable Hermes for Platform Integration` 钉成稳定平台集成基线 tag，并更新测试机 checkout prompt。
- 修改文件：`docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`、`eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已将测试机更新 prompt 从占位符改为 stable tag `phase-2-stable-hermes-platform-integration-baseline`；freeze checklist 已记录 Platform 0B Gateway live smoke Go 与 native session runtime known risk。
- 测试结果：待运行 `git diff --check`、JSON parse、latest ignore check 与 stable checklist semantic check。
- live smoke 结果：采用平台回传结果；`EXPECT_HERMES_AGENT_AVAILABLE=true` 受控 smoke 已 Go，覆盖 authorityHealth.orange、responseId/queryId/traceId、safeMemoryCandidates=[]、sanitizedContextRefs=[]、invalid project fail-closed、高危字段 fail-closed、Missing Evidence、无泄露、无 parser/index/rollout。
- 当前结论：具备创建 stable Hermes platform integration baseline tag 的条件；该 tag 只表示平台稳定集成基线，不是生产 rollout，不是 Phase 2 full PRD/Roadmap closeout。
- 阻塞点 / 风险点：runtime session/thread native lifecycle、Evidence Layer、Memory runtime、target-scale metrics、natural import usability 仍为 known risk / 后续决策；Data Steward full product、Agent DB CRUD/SQL、NAS semantic collection、DWG/RVT/BIM 内容理解仍为 Phase 3+。
- 是否建议 baseline：是，建议 selective docs/checklist baseline 后创建并推送 stable tag。
- 是否建议进入下一阶段：否；stable tag 后先让测试机 checkout 该 tag，再决定 Phase 2 freeze 后续。
- 是否需要 Codex B 审核：本轮由 Codex B 执行稳定基线收口。
- 是否需要 Codex C 真实终端验收：已由平台 / 测试机 controlled live smoke 回传 Go；本仓不重复连接平台服务。
- 当前仍禁止：runtime code、测试修改、平台 repo 修改、共享文件直接修改、DB / NAS / Gateway / API 连接、SQL 执行、Hermes memory 写入、facts 写入、documents/chunks 写入、NAS scan/copy/parser、raw path / raw row / raw answer / secret 输出、production rollout、Phase 3 transition、无关 `docs/digital-delivery-standards/` staging。
