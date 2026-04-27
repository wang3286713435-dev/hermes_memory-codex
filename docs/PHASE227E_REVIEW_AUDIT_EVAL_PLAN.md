# Phase 2.27e Review Audit Eval Route Plan

## 1. 本轮目标

Phase 2.27e 评审 report review audit 是否纳入 readiness / eval。

本轮只做路线规划与文档同步，不写功能代码，不写 DB，不执行 eval，不执行 repair。

## 2. 当前状态

Phase 2.27d 已完成 baseline：

1. commit：`65515681cd48679ebb90e055164c4ad9970bc743`。
2. tag：`phase-2.27d-review-audit-write-baseline`。
3. `phase227b_review_audit_preview.py` 默认 preview-only。
4. 只有显式 `--write-audit` 才写 report-level sanitized `audit_logs`。
5. 写入字段限定为 report-level summary，不包含 notes、reason、approved_action、完整 item_decisions、本机绝对路径或 item-level entity details。
6. 当前仍禁止 item-level audit summary、完整 review record 入库、repair executor、rollout 和业务 DB 扩大写入。

## 3. 候选方向评审

| 方向 | 价值 | 风险 | 依赖 | 结论 |
| --- | --- | --- | --- | --- |
| A. readiness audit 纳入 review audit 状态 | 可让运行体检发现 report review audit 是否长期缺失。 | 低到中；若误读为生产审计覆盖率会夸大成熟度。 | `audit_logs` 已可写 report-level sanitized event。 | 推荐，但只做只读统计与 warning。 |
| B. deterministic eval 纳入 preview / write 断言 | 最高；可防止敏感字段回归进入 payload 或 audit row。 | 低；可用临时 SQLite / fixture DB，不碰真实企业 DB。 | Phase 2.14 / 2.20 eval 与现有 preview tests 已具备。 | 优先推荐。 |
| C. archive / review / audit 三者关联诊断 | 有助于追踪 report hash、review id、audit trace 的链路完整性。 | 中；若过早绑定真实 report path，可能暴露本机路径或业务实体。 | Phase 2.26b archive 与 2.27a review record 已具备。 | 推荐作为第二优先级，只用 hash / id，不写路径。 |
| D. item-level audit summary | 价值有限，可能帮助定位 item 决策趋势。 | 高；容易暴露 fact_id、document_id、source_chunk_id 等 entity details。 | 需要更细脱敏策略。 | 继续后置。 |
| E. repair executor / automatic repair | 不是 eval/readiness 问题。 | 极高；会修改真实业务数据。 | 缺人工批准与执行审计闭环。 | 必须后置，本阶段不得进入。 |

## 4. 推荐路线

建议 Phase 2.27e 后续最小实现优先做 **B + A**，再评估 **C**：

1. 在 deterministic eval / unit test 层固化 review audit preview 与 write 的安全断言。
2. 在 readiness audit 中增加只读 report review audit 状态检查。
3. 将 archive / review / audit 关联诊断作为可选后续增强，先不强制进入第一轮实现。

不建议：

1. 不做 item-level audit summary。
2. 不做完整 review record 入库。
3. 不做 repair executor。
4. 不把 audit event 当作 repair 已执行。

## 5. Phase 2.27e 最小实现边界

### 5.1 Deterministic Eval / Test

最小实现应覆盖：

1. preview payload 不包含 notes、reason、approved_action、完整 item_decisions、本机绝对路径、item-level entity details。
2. preview payload 固定 `executable=false`。
3. `approved_for_manual_action` 不得被描述为 executed。
4. `--write-audit` 只在临时 SQLite / fixture DB 中验证，不触碰真实企业 DB。
5. audit row 只包含 report-level sanitized summary。
6. audit write failure 继续 fail-open，并产生 warning。

建议优先扩展现有 `tests/test_phase227b_review_audit_preview.py`，不必急于并入 Phase 2.14 full eval。

### 5.2 Readiness Audit

只读检查建议：

1. 最近是否存在 `report.review.created` event。
2. event 是否为 report-level sanitized summary。
3. 是否存在 `audit_warning` 或 `audit_written=false` 的本地报告趋势。
4. 若无 report review audit，不直接 fail，可输出 warning。

