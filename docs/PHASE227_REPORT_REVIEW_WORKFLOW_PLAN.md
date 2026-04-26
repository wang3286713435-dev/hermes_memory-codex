# Phase 2.27 Report Review Workflow Plan

## 1. 本轮目标

Phase 2.27 规划 repair plan / readiness report 人工审阅流。

本轮只做规划与文档同步，不写功能代码，不执行 repair，不写业务 DB。

## 2. 当前基线

Phase 2.26b 已收口：

1. commit：`5d11e60`。
2. tag：`phase-2.26b-audit-report-archival-baseline`。
3. readiness audit / repair plan 报告可归档。
4. trend diff 可只读比较报告趋势。
5. `reports/**/*.json`、`manifest.json`、`latest.json` 是本机产物，默认 ignored。

当前仍不允许自动 repair。

## 3. 当前缺口

现有链路已经能：

1. 诊断 readiness 风险。
2. 生成不可执行 repair plan。
3. 归档报告。
4. 对比报告趋势。

缺口是报告出来后没有人工审阅闭环：

1. 没有 report-level review 状态。
2. 没有 item-level review decision。
3. 没有 reviewer notes / decision log。
4. 没有“approved 不等于 executed”的明确状态边界。

## 4. 候选方向评审

### A. report review workflow

建议纳入 Phase 2.27a。

价值：

1. 让 archived report 从“诊断产物”变成“可审阅工单”。
2. 支持 `pending_review`、`approved_for_manual_action`、`rejected`、`acknowledged`。
3. 只管理报告状态，不执行修复。

### B. repair plan item review

建议纳入 Phase 2.27a。

价值：

1. 对单条 repair plan item 做人工判断。
2. 支持 `needs_review`、`approved`、`rejected`、`deferred`。
3. 保留 recommended next step，但不执行 item action。

### C. review notes / decision log

建议纳入 Phase 2.27a。

价值：

1. 记录 reviewer、风险判断、备注和后续建议。
2. 使用本地 JSON 或 Markdown review record。
3. 不写业务 DB，避免引入审计或权限迁移风险。

### D. audit integration

建议后置到 Phase 2.27b。

原因：

1. 写入 `audit_logs` 会引入业务 DB 写操作。
2. 当前阶段更适合先稳定本地 review record schema。
3. 后续可评估 `report.review`、`repair_item.review` audit event。

### E. repair executor

明确后置。

只有 review workflow 稳定后，才允许规划执行型工具。本阶段不得进入。

## 5. 推荐 Phase 2.27a 最小边界

推荐 Phase 2.27a 只做：

1. report-level review record schema。
2. item-level decision schema。
3. 本地 review JSON / Markdown 记录生成。
4. review record 校验。
5. review record 与 archived report path / hash 的绑定。

不做：

1. repair executor。
2. 业务 DB mutation。
3. audit_logs 写入。
4. UI / 管理后台。
5. rollout。

## 6. Review Record JSON Schema

建议字段：

```json
{
  "review_id": "review-...",
  "report_path": "reports/repair_plan/...",
  "report_type": "repair_plan",
  "report_hash": "sha256:...",
  "reviewer": "local-user",
  "reviewed_at": "2026-04-27T00:00:00+08:00",
  "status": "pending_review",
  "notes": "human readable review note",
  "item_decisions": [],
  "executable": false
}
```

允许 `status`：

1. `pending_review`。
2. `approved_for_manual_action`。
3. `rejected`。
4. `acknowledged`。

语义边界：

1. `approved_for_manual_action` 只表示人工同意后续可规划人工动作。
2. 它不等于自动 repair。
3. 它不等于已经执行。
4. 所有 review record 均 `executable=false`。

## 7. Item Decision Schema

建议字段：

```json
{
  "item_id": "item-...",
  "entity_id": "9f98384b-5053-4a8f-9b83-35983b28b38e",
  "item_type": "stale_fact",
  "decision": "deferred",
  "reason": "Needs business owner validation before revalidation.",
  "recommended_next_step": "revalidate_against_latest",
  "approved_action": null,
  "executable": false
}
```

