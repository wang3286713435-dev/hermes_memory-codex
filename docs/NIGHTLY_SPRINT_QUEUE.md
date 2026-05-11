# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 `ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、ignored `latest.json` 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.62 Internal MVP Issue Triage Summary Runner

- lane：Green Lane
- 状态：implemented_pending_codex_b_review
- 目标：已实现只读本地 issue triage summary runner，聚合 ignored issue JSON，输出脱敏 summary。
- 允许动作：新增本地 dry-run 脚本、目标测试、文档同步、静态检查、ignored `latest.json` 更新。
- 禁止动作：生成真实 issue records、读取真实 reports/run records、真实上传、API/CLI smoke、自动启动服务、DB/index 写入、外部 issue 自动创建、repair/backfill/reindex、Data Steward/DB/NAS/BIM 实现、production rollout。
- 完成后：停止等待 Codex B review。

### Next Candidate：Phase 2.62 Git Baseline

- lane：Yellow Lane
- 状态：pending_codex_b_review
- 目标：仅在 Codex B 明确通过后 selective baseline。
- 禁止动作：自动跨 phase 继续开发。

### Next Candidate：Mac mini Internal MVP Operator Polish

- lane：Green Lane
- 状态：pending_phase_262_review
- 目标：根据真实内部 MVP 使用反馈继续做 operator polish / issue triage，不扩大到 rollout。
- 禁止动作：DB 写入、外部 issue 自动创建、repair/backfill/reindex、production rollout。

## Red Lane / 当前禁止

1. 第二真实文件 smoke：必须等待用户提供具体小型非敏感文件路径和显式授权。
2. Data Steward / DB / NAS / BIM 实现。
3. cleanup / delete / repair / backfill / reindex / migration。
4. production rollout。
5. 自动选择文件或自动上传文件。
6. 自动创建 Linear / GitHub / 外部 issue。
