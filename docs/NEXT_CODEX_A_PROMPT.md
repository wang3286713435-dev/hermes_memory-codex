# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.54b File Steward UX runtime display integration review，允许进入 selective Git baseline。

## 本轮目标

Phase 2.54b File Steward UX runtime display integration selective Git baseline。

本轮只做 selective staging / commit / tag / push，不进入 Phase 2.54c，不做真实 upload，不运行 API / CLI smoke，不写 DB / index，不进入 Data Steward / BIM / NAS / TB 文件池。

## Codex B 审核结论

Review 通过：

1. `ContextBuilder` 新增 `File steward diagnostics:` 独立分区。
2. alias missing / retrieval suppressed 场景显示 alias failure helper：
   - `auto_bind_allowed=false`
   - `retrieval_evidence_document_ids=[]`
   - `next_action=...`
3. active document trace 显示 continuation hint，并保留：
   - `metadata_as_answer=false`
   - `requires_retrieval_evidence=true`
4. retrieval item / citation 场景显示 file answer metadata：
   - `document_id`
   - `version_id`
   - `title`
   - `source_name`
   - `source_type`
   - `citation_count`
5. 新增 display integration 未修改 retrieval contract。
6. 未修改 `kernel.py`、`orchestrator.py`、`hermes_memory_adapter.py`。
7. 未调用真实 Hermes_memory API，未上传文件，未写 DB / OpenSearch / Qdrant。
8. facts / transcript / snapshot / metadata 仍不得替代 evidence。

## 已通过测试

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/file_steward_ux.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_file_steward_ux.py tests/agent/test_session_document_scope.py tests/agent/test_facts_agent_context.py -q
```

结果：`73 passed`。

Hermes_memory 校验已通过：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## 允许 stage 的文件

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 只允许 stage：

1. `agent/memory_kernel/context_builder.py`
2. `tests/agent/test_session_document_scope.py`

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

1. 只 stage 允许的 2 个 Phase 2.54b 文件。
2. commit message：

```text
feat: render file steward diagnostics in context
```

3. tag：

```text
phase-2.54b-file-steward-context-display-baseline
```

4. 推送到当前可写远端 / 分支；如仍按既定策略使用 `backup2`，沿用 `backup2`，不要推不可写 origin。

### Hermes_memory

在 `/Users/Weishengsu/Hermes_memory`：

1. 只 stage 允许的 8 个 Phase 2.54b 文件。
2. commit message：

```text
docs: baseline file steward context display
```

3. tag：

```text
phase-2.54b-file-steward-context-display-baseline
```

4. 推送当前分支；如需要同步到 `origin/main`，必须确保只推包含 Phase 2.54b 的合法提交，且不覆盖既有 main 历史。

## 验证命令

执行：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/file_steward_ux.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_file_steward_ux.py tests/agent/test_session_document_scope.py tests/agent/test_facts_agent_context.py -q
git status --short

cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

必须确认 stage 只包含白名单文件。

## 禁止事项

1. 不进入 Phase 2.54c。
2. 不进入 Phase 2.53d 真实 upload smoke。
3. 不修改 `kernel.py`、`orchestrator.py`、`hermes_memory_adapter.py`。
4. 不修改 retrieval contract。
5. 不真实上传文件。
6. 不调用 Hermes_memory API。
7. 不读取真实文件内容。
8. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
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
