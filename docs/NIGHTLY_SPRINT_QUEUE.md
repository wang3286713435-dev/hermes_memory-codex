# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.56e Selective Git Baseline

- lane：Yellow Lane
- 状态：codex_b_review_passed_baseline_prompt_ready
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 目标：只执行 Phase 2.56e 双仓 selective Git baseline。
- 允许动作：轻量验证、白名单 staging、commit、tag、push、更新 ignored latest 状态。
- 禁止动作：再次真实 upload、cleanup/delete/repair/backfill/reindex、DB/facts/version/OpenSearch/Qdrant 写入、Data Steward/DB/NAS 实现、production rollout。
- 完成后：停止等待 Codex B review；不得自动进入 Phase 2.57。

### Next Candidate：Phase 2.57 Natural Import MVP Evidence / Operator Usability Planning

- lane：Green Lane
- 状态：candidate_after_phase_256e_baseline
- 目标：规划自然语言导入的 MVP evidence pack、Mac mini operator runbook 和少量可用性回归；不扩大到 NAS/TB/Data Steward。
