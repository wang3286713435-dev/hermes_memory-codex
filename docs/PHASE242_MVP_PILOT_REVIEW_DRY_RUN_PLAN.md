# Phase 2.42 MVP Pilot Review Dry-run Report Plan

## 1. 定位

Phase 2.42 是 MVP Pilot evidence review dry-run report 的文档规划阶段。

目标是规划一个后续可生成的只读审阅报告，把 checklist、PRD acceptance matrix、Pilot issue records、Codex C sessions、readiness / repair dry-run reports 与人工复核记录汇总成 Go / Pause / No-Go 判断。

本阶段不生成真实 report，不写功能代码，不新增脚本，不运行 API / CLI，不执行真实 Pilot，不批准 production rollout。

## 2. 输入来源

后续 dry-run report 可读取以下输入：

1. `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`。
2. `docs/PRD_ACCEPTANCE_MATRIX.md`。
3. Pilot issue intake / triage records。
4. Codex C terminal validation sessions。
5. readiness audit dry-run report。
6. repair plan dry-run report。
7. human reviewer notes。
8. commit / tag / phase document references。

所有输入只用于人工审阅和 dry-run 汇总。它们不等于 production rollout approval、repair authorization 或自动审标结论。

## 3. 输出报告结构

后续 dry-run report 建议输出以下字段：

| field | meaning |
|---|---|
| report_id | 本地报告 id |
| generated_at | report 生成时间 |
| reviewer / reviewed_by | 审阅人或待审阅人 |
| pilot_round | Pilot 轮次 |
| source_sessions | Codex C / Hermes session refs |
| source_documents | 关联 docs / reports / issue records |
| p0_count | P0 数量 |
| p1_count | P1 数量 |
| p2_count | P2 数量 |
| p3_count | P3 数量 |
| decision | `go` / `pause` / `no_go` |
| decision_reason | 决策原因 |
| evidence_policy_summary | evidence policy 汇总 |
| citation_summary | citation / source 可核验性汇总 |
| missing_evidence_summary | Missing Evidence 汇总 |
| known_risks | 已知风险 |
| not_claimable_confirmed | 不可宣称能力确认 |
| next_phase_candidates | 后续候选 phase |

## 4. Go / Pause / No-Go Dry-run Decision Logic

### 4.1 Go

dry-run report 仅在以下条件同时满足时建议 `go`：

1. `p0_count=0`。
2. P1 均已记录，并可人工复核或进入 bounded backlog。
3. citation / document_id / version_id 可人工核验。
4. `facts_as_answer=false`。
5. `transcript_as_fact=false`。
6. `snapshot_as_answer=false`。
7. Missing Evidence 未被隐藏、改写或编造成确定答案。
8. 不存在权限泄露或实际第三文件污染。
9. 使用者明确知道输出是辅助，不是 production ready。

`go` 只表示可继续内部受控 MVP Pilot，不表示 production rollout ready。

### 4.2 Pause

dry-run report 在以下情况下建议 `pause`：

1. `p0_count=0`，但 P1 连续阻塞关键场景。
2. alias / session 偶发失败影响核心流程。
3. citation 缺失或 trace 展示不稳定，导致人工核验成本过高。
4. Missing Evidence 频率过高，需要补 evidence 或 bounded recall fix。
5. readiness / repair dry-run warning 影响试用风险判断。
6. 使用者对“辅助建议”和“自动结论”边界理解不清。

`pause` 表示暂停扩大范围，继续 bounded fix / issue triage。

### 4.3 No-Go

dry-run report 在以下任一情况建议 `no_go`：

1. 任一 P0 命中。
2. 编造金额、资质、业绩、人员数量或经营结论。
3. facts / transcript / snapshot 替代 retrieval evidence。
4. 权限泄露。
5. 实际第三文件污染进入最终回答。
6. Missing Evidence 被隐藏或改写成确定结论。
7. repair / cleanup / delete / reindex 被误触发。
8. 使用者把输出当作自动审标、自动投标或自动经营决策。

`no_go` 后只能进入重新规划、bounded fix 或人工复核。

## 5. P0 / P1 / P2 / P3 Aggregation Policy

