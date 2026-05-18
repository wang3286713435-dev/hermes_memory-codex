# Active Phase

- 当前 phase：Phase 2.92 Read-only Gateway Acceptance Planning。
- 背景：Phase 2.91 baseline 已完成：commit `cf89e1e`，tag `phase-2.91-runtime-evidence-writer-smoke-gate-baseline`，pushed=true；runtime writer smoke gate 仍是 gate-only，不授权真实 DB 写入。
- 本轮目标：把数据库团队 `hermes-readonly-frontend-gateway-access-review.md` 的 Go / 边界结论收束成 Hermes 主线可执行验收计划，明确只读前端 Gateway 接入的 P0 / P1 gates。
- 修改文件：`docs/PHASE292_READONLY_GATEWAY_ACCEPTANCE_PLAN.md`、standard handoff docs、ignored `reports/agent_runs/latest.json`。
- 完成内容：新增 Phase 2.92 只读 Gateway 验收计划；明确 Hermes 命名、平台后端 Gateway、server-side `project_scope`、catalog-only、Missing Evidence、forbidden fields、P0/P1/P2 gates 与数据库团队回传报告格式；已记录数据库团队初步回传，主要 P0 gates 初步满足，需 Phase 2.93 正式 review。
- 测试结果：本阶段为 docs-only planning；`git diff --check` 通过，latest JSON parse 通过，`reports/agent_runs/latest.json` ignore check 通过，`git status --short` 仅显示 Phase 2.92 docs / handoff 文件。
- live smoke 结果：未执行真实 DB / API / CLI Agent / Mac mini / Gateway / parser / NAS / writer / index / object-store smoke。
- 当前结论：Phase 2.92 planning 已完成，建议 selective docs baseline；数据库团队 read-only Gateway 初步回传为 provisionally go，但仍需 Phase 2.93 review；不得进入 Agent DB CRUD、NAS scan、DWG/RVT 内容理解或 production rollout。
- 阻塞点 / 风险点：前端与平台 Gateway 必须去除 Jarvis / 贾维斯旧称；`project_scope` 不得来自前端可信输入；catalog metadata 不能作为正文 evidence。
- 是否建议 baseline：是，建议执行 Phase 2.92 selective docs baseline。
- 是否建议进入下一阶段：否；baseline 后进入 Phase 2.93 review 数据库团队 Gateway implementation report。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 selective docs baseline，然后停止；不得自动实现 Gateway、运行 DB smoke 或进入 Phase 2.93。
- 是否需要 Codex B 审核：已完成 Phase 2.92 planning review。
- 是否需要 Codex C 真实终端验收：暂不需要；本阶段无 runtime/API/CLI 行为。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
