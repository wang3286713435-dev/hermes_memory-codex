# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.53a review-fix 审核，允许进入 Git baseline。

## 本轮目标

Phase 2.53a Natural Language File Import Parser / Dry-run Planner review-fix Git baseline。

本轮只做 selective staging / commit / tag / push，不进入 Phase 2.53b，不接入真实 upload adapter，不运行 API / CLI smoke，不上传真实文件。

## Codex B 审核结论

Review 通过：

1. 否定导入 intent 已 fail closed：
   - `不要导入 /tmp/demo.pdf` => `detected=false`
   - `请不要上传 /tmp/demo.pdf 到企业记忆` => `detected=false`
   - `不要把 /tmp/demo.pdf 收录到企业记忆` => `detected=false`
2. Parser 仍是纯 dry-run：不访问文件系统、不读取文件内容、不调用 Hermes_memory API、不执行 upload。
3. Diagnostics 仍固定：
   - `dry_run=true`
   - `ingestion_status=not_executed`
   - `facts_as_answer=false`
   - `snapshot_as_answer=false`
   - `transcript_as_fact=false`
4. Hermes_memory 误删的 tracked docs 已恢复：
   - `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`
   - `docs/MVP_PILOT_RUNBOOK.md`
5. 上述两个恢复文件不得纳入本轮 staged / commit。

## 允许 stage 的文件

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 只允许 stage：

1. `agent/memory_kernel/natural_file_import.py`
2. `tests/agent/test_natural_file_import.py`

Hermes_memory `/Users/Weishengsu/Hermes_memory` 只允许 stage：

1. `docs/NEXT_CODEX_A_PROMPT.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
3. `docs/CURRENT_STAGE_INTERNAL_MVP_USER_MANUAL.md`
4. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
5. `docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`
6. `docs/MVP_PILOT_RUNBOOK.md`
7. `reports/agent_runs/latest.json`
8. Hermes 主仓既有 dirty：`agent/memory_kernel/adapters/hermes_memory_adapter.py`、`uv.lock`、`docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`、`tests/agent/test_memory_kernel_adapter_reload.py`

## 验证命令

执行：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py -q
git status --short

cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

必须确认：

1. 主仓目标测试为 `10 passed`。
2. Hermes_memory `git diff --check` 通过。
3. `reports/agent_runs/latest.json` 被 ignore。
4. Hermes_memory status 不包含：

```text
D docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md
D docs/MVP_PILOT_RUNBOOK.md
```

## Git baseline 要求

### Hermes 主仓

在 `/Users/Weishengsu/.hermes/hermes-agent`：

1. 只 stage 允许的两个 Phase 2.53a 文件。
2. commit message：

```text
feat: add natural file import dry-run parser
```

3. 不创建主仓 tag，除非现有双仓 baseline 约定要求同 tag；如需要 tag，必须和 Hermes_memory 使用同一 tag `phase-2.53a-natural-file-import-parser-baseline`。
4. 推送到当前可写远端 / 分支；若主仓仍按既定策略使用 `backup2`，沿用既定可写远端，不推不可写 origin。

### Hermes_memory

在 `/Users/Weishengsu/Hermes_memory`：

1. 只 stage 允许的 7 个 Phase 2.53a 交接 / 文档文件。
2. commit message：

```text
chore: baseline phase 2.53a natural file import parser
```

3. tag：

```text
phase-2.53a-natural-file-import-parser-baseline
```

4. 推送 `origin/main` 与 tag。

## 禁止事项

1. 不进入 Phase 2.53b。
2. 不新增 upload adapter / HTTP client。
3. 不调用真实 Hermes_memory API。
4. 不上传文件。
5. 不读取真实文件内容。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete / migration。
8. 不修改 `DocumentIngestResponse` / ingestion contract / retrieval contract。
9. 不修改 memory kernel 主架构。
10. 不修改已有 session scope / kernel / adapter / orchestrator / context_builder 文件。
11. 不进入 Data Steward / BIM TB 级管理。
12. 不 stage / commit / tag / push 任何无关 dirty。

## 输出要求

返回精简报告：

1. 本轮目标。
2. 两仓修改文件 / staged 文件。
3. 测试结果。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 git status。
8. 当前保留的无关 dirty。
9. 是否建议进入 Phase 2.53b。

baseline 完成后停止，等待 Codex B review，不得自动继续下一阶段。
