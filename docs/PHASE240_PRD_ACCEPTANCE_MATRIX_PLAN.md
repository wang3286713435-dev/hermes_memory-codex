# Phase 2.40 PRD Acceptance Matrix / MVP Evidence Pack Plan

## 1. 定位

Phase 2.40 是 PRD acceptance matrix / MVP evidence pack planning。

目标不是扩功能，而是把 PRD、Roadmap、Technical Design、Phase 文档、eval、真实终端验收和 Git baseline 证据整理成可审核矩阵。后续内部 MVP 落地不应继续依赖口头判断或单轮印象，而应能明确回答：

1. 哪些 PRD 能力已具备可引用证据。
2. 哪些能力只是 partial，需要人工复核或继续补评测。
3. 哪些能力仍是 planned / deferred。
4. 哪些能力当前不得对内外宣称。

## 2. 为什么需要矩阵

Phase 2.10 到 Phase 2.39 已覆盖大量能力：文件作用域、alias、上下文治理、Excel/PPTX、会议纪要、dense ingestion、rerank smoke、access/audit、version governance、facts governance、Pilot issue intake、readiness / repair dry-run、review workflow、tender deep-field recall tail 和 Data Steward 产品线规划。

这些能力已经超过“单个功能点”的规模。若没有 acceptance matrix，容易出现三类风险：

1. 把 `partial` 能力误写成 `done`。
2. 把 docs-only / dry-run / smoke 证据误写成生产能力。
3. 把后置产品线（例如 Data Steward）误并入当前 MVP Pilot。

## 3. Matrix 最小字段

每一行建议使用以下字段：

| field | meaning |
|---|---|
| `prd_item` | PRD / Roadmap / Technical Design 中的能力项或验收项 |
| `capability_area` | 能力域，例如 retrieval、facts、audit、Pilot ops |
| `status` | `done` / `partial` / `planned` / `deferred` |
| `evidence_type` | `test` / `eval` / `live_smoke` / `phase_doc` / `commit_tag` / `manual_review_required` |
| `evidence_ref` | commit、tag、phase doc、eval runner、Codex C session 或 review 记录 |
| `known_gap` | 当前缺口或风险 |
| `next_phase_candidate` | 建议后续 phase 或尾项 |
| `not_claimable` | 当前不可宣称内容 |

`status` 口径：

1. `done`：已有目标测试 / eval / live smoke / baseline，且边界清楚。
2. `partial`：主链路可用，但仍有人工复核、召回、展示、性能或覆盖率缺口。
3. `planned`：已有规划文档，但未进入实现。
4. `deferred`：明确后置，不属于当前 MVP Pilot。

## 4. 当前应纳入矩阵的能力域

### 4.1 文档接入与解析

1. document ingestion / parsing。
2. structured chunking。
3. Excel / PPTX structured citation。
4. meeting transcript / transcript metadata。

建议初始状态：`done` 或 `partial`，具体取决于 evidence 是否覆盖真实样本、citation 字段和回归 eval。

### 4.2 检索与引用

1. sparse retrieval。
2. dense retrieval。
3. hybrid retrieval。
4. rerank smoke。
5. citation / trace。
6. Missing Evidence / 人工复核边界。

建议初始状态：

1. sparse / hybrid / dense ingestion：`done` for MVP baseline evidence。
2. rerank：`partial`，当前有 smoke，不代表排序收益已评估。
3. tender deep-field retrieval：`partial`，人员边界已修，限价、资质等级 / 类别、项目经理等级仍需人工复核或后续召回修复。

### 4.3 会话与上下文治理

1. alias / session scope。
2. active document / compare scope。
3. context contamination guard。
4. facts_as_answer=false。
5. transcript_as_fact=false。

建议初始状态：`done` for bounded MVP use，仍需保留真实 Pilot issue intake 继续观察。

### 4.4 结构化文件与会议记忆

1. Excel sheet / cell citation。
2. PPTX slide citation。
3. meeting transcript action / decision / risk。
4. transcript_as_fact=false。

建议初始状态：`done` for MVP minimal ingestion and retrieval，`partial` for OCR / chart deep extraction / raw audio ASR。

### 4.5 Facts governance

1. evidence-backed facts。
2. confirmed facts read-only search。
3. facts access filtering。
4. facts audit。
5. confirmed facts auxiliary context。
6. facts_as_answer=false。

建议初始状态：`done` for governance skeleton and auxiliary context safety；`deferred` for facts auto extraction and facts replacing retrieval evidence。

