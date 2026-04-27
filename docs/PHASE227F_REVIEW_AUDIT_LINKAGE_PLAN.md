# Phase 2.27f Review Audit Linkage Plan

## 1. 本轮目标

Phase 2.27f 规划 archive / review / audit 三者关联诊断。

本轮只做路线规划与文档同步，不写功能代码，不写业务 DB，不执行 eval，不执行 repair。

## 2. 当前状态

Phase 2.27e 已完成 baseline：

1. commit：`6be9112`。
2. tag：`phase-2.27e-review-audit-eval-checks-baseline`。
3. readiness audit 已能只读检查 `report.review.created` 是否为 report-level sanitized summary。
4. review audit safety assertions 已覆盖 preview / write payload 的敏感字段、item-level entity details 与 executed 语义。
5. 缺少 `report.review.created` 仍为 warning，不代表系统不可用。

已有相关能力：

1. Phase 2.26b：报告归档、manifest、latest 指针与 trend diff。
2. Phase 2.27a：本地 review record，包含 `review_id`、`report_hash`、status 与 item decision skeleton。
3. Phase 2.27b / 2.27d：report-level sanitized audit preview / write，`trace_id=report_review:<review_id>`，`action=report.review.created`。
4. Phase 2.27e：readiness audit 可只读检查 report review audit 是否 sanitized。

当前缺口：

1. archived report、review record 与 audit event 之间还没有统一的只读关联诊断。
2. operator 只能分别查看报告、review record、audit event，无法快速判断链路是否完整。
3. 仍必须避免将本地路径、review notes、item-level entity details 或 repair 状态误写入诊断输出。

## 3. 候选方向评审

| 方向 | 价值 | 风险 | 依赖 | 结论 |
| --- | --- | --- | --- | --- |
| A. Archive -> Review 关联诊断 | 可确认 review record 是否对应某份 archived report。 | 中；若使用本机绝对路径会泄露本地环境。 | report hash 已在归档和 review 中存在。 | 推荐，必须只用 `report_hash` / `report_type`，缺失为 warning。 |
| B. Review -> Audit 关联诊断 | 可确认人工 review 是否已有 report-level audit event。 | 中；若输出 item details 会扩大敏感面。 | audit event 已有 `trace_id=report_review:<review_id>` 与 `report.review.created`。 | 推荐，只检查 sanitized report-level audit。 |
| C. Archive -> Review -> Audit 端到端摘要 | 可形成治理证据链：报告、审阅、审计三者是否一致。 | 中；容易被误读为 repair 已执行。 | 依赖 A/B 两侧关联。 | 推荐作为最小实现目标，但只输出只读 summary。 |
| D. 纳入 readiness audit | 有助于运行体检发现审阅链路长期缺口。 | 中；无 review workflow 使用时不应 fail。 | readiness audit 已有 report review audit 检查。 | 建议作为后续增强，先不默认扫描大量 report 文件。 |
| E. item-level / repair-level linkage | 可能帮助追踪单项 repair decision。 | 高；会暴露 fact_id、document_id、chunk_id，且易被误读为 repair executed。 | 缺更细脱敏模型。 | 后置，不进入 Phase 2.27f 最小实现。 |

## 4. 推荐路线

建议 Phase 2.27f 后续最小实现优先做 **A + B + C**：

1. 使用 `report_hash` / `report_type` 做 archive -> review 关联。
2. 使用 `review_id` / `trace_id=report_review:<review_id>` 做 review -> audit 关联。
3. 输出只读链路摘要，说明 archived report、review record、report-level audit event 是否存在且一致。
4. 缺少任一环节时输出 warning，不自动 fail。
5. 诊断输出不得包含 report 原文、本机绝对路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。

不建议 Phase 2.27f 第一轮实现：

1. 不把 linkage 直接纳入 readiness audit 默认扫描。
2. 不做 item-level audit summary。
3. 不做 repair executor。
4. 不把 audit event 解释为 repair 已执行。

## 5. Phase 2.27f 最小实现边界

后续最小实现建议新增只读 linkage 诊断脚本，例如：

`scripts/phase227f_review_audit_linkage.py`

输入建议：

1. `--archive-manifest <path>`：读取 ignored 的 manifest 或 fake manifest。
2. `--review-record <path>`：读取本地 review record。
3. `--audit-event-file <path>`：读取 fake / exported sanitized audit event JSON。
4. `--json`：输出 JSON summary。

输出建议：

```json
{
  "dry_run": true,
  "destructive_actions": [],
  "status": "pass|warn|fail",
  "archive_review": {
    "status": "pass|warn|fail",
    "report_hash_matched": true,
    "report_type_matched": true
  },
  "review_audit": {
    "status": "pass|warn|fail",
    "review_id_matched": true,
    "trace_id_matched": true,
    "event_type": "report.review.created",
    "sanitized": true
  },
  "end_to_end": {
    "status": "pass|warn|fail",
    "linkage_complete": true,
    "executable": false,
    "repair_executed": false
  },
  "warnings": []
}
```

判定建议：

1. archive 与 review 的 `report_hash` / `report_type` 一致：pass。
2. review record 存在但找不到 archive：warn。
3. review record 存在但找不到 audit event：warn。
4. audit event 不是 `report.review.created`：fail。
5. audit event 出现 unsafe 字段、item-level entity details 或 executed 语义：fail。
6. 任一输出出现本机绝对路径：fail。

## 6. Readiness Audit 关系

Phase 2.27f 第一轮不建议直接修改 readiness audit 默认行为。

后续可评估：

