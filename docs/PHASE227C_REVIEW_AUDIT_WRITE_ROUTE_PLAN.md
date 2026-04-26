# Phase 2.27c Review Audit Write Route Plan

## 1. 本轮目标

Phase 2.27c 评审是否应将 report review 事件真实写入 `audit_logs`。

本轮只做路线规划与文档同步，不写功能代码，不写业务 DB，不执行 repair。

## 2. 当前基线

Phase 2.27b 已收口：

1. commit：`c2c18d6`。
2. tag：`phase-2.27b-review-audit-preview-baseline`。
3. sanitized audit payload preview / dry-run 已完成。
4. preview payload 只保留 report-level summary。
5. payload 明确排除 notes、reason、approved_action、完整 item_decisions、本机绝对路径和 item-level entity details。
6. `would_write_audit_logs=false`，当前未写 `audit_logs`。

## 3. 路线评审

### A. 继续 preview-only

优点：

1. 最安全。
2. 不写 DB。
3. 不扩大敏感审阅信息泄露面。

缺点：

1. report review 行为无法进入集中审计。
2. 与 retrieval / facts / policy audit 仍断开。

结论：可作为保守默认，但不能补齐审计闭环。

### B. report-level sanitized audit 写入

写入字段只允许：

1. `event_type=report.review.created`。
2. `review_id`。
3. `report_hash`。
4. `report_type`。
5. `review_status`。
6. `reviewer`。
7. `reviewed_at`。
8. summary counts。
9. `executable=false`。
10. `source=review_record` 或等价来源标识。

必须排除：

1. notes。
2. reason。
3. approved_action。
4. 完整 item_decisions。
5. report 原文。
6. 本机绝对路径。
7. fact_id / document_id / source_chunk_id 等 item-level entity details。

结论：推荐作为下一阶段最小实现候选，但属于 Yellow Lane，不能夜间自动实现。

### C. item-level sanitized audit summary

风险：

1. 容易暴露 fact_id、document_id 或索引问题实体。
2. 会产生较高审计噪声。
3. 需要更细的脱敏规则。

结论：后置，不进入下一阶段。

### D. 写完整 review record

风险最高：

1. notes / reasons 可能包含敏感业务判断。
2. item_decisions 可能泄露大量实体级治理信息。

结论：当前不推荐。

### E. repair executor

结论：继续后置。review approval 不等于 repair execution。

## 4. 推荐路线

建议进入后续独立实现阶段，但仅限：

1. 显式 opt-in 的 report-level sanitized audit 写入。
2. 复用 Phase 2.27b preview payload builder。
3. 写入前再次执行 unsafe field guard。
4. audit 写入失败 fail-open，并返回 warning。
5. `approved_for_manual_action` 继续只表示人工判断，不表示 executed。

不建议在 Nightly Sprint 中自动实现该阶段，因为真实写 `audit_logs` 属于 Yellow Lane。

## 5. 推荐最小边界

后续最小实现应满足：

1. 新增 CLI 参数，例如 `--write-audit`，默认仍 preview-only。
2. 仅在显式传入 `--write-audit` 时写入 `audit_logs`。
3. 写入事件类型限定为 `report.review.created`。
4. 写入 payload 使用 Phase 2.27b sanitized payload。
5. `notes`、`reason`、`approved_action`、`item_decisions`、本机路径与 item-level entity details 必须二次校验排除。
6. audit 写入失败不影响本地 review record，但必须输出 warning。
7. 不修改 review record。
8. 不修改 facts / versions / indexes。
9. 不执行 repair。

## 6. 非目标

Phase 2.27c 及后续最小实现不做：

1. repair executor。
2. item-level audit summary。
3. 完整 review record 入库。
4. 写 notes / reasons 到 DB。
5. 修改 facts。
6. 修改 document_versions。
7. 修改 OpenSearch。
8. 修改 Qdrant。
9. backfill / reindex / cleanup。
10. rollout。
11. retrieval contract 修改。
12. memory kernel 主架构修改。

## 7. 风险点

1. 真实写 `audit_logs` 会从 Green Lane 变成 Yellow Lane，需要 Codex B 审核与用户显式授权。
2. 即使只写 report-level summary，也可能被误读为 repair 已执行，必须保留 `executable=false`。
3. notes / reasons 泄露风险仍是最大风险，必须保持硬排除。
4. `audit_logs` 表结构如无法承载 metadata，需要先停下评估，不应扩大 schema。

## 8. 当前结论

Phase 2.27c 路线判断：

1. 建议允许进入后续最小实现。
2. 最小实现只做 report-level sanitized audit 写入。
3. 必须显式 opt-in，默认继续 preview-only。
4. 不允许夜间自动执行真实 DB 写入。
5. repair executor 继续禁止。

## 9. 是否建议进入下一阶段

建议进入下一阶段，但下一阶段必须是 Yellow Lane：

`Phase 2.27d report-level review audit write MVP`

进入条件：

1. Codex B 审核本规划。
2. 用户明确授权真实写 `audit_logs`。
3. 明确仍不执行 repair、rollout、DB 结构扩大或 item-level audit。
