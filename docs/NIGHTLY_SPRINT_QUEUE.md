# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 `ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、ignored `latest.json` 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.61b Git Baseline

- lane：Yellow Lane
- 状态：codex_b_reviewed
- 目标：仅对 Phase 2.61b issue storage policy planning 做 selective docs-only Git baseline。
- 允许动作：运行静态检查、selective staging 白名单文档、commit、tag、push、更新 ignored `latest.json`。
- 禁止动作：代码 / 测试 / schema 修改、真实上传、API/CLI smoke、自动启动服务、DB/index 写入、外部 issue 自动创建、repair/backfill/reindex、Data Steward/DB/NAS/BIM 实现、production rollout。
- 完成后：停止等待 Codex B / 用户决定是否进入 Phase 2.61c。

### Next Candidate：Phase 2.61c Local Issue Storage Artifact

- lane：Green Lane
- 状态：pending_phase_261b_baseline
- 目标：如 2.61b 规划通过，提交 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，真实 issue records 继续 ignored。
- 禁止动作：真实 issue 自动生成、外部 issue 创建、DB 写入、repair/backfill/reindex、production rollout。

## Red Lane / 当前禁止

1. 第二真实文件 smoke：必须等待用户提供具体小型非敏感文件路径和显式授权。
2. Data Steward / DB / NAS / BIM 实现。
3. cleanup / delete / repair / backfill / reindex / migration。
4. production rollout。
5. 自动选择文件或自动上传文件。
6. 自动创建 Linear / GitHub / 外部 issue。
