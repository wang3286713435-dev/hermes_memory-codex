# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.29d release candidate checklist planning 收口与 Git baseline。

本轮只做 planning baseline，不写功能代码，不执行 rollout，不执行 repair，不写业务 DB。

## 当前已完成事实

1. 已新增 `docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`。
2. 已明确 MVP freeze candidate 只代表人工审阅候选状态，不等于 production rollout ready。
3. 已定义 release candidate checklist 草案、Codex B 审核标准、Codex C 可选抽样复验、Go / No-Go 条件。
4. 已保留 known risks：stale confirmed fact、soft policy 非完整 RBAC/ABAC、facts 不替代 evidence、专用 rerank key smoke 可选尾项。
5. 未写代码、未写 DB、未执行 repair、未进入 rollout。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 当前应提交文件

1. `/Users/Weishengsu/Hermes_memory/docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`
2. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
3. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
5. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

不得提交：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. 任何真实 reports / reviews / rollout / repair 产物。
3. 任何代码、脚本或测试变更。

## 必须复核

1. `git status --short` 只包含上述 planning 文件和 ignored `latest.json`。
2. `reports/agent_runs/latest.json` 被 `git check-ignore` 命中。
3. 不存在业务代码、脚本、测试变更。
4. 不存在 DB、facts、document_versions、OpenSearch、Qdrant 修改。
5. 不存在真实 reports / reviews JSON 被 staged。

## Git 要求

1. 只 stage 上述 planning 文件。
2. commit message：
   `docs: plan phase 2.29d release candidate checklist`
3. tag：
   `phase-2.29d-release-candidate-checklist-plan-baseline`
4. push `origin/main`。
5. push tag。

## latest.json 目标状态

1. `phase`：`Phase 2.29d Release Candidate Checklist Planning`
2. `status`：`baseline`
3. `tests`：`not run: docs-only planning baseline`
4. `live_smoke`：`not run: docs-only planning baseline`
5. `needs_codex_b_review`：`false`
6. `needs_codex_c_validation`：`false`
7. `git.commit`：本轮 commit hash
8. `git.tag`：`phase-2.29d-release-candidate-checklist-plan-baseline`
9. `git.pushed`：`true`
10. `next_recommendation`：进入 Phase 2.29e checklist dry-run 最小实现规划/实现评审；不直接 rollout

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
15. 不提交 `reports/agent_runs/latest.json`。

## 返回报告

1. 修改文件
2. commit hash
3. tag
4. push 结果
5. final git status
6. `latest.json` 是否 ignored
7. 是否存在代码 / 脚本 / 测试变更
8. 是否建议进入下一阶段
