# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`

## 当前状态

Phase 2.38a Tender P1 Source Availability Audit 已完成最小实现，并已通过 Codex B review（2026-05-03）。

已完成内容：

1. 新增 `scripts/phase238a_tender_p1_source_audit.py`。
2. 新增 `tests/test_phase238a_tender_p1_source_audit.py`。
3. 新增 `reports/tender_p1_audit/.gitignore` 与 `reports/tender_p1_audit/README.md`。
4. 新增 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
5. 文档已同步 `TODO.md`、`DEV_LOG.md`、`ACTIVE_PHASE.md`、`PHASE_BACKLOG.md`、`HANDOFF_LOG.md`。
6. 目标测试已通过：py_compile 通过，`tests/test_phase238a_tender_p1_source_audit.py` 为 `10 passed`，`git diff --check` 通过。
7. live read-only dry-run 已尝试，但本机 `.env` 的 `postgres` 主机名不可解析，字段均返回 `skipped_live_unavailable`。
8. Codex B review 复跑通过：py_compile、pytest 10 passed、`git diff --check` 均通过；ignore 策略命中；未发现 DB、repair、rollout、索引变更或真实报告越界。

## 下一轮目标

Phase 2.38a Git baseline（Codex B approved）。

执行范围：

1. 只做 Git baseline。
2. 不新增功能。
3. 不修改业务逻辑。
4. 不重跑 live DB / OpenSearch audit，除非用户明确要求。
5. 不进入 retrieval fix、repair、rollout 或索引重建。

## 当前应提交文件

只允许提交：

1. `scripts/phase238a_tender_p1_source_audit.py`
2. `tests/test_phase238a_tender_p1_source_audit.py`
3. `reports/tender_p1_audit/.gitignore`
4. `reports/tender_p1_audit/README.md`
5. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
6. `docs/ACTIVE_PHASE.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/PHASE_BACKLOG.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`
11. `docs/NEXT_CODEX_A_PROMPT.md`

不得提交：

1. `reports/agent_runs/latest.json`
2. 真实 `reports/tender_p1_audit/*.json` / `*.md`
3. 真实 `reports/pilot_issues/*.json` / `*.md`
4. 真实 `reports/pilot_triage/*.json` / `*.md`
5. 任何 retrieval / ingestion / indexing / facts / version governance 业务代码变更
6. 任何 DB / OpenSearch / Qdrant 数据变更

## 必须复跑

```bash
cd /Users/Weishengsu/Hermes_memory
uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py
uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q
git diff --check
```

## Git 要求

1. `git status --short` 只包含上述 Phase 2.38a 文件。
2. 只 stage 上述允许文件。
3. commit message：
   `chore: add phase 2.38a tender p1 source audit`
4. tag：
   `phase-2.38a-tender-p1-source-audit-baseline`
5. push `origin/main`。
6. push tag。

## 硬边界

1. 不写业务 DB。
2. 不修改 facts。
3. 不修改 document_versions。
4. 不修改 OpenSearch。
5. 不修改 Qdrant。
6. 不执行 repair / backfill / reindex / cleanup / delete。
7. 不创建外部 issue。
8. 不进入 rollout。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。
11. 不提交真实 audit report 运行产物。

## 返回报告

按固定短格式返回：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 是否存在真实 audit report 被 staged。
8. 是否建议进入下一阶段。
