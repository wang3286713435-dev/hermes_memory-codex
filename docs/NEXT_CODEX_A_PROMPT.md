# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.29a 最小实现：MVP freeze checklist / freeze report dry-run。

本轮只做 readiness freeze 最小闭环，不进入 production rollout，不执行 repair，不修改业务数据。

## 当前基线

Phase 2.29 planning 已完成并准备 baseline：

1. `docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md` 已定义 MVP 候选能力、freeze checklist、复验项、人工验收项与 Go/No-Go 标准。
2. Phase 2.29 明确为 readiness freeze，不是 production rollout。
3. Phase 2.29a 推荐只做 freeze checklist / freeze report dry-run。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 建议新增脚本

`/Users/Weishengsu/Hermes_memory/scripts/phase229a_freeze_report_dry_run.py`

## 建议新增测试

`/Users/Weishengsu/Hermes_memory/tests/test_phase229a_freeze_report_dry_run.py`

## 功能要求

1. 生成只读 freeze report JSON。
2. 汇总 MVP freeze checklist 状态。
3. 支持读取或引用现有只读诊断结果：
   - Phase 2.14 deterministic eval summary
   - CLI smoke summary
   - governance eval summary
   - facts eval summary
   - readiness audit dry-run summary
   - repair plan dry-run summary
   - optional linkage summary path
4. 默认不运行昂贵 eval，不读取真实 reports / reviews 目录。
5. 仅在显式参数传入 report path 时读取对应 JSON。
6. 输出必须保持：
   - `dry_run=true`
   - `destructive_actions=[]`
   - `rollout_ready=false`
   - `production_rollout=false`
   - `repair_executed=false`

## 输出 JSON 建议字段

```json
{
  "phase": "Phase 2.29a",
  "dry_run": true,
  "status": "pass|warn|fail",
  "rollout_ready": false,
  "production_rollout": false,
  "repair_executed": false,
  "destructive_actions": [],
  "checklist": [],
  "evidence_inputs": [],
  "go_no_go": {
    "mvp_freeze_candidate": false,
    "production_rollout": false,
    "reasons": []
  },
  "risks": [],
  "next_steps": []
}
```

## CLI 建议

1. `--json`
2. `--output-file <path>` 可选，默认 stdout。
3. `--eval-summary <path>` 可重复。
4. `--readiness-report <path>` 可选。
5. `--repair-plan <path>` 可选。
6. `--linkage-summary <path>` 可选。
7. `--dry-run-preview` 可选，不写文件。
8. `--fail-on-warn` 可选。

## 硬边界

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts。
4. 不修改 document_versions。
5. 不修改 OpenSearch / Qdrant。
6. 不读取真实 reports / reviews 目录。
7. 不默认运行 full eval。
8. 不执行 repair / backfill / reindex / cleanup / delete。
9. 不进入 rollout。
10. 不进入 repair executor。
11. 不做 facts 自动抽取。
12. 不让 facts 替代 retrieval evidence。
13. 不改 retrieval contract。
14. 不改 memory kernel 主架构。

## 测试要求

1. 单元测试 checklist 聚合。
2. 单元测试 go/no-go 判定。
3. 单元测试 `dry_run=true`、`destructive_actions=[]`、`rollout_ready=false` 恒定。
4. 单元测试显式 report path 输入。
5. 单元测试不默认扫描真实 reports / reviews。
6. 单元测试 unsafe 或缺失 evidence 时输出 warn / fail。

## Live smoke 要求

1. `uv run python -m py_compile scripts/phase229a_freeze_report_dry_run.py`
2. `uv run pytest tests/test_phase229a_freeze_report_dry_run.py -q`
3. 使用临时目录 fake report JSON 执行 dry-run。
4. 不读取真实业务 reports / reviews。
5. 不写 DB。
6. 不生成真实 rollout 产物。

## 文档同步

更新：

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## Git 规则

本轮不提交 Git。完成后停止，等待 review / baseline 指令。

## 返回报告

1. 修改文件
2. 实现内容
3. 测试结果
4. live smoke 结果
5. 是否写 DB
6. 是否生成真实 rollout / repair 产物
7. git status
8. 是否建议 Git baseline
9. 是否建议进入下一阶段
