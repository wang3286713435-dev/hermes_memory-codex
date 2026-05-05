# Phase 2.41 MVP Pilot Evidence Review / Go-No-Go Plan

## 1. 定位

Phase 2.41 是 MVP Pilot evidence review / Go-No-Go planning。

本阶段目标是把 `docs/PRD_ACCEPTANCE_MATRIX.md` 从“能力与证据矩阵”进一步转成可人工审阅的 Pilot 启动 / 继续 / 暂停判断流程。

Phase 2.41 不新增能力，不启动 production rollout，不执行 repair，不自动创建业务结论。

## 2. 输入来源

Phase 2.41 的审阅输入包括：

1. `docs/PRD_ACCEPTANCE_MATRIX.md`。
2. Day-1 / Codex C 真实终端验收结果。
3. Pilot issue intake / triage records。
4. readiness audit dry-run reports。
5. repair plan dry-run reports。
6. 人工复核结论，包括 Missing Evidence、citation 核验、业务判断风险记录。
7. 必要的 commit / tag / phase doc references。

所有输入都只用于人工判断。它们不等于 production rollout approval，也不等于自动修复授权。

## 3. 输出目标

Phase 2.41 规划的输出目标：

1. Go / Pause / No-Go 规则。
2. MVP Pilot evidence review checklist。
3. P0 / P1 / P2 / P3 handling policy。
4. human review requirement。
5. not-claimable checklist。
6. 下一阶段候选边界。

## 4. Go 条件

只有同时满足以下条件时，才可建议进入或继续内部受控 MVP Pilot：

1. P0 为 `0`。
2. alias / session 不阻塞核心流程。
3. citation、document_id、version_id 可由人工核验。
4. `facts_as_answer=false` 稳定。
5. `transcript_as_fact=false` 稳定。
6. `snapshot_as_answer=false` 稳定。
7. Missing Evidence 能被正确记录，而不是被隐藏、改写或编造。
8. 使用者明确知道输出是辅助，不是自动审标、自动投标或自动经营决策。
9. 权限 / tenant deny 不泄露 evidence。
10. compare / multi-document query 未出现实际第三文件污染。
11. Pilot issue intake 能记录 pass / partial / fail、priority、issue_type 和 human_review_required。

Go 只表示“可继续内部受控试用”。Go 不表示 production ready。

## 5. Pause 条件

出现以下任一情况时，应暂停 Pilot 扩大范围，先进入 bounded fix / review：

1. P0 暂未出现，但 P1 连续阻塞关键场景。
2. alias / session 偶发失败影响核心流程，但有可复现路径。
3. citation 缺失或 trace 展示不稳定，导致人工核验成本过高。
4. Missing Evidence 被记录，但频率过高，需要补 evidence 或召回质量修复。
5. readiness audit / repair plan dry-run 出现 warning，且 warning 影响试用风险判断。
6. 使用者反馈显示“辅助建议”和“自动结论”边界理解不清。
7. 长输出延迟影响关键演示或关键工作流。

Pause 不代表废弃能力；它表示当前需要先补 bounded evidence、issue triage 或局部修复。

## 6. No-Go 条件

出现以下任一情况时，应判定 No-Go，不应继续 Pilot 或对外宣称能力：

1. 编造金额、资质、业绩、人员数量或经营结论。
2. facts 替代 retrieval evidence。
3. transcript 替代 retrieval evidence。
4. metadata snapshot 替代 retrieval evidence。
5. 跨文件污染，且错误 evidence 进入最终回答。
6. 权限泄露或 tenant / requester deny 后仍返回 evidence。
7. alias / session 导致核心流程不可用。
8. 无法保存人工复核记录。
9. Missing Evidence 被隐藏、改写为确定结论或被模型自行填补。
10. 使用者把输出当作自动审标、自动投标、自动经营决策且流程没有拦截。
11. repair / cleanup / delete / reindex 被误触发。

No-Go 后只能进入重新规划、bounded fix 或人工复核；不得直接 baseline 为可用。

## 7. MVP Pilot Evidence Review Checklist

每轮 review 至少检查：

