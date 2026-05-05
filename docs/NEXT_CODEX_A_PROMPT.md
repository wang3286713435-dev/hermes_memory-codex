# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.39 Data Steward / BIM 数据管家 docs-only baseline 已进入收口：

1. Data Steward 已明确为 Hermes 后置产品线，不并入当前 MVP Pilot。
2. BIM 是首个高价值垂直场景，但当前只做资产目录 / 本体 / 图谱 / 空间索引 / 子 Agent 监控规划。
3. 当前不新增 DB schema、Neo4j、PostGIS、空间索引代码、生产级 scheduler。
4. 当前不解析 TB 级 BIM 原始模型，不把原始模型直接送入向量库或 LLM 上下文。
5. 当前不进入 Data Steward 实现、repair、rollout 或真实数据迁移。

## 下一轮建议目标

Phase 2.40 PRD Acceptance Matrix / MVP Evidence Pack planning。

本轮建议只做文档规划：把 PRD / Roadmap / Technical Design 中的 MVP 能力、已完成 evidence、仍需人工复核项、后置产品线和不可宣称能力整理成可审核矩阵。

## 建议新增文档

`/Users/Weishengsu/Hermes_memory/docs/PHASE240_PRD_ACCEPTANCE_MATRIX_PLAN.md`

## 建议更新

1. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
2. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## Phase 2.40 规划边界

应覆盖：

1. PRD capability item。
2. 当前完成状态：done / partial / planned / deferred。
3. evidence 来源：commit、tag、phase doc、eval、Codex C live validation。
4. 仍需人工复核项。
5. 不得宣称能力。
6. 后置路线：Data Steward、rollout、repair executor、facts 自动抽取、BIM 全量解析。

## 硬边界

1. 不写功能代码。
2. 不写 DB / facts / document_versions。
3. 不修改 OpenSearch / Qdrant。
4. 不执行 repair / backfill / reindex / cleanup / delete。
5. 不进入 rollout。
6. 不改 retrieval contract。
7. 不改 memory kernel 主架构。
8. 不启动 Data Steward 实现。
9. 不新增 Neo4j / PostGIS / scheduler / DB schema。
10. 不运行无关 pytest。

## 完成要求

1. 更新交接文件：`ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、`reports/agent_runs/latest.json`。
2. 返回精简摘要。
3. 不提交 Git，除非用户明确要求 baseline。
