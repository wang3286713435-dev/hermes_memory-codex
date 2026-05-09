# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Current Item：Phase 2.59 Natural Import Second Smoke Planning

- lane：Green Lane
- 状态：implemented_waiting_codex_b_review
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 目标：规划第二个用户授权文件 natural import smoke 与 Codex C 待授权模板。
- 允许动作：docs-only planning、git diff/json/status checks、ignored latest 更新。
- 禁止动作：上传文件、API/CLI smoke、DB/index 写入、repair/backfill/reindex、Data Steward/DB/NAS 实现、rollout、baseline。
- 完成结果：Phase 2.59 planning、Codex C pending authorization template、operator checklist update 已完成。
- 下一步：停止等待 Codex B review；通过后再执行 docs-only baseline。