| item | required check |
|---|---|
| Scope | 是否仍是内部受控 MVP Pilot，不是 production rollout |
| P0 | P0 是否为 0 |
| P1 | P1 是否被记录、分类并有明确 owner / next phase candidate |
| Citation | document_id / version_id / chunk_id / sheet / slide / meeting source 是否可核验 |
| Evidence policy | `facts_as_answer=false` / `transcript_as_fact=false` / `snapshot_as_answer=false` |
| Missing Evidence | 是否明确输出并进入人工复核 |
| Alias/session | 是否可完成核心 alias bind / use / compare |
| Contamination | 是否无第三文件污染或权限泄露 |
| Governance | access / audit / version / stale diagnostics 是否有可查证据 |
| Human review | 是否保留人工复核结论和业务判断记录 |
| Not claimable | 是否避免 production ready、自动审标、Data Steward 已实现等越界口径 |

## 8. P0 / P1 / P2 / P3 Handling Policy

### 8.1 P0

P0 必须立即暂停 Pilot 扩大范围。

P0 包括：

1. 编造金额、资质、业绩、人员数量或经营结论。
2. facts / transcript / snapshot 替代 retrieval evidence。
3. 权限泄露。
4. 实际第三文件污染进入回答。
5. 自动决策越界。
6. repair / delete / cleanup / reindex 被误触发。

### 8.2 P1

P1 可继续内部受控 Pilot，但必须人工复核并进入 bounded fix backlog。

P1 包括：

1. 标书深层字段召回 partial。
2. 限价、资质等级 / 类别、项目经理等级、业绩、人员数量 Missing Evidence。
3. alias / session 偶发失败。
4. citation 可用但需要人工查证。

### 8.3 P2

P2 进入体验 / 性能 / trace polish backlog。

P2 包括：

1. 长输出 latency 偏高。
2. trace 字段展示不够易读。
3. evidence pack references 维护成本高。
4. 部分 UX 表达需要收敛。

### 8.4 P3

P3 作为 polish 或文档优化项，不阻塞 Pilot。

P3 包括：

1. 文档措辞。
2. runbook 小修。
3. 非关键 checklist 格式优化。

## 9. Human Review Requirement

以下内容必须人工复核：

1. 所有 Missing Evidence。
2. 主标书最高投标限价 / 招标控制价 / 投标报价上限。
3. 投标资质具体等级 / 类别。
4. 项目经理等级 / B 证。
5. 类似业绩金额 / 规模 / 年限。
6. 人员数量 / 专业 / 职称 / 资质。
7. 公司经营方向、客户建议、投标策略。
8. 任何可能影响投标、合同、财务、法务或管理决策的结论。

人工复核记录至少应保留：

1. reviewer。
2. reviewed_at。
3. source query。
4. document_id / version_id / citation。
5. pass / partial / fail。
6. issue_type / priority。
7. next action。

## 10. Not-Claimable Checklist

当前不得宣称：

1. production rollout ready。
2. 自动审标可替代人工。
3. 自动经营决策可替代管理层。
4. repair executor ready。
5. facts 自动抽取已完成。
6. facts 可替代 retrieval evidence。
7. Data Steward 已实现。
8. TB BIM 全量解析已完成。
9. Neo4j / PostGIS / 空间索引 / scheduler 已落地。
10. 完整知识图谱 / 多 agent / 完整 RBAC 已完成。

## 11. 非目标

Phase 2.41 不做：

1. production rollout。
2. 自动审标。
3. 自动经营决策。
4. repair executor。
5. Data Steward 实现。
6. DB schema / Neo4j / PostGIS / 空间索引 / scheduler。
7. 新 API / 新脚本 / 新测试 / migration。
8. DB、facts、document_versions、OpenSearch、Qdrant 写入。
9. retrieval contract 修改。
10. memory kernel 主架构修改。

## 12. 后续候选

Codex B review 后，后续可选一项：

1. Phase 2.41a：只读 Pilot evidence review checklist artifact。
2. Phase 2.41a：Pilot evidence review dry-run report。

这两个候选都应保持只读，不直接进入新能力开发。

## 13. 本轮验收

本轮验收标准：

1. 新增 `docs/PHASE241_MVP_PILOT_EVIDENCE_REVIEW_PLAN.md`。
2. Go / Pause / No-Go 条件明确。
3. P0 / P1 / P2 / P3 handling policy 明确。
4. human review requirement 明确。
5. not-claimable checklist 明确。
6. TODO / DEV_LOG / PHASE_BACKLOG / ACTIVE_PHASE / HANDOFF_LOG / latest 状态同步。
7. `git diff --check` 通过。
8. 关键词 `rg` 复核通过。
9. 不提交 Git。
