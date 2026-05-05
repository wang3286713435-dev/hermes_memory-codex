# Nightly Sprint Protocol

## 1. 目的

Nightly Sprint 用于让 Codex A 在用户离开期间执行有限、可审计、可停止的夜间任务。

该机制不是 24 小时无限制自动开发，也不是 rollout、repair 或生产调度系统。

## 2. 启动方式

夜间 sprint 只能在用户明确授权后启动。

本文件是协议，不是调度器。Markdown 文件本身不会自动唤醒 Codex A。

当前推荐启动方式：

```text
执行 /Users/Weishengsu/Hermes_memory/docs/NIGHTLY_CODEX_A_PROMPT.md
```

用户在睡前只需要把上述路径交给 Codex A。Codex A 启动后读取本协议与 `docs/NIGHTLY_SPRINT_QUEUE.md`，按队列推进。

如没有一个正在运行的 Codex A 会话或外部调度器，Nightly Sprint 不会自己执行。当前项目不创建 production cron / scheduler。

启动前 Codex A 必须读取：

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/NIGHTLY_SPRINT_PROTOCOL.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

如果 queue item 指向 `docs/NEXT_CODEX_A_PROMPT.md`，还必须读取该文件完整内容。

如果用户使用 `docs/NIGHTLY_CODEX_A_PROMPT.md` 启动，还必须读取该文件完整内容。

## 3. 执行上限

1. 每个 sprint 最长 60-120 分钟。
2. 每晚最多执行 1-3 个 queue item。
3. 每个 queue item 必须是 bounded task。
4. 不得跨多个大 phase 连续推进。
5. 不得在同一夜间链式进入新路线、新 rollout 或 repair executor。

## 4. 每个 Sprint 必须输出

每个 sprint 结束必须更新：

1. `docs/ACTIVE_PHASE.md`
2. `docs/HANDOFF_LOG.md`
3. `reports/agent_runs/latest.json`
4. `reports/nightly_runs/<timestamp>.json`

`reports/nightly_runs/*.json` 是本地运行产物，默认 ignored，不提交 Git。

## 5. Green Lane

允许夜间自动推进：

1. 文档规划。
2. dry-run 工具。
3. 本地报告归档。
4. preview / sanitized payload。
5. 单元测试。
6. 临时目录 smoke。
7. 不写 DB 的脚本。
8. 不改 retrieval contract 的小工具。

Green Lane 完成后仍必须写交接文件。若出现硬停止条件，必须停止，不得继续下一个 queue item。

## 6. Yellow Lane

完成后必须停止等待 Codex B：

1. 新 API endpoint。
2. `audit_logs` 真实写入。
3. 真实 DB smoke。
4. 多仓库联动。
5. 需要 Codex C 终端验收。
6. baseline / tag / push。

Yellow Lane 可以做准备、验证或文档同步，但不得自动继续下一个阶段。

例外：仅当 `docs/NIGHTLY_SPRINT_QUEUE.md` 明确标记 `preapproved_docs_only_baseline=true` 且 `continue_after_success=true`，并且满足 `AGENT_OPERATING_PROTOCOL.md` 的 Baseline Gate 时，Codex A 可以在 docs-only baseline 成功后继续下一个 Green Lane item。

该例外只适用于文档 / README / `.gitignore` / 状态文件 baseline；不得用于代码、脚本、测试、多仓库、DB、API、CLI smoke、真实 audit 写入或任何数据 mutation。

小修不 baseline。夜间不得因为 prompt wording、状态文件小改、单行文档修正或未完成验收的局部 polish 自动打 tag / push。

## 7. Red Lane

夜间禁止：

1. repair executor。
2. delete / cleanup。
3. migration。
4. production rollout。
5. facts 自动抽取。
6. facts 替代 retrieval evidence。
7. retrieval contract 修改。
8. memory kernel 主架构修改。
9. production cron / scheduler。
10. 真实业务数据 mutation。

遇到 Red Lane 需求必须停止，并在 `ACTIVE_PHASE.md`、`HANDOFF_LOG.md` 与 `reports/agent_runs/latest.json` 中记录原因。

## 8. 硬停止条件

除 `AGENT_OPERATING_PROTOCOL.md` 中的硬停止条件外，Nightly Sprint 还必须在以下情况停止：

1. queue item 缺少明确目标或边界。
2. dirty 文件超出当前 queue item 范围。
3. 需要用户提供样本、密钥、真实终端结果或业务判断。
4. 测试失败超过 2 轮仍无法定位。
5. 任何数据 mutation、repair、delete、cleanup 或 migration 被触发。
6. 需要创建系统 cron / scheduler。

## 9. Nightly Run JSON

每次 night sprint 可写入 ignored 本地 JSON：

```json
{
  "sprint_id": "",
  "queue_item": "",
  "start_time": "",
  "end_time": "",
  "changed_files": [],
  "tests": [],
  "status": "completed|blocked|stopped",
  "stop_reason": "",
  "needs_codex_b_review": true,
  "needs_codex_c_validation": false,
  "git_status": ""
}
```

该 JSON 不得提交 Git。

## 10. 早晨审核流程

早晨由 Codex B 读取：

1. `docs/ACTIVE_PHASE.md`
2. `docs/HANDOFF_LOG.md`
3. `reports/agent_runs/latest.json`
4. `reports/nightly_runs/*.json` 中最新运行产物

Codex B 判断：

1. 是否偏离 PRD / ROADMAP / TECHNICAL_DESIGN。
2. 是否违反 Green / Yellow / Red Lane。
3. 是否需要 Codex C 真实终端验收。
4. 是否允许 baseline。
5. 下一轮是否继续当前 phase，还是重新规划。

## 11. 当前非目标

Nightly Sprint 当前不做：

1. 生产 cron。
2. repair executor。
3. rollout。
4. 自动跨阶段开发。
5. 自动提交 / tag / push。
6. 真实业务数据修改。

## 12. 常见误区

1. Nightly Sprint 不是一个自动运行的系统服务；它需要 Codex A 会话被启动。
2. `NIGHTLY_SPRINT_QUEUE.md` 为空或等待 Codex B review 时，夜间模式会安全停止，这不是 bug。
3. 想利用睡眠时间推进，睡前必须确保 Current Queue 有至少一个可执行 Green item，或有 Codex B 显式批准的 docs-only baseline bundle。
4. 如果第一个 item 是普通 Yellow Lane，完成后会停止，不会继续开发。
