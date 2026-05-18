# Active Phase

- 当前 phase：Phase 2.94 Frontend / Gateway Controlled Smoke Planning。
- 背景：Phase 2.93 baseline 已完成：commit `d84cb62`，tag `phase-2.93-readonly-gateway-implementation-review-baseline`，pushed=true。
- 本轮目标：规划未来 read-only frontend / Gateway controlled smoke，覆盖 response schema、trace identifiers、safe catalog identifiers、permission-denied copy、Missing Evidence / `asset_catalog_only` 与 forbidden-field negative assertions。
- 修改文件：`docs/PHASE294_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PLAN.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 `docs/PHASE294_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PLAN.md`；规划了 future controlled smoke 的 preconditions、case matrix、sanitized inputs、safe response fields、forbidden assertions、Missing Evidence、permission-denied checks、Go / Pause / No-Go 与 Codex C / DB team handoff。Codex B review 已通过，并已写入 selective baseline prompt。
- 测试结果：`git diff --check`、latest JSON parse、latest ignore check、`git status --short` 已按本轮要求执行并通过；无 pytest，因为没有代码变更。
- live smoke 结果：未执行真实 DB / API / CLI Agent / Mac mini / Gateway / parser / NAS / writer / OpenSearch / Qdrant / MinIO / rollout smoke。
- 当前结论：Phase 2.94 planning 已完成；默认不执行真实 smoke，后续 runtime smoke 需要单独授权。
- 阻塞点 / 风险点：未来真实 smoke 必须由 DB team / Codex C 使用 sanitized inputs，并保持 read-only；Phase 2.94a 仍需单独规划和授权。
- 是否建议 baseline：是，建议执行 Phase 2.94 selective docs baseline。
- 是否建议进入下一阶段：否；baseline 后再规划 Phase 2.94a，不得自动进入真实 smoke。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 Phase 2.94 selective docs baseline，然后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要；只有 Phase 2.94a 或后续显式授权后才需要。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