允许 `decision`：

1. `needs_review`。
2. `approved`。
3. `rejected`。
4. `deferred`。

语义边界：

1. `approved` 只表达审阅判断。
2. `approved_action` 只记录人工认可的后续动作名称。
3. 本阶段不执行 `approved_action`。
4. 每条 item decision 均 `executable=false`。

## 8. Git / Report / Review 产物策略

真实 review records 默认不入 Git。

建议策略：

1. `reports/reviews/**/*.json` 默认 ignored。
2. `reports/reviews/**/*.md` 默认 ignored，除非明确是模板。
3. 可提交 `reports/README.md` 中的 review 说明。
4. 可提交 schema template，例如 `reports/examples/review_record.template.json`。
5. 不提交真实 review record。

原因：

1. review note 可能包含业务判断、人员名、风险备注。
2. review record 与 report path / hash / fact_id 相关，属于本机运行与人工审阅产物。
3. 真实记录应进入受控 artifact 或内部归档，而非默认 Git。

## 9. 非目标

Phase 2.27 不做：

1. 修改 facts。
2. 修改 document_versions。
3. 修改 OpenSearch。
4. 修改 Qdrant。
5. 执行 repair / backfill / reindex。
6. 创建系统 cron。
7. 进入 rollout。
8. 写业务 DB。
9. 改 retrieval contract。
10. 改 memory kernel 主架构。
11. 创建 UI / 管理后台。

## 10. 风险点

1. reviewer approval 容易被误读为 repair 已执行，需要字段和文档反复强调。
2. review notes 可能包含敏感业务判断，必须默认不入 Git。
3. 若过早接 audit_logs，会把只读治理阶段变成 DB 写入阶段。
4. item decision 粒度过细时可能增加人工负担，Phase 2.27a 应保持最小 schema。

## 11. 是否建议进入实现

建议进入 Phase 2.27a 最小实现。

实现前提：

1. 只生成本地 review records。
2. review records 默认 ignored。
3. 所有 record / decision 均 `executable=false`。
4. 不执行任何 repair。
5. 不写业务 DB。

## 12. Phase 2.27a 实现结果

Phase 2.27a 最小实现已完成。

新增：

1. `scripts/phase227a_review_report.py`。
2. `tests/test_phase227a_review_report.py`。
3. `reviews/.gitignore`。
4. `reviews/README.md`。

已实现能力：

1. 读取 readiness / repair plan report JSON。
2. 生成本地 review record JSON。
3. 支持 report-level status：`pending_review`、`acknowledged`、`approved_for_manual_action`、`rejected`、`deferred`。
4. 支持 item decision skeleton，默认 `needs_review`，不自动 approve。
5. 支持 `--dry-run-preview` 只预览、不写文件。
6. 计算稳定 `report_hash=sha256:...`。

不变边界：

1. 不写业务 DB。
2. 不写 audit_logs。
3. 不执行 repair / backfill / reindex。
4. 所有 review record 与 item decision 均 `executable=false`。

## 13. 验证结果

已完成：

1. `uv run python -m py_compile scripts/phase227a_review_report.py`：通过。
2. `uv run pytest tests/test_phase227a_review_report.py -q`：`7 passed`。
3. 临时目录 live smoke：fake repair report 的 `--dry-run-preview` 通过，未写文件。
4. 临时目录 live smoke：fake repair report 写入 tmp reviews 目录通过。
5. 临时目录 live smoke：生成 skeleton decision，`decision=needs_review`，`executable=false`。

未生成真实仓库 `reviews/**/*.json`。

## 14. 当前结论

Phase 2.27a 已完成本地 report review record + item decision dry-run 最小闭环。

下一步建议先做 Git baseline；之后再评估 Phase 2.27b 是否需要把 review 事件纳入 audit_logs。
