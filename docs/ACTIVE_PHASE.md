# Active Phase

- 当前 phase：Phase 2.95 Shared Contract Alignment。
- 背景：Phase 2.94a baseline 已完成：commit `712cd83`，tag `phase-2.94a-gateway-smoke-handoff-baseline`，pushed=true。
- 本轮目标：将共享文档空间 `DigitalDeliveryProject` 正式纳入 Hermes 主线契约维护流程，记录 Hermes 对 catalog-only、Missing Evidence、memory、Gateway 权限与路径脱敏边界的对齐结果。
- 修改文件：`docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已读取 Phase 2.95 指定的 14 个共享文件，并新增 Hermes-side alignment 文档，记录 adopted shared files、Hermes-owned / reviewed files、contract boundaries、sync rules、mismatch list 与 runtime 禁止项。Codex B review 已通过，并已写入 selective baseline prompt。
- 测试结果：`git diff --check` 通过；latest JSON parse 通过；`git check-ignore reports/agent_runs/latest.json` 命中；`git status --short` 仅显示 Phase 2.95 文档 / handoff 文件；无 pytest，因为没有代码变更。
- live smoke 结果：未执行真实 DB / API / CLI Agent / Mac mini / Gateway / parser / NAS / writer / OpenSearch / Qdrant / MinIO / rollout smoke。
- 当前结论：Phase 2.95 docs-only shared contract alignment 已完成；未发现 required shared contract mismatch；未修改共享空间文件；Codex B review 通过。
- 阻塞点 / 风险点：后续修改 Catalog Tool schema、Missing Evidence、feedback、memory boundary、Gateway response 或能力状态时，必须同步共享文档；不能把 shared docs 当 runtime 授权。实际 frontend / Gateway controlled smoke 已在正常平台登录 + 项目切换链路下返回 Go；仍需 Phase 2.96 做结果审查，不得视为 production rollout。
- 是否建议 baseline：是，建议执行 Phase 2.95 selective docs baseline。
- 是否建议进入下一阶段：否；baseline 后再进入 Phase 2.96 Gateway controlled smoke result review，不得自动执行真实 frontend / Gateway smoke。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 Phase 2.95 selective docs baseline，然后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
