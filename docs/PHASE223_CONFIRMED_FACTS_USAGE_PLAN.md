# Phase 2.23 Confirmed Facts Usage Plan

## 1. 目标

Phase 2.23 只做 confirmed facts 如何进入可用层的路线裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构。

## 2. 当前基线

Phase 2.21a / 2.21b / 2.22a 已完成：

1. evidence-backed facts。
2. facts eval。
3. facts 查询权限过滤。
4. fact query audit。
5. confirm / reject 人工确认。
6. facts 管理列表、pending 列表、review history。

当前边界：

1. facts 仍不参与 Agent 回答生成。
2. facts 不自动抽取。
3. facts 只作为结构化记录和治理对象。

## 3. 候选方向评审

| 方向 | 企业落地价值 | 技术风险 | 当前依赖 | 是否会放大风险 | 是否适合下一阶段 |
| --- | --- | --- | --- | --- | --- |
| A. confirmed facts 只读检索 / 引用展示 | 高。让人工可直接查已确认事实，并回链来源 evidence。 | 低中。不进入回答链路，风险可控。 | facts source、权限、audit、管理查询已具备。 | 低。能提升可用性而不替代 retrieval evidence。 | 推荐。 |
| B. confirmed facts 参与 Agent 回答生成 | 高。可提升回答稳定性与结构化程度。 | 高。若 conflict、stale、权限、引用策略不足，容易把 fact 当最终答案。 | 管理入口已具备，但 answer policy 尚未设计。 | 高。会扩大误用 confirmed/stale facts 的风险。 | 暂不推荐。 |
| C. facts 自动抽取 | 高。可扩大事实覆盖。 | 很高。会批量制造待确认事实。 | evidence-backed 创建具备，但抽取和审核队列不足。 | 很高。会增加治理压力。 | 不推荐现在做。 |
| D. facts 管理后台 / UI | 高。企业落地需要可视化审核。 | 中。涉及前端、权限、操作审计。 | API/service 管理入口已具备雏形。 | 中。实现过早会固化未成熟流程。 | 可后续规划，不作为下一阶段。 |
| E. facts 权限与 eval 继续增强 | 中高。能提高治理可靠性。 | 低中。主要补 eval 和 policy case。 | access/audit/eval 已具备。 | 低。适合作为配套尾项。 | 可与 A 配套，但不替代 A。 |

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.23a：confirmed facts 只读检索 / 引用展示。**

推荐原因：

1. confirmed facts 已具备来源、版本、权限、审计和人工确认基础。
2. 先做只读检索可以让 confirmed facts 进入可用层，但不进入 Agent final answer。
3. 只读展示能验证 fact citation、stale source、权限过滤和 audit 是否足够稳定。
4. 相比直接参与回答生成，该路线风险更小，也更符合渐进落地。

## 5. Phase 2.23a 最小边界

最小 service / API 能力：

1. list / search confirmed facts。
2. 仅返回 `verification_status=confirmed` 的 fact。
3. 支持按 `source_document_id`、`source_version_id`、`subject`、`fact_type`、`predicate` 查询。
4. fact citation 回链 `source_document_id`、`source_version_id`、`source_chunk_id`。
5. 返回 `source_version_is_latest` 与 `stale_source_version`。
6. 继承 source document soft policy；deny 后不得返回 fact。
7. 写入 `fact.read` 或 `fact.query` audit，记录 requester、filters、returned_fact_ids、denied_fact_ids。

最小展示语义：

1. confirmed fact 可作为只读结构化知识卡片展示。
2. citation 必须指向原始 retrieval evidence chunk。
3. stale source 必须显式可见。
4. fact 不替代 retrieval evidence，也不进入 Agent final answer。

## 6. 非目标

Phase 2.23a 不做：

1. 自动抽取 facts。
2. Agent 回答引用 facts。
3. facts 替代 retrieval evidence。
4. 复杂知识图谱。
5. UI / 管理后台。
6. rollout。
7. retrieval contract 重构。
8. memory kernel 主架构重构。

## 7. 当前结论

建议开始 Phase 2.23a 最小实现。

confirmed facts 应先进入“可查询、可引用、可审计”的只读可用层；是否参与 Agent 回答生成，应在只读层稳定后单独评审。

## 8. Phase 2.23a 最小实现结果

Phase 2.23a 已完成 confirmed facts 只读检索 / 引用展示的最小闭环。

已实现能力：

1. `search_confirmed_facts` 只返回 `verification_status=confirmed` 的 facts。
2. 支持按 `subject`、`predicate`、`fact_type`、`source_document_id`、`source_version_id` 过滤。
3. API 新增 `GET /api/v1/facts/confirmed`。
4. 返回 citation 回链字段：`source_document_id`、`source_version_id`、`source_chunk_id`。
5. 返回 `source_excerpt` 与 `source_location`，用于只读引用展示。
6. 返回 `source_version_is_latest`、`stale_source_version`、`latest_version_id`。
7. confirmed facts 查询继续继承 source document soft policy，deny 后不返回 fact。
8. confirmed facts 查询写入 `fact.search` audit，记录 filters、returned_fact_ids、denied_fact_ids、requester / tenant / role。

验证结果：

1. `tests/test_phase221_facts.py` 覆盖 confirmed-only、unverified/rejected 不返回、predicate / fact_type / document / version filter、stale source、deny 与 audit。
2. confirmed facts 仍不参与 retrieval/search 或 Agent final answer。

边界保持：

1. 不自动抽取 facts。
2. 不让 facts 替代 retrieval evidence。
3. 不做复杂知识图谱。
4. 不做 UI / 管理后台。
5. 不进入 rollout。
