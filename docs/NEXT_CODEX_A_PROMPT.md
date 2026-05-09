# NEXT_CODEX_A_PROMPT

## Phase 2.56d Codex B Review Passed - Selective Git Baseline

你是 Codex A。本轮只做 Phase 2.56d Natural Import Runtime Wiring Minimum Implementation 的双仓 selective Git baseline。

Codex B 已完成复核：

1. Hermes 主仓 runtime hook 已接入 `run_agent.py`。
2. 非导入 prompt 不被拦截。
3. 明确导入 prompt 默认 `real_upload_enabled=false`，会 fail-closed 返回 diagnostics。
4. `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` 但没有真实 client 时，会返回 `upload_client_not_configured`，不进入普通 retrieval。
5. 未调用真实 Hermes_memory upload API。
6. 未上传真实文件。
7. 未写 DB / OpenSearch / Qdrant。

Codex B 已复跑验证：

1. Hermes 主仓 py_compile：通过。
2. Hermes 主仓 targeted pytest：`28 passed`。
3. Hermes_memory `git diff --check`：通过。
4. `reports/agent_runs/latest.json` JSON 校验：通过。
5. disabled-path CLI smoke：通过。
6. enabled-without-client CLI smoke：通过。

## 本轮目标

只做 Git baseline。

不得进入 Phase 2.56e。
不得真实上传用户文件。
不得实现真实 upload client。

## Hermes 主仓白名单

工作目录：`/Users/Weishengsu/.hermes/hermes-agent`

只允许 stage / commit：

1. `run_agent.py`
2. `agent/memory_kernel/natural_file_import_flow.py`
3. `agent/memory_kernel/natural_file_import_runtime.py`
4. `tests/agent/test_natural_file_import_runtime.py`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`

不得 stage：

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`
5. 任何未在白名单内的文件。

## Hermes_memory 白名单

工作目录：`/Users/Weishengsu/Hermes_memory`

只允许 stage / commit：

1. `docs/PHASE256D_NATURAL_IMPORT_RUNTIME_WIRING_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/NEXT_CODEX_C_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. `reports/internal_mvp_runs/*.json`
6. 任何 app / scripts / tests / migrations 文件。

## 必跑检查

Hermes 主仓：

```bash
./.venv/bin/python -m py_compile \
  run_agent.py \
  agent/memory_kernel/natural_file_import.py \
  agent/memory_kernel/natural_file_import_flow.py \
  agent/memory_kernel/natural_file_upload_adapter.py \
  agent/memory_kernel/natural_file_import_runtime.py

./.venv/bin/python -m pytest -o addopts='' \
  tests/agent/test_natural_file_import.py \
  tests/agent/test_natural_file_import_flow.py \
  tests/agent/test_natural_file_import_runtime.py -q
```

Hermes_memory：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

Staged diff 复核：

1. `git diff --cached --name-only` 必须只包含白名单。
2. `git diff --cached --check` 必须通过。

## Git 操作

Hermes 主仓：

1. selective stage 白名单文件。
2. commit message：
   - `feat: wire natural import runtime preflight`

Hermes_memory：

1. selective stage 白名单文件。
2. commit message：
   - `docs: baseline phase 2.56d natural import runtime wiring`

Tag：

1. tag name：
   - `phase-2.56d-natural-import-runtime-wiring-baseline`
2. 两个仓库都打同名 tag。

Push：

1. Hermes 主仓推送到既有可写远端 / 分支，沿用本项目既定策略；不要推不可写 `origin`。
2. Hermes_memory 推送当前分支到 `origin`，并推送 tag。

## 完成后更新 ignored latest

更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `status=baseline`
2. 写入两个仓库 commit hash。
3. 写入 tag。
4. 写入 push 结果。
5. `needs_codex_b_review=true`
6. `needs_codex_c_validation=false`
7. 下一步建议：Phase 2.56e real natural-language import smoke planning / prompt。

不要 stage `latest.json`。

## 硬禁止

1. 不上传真实文件。
2. 不调用真实 Hermes_memory upload API。
3. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
4. 不执行 cleanup / delete / repair / backfill / reindex / migration。
5. 不修改 retrieval contract。
6. 不修改 memory kernel 主架构。
7. 不进入 Data Steward / DB / NAS / BIM 分支实现。
8. 不进入 production rollout。
9. baseline 后停止，不进入 Phase 2.56e。

## 完成报告必须包含

1. 两个仓库 staged 文件。
2. 检查结果。
3. Hermes 主仓 commit hash。
4. Hermes_memory commit hash。
5. tag。
6. push 结果。
7. 最终 git status。
8. 明确说明未执行真实 upload / API upload call / DB-index 写入。
