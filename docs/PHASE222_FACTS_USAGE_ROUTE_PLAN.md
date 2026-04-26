# Phase 2.22 Facts Usage Route Plan

## 1. 目标

Phase 2.22 只做项目状态审计与 facts 使用路线裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构。

## 2. 当前基线

Phase 2.21a / 2.21b 已完成：

1. evidence-backed facts。
2. facts eval。
3. facts 查询权限过滤。
4. fact query audit。
5. confirm / reject 人工确认字段。

当前边界：

1. facts 仍不参与回答生成。
2. 不做自动 facts 抽取。
3. 不做复杂知识图谱。
4. 不进入 rollout。

## 3. 候选方向评审

| 方向 | 企业落地价值 | 技术风险 | 当前依赖 | 是否会放大风险 | 是否适合下一阶段 |
| --- | --- | --- | --- | --- | --- |
| A. confirmed facts 参与回答生成 | 高。可让 Agent 使用已确认结构化事实。 | 高。若查询、过滤、审计和冲突提示不足，容易把事实当万能依据。 | facts source / 权限 / audit 已具备雏形，但管理入口不足。 | 高。会放大错误确认或过期事实风险。 | 暂不推荐。 |
| B. facts 自动抽取 | 高。可扩大结构化事实覆盖面。 | 很高。自动抽取会批量制造待确认事实，误抽取风险大。 | evidence-backed 创建已具备，但抽取策略、人工审核队列不足。 | 很高。会迅速增加治理负担。 | 不推荐现在做。 |
| C. facts 管理 / 确认工作流增强 | 很高。让 unverified / confirmed / rejected facts 可筛选、复核、审计。 | 中。主要是 service/API 查询增强，不触碰回答链路。 | Phase 2.21b 已具备状态、权限、audit 基础。 | 低。先增强治理入口，能降低后续使用风险。 | 推荐作为下一阶段。 |
| D. 增量更新 / 删除治理增强 | 高。可减少失效文档与旧 facts 来源风险。 | 中高。涉及索引、版本、facts stale 关系。 | 版本治理与 stale source 已具备。 | 中。处理不全会造成残留。 | 适合后续紧随 C 推进。 |
| E. 原始音频 ASR | 中。扩大会议入口。 | 高。隐私、ASR 质量、说话人、权限与成本复杂。 | 会议纪要文本已完成，但音频治理仍不足。 | 高。会扩大敏感数据入口。 | 不推荐现在做。 |
| F. rollout readiness | 高。面向真实上线。 | 高。需要权限、监控、管理、评测与运维成熟。 | 当前仍缺 facts 管理入口和更完整权限体系。 | 高。容易过早生产化。 | 不推荐现在做。 |

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.22a：facts 管理 / 确认工作流增强。**

原因：

1. PRD / Roadmap 均强调结构化事实必须可查询、可确认、可审计。
2. confirmed facts 进入回答前，必须先让人工能筛选、复核、追踪和批量处理 pending facts。
3. 当前 facts 已能创建、权限过滤、审计和确认，但缺少面向治理操作的查询入口。
4. 自动抽取与回答生成都应建立在更清晰的确认工作流之后。

## 5. Phase 2.22a 最小边界

最小 service / API 能力：

1. list facts by `verification_status`。
2. list pending / unverified facts。
3. filter by `source_document_id`。
4. filter by `subject`。
5. filter by project metadata，可先基于 source document `project_id`。
6. 返回 confirm / reject audit history。
7. 返回 source document / version / chunk 与 stale source 诊断。
8. 继续继承 source document soft policy。

最小 audit 需求：

1. fact list query 记录 requester / tenant / role。
2. fact list query 记录 filters。
3. fact list query 记录 returned_fact_ids / denied_fact_ids。
4. confirm / reject history 可按 fact 查询。

## 6. 非目标

Phase 2.22a 不做：

1. 自动抽取 facts。
2. Agent 回答引用 facts。
3. 复杂知识图谱。
4. UI / 管理后台。
5. 完整 RBAC / ABAC。
6. rollout。
7. retrieval contract 重构。
8. memory kernel 主架构重构。

## 7. 当前结论

建议开始 Phase 2.22a 最小实现。

本阶段应先把 facts 管理 / 确认入口打稳；confirmed facts 参与回答生成和自动 facts 抽取继续后置。

## 8. Phase 2.22a 最小实现结果

Phase 2.22a 已完成 facts 管理 / 确认工作流增强的最小闭环。

已实现能力：

1. `list_facts` 支持按 `verification_status` 查询 `unverified` / `confirmed` / `rejected`。
2. `list_pending_facts` 等价于 `verification_status=unverified`。
3. 支持按 `source_document_id`、`source_version_id`、`subject`、`fact_type`、`created_by`、`confirmed_by` 过滤。
4. `list_review_history` 可查询单个 fact 的 `fact.confirm` / `fact.reject` 审计历史。
5. 管理查询继续继承 source document soft policy，deny 后不返回 fact。
6. 管理查询继续写入 `fact.query` audit；audit 写入失败仍 fail-open。

API 入口：

1. `GET /api/v1/facts`
2. `GET /api/v1/facts/pending`
3. `GET /api/v1/facts/{fact_id}/review-history`

验证结果：

1. `tests/test_phase221_facts.py`：18 passed。
2. `tests/test_phase214_regression_eval.py tests/test_phase221_facts.py`：31 passed。
3. live smoke 通过：创建 `unverified` fact、confirm 一条、reject 一条，pending / confirmed / rejected 查询与 review history 查询均通过。
4. live smoke 验证 tenant mismatch deny 后管理列表不返回 denied fact。

边界保持：

1. facts 仍不参与 Agent 回答生成。
2. 不做自动 facts 抽取。
3. 不做复杂知识图谱。
4. 不做 UI / 管理后台。
5. 不进入 rollout。