| priority | aggregation rule | default action |
|---|---|---|
| P0 | 任一命中即 `no_go` | pause Pilot expansion and re-plan |
| P1 | 计数、分组、绑定 owner / next phase candidate | continue only with manual review or `pause` if repeated |
| P2 | 汇总为 UX / latency / trace polish backlog | not blocking if bounded |
| P3 | 汇总为 doc / polish backlog | not blocking |

P1 不得被写成 done。所有 P1 必须保留 human review or bounded backlog 指向。

## 6. Evidence Policy 必查项

dry-run report 必须显式检查：

1. `facts_as_answer=false`。
2. `transcript_as_fact=false`。
3. `snapshot_as_answer=false`。
4. Missing Evidence not hidden。
5. Missing Evidence not rewritten as certain answer。
6. no production ready claim。
7. facts 不替代 retrieval evidence。
8. transcript 不替代 retrieval evidence。
9. metadata snapshot 不替代 retrieval evidence。

## 7. Citation Summary

citation summary 至少应统计：

1. document_id present / missing。
2. version_id present / missing。
3. chunk_id present / missing。
4. Excel sheet / cell range present / missing。
5. PPTX slide number / title present / missing。
6. meeting source / transcript location present / missing。
7. source document title present / missing。
8. manually checkable citations count。

## 8. Missing Evidence Summary

Missing Evidence summary 至少应覆盖：

1. 最高投标限价 / 招标控制价 / 投标报价上限。
2. 投标资质具体等级 / 类别。
3. 项目经理等级 / B 证。
4. 类似业绩金额 / 规模 / 年限。
5. 人员数量 / 专业 / 职称 / 资质。
6. 经营方向、客户建议、投标策略。
7. 任何影响投标、合同、财务、法务或管理决策的结论。

这些字段若缺 evidence，必须进入人工复核，不得自动填补。

## 9. Storage Policy

后续真实 dry-run report 默认作为本地运行产物，建议目录：

1. `reports/mvp_pilot_reviews/`
2. `reports/mvp_pilot_reviews/README.md`
3. `reports/mvp_pilot_reviews/.gitignore`

真实 report JSON / Markdown 默认 ignored，不入 Git。

本轮不创建 `reports/mvp_pilot_reviews/`，不生成真实 report，不创建示例业务数据。

## 10. Codex B / Codex C 分工

### 10.1 Codex B

Codex B 负责：

1. review dry-run report schema。
2. 检查 Go / Pause / No-Go 判断是否越界。
3. 判断是否需要 Codex C 真实终端复验。
4. 生成下一轮 bounded prompt。

### 10.2 Codex C

Codex C 仅在需要真实终端复验时介入。

Codex C 不负责主实现，不执行 repair，不批准 rollout。

## 11. 非目标

Phase 2.42 不做：

1. production rollout。
2. repair / cleanup / delete / reindex。
3. DB / facts / document_versions 写入。
4. OpenSearch / Qdrant mutation。
5. API / CLI / script / test 实现。
6. Data Steward 实现。
7. 自动审标。
8. 自动经营决策。
9. retrieval contract 修改。
10. memory kernel 主架构修改。
11. Neo4j / PostGIS / scheduler / DB schema。

## 12. 后续候选

Codex B review 后，下一步只能选择一个 bounded path：

1. Phase 2.42a：local ignored MVP Pilot review dry-run report artifact。
2. Phase 2.42a：local dry-run report generator planning / implementation。

两者都必须保持只读，不进入 rollout，不执行 repair，不写业务 DB。

## 13. 本轮验收

本轮验收标准：

1. 新增 `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`。
2. dry-run report 输入、输出、decision schema、P0/P1/P2/P3 aggregation policy 明确。
3. Go / Pause / No-Go dry-run decision logic 明确。
4. evidence policy、citation summary、Missing Evidence summary 明确。
5. storage policy 明确真实 report 默认 ignored。
6. 非目标明确覆盖 production rollout、repair、DB 写入、OpenSearch / Qdrant mutation、Data Steward、自动审标和自动经营决策。
7. TODO / DEV_LOG / PHASE_BACKLOG / ACTIVE_PHASE / HANDOFF_LOG / latest 状态同步。
8. `git diff --check` 通过。
9. 关键词 `rg` 复核通过。
10. 不提交 Git。
