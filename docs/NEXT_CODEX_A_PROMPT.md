# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.53c mocked integration review，允许进入 selective Git baseline。

## 本轮目标

Phase 2.53c Natural Import Mocked Integration + Enterprise Memory Native UX Bridge selective Git baseline。

本轮只做 selective staging / commit / tag / push，不进入 Phase 2.53d，不做真实 upload smoke，不进入 Phase 2.54a 实现。

## Codex B 审核结论

Review 通过：

1. `natural_file_import_flow.py` 仍为 mocked-only，不调用真实 Hermes_memory API。
2. no import intent 不拦截 normal flow。
3. fail-closed import 返回 diagnostics，不创建 retrieval evidence。
4. mocked upload success 返回 document_id / version_id / chunk_count / indexed_count。
5. alias seed 只在 mocked upload 成功且 document_id / version_id 存在时发生。
6. upload failed / missing document_id / missing version_id 均 fail closed，且 alias not bound。
7. safe flags 保持 false。
8. import diagnostics 与 retrieval evidence 分离。
9. Phase 2.54 Enterprise Memory Native UX 已固化为后续主线，不放松 evidence boundary。

## 已通过测试

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py -q
```

结果：`21 passed`。

Hermes_memory 校验已通过：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## 允许 stage 的文件

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 只允许 stage：

1. `agent/memory_kernel/natural_file_import_flow.py`
2. `tests/agent/test_natural_file_import.py`
3. `tests/agent/test_natural_file_import_flow.py`

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

1. 只 stage 允许的 3 个 Phase 2.53c 文件。
2. commit message：

```text
feat: add mocked natural import preflight flow
```

3. tag：

```text
phase-2.53c-natural-import-mocked-integration-baseline
```

4. 推送到当前可写远端 / 分支；如仍按既定策略使用 `backup2`，沿用 `backup2`，不要推不可写 origin。

### Hermes_memory

在 `/Users/Weishengsu/Hermes_memory`：

1. 只 stage 允许的 8 个 Phase 2.53c / 2.54 bridge 文档文件。
2. commit message：

```text
docs: bridge natural import to enterprise memory ux
```

3. tag：

```text
phase-2.53c-natural-import-mocked-integration-baseline
```

4. 推送当前分支；如需要同步到 `origin/main`，必须确保只推包含 Phase 2.53c / 2.54 bridge 的合法提交，且不覆盖既有 main 历史。

## 验证命令

执行：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py -q
git status --short

cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

必须确认 stage 只包含白名单文件。

## 禁止事项

1. 不进入 Phase 2.53d。
2. 不进入 Phase 2.54a 实现。
3. 不调用真实 Hermes_memory API。
4. 不上传文件。
5. 不读取真实文件内容。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete / migration。
8. 不修改 `DocumentIngestResponse` / ingestion contract / retrieval contract。
9. 不修改 memory kernel 主架构。
10. 不进入 Data Steward / BIM / NAS / TB 文件池。
11. 不做 production rollout。
12. 不 stage / commit / tag / push 任何无关 dirty。

## 输出要求

返回精简报告：

1. 本轮目标。
2. 两仓 staged 文件。
3. 测试结果。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 git status。
8. 当前保留的 out-of-scope dirty。
9. 是否建议进入 Phase 2.54a。

baseline 完成后停止，等待 Codex B review，不得自动继续下一阶段。
