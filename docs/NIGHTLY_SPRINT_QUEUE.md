# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后默认必须停止等待 Codex B；除非该 item 明确标记 `preapproved_docs_only_baseline=true` 与 `continue_after_success=true`。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Current Queue

### Item 1：Phase 2.35c Git baseline

- lane：Yellow Lane
- 状态：ready for explicit baseline command
- 目标：固化 Phase 2.35 / 2.35b / 2.35c bounded work。
- 任务入口：`docs/NEXT_CODEX_A_PROMPT.md`
- 允许动作：
  - 复跑指定 py_compile / pytest / direct assertion tests。
  - 只 stage Phase 2.35 相关 retrieval、alias/session 测试与文档。
  - commit / tag / push 仅在用户明确 baseline 指令下执行。
- 禁止动作：
  - 不写业务 DB、OpenSearch、Qdrant、facts 或 document_versions。
  - 不执行 repair / backfill / reindex / cleanup / delete。
  - 不进入 production rollout。
  - 不写自动审标结论。
  - 不隐藏 Missing Evidence。
  - 不把 deep-field recall 写成完全收口。
- 当前结果：Codex C 真实终端复验已通过 alias/session；deep-field recall 仍 partial。
- 默认：等待用户明确 baseline 指令，不夜间自动提交。

## Archived Queue

### Phase 2.35 main tender deep-field retrieval implementation

- 类型：Yellow Lane
- 状态：implemented / validated partial
- 结果：目标测试 `22 passed`；Codex C 复验安全边界通过，但最高投标限价和具体资质等级仍未命中。
- 备注：不 baseline，进入 Phase 2.35b 小修 / 诊断。

### Phase 2.34 compare false-positive baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：Hermes_memory commit `789ed22`；Hermes 主仓库 commit `5de49bf5`；tag `phase-2.34-compare-contamination-baseline`。
- 备注：已通过 Codex C 复验；未进入 rollout。

### Phase 2.33 MVP Pilot Day-1 run sheet baseline

- 类型：Yellow Lane
- 状态：completed
- 结果：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`，已推送 `origin/main` 与 tag。
- 备注：docs-only baseline；未写代码、未进入 rollout。

## Red Lane

夜间禁止：

1. production rollout。
2. repair executor。
3. DB mutation。
4. default real reports / reviews scan。
5. facts 自动抽取。
6. facts 替代 retrieval evidence 或 final answer。
7. migration。
8. retrieval contract 修改。
9. memory kernel 主架构修改。
10. production cron / scheduler。
