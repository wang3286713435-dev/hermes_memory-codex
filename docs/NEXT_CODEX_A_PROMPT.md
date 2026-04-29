# Next Codex A Prompt

这是 Codex A 的下一轮固定任务入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/.hermes/hermes-agent/AGENTS.md`

## 当前状态

Phase 2.35c alias/session 修复已通过 Codex C 真实终端复验。

复验结论：

1. `@主标书` bind 后正式 Q1 / Q2 均为 `alias_resolved`。
2. `alias_missing=false`。
3. `retrieval_suppressed=false`。
4. retrieval evidence 仅来自主标书。
5. `snapshot_as_answer=false`、`facts_as_answer=false`、`transcript_as_fact=false`。

仍未收口：

1. 最高投标限价 / 招标控制价 / 投标报价上限仍 Missing Evidence。
2. 投标资质具体等级 / 类别仍 Missing Evidence。
3. 类似业绩与人员要求仍 Missing Evidence 或缺主标具体条件。
4. `metadata_deep_field_profile=null` 与 `deep_field_profile=single_pass` 仍是 trace / 展示尾项。

## 下一轮目标

Phase 2.35c Git baseline。

仅在用户明确要求 baseline 时执行：

1. 复核 dirty 文件，只包含 Phase 2.35 / 2.35b / 2.35c 相关变更。
2. 复跑指定测试。
3. 只 stage 相关文件。
4. commit / tag / push。

baseline 文案必须明确：

1. alias/session 修复已通过真实终端复验。
2. deep-field recall 仍 partial。
3. Missing Evidence 仍是正确安全口径。
4. 当前不是 production rollout，不是自动审标收口。

## 建议 baseline 文件范围

Hermes_memory：

1. `app/services/retrieval/service.py`
2. `app/services/retrieval/tender_metadata.py`
3. `tests/test_tender_metadata_retrieval.py`
4. `tests/test_phase235_tender_deep_field_retrieval.py`
5. `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`
8. `docs/ACTIVE_PHASE.md`
9. `docs/HANDOFF_LOG.md`
10. `docs/PHASE_BACKLOG.md`
11. `docs/NIGHTLY_SPRINT_QUEUE.md`
12. `docs/NEXT_CODEX_A_PROMPT.md`

Hermes 主仓库：

1. `agent/memory_kernel/session_document_scope.py`
2. `tests/agent/test_session_document_scope.py`
3. `docs/TODO.md`
4. `docs/DEV_LOG.md`

不得混入：

1. 主仓库 `uv.lock`
2. 主仓库 `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
3. 主仓库 `tests/agent/test_memory_kernel_adapter_reload.py`
4. `reports/agent_runs/latest.json`
5. 任何业务数据、真实 reports、真实 reviews。

## 硬边界

1. 不进入 production rollout。
2. 不写业务 DB / facts / document_versions。
3. 不修改 OpenSearch / Qdrant 数据。
4. 不执行 repair / backfill / reindex / cleanup / delete。
5. 不做自动审标结论。
6. 不隐藏 Missing Evidence。
7. 不编造最高投标限价、资质等级、业绩或人员数量。
