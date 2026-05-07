# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已 review Phase 2.48a / 2.48b，Codex C targeted smoke 已通过；现在授权执行 combined Git baseline。

## 本轮目标

Phase 2.48a / 2.48b / 2.48c combined Git baseline。

只提交 P2 display tails 相关文件：

1. Phase 2.48 docs-only triage plan。
2. Phase 2.48a Excel citation display polish。
3. Phase 2.48b Meeting transcript boundary trace display polish。
4. Phase 2.48c Codex C targeted smoke 结果与交接文档。

不要进入 Phase 2.49。不要写新功能代码。不要运行新的 smoke。

## Codex C targeted smoke 通过事实

Codex C session：`20260507_215047_a81e78`。

结果：`pass`。

验收摘要：

1. API / CLI 可用；API 首次不可用后按既有 runbook 启动，复查 `/health=200 OK`。
2. `@硬件清单` alias_bound，`alias_missing=false`，`retrieval_suppressed=false`。
3. `@会议纪要` alias_bound，`alias_missing=false`，`retrieval_suppressed=false`。
4. Excel citation display pass：仅见 `@硬件清单` evidence，显示 `sheet_name=开始`、`cell_range=A3:P24`、`citation_precision=multi_row_range`、`row_range_fallback=[3,24]`。
5. Meeting transcript boundary display pass：仅见 `@会议纪要` evidence，显示 `meeting_transcript_used=true`、`transcript_as_fact=false`、`evidence_required=true`、`meeting_transcript_as_confirmed_fact=false`、`facts_context_fact_ids=[]`。
6. 未出现 facts 替代 evidence、meeting transcript 当 confirmed fact、第三文件污染。
7. Codex C 建议 Phase 2.48a / 2.48b combined Git baseline。

## 必读文件

Hermes_memory：

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `docs/PHASE248_P2_DISPLAY_TAILS_TRIAGE_PLAN.md`
8. `reports/agent_runs/latest.json`

Hermes 主仓库：

1. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
2. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_facts_agent_context.py`

## Baseline 白名单

Hermes_memory 允许 stage / commit：

1. `docs/PHASE248_P2_DISPLAY_TAILS_TRIAGE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

Hermes 主仓库允许 stage / commit：

1. `agent/memory_kernel/context_builder.py`
2. `tests/agent/test_structured_citation_context.py`
3. `tests/agent/test_facts_agent_context.py`

## 必须排除

Hermes_memory 不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`（ignored 本地状态）

Hermes 主仓库不得 stage / commit：

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`

## 轻量验证

Hermes 主仓库：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py tests/agent/test_facts_agent_context.py -q
git diff --check
```

Hermes_memory：

```bash
cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
```

不运行新的 Codex C smoke。
不启动 / 停止服务。
不运行 Hermes CLI chat。
不生成真实 internal MVP run record。

## Git baseline 命令要求

Hermes 主仓库：

1. 只 stage 白名单 3 个文件。
2. commit message：`chore: polish phase 2.48 p2 display tails`
3. tag：`phase-2.48-p2-display-tails-baseline`
4. push 到既有可写远端 / 分支，遵循主仓既定策略：不要推主仓 origin，使用 `backup2` 当前工作分支。
5. push tag 到 `backup2`。

Hermes_memory：

1. 只 stage 白名单 8 个文件。
2. commit message：`docs: baseline phase 2.48 p2 display tails`
3. tag：`phase-2.48-p2-display-tails-baseline`
4. push `origin/main`。
5. push tag 到 `origin`。

## Baseline 后更新 ignored 状态

更新 `reports/agent_runs/latest.json`：

1. `phase=Phase 2.48 P2 Display Tails Combined Baseline`
2. `status=baseline`
3. 记录两个仓库 commit hash、tag、push result。
4. 记录 Codex C targeted smoke `pass`。
5. `needs_codex_b_review=false`
6. `needs_codex_c_validation=false`

`latest.json` 必须保持 ignored，不得 stage。

## 硬禁止

1. 不进入 Phase 2.49。
2. 不写新功能代码。
3. 不改 meeting ingestion contract。
4. 不改 retrieval contract。
5. 不改 memory kernel 主架构。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete / migration。
8. 不进入 production rollout。
9. 不进入 Data Steward 实现。
10. 不 stage / commit out-of-scope dirty。

## 完成后输出

请输出：

1. 两仓库 commit hash。
2. tag。
3. push 结果。
4. 测试结果。
5. final git status。
6. out-of-scope dirty 是否仍保留。
7. 是否建议进入 Phase 2.49 planning。