### 4.6 Access / audit / version governance

1. soft access policy。
2. retrieval audit。
3. facts query audit。
4. document version latest / historical filtering。
5. stale alias / stale fact source diagnostics。

建议初始状态：`done` for MVP soft-policy and audit trail；`partial` for complete RBAC / ABAC, admin UI and production audit compliance.

### 4.7 Readiness / repair / review workflow

1. readiness audit dry-run。
2. repair plan dry-run。
3. report archival and trend diff。
4. local report review record。
5. sanitized review audit preview / write flow。

建议初始状态：`done` for dry-run / preview workflows；`deferred` for repair executor and production automation。

### 4.8 Pilot issue intake / triage

1. local issue intake template。
2. triage summary generator。
3. runbook and Day-1 query set。
4. P0/P1/P2/P3 分流。

建议初始状态：`done` for local controlled Pilot operations；`partial` for sustained issue trend and release-candidate evidence pack。

### 4.9 Data Steward deferred product line

Data Steward / 数据管家应纳入 matrix，但状态必须是 `planned` / `deferred`，不是 `done`。

当前只完成：

1. PRD / Roadmap / Technical Design 产品线口径。
2. Phase 2.39 docs-only plan。

不可宣称：

1. Data Steward 已实现。
2. Building Asset Catalog MVP 已实现。
3. BIM / IoT / 运维系统真实接入已实现。
4. TB BIM 全量解析、Neo4j、PostGIS、空间索引代码或 scheduler 已实现。

## 5. MVP Evidence Pack 优先级

Phase 2.40 后续若进入最小实现，建议优先收集以下 evidence：

1. citation 质量：document_id、version_id、chunk_id、sheet/cell、slide、meeting source 是否稳定。
2. Top-K / rerank / retrieval trace：dense_status、sparse_status、candidate_pool、rerank_status 是否可审计。
3. permission deny behavior：tenant mismatch / requester deny 后是否无 evidence 泄露。
4. evidence policy flags：`facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`。
5. Pilot query pass rate：Day-1 / Codex C query 的 pass / partial / fail 与 issue type。
6. Missing Evidence / 人工复核边界：无证据时是否保守输出，不编造金额、资质、业绩、人员数量或经营结论。
7. baseline refs：commit、tag、phase doc 和 eval output 是否能对应到 matrix 行。

## 6. 不可宣称能力

当前不得宣称：

1. production rollout ready。
2. 完整自动审标 / 自动投标结论。
3. 自动经营决策。
4. repair executor ready。
5. facts 自动抽取已完成。
6. facts 可替代 retrieval evidence。
7. Data Steward 已实现。
8. TB 级 BIM 全量解析已实现。
9. 完整知识图谱已实现。
10. 多 agent 自治工作流已实现。
11. 完整 RBAC / ABAC 已实现。
12. 完整 OCR / ASR / 图片与原始音频解析已实现。

## 7. Phase 2.40a 候选最小实现

如果 Codex B 审核通过，Phase 2.40a 可做只读文档 / JSON 工具：

1. 新增 `docs/PRD_ACCEPTANCE_MATRIX.md` 或 `reports/mvp_evidence_pack/` ignored 输出策略。
2. 从手写 YAML / JSON / Markdown records 生成 acceptance matrix summary。
3. 不扫描 DB，不写 DB，不跑真实 API。
4. 不自动判断 production ready。
5. 输出 `done / partial / planned / deferred` 分布和 `not_claimable` 清单。

## 8. 非目标

1. 不写功能代码。
2. 不新增脚本、测试、migration 或 schema。
3. 不写 DB / facts / document_versions。
4. 不修改 OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / cleanup / delete。
6. 不进入 rollout。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。
9. 不启动 Data Steward 实现。
10. 不新增 Neo4j、PostGIS、scheduler 或 DB schema。

## 9. 本轮验收

本轮只要求：

1. 新增本规划文档。
2. TODO / DEV_LOG / PHASE_BACKLOG / ACTIVE_PHASE / HANDOFF_LOG 同步 Phase 2.40 planning 状态。
3. `git diff --check` 通过。
4. 关键词复核命中 `PRD Acceptance Matrix`、`MVP Evidence Pack`、`done`、`partial`、`planned`、`deferred`、`facts_as_answer=false`、`transcript_as_fact=false`、`Data Steward`、`not_claimable`、`production rollout`、`repair executor`。
5. 不提交 Git。
