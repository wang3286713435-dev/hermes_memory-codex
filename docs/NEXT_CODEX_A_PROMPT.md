# NEXT_CODEX_A_PROMPT

## Phase 2.56a Codex B Review Passed - Selective Dual-repo Git Baseline

你是 Codex A。本轮只做 Phase 2.56a Natural Import Real Adapter Skeleton 的双仓 selective Git baseline。

Codex B 已独立 review 并复跑测试，结论如下：

1. Phase 2.56a 实现符合边界：真实 upload 默认关闭。
2. `FeatureFlaggedHermesMemoryUploadAdapter(enabled=False)` 不调用 client，返回 `real_upload_disabled`。
3. fake adapter success 只有 `real_upload_enabled=True` 时才执行。
4. upload failure / missing document_id / missing version_id 均不绑定 alias。
5. import diagnostics 不作为 retrieval evidence。
6. 目录 / NAS / 批量 / BIM / unsupported extension 继续 fail-closed。
7. Codex B 复跑通过：
   - Hermes 主仓 py_compile 通过。
   - Hermes 主仓 targeted pytest：`25 passed`。
   - Hermes_memory `git diff --check` 通过。
   - Hermes_memory `latest.json` JSON / ignore 检查通过。

## Baseline 目标

1. Hermes 主仓提交 Phase 2.56a 相关代码 / 测试 / 文档。
2. Hermes_memory 提交 Phase 2.56a 规划 / 交接文档。
3. 创建并推送同一个 tag：`phase-2.56a-natural-import-adapter-skeleton-baseline`。
4. baseline 后停止等待 Codex B review；不得进入 Phase 2.56b。

## Hermes 主仓白名单

工作目录：`/Users/Weishengsu/.hermes/hermes-agent`

只允许 stage / commit：

1. `agent/memory_kernel/natural_file_import_flow.py`
2. `agent/memory_kernel/natural_file_upload_adapter.py`
3. `tests/agent/test_natural_file_import_flow.py`
4. `tests/agent/test_natural_file_upload_adapter.py`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`

不得 stage：

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`
5. 任何其他文件。

## Hermes_memory 白名单

工作目录：`/Users/Weishengsu/Hermes_memory`

只允许 stage / commit：

1. `docs/PHASE256_NATURAL_IMPORT_REAL_ADAPTER_PLAN.md`
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
5. 任何 app / scripts / tests / migrations 文件。

## Baseline 前验证

Hermes 主仓运行：

```bash
./.venv/bin/python -m py_compile \
  agent/memory_kernel/natural_file_import.py \
  agent/memory_kernel/natural_file_import_flow.py \
  agent/memory_kernel/natural_file_upload_adapter.py

./.venv/bin/python -m pytest -o addopts='' \
  tests/agent/test_natural_file_import.py \
  tests/agent/test_natural_file_import_flow.py \
  tests/agent/test_natural_file_upload_adapter.py -q
```

Hermes_memory 运行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## Git 操作

Hermes 主仓：

1. selective stage 白名单文件。
2. 复核 staged diff 不包含禁止文件。
3. commit message：
   - `feat: add phase 2.56a natural import adapter skeleton`
4. push 当前分支到 `backup2` 的既有可写分支。

Hermes_memory：

1. selective stage 白名单文件。
2. 复核 staged diff 不包含禁止文件。
3. commit message：
   - `docs: baseline phase 2.56a natural import adapter skeleton`
4. push 当前分支到 `origin`。

Tag：

1. 在两个仓库创建 tag：`phase-2.56a-natural-import-adapter-skeleton-baseline`。
2. Hermes 主仓 tag 推送到 `backup2`。
3. Hermes_memory tag 推送到 `origin`。

## 完成后更新

更新 ignored `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `status=baseline`
2. 写入两个仓库 commit hash。
3. 写入 tag。
4. 写入 push 结果。
5. `needs_codex_b_review=true`
6. `needs_codex_c_validation=false`

不要 stage `latest.json`。

## 硬边界

1. 不调用真实 Hermes_memory upload API。
2. 不上传文件。
3. 不启动 API / CLI smoke。
4. 不写 DB / facts / document_versions / audit_logs。
5. 不写 OpenSearch / Qdrant。
6. 不 cleanup / delete / repair / backfill / reindex / migration。
7. 不修改 retrieval contract。
8. 不修改 memory kernel 主架构。
9. 不进入 Data Steward / DB / NAS / BIM 分支实现。
10. 不进入 production rollout。
11. baseline 后停止，不进入 Phase 2.56b。

## 完成报告必须包含

1. Hermes 主仓 commit hash / push 结果。
2. Hermes_memory commit hash / push 结果。
3. tag 与 tag push 结果。
4. 最终两个仓库 `git status --short`。
5. 明确说明真实 upload 仍默认关闭，未运行 API / CLI smoke。
