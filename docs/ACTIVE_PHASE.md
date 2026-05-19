# Active Phase

- 当前 phase：Phase 2.97 Frontend Gateway Read-only Trial Runbook / Operator Checklist / Git Baseline。
- 背景：Phase 2.96 baseline 已完成：commit `6fff43f`，tag `phase-2.96-gateway-controlled-smoke-result-review-baseline`，pushed=true。
- 本轮目标：完成 Phase 2.97 Codex B review 后的 selective docs baseline；不进入 Phase 2.98。
- 修改文件：`docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：Codex B review 通过，确认 `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md` 正确定义内部受控 read-only frontend trial runbook，并保留 no rollout / no mutation / no content-understanding 边界。
- 测试结果：待 Codex A baseline 前复跑 `git diff --check`、latest JSON parse、latest ignore check、`git status --short`、cached diff checks。
- live smoke 结果：未执行；Phase 2.97 只规划 runbook，不运行 Gateway smoke。
- 当前结论：Phase 2.97 review 通过；下一步只做 selective docs baseline。
- 阻塞点 / 风险点：前端 Gateway 只读试用仍不是生产发布；必须继续禁止 Agent DB CRUD、Agent SQL、NAS scan/copy、parser/writer/index 写入、DWG/RVT 内容理解、真实 `storage_path` 暴露与 rollout。
- 是否建议 baseline：是，建议 Codex A 按 `docs/NEXT_CODEX_A_PROMPT.md` 执行 Phase 2.97 selective docs baseline。
- 是否建议进入下一阶段：否；baseline 后再规划 Phase 2.98，不自动进入。
- 下一轮建议：Codex A 执行 Phase 2.97 baseline，提交并推送 tag 后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
