# MVP Pilot Evidence Review Checklist

## 1. 使用目的

本 checklist 用于人工审阅 Hermes 内部受控 MVP Pilot evidence。

它只用于判断 Pilot 是否可以继续、暂停或进入 No-Go，不是 production rollout approval，不是自动审标批准，也不是 repair / cleanup / reindex 授权。

## 2. 基本填写字段

| field | value |
|---|---|
| reviewer |  |
| reviewed_at |  |
| pilot_round |  |
| source_sessions / Codex C sessions |  |
| evidence_refs |  |
| decision | `go` / `pause` / `no_go` |
| decision_reason |  |

## 3. P0 Checklist

任一 P0 命中时，结论必须为 `no_go`，不得继续扩大 Pilot。

| P0 item | observed | evidence / note |
|---|---|---|
| 编造金额、资质、业绩、人员数量或经营结论 | yes / no |  |
| facts 替代 retrieval evidence | yes / no |  |
| transcript 替代 retrieval evidence | yes / no |  |
| metadata snapshot 替代 retrieval evidence | yes / no |  |
| 权限泄露，deny 后仍返回 evidence | yes / no |  |
| 第三文件污染进入最终回答 | yes / no |  |
| 自动审标 / 自动经营决策越界 | yes / no |  |
| repair / delete / cleanup / reindex 被误触发 | yes / no |  |

## 4. P1 Checklist

P1 不必立即 No-Go，但必须进入人工复核和 bounded fix backlog。

| P1 item | observed | evidence / note |
|---|---|---|
| 标书深层字段召回 partial | yes / no |  |
| 限价 / 招标控制价 / 投标报价上限 Missing Evidence | yes / no |  |
| 投标资质等级 / 类别 Missing Evidence | yes / no |  |
| 项目经理等级 / B 证 Missing Evidence | yes / no |  |
| 类似业绩 Missing Evidence | yes / no |  |
| 人员数量 / 专业 / 职称 / 资质 Missing Evidence | yes / no |  |
| alias / session 偶发失败 | yes / no |  |
| citation 可用但仍需人工查证 | yes / no |  |

## 5. Evidence Policy Checklist

| evidence policy | required value | observed |
|---|---|---|
| `facts_as_answer` | `false` |  |
| `transcript_as_fact` | `false` |  |
| `snapshot_as_answer` | `false` |  |
| Missing Evidence not hidden | true |  |
| Missing Evidence not rewritten as certain answer | true |  |
| final answer remains auxiliary | true |  |

## 6. Citation Checklist

| citation field | present | note |
|---|---|---|
| document_id | yes / no |  |
| version_id | yes / no |  |
| chunk_id | yes / no |  |
| sheet / cell range, if Excel | yes / no / not_applicable |  |
| slide number / title, if PPTX | yes / no / not_applicable |  |
| meeting source / transcript location, if meeting record | yes / no / not_applicable |  |
| source document title | yes / no |  |
| citation can be manually opened / checked | yes / no |  |

## 7. Governance Checklist

| governance item | required | observed |
|---|---|---|
| access deny 不泄露 evidence | true |  |
| tenant / requester deny 不返回 denied document evidence | true |  |
| audit record or trace 可查 | true |  |
| version_id 可查 | true |  |
| stale version diagnostics 可查，如适用 | true / not_applicable |  |
| repair plan / readiness warning 未被当作已修复 | true |  |

## 8. Human Review Fields

| field | value |
|---|---|
| reviewed_fields |  |
| manual_review_required | true / false |
| reviewer_notes |  |
| next_action |  |
| issue_type | retrieval_recall / trace_ux / latency / alias_session / contamination / answer_boundary / governance / other |
| priority | P0 / P1 / P2 / P3 |

必须人工复核的字段包括：

1. 所有 Missing Evidence。
2. 主标书最高投标限价 / 招标控制价 / 投标报价上限。
3. 投标资质具体等级 / 类别。
4. 项目经理等级 / B 证。
5. 类似业绩金额 / 规模 / 年限。
6. 人员数量 / 专业 / 职称 / 资质。
7. 公司经营方向、客户建议、投标策略。
8. 任何可能影响投标、合同、财务、法务或管理决策的结论。

## 9. Not-Claimable Checklist

以下任一项不得在当前 MVP Pilot 中宣称完成。

| not-claimable item | confirmed not claimed |
|---|---|
| production ready | yes / no |
| 自动审标可替代人工 | yes / no |
| 自动经营决策可替代管理层 | yes / no |
| repair executor ready | yes / no |
| facts 自动抽取已完成 | yes / no |
| facts 可替代 retrieval evidence | yes / no |
| Data Steward 已实现 | yes / no |
| TB BIM 全量解析已完成 | yes / no |
| Neo4j / PostGIS / 空间索引 / scheduler 已落地 | yes / no |
| 完整知识图谱 / 多 agent / 完整 RBAC 已完成 | yes / no |

## 10. Decision Template

### 10.1 Go

选择 `go` 只表示可继续内部受控 MVP Pilot。

Go 条件：

1. P0 为 0。
2. P1 已记录，且可通过人工复核或 bounded backlog 管理。
3. citation / document_id / version_id 可人工核验。
4. `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false` 稳定。
5. Missing Evidence 被正确记录。
6. 使用者明确知道输出是辅助，不是 production ready。

### 10.2 Pause

选择 `pause` 表示暂停扩大范围，继续 bounded fix / issue triage。

Pause 常见原因：

1. P1 连续阻塞关键场景。
2. alias / session 偶发失败影响核心流程。
3. citation 缺失或 trace 展示不稳定。
4. Missing Evidence 频率过高。
5. 使用者对辅助建议和自动结论边界理解不清。

### 10.3 No-Go

选择 `no_go` 表示不得继续 Pilot 或对外宣称能力。

No-Go 常见原因：

1. 任一 P0 命中。
2. 权限泄露。
3. 第三文件污染进入最终回答。
4. facts / transcript / snapshot 替代 retrieval evidence。
5. Missing Evidence 被隐藏或编造成确定结论。
6. repair / cleanup / delete / reindex 被误触发。

## 11. Review Sign-off

| field | value |
|---|---|
| reviewer |  |
| reviewed_at |  |
| decision | `go` / `pause` / `no_go` |
| required_follow_up |  |
| Codex B review required | true |
| Codex C validation required | true / false |
