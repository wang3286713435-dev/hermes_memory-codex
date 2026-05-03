# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

## 当前状态

Phase 2.38b Tender P1 Concrete Source Recall Diagnostics 已完成 Codex B review。

Codex B 复核结果：

1. 代码范围符合 Phase 2.38b 边界：只读 diagnostics runner + tests + ignored reports 策略 + 文档同步。
2. 未修改 retrieval ranking。
3. 未改 retrieval contract。
4. 未改 memory kernel 主架构。
5. 未写 DB / facts / document_versions。
6. 未修改 OpenSearch / Qdrant。
7. 未执行 repair / backfill / reindex / cleanup / delete。
8. 未进入 rollout。
9. 未自动审标。

复跑验证：

1. `uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
2. `uv run pytest tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`9 passed`。
3. `git diff --check`：通过。
4. ignore 策略命中：`reports/tender_recall_diagnostics/*.json`、`*.md` 与 `reports/agent_runs/latest.json` 不入 Git。

Codex B 只读 live preview 复核：

1. `output_file=None`，未写真实报告。
2. `price_ceiling=field_should_remain_missing_evidence`。
3. `qualification_grade_category=candidate_in_top_k`，candidate rank 包含 2。
4. `project_manager_level=field_requires_human_review`。
5. `performance_requirement=candidate_in_top_k`，candidate rank 包含 1。
6. `personnel_requirement=candidate_present_but_low_rank`，candidate ranks 为 19 / 17 / 41。

## 下一轮目标

Phase 2.38b Git baseline（Codex B approved）。

执行范围：

1. 只做 Git baseline。
2. 不新增功能。
3. 不修改业务逻辑。
4. 不重跑 live DB / OpenSearch diagnostics，除非用户明确要求。
5. 不进入 Phase 2.38c。
6. 不进入 retrieval fix、repair、rollout 或索引重建。

## 当前应提交文件

只允许提交：

1. `scripts/phase238b_tender_concrete_recall_diagnostics.py`
2. `tests/test_phase238b_tender_concrete_recall_diagnostics.py`
3. `reports/tender_recall_diagnostics/.gitignore`
4. `reports/tender_recall_diagnostics/README.md`
5. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
6. `docs/ACTIVE_PHASE.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/PHASE_BACKLOG.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`
11. `docs/NEXT_CODEX_A_PROMPT.md`

不得提交：

1. `reports/agent_runs/latest.json`
2. 真实 `reports/tender_recall_diagnostics/*.json` / `*.md`
3. 真实 `reports/tender_p1_audit/*.json` / `*.md`
4. 真实 `reports/pilot_issues/*.json` / `*.md`
5. 任何 retrieval / ingestion / indexing / facts / version governance 业务代码变更
6. 任何 DB / OpenSearch / Qdrant 数据变更

## 必须复跑

```bash
cd /Users/Weishengsu/Hermes_memory
uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py
uv run pytest tests/test_phase238b_tender_concrete_recall_diagnostics.py -q
git diff --check
git status --short
```

## Git 要求

1. `git status --short` 只包含上述 Phase 2.38b 文件。
2. 只 stage 上述允许文件。
3. commit message：
   `chore: add phase 2.38b tender recall diagnostics`
4. tag：
   `phase-2.38b-tender-recall-diagnostics-baseline`
5. push `origin/main`。
6. push tag。

## 硬边界

1. 不修 retrieval ranking。
2. 不改 retrieval contract。
3. 不改 memory kernel 主架构。
4. 不写业务 DB。
5. 不修改 facts。
6. 不修改 document_versions。
7. 不修改 OpenSearch。
8. 不修改 Qdrant。
9. 不执行 repair / backfill / reindex / cleanup / delete。
10. 不创建外部 issue。
11. 不进入 rollout。
12. 不提交真实 diagnostics report 运行产物。
13. 不把 `price_ceiling` 或 `project_manager_level` 当作可修复字段。

## 返回报告

按固定短格式返回：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 是否存在真实 diagnostics report 被 staged。
8. 是否建议进入 Phase 2.38c。

baseline 后必须停止，等待 Codex B 检查。不得自动进入 Phase 2.38c。
