# Active Phase

- 当前 phase：Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack。
- 背景：Phase 2.94 baseline 已完成：commit `b41bf9b`，tag `phase-2.94-frontend-gateway-smoke-plan-baseline`，pushed=true。
- 本轮目标：把 Phase 2.94 的 read-only frontend / Gateway controlled smoke plan 转成可直接交给 Codex C / 数据库团队 Codex 的执行交接 prompt。
- 修改文件：`docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 Codex C / 数据库团队 controlled smoke handoff prompt，覆盖 placeholders、sanitized inputs、endpoint matrix、safe fields、forbidden-field scan、permission-denied、catalog-only Missing Evidence、Go/Pause/No-Go 与 final report template。Codex B review 已通过，并已写入 selective baseline prompt。
- 测试结果：`git diff --check` 通过；latest JSON parse 通过；`git check-ignore reports/agent_runs/latest.json` 命中；`git status --short` 仅显示 Phase 2.94a 文档 / handoff 文件；无 pytest，因为没有代码变更。
- live smoke 结果：未执行真实 DB / API / CLI Agent / Mac mini / Gateway / parser / NAS / writer / OpenSearch / Qdrant / MinIO / rollout smoke。
- 当前结论：Phase 2.94a handoff pack 已完成为 docs-only artifact；它不是 runtime authorization，未来真实 smoke 仍需用户单独授权。
- 阻塞点 / 风险点：未来执行 smoke 时必须继续保持 read-only、sanitized、fail-closed，且不得泄露 `storage_path` / raw row / NAS path / secrets。
- 是否建议 baseline：是，建议执行 Phase 2.94a selective docs baseline。
- 是否建议进入下一阶段：否；baseline 后再决定是否进入 Phase 2.94b / runtime smoke authorization，不得自动执行真实 frontend / Gateway smoke。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 Phase 2.94a selective docs baseline，然后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要；只有 handoff prompt 经 Codex B review 后、且用户单独授权时才需要。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