边界：

1. readiness audit 只读。
2. 不写 DB。
3. 不把无 report review audit 误判为系统不可用。
4. 不检查 notes / reason 原文，因为这些字段不应进入 audit。

### 5.3 Archive / Review / Audit 关联诊断

可规划但不进入第一优先级：

1. 使用 `report_hash` 关联 archived report。
2. 使用 `review_id` / `report_hash` 关联 review record。
3. 使用 `trace_id=report_review:<review_id>` 或等价字段关联 audit event。
4. 不使用本机绝对路径。
5. 不输出 item-level entity id。

## 6. 非目标

Phase 2.27e 不做：

1. item-level audit summary。
2. 完整 review record 入库。
3. notes / reason / approved_action 入库。
4. repair executor。
5. facts、document_versions、OpenSearch、Qdrant 修改。
6. backfill / reindex / cleanup / delete。
7. rollout。
8. retrieval contract 修改。
9. memory kernel 主架构修改。
10. 生产 cron / scheduler。

## 7. 测试 / Smoke 建议

后续最小实现建议验证：

1. `py_compile` 相关脚本。
2. review audit preview / write 单元测试。
3. readiness audit 只读检查单元测试。
4. 临时 SQLite smoke：写入 1 条 sanitized `report.review.created` event。
5. 不运行昂贵 full eval，除非后续明确要求。

不建议在 Phase 2.27e 第一轮执行真实业务 DB smoke。

## 8. 风险与硬停止条件

风险：

1. report review audit 容易被误解为 repair 已执行，必须继续保留 `executable=false`。
2. 如果引入 item-level 字段，会扩大 sensitive entity 暴露面。
3. readiness audit 若把缺少 report review audit 视为 fail，可能造成早期阶段误报。

硬停止条件：

1. 需要写真实业务 DB。
2. 需要修改 facts、document_versions、OpenSearch 或 Qdrant。
3. 需要 repair / backfill / reindex / cleanup / delete。
4. 需要 item-level audit summary。
5. 需要进入 rollout。
6. 需要修改 retrieval contract 或 memory kernel 主架构。

## 9. 是否建议进入 Phase 2.27e 最小实现

建议进入 Phase 2.27e 最小实现，但边界必须限定为：

1. deterministic eval / unit test 的安全断言。
2. readiness audit 的只读 report review audit 状态检查。
3. 临时 SQLite 或 fixture DB smoke。

不建议直接把 report review audit 扩展为 item-level audit，也不建议进入 repair executor。

## 10. Phase 2.27e 最小实现结果

本轮已完成 Phase 2.27e 最小实现：

1. `scripts/phase225_readiness_audit.py` 新增 `report.review.created` 只读检查。
2. readiness audit 会检查 report review audit 是否只包含 report-level sanitized summary。
3. 若当前环境没有 `report.review.created` event，只输出 warning，不判定为 fail。
4. 检测到 notes、reason、approved_action、完整 item_decisions、本机绝对路径、item-level entity details 或 executed 语义时，会标记为 fail。
5. `--skip-service-check` 下依赖服务未确认的检查降级为 warning，避免本地只读 smoke 因主动跳过服务检查而误报失败。
6. `tests/test_phase225_readiness_audit.py` 新增 readiness audit 安全断言。
7. `tests/test_phase227b_review_audit_preview.py` 补强真实 audit payload 不含 item-level entity details 的断言。

验证结果：

1. `uv run python -m py_compile scripts/phase225_readiness_audit.py scripts/phase227b_review_audit_preview.py` 通过。
2. `uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q` 通过，`26 passed`。
3. `uv run python scripts/phase225_readiness_audit.py --skip-service-check --json` 返回 `status=warn`、`failed=0`、`dry_run=true`、`destructive_actions=[]`。

边界保持：

1. 未写 `audit_logs`。
2. 未写业务 DB。
3. 未修改 facts、document_versions、OpenSearch 或 Qdrant。
4. 未执行 repair / backfill / reindex / cleanup / delete。
5. 未进入 rollout。
