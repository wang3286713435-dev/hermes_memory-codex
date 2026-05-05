# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
7. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前状态

Phase 2.38d `personnel-only runtime post-answer guard` 已完成实现、目标测试和 Codex C 真实终端复验。

Codex C 最新复验结论：

1. API `/health` 返回 `200 OK`，Hermes CLI 可用。
2. session_id：`20260505_211355_d19af3`。
3. `@主标书` alias 绑定成功：
   - document_id：`869d4684-0a98-4825-bc72-ada65c15cfc9`
   - version_id：`43558ba9-2813-42ff-b11b-3fbb4448a5bb`
   - `alias_missing=false`
   - `retrieval_suppressed=false`
4. Q1 personnel-only：pass，safe fallback 已触发，未出现 forbidden terms 或隐式数量推断，保留 Missing Evidence / 人工复核。
5. Q2 personnel-only：pass，safe fallback 已触发，未出现 forbidden terms 或隐式数量推断，保留 Missing Evidence / 人工复核。
6. Q3 broad qualification：pass，未触发 personnel-only fallback，正常展开 broad query，citation 均来自 `@主标书`。
7. 未出现 facts 替代 evidence、transcript_as_fact、第三文件污染。
8. Codex C 建议 Phase 2.38d Git baseline；当前无 runtime guard 阻塞。

## 本轮目标

Phase 2.38d personnel runtime guard Git baseline。

只做 baseline，不新增功能，不进入 Phase 2.38e，不处理 Data Steward，不处理 Phase 2.39。

## 必须保持的阶段边界

1. 本 baseline 只收口 Phase 2.38d personnel runtime guard。
2. 不继续修改 runtime guard，除非复跑测试暴露直接失败。
3. 不处理 `price_ceiling`。
4. 不处理 `project_manager_level`。
5. 不做 broad retrieval tuning。
6. 不写 DB / facts / document_versions。
7. 不修改 OpenSearch / Qdrant。
8. 不执行 repair / backfill / reindex / cleanup / delete。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。
11. 不进入 production rollout。
12. 不进入 Data Steward / BIM 数据管家实现或 baseline。

## 严格禁止 stage 的 Data Steward 文件 / hunks

当前工作区包含 Phase 2.39 Data Steward docs-only 规划 dirty。它必须与 Phase 2.38d baseline 分开。

本轮禁止 stage 以下整文件：

1. `/Users/Weishengsu/Hermes_memory/docs/PRD.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ROADMAP.md`
3. `/Users/Weishengsu/Hermes_memory/docs/TECHNICAL_DESIGN.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE239_DATA_STEWARD_PRODUCT_PLAN.md`

对于共享文档，必须选择性 stage，只纳入 Phase 2.38d hunks，排除 Data Steward hunks：

1. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
2. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`

如果无法可靠选择性 stage，则停止并写交接，不要 baseline。

## 允许 stage 的 Phase 2.38d 范围

Hermes_memory 允许 stage：

1. `/Users/Weishengsu/Hermes_memory/app/services/retrieval/service.py`
2. `/Users/Weishengsu/Hermes_memory/app/services/retrieval/tender_metadata.py`
3. `/Users/Weishengsu/Hermes_memory/scripts/phase238b_tender_concrete_recall_diagnostics.py`
4. `/Users/Weishengsu/Hermes_memory/tests/test_phase238d_personnel_recall_tail.py`
5. `/Users/Weishengsu/Hermes_memory/docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
6. Phase 2.38d hunks only in `ACTIVE_PHASE.md` / `HANDOFF_LOG.md` / `PHASE_BACKLOG.md` / `TODO.md` / `DEV_LOG.md` / `NEXT_CODEX_A_PROMPT.md`

Hermes 主仓允许 stage：

1. `/Users/Weishengsu/.hermes/hermes-agent/run_agent.py`
2. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
3. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
4. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
5. Phase 2.38d hunks only in `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md` and `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

Hermes 主仓以下既存无关 dirty 必须保留，不得 stage：

1. `/Users/Weishengsu/.hermes/hermes-agent/uv.lock`
2. `/Users/Weishengsu/.hermes/hermes-agent/docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_memory_kernel_adapter_reload.py`

## 验证命令

在 Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent` 运行：

```bash
./.venv/bin/python -m py_compile run_agent.py agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py -q
git diff --check
```

在 Hermes_memory `/Users/Weishengsu/Hermes_memory` 运行：

```bash
uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py
uv run pytest tests/test_phase238d_personnel_recall_tail.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q
git diff --check
```

若目标测试因环境不可用失败，应停止并写交接；不得跳过后 baseline。

## Baseline 操作

1. 先复核 `git status --short`，确认 dirty 符合上述范围。
2. 选择性 stage Phase 2.38d 文件 / hunks。
3. stage 后复核 `git diff --cached --name-only`，必须不包含 Data Steward 文件。
4. stage 后复核 `git diff --cached --check`。
5. Hermes_memory commit message：`chore: baseline phase 2.38d personnel runtime guard`
6. Hermes 主仓 commit message：`chore: baseline phase 2.38d personnel runtime guard`
7. tag：`phase-2.38d-personnel-runtime-guard-baseline`
8. Hermes_memory 推送 `origin/main` 与 tag。
9. Hermes 主仓按既定策略推送 `backup2/codex/phase-2.11d-context-regression-baseline` 与 tag，不推主仓 origin。
10. baseline 完成后停止，不得继续 Phase 2.39 或 Phase 2.38e。

## 完成后必须更新

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：记录 `status=baseline`、commit、tag、pushed。
2. `docs/HANDOFF_LOG.md`：记录 Phase 2.38d baseline 结果。
3. `docs/ACTIVE_PHASE.md`：记录 Phase 2.38d baseline 完成，并建议下一步单独处理 Phase 2.39 Data Steward docs-only baseline。
4. 如更新 `TODO.md` / `DEV_LOG.md` / `PHASE_BACKLOG.md`，只写 Phase 2.38d baseline 结论，不写 Data Steward 新内容。

## 验收标准

1. Codex C session `20260505_211355_d19af3` 的 pass 结论已写入交接。
2. 两仓目标测试通过。
3. 两仓 staged 内容只包含 Phase 2.38d 范围。
4. Data Steward 文件未被 staged / committed。
5. tag `phase-2.38d-personnel-runtime-guard-baseline` 指向对应 baseline HEAD。
6. push 成功。
7. 最终报告包含：commit hash、tag、push 结果、最终 git status、剩余无关 dirty。
