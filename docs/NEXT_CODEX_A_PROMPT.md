# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.53b planning review，允许进入 docs-only Git baseline。

## 本轮目标

Phase 2.53b Natural Language File Import Adapter / Kernel Integration Planning docs-only Git baseline。

本轮只做 selective staging / commit / tag / push，不进入 Phase 2.53c，不写功能代码，不运行 API / CLI smoke，不上传真实文件。

## Codex B 审核结论

Review 通过：

1. Phase 2.53b 规划推荐 import preflight layer，在 normal retrieval / answer flow 前处理显式导入 intent。
2. 规划明确 Hermes_memory upload adapter 最小输入 / 输出 / 失败字段。
3. 规划明确 alias seed 只能在 upload 成功且返回 `document_id` / `version_id` 后发生。
4. 规划明确 import diagnostics 必须独立于 retrieval evidence 展示。
5. 规划明确 fail-closed 策略。
6. 规划明确 Phase 2.53c 只做 mocked adapter / kernel integration tests；Phase 2.53d 才可在用户显式授权后做小文件真实 upload smoke。
7. 本轮未改代码、未运行 API / CLI smoke、未上传文件、未写 DB / OpenSearch / Qdrant。

## 允许 stage 的文件

只允许在 `/Users/Weishengsu/Hermes_memory` stage：

1. `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
3. `docs/CURRENT_STAGE_INTERNAL_MVP_USER_MANUAL.md`
4. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
5. `reports/agent_runs/latest.json`

不得修改或 stage Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent`。

## 验证命令

执行：

```bash
cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

必须确认：

1. `git diff --check` 通过。
2. `reports/agent_runs/latest.json` 被 ignore。
3. 当前 stage 只包含允许文件。
4. 无业务代码、scripts、tests、migrations 被 stage。

## Git baseline 要求

在 `/Users/Weishengsu/Hermes_memory`：

1. 只 stage 允许的 8 个 Phase 2.53b 文件。
2. commit message：

```text
docs: plan phase 2.53b natural import integration
```

3. tag：

```text
phase-2.53b-natural-import-integration-plan-baseline
```

4. 推送 `origin/main` 与 tag。

## 禁止事项

1. 不进入 Phase 2.53c。
2. 不写功能代码。
3. 不修改 Hermes 主仓。
4. 不新增 upload adapter / HTTP client。
5. 不调用真实 Hermes_memory API。
6. 不上传文件。
7. 不读取真实文件内容。
8. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
9. 不执行 repair / backfill / reindex / cleanup / delete / migration。
10. 不修改 `DocumentIngestResponse` / ingestion contract / retrieval contract。
11. 不修改 memory kernel 主架构。
12. 不进入 Data Steward / BIM TB 级管理。
13. 不 stage / commit / tag / push 任何无关 dirty。

## 输出要求

返回精简报告：

1. 本轮目标。
2. staged 文件。
3. 验证结果。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 git status。
8. 当前保留的无关 dirty。
9. 是否建议进入 Phase 2.53c。

baseline 完成后停止，等待 Codex B review，不得自动继续下一阶段。
