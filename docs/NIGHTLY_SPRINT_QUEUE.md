# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 `ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、ignored `latest.json` 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.60 Internal MVP Launch Readiness Pack

- lane：Green Lane
- 状态：implemented_waiting_codex_b_review
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 目标：实现只读 local readiness runner、目标测试与 Mac mini operator 文档同步，让本地 MVP 更接近内部真实使用。
- 允许动作：只读脚本、unit tests、offline dry-run、文档同步、ignored latest 更新。
- 禁止动作：真实上传、第二文件 smoke、Hermes CLI query smoke、自动启动服务、DB/index 写入、repair/backfill/reindex、Data Steward/DB/NAS/BIM 实现、production rollout、baseline。
- 完成结果：runner、目标测试、readiness plan、operator checklist update 已完成。
- 下一步：停止等待 Codex B review。

### Next Candidate：Phase 2.60 Codex B Review

- lane：Green Lane
- 状态：pending_current_item
- 目标：审核 2.60 diff、测试结果、readiness dry-run 输出和边界。
- 禁止动作：实现新功能、真实上传、DB/index 写入、rollout。

### Next Candidate：Phase 2.60 Git Baseline

- lane：Yellow Lane
- 状态：pending_codex_b_review
- 目标：仅在 Codex B 明确通过后 selective baseline。
- 禁止动作：自动跨 phase 继续开发。

## Red Lane / 当前禁止

1. 第二真实文件 smoke：必须等待用户提供具体小型非敏感文件路径和显式授权。
2. Data Steward / DB / NAS / BIM 实现。
3. cleanup / delete / repair / backfill / reindex / migration。
4. production rollout。
5. 自动选择文件或自动上传文件。
