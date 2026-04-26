# Phase 2.21 路线规划：结构化 Facts 最小闭环

## 1. 本轮目标

Phase 2.21 只做 facts / 增量治理 / 音频 ASR / RBAC / rollout 的优先级裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构。

## 2. 当前基线

Phase 2.10-2.20a 已完成并 baseline：

1. document scope / context governance / file alias。
2. tender metadata snapshot。
3. Excel / PPTX ingestion。
4. meeting transcript ingestion。
5. dense ingestion。
6. rerank smoke。
7. access / audit。
8. version governance。
9. API eval / CLI smoke / governance eval。

当前系统已具备从 retrieval evidence、version_id、audit log 中追溯来源的基础条件，因此可以开始规划结构化 facts 最小闭环。

## 3. 候选方向评审

| 方向 | 企业落地价值 | 技术风险 | 当前依赖 | 是否会放大现有风险 | 是否适合下一阶段 |
| --- | --- | --- | --- | --- | --- |
| A. 增量更新增强 / 删除与失效治理 | 高。能减少旧文档、旧版本、失效 evidence 风险。 | 中。需要删除、失效、索引同步与回滚策略。 | Phase 2.19a 已具备 latest / superseded 基础。 | 中。若处理不完整，会造成索引残留。 | 适合后续紧随 facts 前后推进，但不是当前最高价值。 |
| B. 结构化 facts 最小闭环 | 很高。把系统从文档检索助手推进到企业长期记忆层。 | 中高。事实可信度、来源、版本、人工确认边界必须严格。 | retrieval evidence、version_id、audit、access 已具备。 | 可控。只做 evidence-backed + unverified / confirmed，不做自动决策。 | 推荐作为下一阶段。 |
| C. 原始音频 ASR | 中。扩展会议输入源。 | 高。ASR、说话人、隐私、长音频成本与质量风险明显。 | 会议纪要文本 MVP 已完成，但音频链路未准备好。 | 高。会扩大敏感数据入口。 | 不推荐现在做。 |
| D. 完整 RBAC / ABAC | 高。生产级权限必需。 | 高。需要组织、角色、项目、密级、继承与管理后台。 | Phase 2.18a soft policy 已有占位。 | 中高。过早复杂化会拖慢主线。 | 不推荐直接做完整版本，可后续逐步增强。 |
| E. 生产级 rollout readiness | 高。面向真实上线。 | 高。需要稳定部署、监控、权限、评测、数据治理综合成熟。 | 当前仍有 facts、增量删除、完整权限等缺口。 | 高。容易把 MVP 能力误判为生产完备。 | 不推荐现在进入。 |

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.21a：结构化 facts 最小闭环。**

推荐原因：

1. PRD 明确要求结构化事实层，这是从“可引用检索”升级为“企业长期记忆系统”的关键层。
2. 当前 retrieval evidence、version governance、access/audit、eval 已具备 facts 最小可信来源基础。
3. facts 若严格绑定 source document / version / chunk / audit，可避免无来源事实污染。
4. 增量删除、RBAC、ASR、rollout 都应建立在 facts 来源和确认边界更清楚之后。

## 5. Phase 2.21a 最小边界

结构化 fact 最小字段：

1. `fact_type`
2. `subject`
3. `predicate`
4. `value`
5. `source_document_id`
6. `source_version_id`
7. `source_chunk_id`
8. `confidence`
9. `verification_status`
10. `created_by`
11. `confirmed_by`
12. `audit_event_id`

最小规则：

1. fact 必须来源于 retrieval evidence。
2. fact 必须绑定 `source_document_id`、`source_version_id`、`source_chunk_id`。
3. fact 创建必须绑定 audit event 或 request trace。
4. 未经人工确认的 fact 必须标记 `unverified`。
5. 人工确认后才可标记 `confirmed`。
6. 旧版本来源的 fact 必须可诊断 stale source。
7. facts 查询结果不得绕过 access policy。

## 6. 最小验收建议

Phase 2.21a 可先覆盖 3 类 fact：

1. 招标基础信息：工程地点、建设单位、代建单位、项目编号。
2. 会议纪要事项：行动项、负责人、风险、决策。
3. Excel / PPTX 结构化引用：金额项、清单项、slide 主题。

最小验收：

1. 从 retrieval evidence 创建 unverified fact。
2. fact 记录 source document / version / chunk。
3. confirmed / unverified 状态可查询。
4. stale version source 可诊断。
5. audit log 可追溯 fact 创建来源。
6. deny policy 下不可返回无权 document 派生 fact。

## 7. 非目标

Phase 2.21a 不做：

1. 自动把所有文档内容转 facts。
2. 复杂知识图谱。
3. 自动决策。
4. 自动最终审标结论。
5. 完整 RBAC / ABAC。
6. 原始音频 ASR。
7. 生产级 rollout。
8. retrieval contract 重构。
9. memory kernel 主架构重构。

## 8. 当前结论

建议开始 Phase 2.21a 最小实现规划与实施，但必须限定为 evidence-backed facts。

facts 只能从当前 retrieval evidence 中抽取或由用户基于 evidence 显式确认；任何未确认 facts 都必须标记 `unverified`，不能被系统当作已确认企业事实使用。

## 9. Phase 2.21a 最小实现结果

已完成：

1. 复用并扩展 `facts` 表，补齐 evidence-backed facts 最小字段。
2. 新增 `FactService`，提供 `create_fact_from_evidence`、`list_facts_by_document`、`list_facts_by_subject`、`confirm_fact`、`mark_fact_rejected`。
3. 新增 `/api/v1/facts` 最小 API 路由，用于创建、按 document 查询、按 subject 查询、确认和拒绝 fact。
4. fact 创建必须绑定 `source_chunk_id`，并由 chunk 反查 `source_document_id` 与 `source_version_id`。
5. 默认 `verification_status=unverified`；新建 fact 不允许直接绕过为 confirmed。
6. fact 查询会返回 `source_version_is_latest` 与 `stale_source_version`。
7. fact 创建 / 状态变更会写入 `audit_logs`，并可关联 retrieval audit event。

实现文件：

1. `app/models/fact.py`
2. `app/services/facts.py`
3. `app/schemas/facts.py`
4. `app/api/routes/facts.py`
5. `migrations/versions/0002_phase221_facts_schema.py`
6. `tests/test_phase221_facts.py`

验证结果：

1. targeted tests：`25 passed`
2. facts 单测：`4 passed`
3. py_compile：通过
4. live smoke：从会议纪要 evidence 创建 1 条 `meeting_action_item` unverified fact；从主标书 evidence 创建 1 条 `tender_basic_info` unverified fact。
5. live 查询：by document / by subject 均可返回，并保留 `source_document_id`、`source_version_id`、`source_chunk_id`。

降级与非目标：

1. facts 本阶段不参与 retrieval / answer generation。
2. 不自动批量抽取所有文档内容。
3. 不做复杂知识图谱。
4. 不做自动决策。
5. 不进入 rollout。
6. 真实库中曾存在 legacy `facts` 表结构，迁移已兼容旧表并补齐新列；后续部署需执行 alembic upgrade。
