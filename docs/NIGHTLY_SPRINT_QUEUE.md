# Nightly Sprint Queue

## Current Queue

### Current Item：Phase 2.63 Git Baseline

- lane：Yellow Lane
- 状态：codex_b_reviewed_baseline_ready
- 目标：仅对 Phase 2.63 operator daily summary runner 做 selective Git baseline。
- 允许动作：复跑目标测试、selective stage 白名单、commit/tag/push、更新 ignored latest。
- 禁止动作：真实 issue records、API/CLI smoke、upload、DB/index 写入、外部 issue 自动创建、repair/backfill/reindex、Data Steward/DB/NAS/BIM 实现、production rollout。
- 完成后：停止等待 Codex B / 用户，不自动进入 Phase 2.64。

### Next Candidate：Phase 2.64 Data Steward DB Branch Intake / PR Review

- lane：Green / Yellow Lane
- 状态：pending_after_phase_263_baseline
- 目标：独立阶段评审 DB branch closeout、PR readiness 与 feature flag / catalog-only 边界。
- 禁止动作：真实 DB 连接、NAS scan、BIM/TB 文件池、migration、merge to main、OpenSearch/Qdrant 写入。

## Red Lane / 当前禁止

1. 第二真实文件 smoke：必须等待用户提供具体小型非敏感文件路径和显式授权。
2. Data Steward / DB / NAS / BIM 实现或 merge。
3. cleanup / delete / repair / backfill / reindex / migration。
4. production rollout。
5. 自动选择文件或自动上传文件。
6. 自动创建 Linear / GitHub / 外部 issue。