1. 增加可选参数，例如 `--review-linkage-file` 或 `--review-manifest`。
2. 只在显式传入 linkage 输入时检查。
3. 缺失 review workflow 使用时输出 warning，不 fail。
4. 不默认扫描 `reports/`、`reviews/` 或真实 audit 表中的大量记录。

## 7. 非目标

Phase 2.27f 不做：

1. 写 `audit_logs`。
2. 写业务 DB。
3. 修改 facts。
4. 修改 document_versions。
5. 修改 OpenSearch。
6. 修改 Qdrant。
7. 执行 repair / backfill / reindex / cleanup / delete。
8. item-level audit summary。
9. 完整 review record 入 DB。
10. 读取或输出 report 原文。
11. 输出 notes / reason / approved_action。
12. 输出 fact_id / document_id / source_chunk_id 等 item-level entity details。
13. 创建 cron / scheduler。
14. rollout。
15. retrieval contract 或 memory kernel 主架构修改。

## 8. 测试 / Smoke 建议

后续最小实现建议验证：

1. archive manifest 与 review record 通过 `report_hash` 成功关联。
2. review record 与 sanitized audit event 通过 `review_id` / `trace_id` 成功关联。
3. archive 缺失时为 warning。
4. audit event 缺失时为 warning。
5. audit event 含 unsafe 字段时 fail。
6. 输出中不含本机绝对路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。
7. `dry_run=true`、`destructive_actions=[]`、`executable=false` 保持稳定。

Smoke 只使用临时目录 fake manifest / fake review / fake audit event，不读取真实业务报告，不写 DB。

## 9. 风险与硬停止条件

风险：

1. linkage summary 容易被误解为 repair 已执行，必须显式输出 `repair_executed=false`。
2. 过早读取真实 reports / reviews 目录可能暴露本地路径或业务实体。
3. item-level linkage 价值有限但敏感面大，应继续后置。
4. 如果默认纳入 readiness audit，可能对未使用 review workflow 的环境产生噪声。

硬停止条件：

1. 需要写真实业务 DB 或 `audit_logs`。
2. 需要修改 facts、document_versions、OpenSearch 或 Qdrant。
3. 需要 repair / backfill / reindex / cleanup / delete。
4. 需要 item-level audit summary。
5. 需要读取或输出 report 原文、notes、reason、approved_action。
6. 需要输出 fact_id、document_id、source_chunk_id 等 item-level entity details。
7. 需要进入 rollout。
8. 需要修改 retrieval contract 或 memory kernel 主架构。

## 10. 是否建议进入 Phase 2.27f 最小实现

建议进入 Phase 2.27f 最小实现，但只限：

1. 只读 linkage summary。
2. fake manifest / fake review / fake audit event 单元测试。
3. 临时目录 smoke。
4. 不写 DB、不写 audit_logs、不执行 repair。

不建议直接纳入 readiness audit 默认扫描，也不建议进入 item-level / repair-level linkage。

## 11. Phase 2.27f 最小实现结果

本轮已完成只读 linkage summary 最小实现：

1. 新增 `scripts/phase227f_review_audit_linkage.py`。
2. 支持 fake / ignored archive manifest、review record、sanitized audit event 输入。
3. 输出 `archive_review`、`review_audit`、`end_to_end` 三段摘要。
4. 全局固定 `dry_run=true`、`destructive_actions=[]`、`executable=false`、`repair_executed=false`。
5. archive 缺失与 audit event 缺失输出 warning，不执行任何修复。
6. unsafe audit event、item-level entity details、非 `report.review.created` event 输出 fail。
7. 输出不包含 report 原文、本机绝对路径、notes、reason、approved_action、完整 item_decisions、fact_id / document_id / source_chunk_id 等 item-level entity details。

验证结果：

1. `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py` 通过。
2. `uv run pytest tests/test_phase227f_review_audit_linkage.py -q` 通过，9 passed。
3. 临时目录 live smoke 通过：
   - fake manifest + fake review + fake sanitized audit event：pass。
   - missing audit event：warn。
   - unsafe audit event：fail。

当前结论：

1. Phase 2.27f 最小实现已完成，建议进入 Codex B review。
2. 仍不写 `audit_logs`、不写业务 DB、不执行 repair、不纳入 readiness 默认扫描。
3. 后续如需 Git baseline，必须单独执行 baseline 任务。

## 12. Phase 2.27f 安全补丁

Codex B 审核发现首轮实现只检查 `request_json` / `result_json`，未检查 audit event 顶层 unsafe 字段。

本轮补丁已修复：

1. audit event 顶层出现 `document_id`、`fact_id`、`report_path` 等 forbidden 字段时输出 fail。
2. audit event 顶层出现本机绝对路径字符串时输出 fail。
3. `request_json` / `result_json` 原有 unsafe 检查保持不变。
4. 失败输出只包含 unsafe 路径，不包含 `doc-secret`、`fact-secret`、本机绝对路径或其他敏感值。
5. `dry_run=true`、`destructive_actions=[]`、`executable=false`、`repair_executed=false` 继续稳定。

补丁验证：

1. `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py` 通过。
2. `uv run pytest tests/test_phase227f_review_audit_linkage.py -q` 通过，12 passed。
3. 临时目录 live smoke 已覆盖：
   - sanitized audit event：pass。
   - missing audit event：warn。
   - unsafe `result_json`：fail。
   - unsafe top-level audit event：fail。

当前仍不写 DB、不写 `audit_logs`、不执行 repair、不读取真实业务 report / review 产物。
