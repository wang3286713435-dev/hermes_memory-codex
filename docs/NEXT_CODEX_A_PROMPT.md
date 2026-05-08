# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。请只做 Phase 2.54c File Steward UX display-tail selective Git baseline。不要进入 Phase 2.55，不要做新功能，不要运行真实 upload / API / CLI smoke。

## 1. 背景

Phase 2.54c display-tail fix 已完成并通过 Codex B review 与 Codex C 真实终端复验。

已完成事实：

1. Hermes 主仓 display-layer fix：
   - `ContextBuilder` 的 `file_answer_metadata` 分支增加 required fields、echo required、source fields present 与 safety flags 邻近展示。
   - `source_name` 增加 metadata fallback。
2. 主仓测试：
   - py_compile 通过。
   - targeted pytest：`74 passed`。
3. Codex C 真实终端复验：
   - API `/health=200 OK`，Hermes CLI 可用。
   - session_id：`20260508_181817_c7c9a3`
   - `@主标书` 绑定通过。
   - Q3 file answer metadata：pass。
   - `file_answer_metadata_required_fields` 可见。
   - `file_answer_metadata_echo_required=true` 可见。
   - `title/source_name/source_type/citation_count` 字段可见。
   - `metadata_as_answer=false`、`facts_as_answer=false`、`snapshot_as_answer=false`、`requires_retrieval_evidence=true` 全部可见。
   - 未出现 metadata / facts / transcript / snapshot 替代 evidence。
   - 未出现第三文件污染。

保留尾项：`source_name/source_type` 的底层值为空时会显示 `Missing Evidence`，这是正确边界，不阻塞 baseline。

## 2. 本轮目标

执行 Phase 2.54c 双仓 selective Git baseline。

建议 tag：

`phase-2.54c-file-steward-display-tail-baseline`

建议 commit message：

`chore: baseline phase 2.54c file steward display tail`

## 3. 允许 stage / commit 的文件

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 只允许：

1. `agent/memory_kernel/context_builder.py`
2. `tests/agent/test_session_document_scope.py`

Hermes_memory `/Users/Weishengsu/Hermes_memory` 只允许：

1. `docs/ACTIVE_PHASE.md`
2. `docs/PHASE_BACKLOG.md`
3. `docs/HANDOFF_LOG.md`
4. `docs/NIGHTLY_SPRINT_QUEUE.md`
5. `docs/NEXT_CODEX_A_PROMPT.md`
6. `docs/NEXT_CODEX_C_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

`reports/agent_runs/latest.json` 是 ignored 本地状态，只更新，不 stage。

## 4. 禁止 stage / 修改的既有 dirty

Hermes_memory 禁止纳入：

- `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

Hermes 主仓禁止纳入：

- `agent/memory_kernel/adapters/hermes_memory_adapter.py`
- `uv.lock`
- `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
- `tests/agent/test_memory_kernel_adapter_reload.py`

如果发现 staged 文件超出白名单，必须停止并 reset staged，不要 commit。

## 5. baseline 前检查

Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent`：

```bash
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/file_steward_ux.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_file_steward_ux.py tests/agent/test_session_document_scope.py tests/agent/test_facts_agent_context.py -q
git diff --check
```

Hermes_memory `/Users/Weishengsu/Hermes_memory`：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

不需要再跑 API / CLI smoke；Codex C 已完成。

## 6. Git 操作要求

### Hermes 主仓

1. 只 stage 白名单 2 个文件。
2. commit。
3. tag `phase-2.54c-file-steward-display-tail-baseline`。
4. 推送到可写远端 `backup2` 的当前工作分支。
5. 推送 tag 到 `backup2`。

### Hermes_memory

1. 只 stage 白名单 8 个文档文件。
2. commit。
3. tag `phase-2.54c-file-steward-display-tail-baseline`。
4. 推送 `origin` 当前分支。
5. 推送 tag 到 `origin`。

## 7. 完成后更新 ignored latest

更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：

1. `status=baseline`
2. 写入双仓 commit hash。
3. 写入 tag。
4. 写入 push 结果。
5. 写入最终 git status。
6. `needs_codex_b_review=false`
7. `needs_codex_c_validation=false`

仍不要 stage `latest.json`。

## 8. 完成后输出

请输出：

1. 修改 / staged 文件。
2. 测试结果。
3. Hermes 主仓 commit hash。
4. Hermes_memory commit hash。
5. tag。
6. push 结果。
7. 最终 git status。
8. 是否建议进入下一阶段。

完成 baseline 后停止。不要进入 Phase 2.55，不要写下一阶段 prompt。
