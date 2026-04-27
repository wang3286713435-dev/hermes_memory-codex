# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.29b 路线规划：readiness freeze baseline decision。

本轮只做规划与文档同步，不写功能代码，不执行 rollout，不执行 repair。

## 当前基线

Phase 2.29a 已完成 baseline：

1. `scripts/phase229a_freeze_report_dry_run.py` 已提供只读 freeze report dry-run。
2. 目标测试 `8 passed`。
3. freeze report 输出恒定保持 `dry_run=true`、`destructive_actions=[]`、`rollout_ready=false`、`production_rollout=false`、`repair_executed=false`。
4. 当前仍不允许 production rollout、repair executor、facts 自动抽取或默认扫描真实 reports/reviews。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 规划目标

评审 Phase 2.29b 是否应生成 readiness freeze baseline decision record。

重点回答：

1. freeze report 的 `pass/warn/fail` 如何映射为 `mvp_freeze_candidate`。
2. `warn` 是否允许进入 MVP candidate，还是必须人工确认后才允许。
3. 哪些条件仍是 No-Go：
   - production rollout
   - repair executor
   - facts 替代 retrieval evidence
   - 默认扫描真实 reports/reviews
   - 真实 DB mutation
4. Phase 2.29b 是否只生成 decision record / no-go reasons，不执行任何动作。
5. Phase 2.29b 是否需要 Codex C 真实终端验收。

## 建议新增文档

`/Users/Weishengsu/Hermes_memory/docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`

## 文档同步

更新：

1. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
2. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 硬边界

1. 不写功能代码。
2. 不写 `audit_logs`。
3. 不写业务 DB。
4. 不修改 facts。
5. 不修改 document_versions。
6. 不修改 OpenSearch / Qdrant。
7. 不读取真实 reports / reviews 目录。
8. 不默认运行 full eval。
9. 不执行 repair / backfill / reindex / cleanup / delete。
10. 不进入 rollout。
11. 不进入 repair executor。
12. 不做 facts 自动抽取。
13. 不让 facts 替代 retrieval evidence。
14. 不改 retrieval contract。
15. 不改 memory kernel 主架构。

## Git 规则

本轮不要 commit / tag / push。

## 返回报告

1. 修改文件
2. 规划结论
3. 推荐 Phase 2.29b 最小边界
4. No-Go 条件
5. 是否建议进入 Phase 2.29b 实现
