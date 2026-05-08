# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.54a File Steward UX helper review，允许进入 selective Git baseline。

## 本轮目标

Phase 2.54a Enterprise Memory Native UX / File Steward UX helper selective Git baseline。

本轮只做 selective staging / commit / tag / push，不进入 Phase 2.54b，不接 runtime，不做真实 upload，不运行 API / CLI smoke，不写 DB / index，不进入 Data Steward / BIM / NAS / TB 文件池。

## Codex B 审核结论

Review 通过：

1. `file_steward_ux.py` 是纯 Python helper。
2. helper 不调用 Hermes_memory API，不读取真实文件内容，不调用 upload adapter。
3. helper 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
4. alias failure helper 能区分无候选、多候选、active document 可用等状态，且 `auto_bind_allowed=false`。
5. active document continuation hint 只给继续工作建议，不把 metadata 当 answer。
6. file answer metadata 输出 document_id / version_id / title / source / evidence_scope / citation_count。
7. 所有 helper 固定保留：
   - `facts_as_answer=false`
   - `transcript_as_fact=false`
   - `snapshot_as_answer=false`
   - `metadata_as_answer=false`
   - `requires_retrieval_evidence=true`
8. 本轮未修改 runtime：`context_builder.py`、`kernel.py`、`orchestrator.py`、`hermes_memory_adapter.py` 均未纳入本阶段。

## 已通过测试

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/file_steward_ux.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_file_steward_ux.py -q
```

结果：`6 passed`。

Hermes_memory 校验已通过：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## 允许 stage 的文件

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 只允许 stage：

1. `agent/memory_kernel/file_steward_ux.py`
2. `tests/agent/test_file_steward_ux.py`

不得 stage Hermes 主仓既有 out-of-scope dirty：

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`

Hermes_memory `/Users/Weishengsu/Hermes_memory` 只允许 stage：

1. `docs/PHASE254_ENTERPRISE_MEMORY_NATIVE_UX_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`

## Git baseline 要求

### Hermes 主仓

在 `/Users/Weishengsu/.hermes/hermes-agent`：

1. 只 stage 允许的 2 个 Phase 2.54a 文件。
2. commit message：

```text
feat: add file steward UX helpers
```

3. tag：

```text
phase-2.54a-file-steward-ux-helper-baseline
```

4. 推送到当前可写远端 / 分支；如仍按既定策略使用 `backup2`，沿用 `backup2`，不要推不可写 origin。

### Hermes_memory

在 `/Users/Weishengsu/Hermes_memory`：

1. 只 stage 允许的 8 个 Phase 2.54a 文件。
2. commit message：

```text
docs: baseline file steward UX helper
```

3. tag：

```text
phase-2.54a-file-steward-ux-helper-baseline
```

4. 推送当前分支；如需要同步到 `origin/main`，必须确保只推包含 Phase 2.54a 的合法提交，且不覆盖既有 main 历史。

## 验证命令

执行：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/file_steward_ux.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_file_steward_ux.py -q
git status --short

cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

必须确认 stage 只包含白名单文件。

## 禁止事项

1. 不进入 Phase 2.54b。
2. 不接入 `context_builder.py` / `kernel.py` / `orchestrator.py` runtime。
3. 不修改 `hermes_memory_adapter.py`。
4. 不真实上传文件。
5. 不调用 Hermes_memory API。
6. 不读取真实文件内容。
7. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
8. 不进入 Phase 2.53d 真实 upload smoke。
9. 不进入 Data Steward / BIM / NAS / TB 文件池。
10. 不执行 repair / backfill / reindex / cleanup / delete / migration。
11. 不做 production rollout。

## 完成后交接

baseline 后必须停止，等待 Codex B review。

输出必须包含：

1. 双仓 commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 是否有 out-of-scope dirty 保留。
6. 下一步建议。
