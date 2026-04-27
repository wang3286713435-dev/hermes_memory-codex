# Phase 2.29b Readiness Freeze Decision Plan

## 1. 阶段目标

Phase 2.29b 的目标是规划 readiness freeze baseline decision record。

它只回答一个问题：

当前 freeze report 结果是否足以进入 MVP freeze candidate。

它不回答：

1. 是否可以 production rollout。
2. 是否可以执行 repair。
3. 是否可以自动确认 facts。
4. 是否可以默认扫描真实 reports / reviews。
5. 是否可以修改业务数据。

## 2. 输入来源

Phase 2.29b 的输入应来自 Phase 2.29a freeze report dry-run。

允许的输入：

1. 显式传入的 freeze report JSON。
2. 显式传入的补充 evidence summary。
3. 人工填写的 decision note / reviewer / reviewed_at。

禁止的输入：

1. 默认扫描真实 `reports/` / `reviews/` 目录。
2. 自动运行 full eval。
3. 自动读取业务 DB。
4. 自动执行 repair plan。

## 3. pass / warn / fail 映射规则

### 3.1 pass

`status=pass` 可以映射为：

1. `mvp_freeze_candidate=true`
2. `decision_status=approved_for_mvp_freeze_candidate`
3. `production_rollout=false`
4. `repair_approved=false`

注意：`pass` 仍不等于 production ready。

### 3.2 warn

`status=warn` 不应自动进入 MVP candidate。

推荐映射：

1. `mvp_freeze_candidate=false`
2. `decision_status=needs_manual_review`
3. `manual_review_required=true`
4. `production_rollout=false`
5. `repair_approved=false`

只有在后续人工 review 明确记录并完成补充证据后，才允许进入新的 decision record。

### 3.3 fail

`status=fail` 必须 No-Go。

推荐映射：

1. `mvp_freeze_candidate=false`
2. `decision_status=no_go`
3. `manual_review_required=true`
4. `production_rollout=false`
5. `repair_approved=false`

## 4. No-Go 条件

以下任一条件存在时必须 No-Go：

1. freeze report `status=fail`。
2. evidence 中存在 `production_rollout=true`。
3. evidence 中存在 `repair_executed=true`。
4. evidence 中存在非空 `destructive_actions`。
5. facts 被标记为可替代 retrieval evidence。
6. 默认扫描真实 reports / reviews 才能得出结论。
7. 需要真实 DB mutation 才能得出结论。
8. 需要 repair / backfill / reindex / cleanup / delete。

## 5. Phase 2.29b 最小实现边界

推荐 Phase 2.29b 最小实现只做：

1. 读取显式传入的 freeze report JSON。
2. 生成 decision record JSON。
3. 输出 `mvp_freeze_candidate`、`decision_status`、`manual_review_required`、`go_no_go_reasons`。
4. 固定输出 `production_rollout=false`。
5. 固定输出 `repair_approved=false`。
6. 固定输出 `destructive_actions=[]`。
7. 支持 `--dry-run-preview`。

不做：

1. 写业务 DB。
2. 写 `audit_logs`。
3. 执行 repair。
4. 生成 rollout artifact。
5. 默认扫描真实 reports / reviews。

## 6. Codex C 真实终端验收判断

Phase 2.29b planning 不需要 Codex C 真实终端验收。

Phase 2.29b 最小实现也默认不需要 Codex C，因为它只是读取 freeze report 并生成 decision record。

只有在后续阶段要声明“真实 Hermes 终端 MVP candidate 已通过”时，才需要 Codex C 参与：

1. 复跑关键 CLI smoke。
2. 检查 facts 不替代 evidence。
3. 检查 alias / compare / metadata / structured file / meeting transcript 场景。
4. 回传人工可审计证据。

## 7. 推荐输出 JSON

```json
{
  "phase": "Phase 2.29b",
  "dry_run": true,
  "decision_status": "approved_for_mvp_freeze_candidate|needs_manual_review|no_go",
  "mvp_freeze_candidate": false,
  "manual_review_required": true,
  "production_rollout": false,
  "repair_approved": false,
  "destructive_actions": [],
  "freeze_report_status": "pass|warn|fail",
  "go_no_go_reasons": [],
  "reviewer": "",
  "reviewed_at": "",
  "next_steps": []
}
```

## 8. 规划结论

建议进入 Phase 2.29b 最小实现。

但实现边界必须保持：

1. 只生成 decision record。
2. 不执行任何动作。
3. `warn` 不自动进入 MVP candidate。
4. `pass` 也不等于 production rollout。
5. repair executor 与 rollout 继续后置。
