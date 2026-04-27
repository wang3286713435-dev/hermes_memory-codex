# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.29d 路线规划：MVP freeze candidate 人工复核 / release candidate checklist。

本轮只做规划与文档同步，不写功能代码，不执行 rollout，不执行 repair，不写业务 DB。

## 当前基线

Phase 2.29c docs drift cleanup 已完成并进入 baseline：

1. TODO 中 rerank、dense ingestion、Aliyun provider smoke、audit_logs 的旧状态已修正。
2. Nightly Sprint Queue 已归档 Phase 2.27b / 2.27c 旧队列。
3. 当前不进入 production rollout。
4. 当前不进入 repair executor。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
7. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 规划目标

评审 MVP freeze candidate 是否可以进入人工复核 / release candidate checklist。

需要明确：

1. MVP freeze candidate 与 production rollout 的边界。
2. Codex B 人工审核 freeze report 与 decision record 的标准。
3. Codex C 是否需要抽样复验关键 Hermes CLI / API 场景。
4. release candidate checklist 应包含哪些只读证据。
5. 当前哪些 warning / known risk 必须继续保留。

## 推荐最小边界

1. 只规划人工复核流程。
2. 只规划 release candidate checklist。
3. 只定义证据清单、Go / No-Go 条件、人工签核字段。
4. 不生成 production rollout artifact。
5. 不执行 repair executor。
6. 不默认扫描真实 reports / reviews。
7. 不写 DB。

## 建议新增文档

`/Users/Weishengsu/Hermes_memory/docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`

## 文档同步

更新：

1. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
2. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
6. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

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

## Git 规则

本轮不提交 Git。完成后停止，等待 review / baseline 指令。

## 返回报告

1. 修改文件
2. 规划结论
3. MVP freeze candidate 边界
4. release candidate checklist 草案
5. 风险点
6. 是否建议进入 Phase 2.29d baseline
