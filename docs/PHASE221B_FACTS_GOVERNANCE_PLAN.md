# Phase 2.21b Facts Governance Plan

## 1. 目标

Phase 2.21b 只规划 facts eval、facts 查询权限过滤与人工确认工作流。

本阶段不写功能代码，不改 retrieval contract，不改 memory kernel 主架构，不让 facts 参与回答生成，不做自动全量 facts 抽取。

## 2. 当前基线

Phase 2.21a 已完成 evidence-backed facts 最小闭环：

1. fact 创建必须绑定 `source_document_id`、`source_version_id`、`source_chunk_id`。
2. 默认 `verification_status=unverified`。
3. 支持 by document / by subject 查询。
4. 支持 confirm / reject 状态变更。
5. facts 当前只作为结构化记录，不参与 retrieval 或 answer generation。

## 3. 候选子方向评审

| 方向 | 判断 | 结论 |
| --- | --- | --- |
| A. facts eval 纳入 Phase 2.14 | 可验证来源、状态、stale 诊断与状态流转。 | 优先规划。 |
| B. facts 查询权限过滤 | facts 来源于 document evidence，必须继承 source document ACL / tenant soft policy。 | 优先规划。 |
| C. facts 人工确认工作流 | facts 默认 unverified，企业落地前必须有确认 / 拒绝闭环。 | 优先规划。 |
| D. facts 参与回答生成 | 风险较高，容易把未确认 facts 当成最终依据。 | 不进入本阶段。 |
| E. 自动抽取 facts | 风险最高，容易批量制造无人工确认事实。 | 不进入本阶段。 |

推荐 Phase 2.21b 只推进 A + B + C 的最小规划。

## 4. Facts Eval 最小边界

Phase 2.14 eval 后续应新增 facts case group，至少覆盖：

1. fact 必须有 `source_document_id`。
2. fact 必须有 `source_version_id`。
3. fact 必须有 `source_chunk_id`。
4. 新建 fact 默认 `verification_status=unverified`。
5. `confirm_fact` 后状态变为 `confirmed`，并记录 `confirmed_by` / `confirmed_at`。
6. `reject_fact` 后状态变为 `rejected`。
7. 来源 version 被 superseded 时，fact 查询可诊断 `stale_source_version=true`。
8. 缺失 source chunk 时禁止创建 fact。

建议指标：

1. `fact_id`
2. `verification_status`
3. `source_document_id`
4. `source_version_id`
5. `source_chunk_id`
6. `source_version_is_latest`
7. `stale_source_version`
8. `audit_event_id`

## 5. Facts 查询权限过滤最小边界

facts 查询应继承 source document 的 soft policy：

1. 查询 by document / by subject 时读取 fact 的 `source_document_id`。
2. 使用 source document ACL / tenant metadata 做 allow / deny / not_configured_allow 判定。
3. deny 后不得返回该 fact。
4. deny 后不得泄露 source chunk / source document evidence。
5. audit 记录 fact query、`returned_fact_ids`、`denied_fact_ids`、`policy_decision`。
6. 缺失 ACL 时保持本地默认 `not_configured_allow`，但必须可诊断。

最小 audit 字段建议：

1. `event_type=fact_query`
2. `requester_id`
3. `tenant_id`
4. `query_subject` / `query_document_id`
5. `returned_fact_ids`
6. `denied_fact_ids`
7. `source_document_ids`
8. `policy_decision`
9. `timestamp`

## 6. 人工确认工作流最小边界

状态流转：

1. `unverified -> confirmed`
2. `unverified -> rejected`
3. `confirmed -> rejected` 可作为后续治理能力，当前可暂不实现。
4. `rejected -> confirmed` 可作为后续复核能力，当前可暂不实现。

确认字段：

1. `confirmed_by`
2. `confirmed_at`
3. `verification_status`

拒绝字段：

1. `rejected_by` 可后续补充。
2. `rejected_at` 可后续补充。
3. `rejected_reason` 可选，不作为最小实现硬要求。

当前不做 UI 管理后台；人工确认可先通过 API / service 完成。

## 7. 非目标

Phase 2.21b 不做：

1. 知识图谱。
2. 自动事实抽取。
3. Agent 回答引用 facts。
4. 自动决策。
5. rollout。
6. 完整 RBAC / ABAC。
7. retrieval contract 重构。
8. memory kernel 主架构重构。

## 8. 建议下一步

建议开始 Phase 2.21b 最小实现，顺序为：

1. 先把 facts eval 纳入 deterministic eval。
2. 再补 facts 查询权限过滤与 audit。
3. 最后补人工确认工作流字段与测试。

在这些完成前，不建议让 facts 参与回答生成，也不建议做自动全量 facts 抽取。

## 9. Phase 2.21b 第一阶段实现结果：facts eval

已完成：

1. 扩展 `scripts/phase214_regression_eval.py`，新增 `facts` group。
2. 使用固定 `phase221b:*` fixture 创建测试专用 facts，不触碰真实企业文件池。
3. eval summary 新增 facts 汇总字段：`facts_total`、`facts_passed`、`facts_failed`、`missing_source_fields`、`invalid_verification_status`、`stale_source_version_detected`。
4. 覆盖 5 条 facts eval case：
   - `facts_source_fields_present`
   - `facts_default_unverified`
   - `facts_confirmed_status`
   - `facts_rejected_status`
   - `facts_stale_source_version`

