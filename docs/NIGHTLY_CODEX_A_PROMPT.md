# Nightly Codex A Prompt

这是 Codex A 夜间模式的固定启动入口。

当用户准备睡觉并希望 Codex A 利用夜间时间推进项目时，只需要把本文件路径交给 Codex A：

```text
执行 /Users/Weishengsu/Hermes_memory/docs/NIGHTLY_CODEX_A_PROMPT.md
```

## 重要说明

1. 本文件和 `NIGHTLY_SPRINT_PROTOCOL.md` 只是文件化控制面，不会自己唤醒 Codex A。
2. 若没有一个正在运行的 Codex A 会话或外部调度器，本文件不会自动执行。
3. 当前项目不创建 production cron / scheduler。
4. 夜间模式不是无限自动开发，只能执行 `NIGHTLY_SPRINT_QUEUE.md` 中明确列出的 bounded items。

## 启动后必须读取

Codex A 启动后必须按顺序读取：

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `docs/NIGHTLY_SPRINT_QUEUE.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`
10. `reports/agent_runs/latest.json`

然后检查：

1. `git status --short`
2. 当前 `HEAD`
3. 当前 `HEAD` 指向的 tag
4. `reports/agent_runs/auto_runner.lock` 是否存在且未过期

## 执行规则

1. 每次夜间最多执行 `NIGHTLY_SPRINT_QUEUE.md` 中 1-3 个 bounded items。
2. 优先执行 `Current Queue` 中第一个未完成 item。
3. item 必须完整写明 lane、目标、允许动作、禁止动作、修改文件白名单和停止条件。
4. Green Lane 完成后可以继续下一个 Green item。
5. Yellow Lane 默认完成后必须停止。
6. 唯一例外：如果 `NIGHTLY_SPRINT_QUEUE.md` 明确标记 `preapproved_docs_only_baseline=true` 且 `continue_after_success=true`，并且本次 baseline 只包含文档 / ignore / README / 状态文件，不含代码、脚本、测试或数据修改，则 baseline 成功后可继续下一个 Green item。
7. Red Lane 或硬停止条件出现时必须立即停止。

## 并发保护

1. 若 `reports/agent_runs/auto_runner.lock` 存在且未过期，停止并报告。
2. 若 lock 不存在，创建 ignored lock。
3. 结束时删除 lock。
4. 若无法可靠判断 lock 状态，停止，不得强行继续。

## 严禁动作

夜间模式严禁：

1. production rollout。
2. repair executor。
3. delete / cleanup。
4. backfill / reindex。
5. migration。
6. 默认扫描真实 reports / reviews。
7. 真实业务 DB 写入，除非 queue item 明确授权且不是 Red Lane。
8. OpenSearch / Qdrant / facts / document_versions 数据 mutation。
9. facts 自动抽取。
10. facts 替代 retrieval evidence。
11. retrieval contract 修改。
12. memory kernel 主架构修改。
13. production cron / scheduler。

## 每个 item 完成后必须更新

1. `docs/ACTIVE_PHASE.md`
2. `docs/HANDOFF_LOG.md`
3. `docs/PHASE_BACKLOG.md`
4. `reports/agent_runs/latest.json`
5. `reports/nightly_runs/<timestamp>.json`

如 item 修改了 TODO / DEV_LOG / phase 文档，也必须同步更新。

## 结束报告

结束时输出：

1. 执行了哪些 queue items。
2. 修改文件。
3. 测试结果。
4. git status。
5. 是否停止在 Codex B review。
6. 是否需要 Codex C 验收。
7. 是否还有可继续夜间执行的 Green Lane item。

