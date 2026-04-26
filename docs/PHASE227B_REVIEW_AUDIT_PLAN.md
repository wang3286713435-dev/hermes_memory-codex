# Phase 2.27b Review Audit Plan

## 1. 本轮目标

Phase 2.27b 规划 report review 事件是否纳入 `audit_logs`。

本轮只做规划与文档同步，不写功能代码，不写业务 DB，不执行 repair。

## 2. 当前基线

Phase 2.27a 已收口：

1. commit：`c6ce14d`。
2. tag：`phase-2.27a-report-review-dry-run-baseline`。
3. 本地 review record dry-run 已完成。
4. review record 支持 report-level status、item decision skeleton、report hash、dry-run-preview。
5. `reviews/**/*.json` 与 `reviews/**/*.md` 默认 ignored。
6. `approved_for_manual_action` 仍只是人工判断，不是已执行。

repair executor 继续后置。

## 3. 核心问题

当前需要判断：

1. 是否应把 report review 事件纳入 `audit_logs`。
2. 若纳入，写哪些字段。
3. 哪些字段必须排除，避免泄露敏感业务判断。
4. audit 写入失败如何处理。
5. 如何继续保证 review 不等于 repair execution。

## 4. 候选方向评审

### A. 不写 audit_logs，继续本地 review records

优点：

1. 最安全。
2. 不写业务 DB。
3. notes / reasons 不会进入集中审计表。

缺点：

1. 审阅行为不可集中检索。
2. 无法和 retrieval / facts audit 串联。

结论：可以作为保守默认，但不解决集中审计缺口。

### B. 只写 report-level audit summary

推荐作为最小候选。

写入字段：

1. `event_type=report.review.created`。
2. `report_hash`。
3. `report_type`。
4. `review_status`。
5. `reviewer`。
6. summary counts：`items_total`、`approved_count`、`rejected_count`、`deferred_count`、`needs_review_count`。
7. `executable=false`。

不写：

1. notes。
2. reason。
3. 完整 item_decisions。
4. report 原文。

结论：推荐进入 Phase 2.27b 最小实现，但先做 audit preview / dry-run。

### C. 写 item-level audit summary

风险较高。

可能写入字段：

1. `entity_id`。
2. `item_type`。
3. `decision`。

风险：

1. `entity_id` 可能暴露 fact_id、document_id 或 index issue 细节。
2. item-level 行数可能较多，增加审计噪声。

结论：后置，除非 report-level audit summary 不够用。

### D. 写完整 review record 到 audit_logs

不推荐。

原因：

1. notes / reason 可能包含敏感业务判断。
2. 完整 item_decisions 可能泄露大量实体 ID。
3. 会把本地 review record 的隐私边界打破。

结论：当前阶段不做。

### E. audit preview / dry-run

推荐作为 Phase 2.27b 最小实现前置。

能力：

1. 读取 review record。
2. 输出将写入 audit 的 sanitized payload。
3. 不写 DB。
4. 验证 notes / reasons / full item decisions 不会进入 payload。

结论：推荐优先做 B + E。

## 5. 推荐 Phase 2.27b 最小边界

建议 Phase 2.27b 只实现：

1. report-level audit summary payload builder。
2. audit preview / dry-run CLI。
3. payload schema validation。
4. 明确 notes / reasons / full item decisions 排除。

不建议本阶段真实写 `audit_logs`。

如果后续进入真实写 audit，则必须另开小阶段，并先验证：

1. `audit_logs` 表结构是否足够承载 sanitized metadata。
2. audit 写入失败是否 fail-open。
3. 是否需要 requester / reviewer 的统一 identity 规则。

## 6. 建议 Audit Payload

建议预览 payload：

```json
{
  "event_type": "report.review.created",
  "review_id": "review-...",
  "report_hash": "sha256:...",
  "report_type": "repair_plan",
  "review_status": "acknowledged",
  "reviewer": "local-user",
  "reviewed_at": "2026-04-27T00:00:00+08:00",
  "summary": {
    "items_total": 1,
    "approved_count": 0,
    "rejected_count": 0,
    "deferred_count": 0,
    "needs_review_count": 1
  },
  "executable": false
}
```

必须排除：

1. `notes`。
2. item decision `reason`。
3. item decision `approved_action`。
4. 完整 `item_decisions`。
5. report 原文。
6. report path 的本机绝对路径。

## 7. 写入策略规划

如果未来写入 `audit_logs`：

1. audit 写入失败应 fail-open，不阻断 review record 生成。
2. audit event 不应包含敏感 notes。
3. audit event 不代表 repair execution。
4. event_type 可采用：
   - `report.review.created`
   - `report.review.acknowledged`
   - `report.review.approved_for_manual_action`
   - `report.review.rejected`
5. reviewer 来源优先取 CLI 参数；后续可对接 requester identity。

## 8. Git / Review / Audit 策略

1. 真实 review records 仍默认不入 Git。
2. audit preview JSON 若为真实 review 生成，也默认不入 Git。
3. 可提交 schema template / README / 测试 fake payload。
4. 本地 review record ignored 策略不变。

## 9. 非目标

Phase 2.27b 不做：

1. 写 `audit_logs`。
2. 写业务 DB。
3. 修改 facts。
4. 修改 document_versions。
5. 修改 OpenSearch。
6. 修改 Qdrant。
7. 执行 repair / backfill / reindex。
8. 进入 rollout。
9. 提交真实 review JSON / Markdown。
10. 把 `approved_for_manual_action` 描述为已执行。
11. repair executor。

## 10. 风险点

1. notes / reasons 进入 DB 会泄露敏感业务判断。
2. item-level audit 可能暴露实体 ID，需后置。
3. audit 写入一旦失败，不应影响本地 review 记录生成。
4. 审计事件容易被误读为 repair 已执行，必须带 `executable=false`。

## 11. 是否建议进入实现

建议进入 Phase 2.27b 最小实现。

推荐实现内容：

1. audit preview / dry-run。
2. report-level sanitized audit summary。
3. 单元测试确认 notes / reasons / full item decisions 不进入 payload。

不建议直接写 `audit_logs`；真实写入应等 preview 稳定后另行裁决。

## 12. 最小实现结果

Phase 2.27b 最小实现已完成：

1. 新增 `scripts/phase227b_review_audit_preview.py`。
2. 新增 `tests/test_phase227b_review_audit_preview.py`。
3. CLI 读取本地 review record JSON，输出 sanitized audit payload。
4. 输出固定为 `dry_run=true`、`executable=false`、`would_write_audit_logs=false`。
5. payload 仅保留 report-level summary，不包含 notes、reason、approved_action、完整 item_decisions、report 原文、本机绝对路径或 item-level entity details。
6. unsafe review record 会被拒绝：`executable=true`、`dry_run=false` 或 `destructive_actions` 非空均失败。
7. `approved_for_manual_action` 继续只表示人工判断，不表示 executed。

验证结果：

1. `uv run python -m py_compile scripts/phase227b_review_audit_preview.py` 通过。
2. `uv run pytest tests/test_phase227b_review_audit_preview.py -q` 通过，`10 passed`。
3. 临时目录 fake review record live smoke 通过；stdout payload 未包含 notes / reason / approved_action / item_decisions / 本机绝对路径 / entity id / executed。

本阶段仍未做：

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts / document_versions / OpenSearch / Qdrant。
4. 不执行 repair / backfill / reindex。
5. 不进入 rollout。