验证结果：

1. `uv run pytest tests/test_phase214_regression_eval.py tests/test_phase221_facts.py -q`：`17 passed`。
2. facts group live eval：`5 passed / 0 failed / 0 skipped`。
3. governance group live eval：`5 passed / 0 failed / 0 skipped`。
4. full Phase 2.14 eval：`21 passed / 0 failed / 1 skipped`，其中 facts group `5 passed / 0 failed`。
5. full eval latency：`p50/p95 = 7.806 ms / 782.726 ms`。

边界：

1. 本轮只做 facts eval。
2. 未实现 facts 查询权限过滤。
3. 未扩展人工确认工作流字段。
4. facts 仍不参与 retrieval 或 answer generation。
5. 未做自动 facts 抽取。

## 10. Phase 2.21b 第二阶段实现结果：facts query policy / audit

已完成：

1. `FactService.list_facts_by_document()` 与 `list_facts_by_subject()` 支持 requester / tenant / role soft policy。
2. facts 查询继承 source document metadata 中的 `tenant_id`、`allowed_requester_ids`、`allowed_roles`。
3. 无 ACL 时默认 `not_configured_allow`，与 retrieval policy 保持一致。
4. requester / role 命中时返回 fact，tenant mismatch 或 ACL 不匹配时 deny。
5. denied fact 不返回，也不泄露为返回结果。
6. facts query 写入 `audit_logs`，action 为 `fact.query`。
7. audit 记录 `requester_id`、`tenant_id`、`role`、query/filter、`returned_fact_ids`、`denied_fact_ids`、`source_document_ids`、`denied_document_ids` 与 `policy_decision`。
8. audit 写入失败 fail-open，只记录 warning，不阻断 facts 查询。
9. Facts API 查询接口支持 `X-Requester-Id`、`X-Tenant-Id`、`X-Requester-Role` headers。

测试结果：

1. `uv run pytest tests/test_phase221_facts.py -q`：`8 passed`。
2. `uv run python -m py_compile app/services/facts.py app/api/routes/facts.py`：通过。
3. `uv run pytest tests/test_phase214_regression_eval.py tests/test_phase221_facts.py -q`：`21 passed`。
4. live smoke：`phase221b:acl:*` 测试 facts 验证 no ACL / requester allow / role allow / tenant deny 均符合预期。
5. full Phase 2.14 eval：`21 passed / 0 failed / 1 skipped`，`p50/p95 = 12.115 ms / 650.397 ms`。

边界：

1. 本轮未让 facts 参与回答生成。
2. 未做自动 facts 抽取。
3. 未做复杂知识图谱。
4. 未做 UI / 管理后台。
5. 人工确认工作流字段增强仍留后续。

## 11. Phase 2.21b 第三阶段实现结果：人工确认工作流字段增强

已完成：

1. facts 模型新增 `confirmed_at`、`rejected_by`、`rejected_at`、`rejection_reason`。
2. 新增兼容 migration：`0003_phase221b_fact_review_fields.py`。
3. `confirm_fact()` 要求必须提供确认人，缺失时返回 `confirmed_by_required`。
4. `reject_fact()` 要求必须提供拒绝人，缺失时返回 `rejected_by_required`。
5. reject 支持 `rejection_reason`；如未提供，默认写入 `not_specified`。
6. 状态流转支持：
   - `unverified -> confirmed`
   - `unverified -> rejected`
   - `confirmed -> rejected`
   - `rejected -> confirmed`
7. 状态变更写入 audit：
   - `fact.confirm`
   - `fact.reject`
8. rejected fact 在 policy allow 时仍可查询，但 `verification_status=rejected` 明确可见。

测试结果：

1. `uv run pytest tests/test_phase221_facts.py -q`：`12 passed`。
2. `uv run python -m py_compile app/models/fact.py app/services/facts.py app/api/routes/facts.py app/schemas/facts.py`：通过。
3. `uv run pytest tests/test_phase214_regression_eval.py tests/test_phase221_facts.py -q`：`25 passed`。
4. local DB `alembic upgrade head` 已验证通过；注意 revision id 已缩短为 `0003_phase221b_review`，避免超过 `alembic_version.version_num` 长度。
5. live smoke：`phase221b:review:*` 测试 fact confirm / reject 均成功，字段与 audit 均写入。
6. full Phase 2.14 eval：`21 passed / 0 failed / 1 skipped`，`p50/p95 = 10.391 ms / 637.154 ms`。

边界：

1. facts 仍不参与 retrieval 或 answer generation。
2. 未做自动 facts 抽取。
3. 未做复杂知识图谱。
4. 未做 UI / 管理后台。
5. 仍不进入 rollout。

## 12. Phase 2.21b 收口判断

Phase 2.21b 已完成三项最小目标：

1. facts eval 纳入 deterministic eval。
2. facts 查询权限过滤 + fact query audit。
3. facts 人工确认工作流字段增强。

建议 Phase 2.21b 在 Git baseline 后收口。
