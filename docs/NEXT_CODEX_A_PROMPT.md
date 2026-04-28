# Next Codex A Prompt

这是 Codex A 的下一轮固定任务入口。请读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.34 compare false-positive fix 收口与 Git baseline。

Phase 2.34 最小修复与 Codex C 真实终端复验均已完成：

1. Day-1 原问题：`@会议纪要 vs @主标书` compare 实际 evidence 只有两份目标文档，但输出层误报 `third_document_mixed=true`。
2. 修复后 Codex C 复验 session：`20260428_174853_31a315`。
3. API `/health` 返回 `200 OK`，Hermes CLI 可用。
4. `@主标书` 绑定成功：
   - `document_id=869d4684-0a98-4825-bc72-ada65c15cfc9`
   - `version_id=43558ba9-2813-42ff-b11b-3fbb4448a5bb`
5. `@会议纪要` 绑定成功：
   - `document_id=92051cc6-56b5-4930-bdf0-119163c83a75`
   - `version_id=e3b422e3-35e2-4d89-8136-66a558e8cfbe`
6. Compare 复验通过：
   - `comparedocumentids=["92051cc6-56b5-4930-bdf0-119163c83a75", "869d4684-0a98-4825-bc72-ada65c15cfc9"]`
   - `retrieval_evidence_documentids=["92051cc6-56b5-4930-bdf0-119163c83a75", "869d4684-0a98-4825-bc72-ada65c15cfc9"]`
   - `third_document_mixed=false`
   - `third_document_mixed_document_ids=[]`
   - `contaminationflags=none`
   - `facts_as_answer=false`
   - `transcript_as_fact=false`
7. Facts / transcript 抽样通过：`@会议纪要` 行动项总结保持 `facts_context_used=false`、`facts_context_fact_ids=[]`、`facts_as_answer=false`、`transcript_as_fact=false`。
8. 未出现实际第三文件 evidence。

本轮只做 Git baseline，不新增功能。

## 必须先读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_DAY1_RUN_SHEET.md`
6. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
7. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
8. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
9. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
10. Hermes 主仓库相关文件：
    - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
    - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
    - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
    - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
    - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

## Stage 白名单

Hermes 主仓库只允许 stage：

1. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
2. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
4. `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
5. `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

Hermes 主仓库不得 stage 既存无关 dirty：

1. `/Users/Weishengsu/.hermes/hermes-agent/uv.lock`
2. `/Users/Weishengsu/.hermes/hermes-agent/docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_memory_kernel_adapter_reload.py`

Hermes_memory 只允许 stage：

1. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
6. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
7. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

不得 stage：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/Hermes_memory/reports/nightly_runs/*.json`
3. 任何真实 reports / reviews / agent run JSON。

## 验证要求

Hermes 主仓库运行：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
python3 -m py_compile agent/memory_kernel/kernel.py agent/memory_kernel/context_builder.py agent/memory_kernel/orchestrator.py agent/memory_kernel/adapters/hermes_memory_adapter.py
```

如果 pytest 不可用，沿用 direct assertion test 函数执行方式，并在报告中写明。

Hermes_memory 运行：

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git diff --check -- docs/ACTIVE_PHASE.md docs/HANDOFF_LOG.md docs/PHASE_BACKLOG.md docs/NIGHTLY_SPRINT_QUEUE.md docs/TODO.md docs/DEV_LOG.md
```

不需要再次跑真实 Hermes CLI；Codex C 复验已经通过。

## Git baseline

Hermes 主仓库：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
git add agent/memory_kernel/kernel.py agent/memory_kernel/context_builder.py tests/agent/test_session_document_scope.py docs/TODO.md docs/DEV_LOG.md
git commit -m "Phase 2.34 compare contamination baseline"
git tag phase-2.34-compare-contamination-baseline
git push backup2 <current-branch>
git push backup2 phase-2.34-compare-contamination-baseline
```

Hermes_memory：

```bash
cd /Users/Weishengsu/Hermes_memory
git add docs/NEXT_CODEX_A_PROMPT.md docs/ACTIVE_PHASE.md docs/HANDOFF_LOG.md docs/PHASE_BACKLOG.md docs/NIGHTLY_SPRINT_QUEUE.md docs/TODO.md docs/DEV_LOG.md
git commit -m "docs: record phase 2.34 compare validation"
git tag phase-2.34-compare-contamination-baseline
git push origin main
git push origin phase-2.34-compare-contamination-baseline
```

如果 tag 已存在或 remote 拒绝，停止并报告，不要强推。

baseline 后更新 `reports/agent_runs/latest.json`，但不得提交该文件。

## 硬禁止

1. 不修改 retrieval contract。
2. 不修改 memory kernel 主架构。
3. 不写业务 DB。
4. 不修改 OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / cleanup / delete。
6. 不进入 production rollout。
7. 不做 facts 自动抽取。
8. 不让 facts 替代 retrieval evidence。
9. 不扩大到主标书深层召回实现。
10. 不扩大到 latency 优化实现。
11. 不混入无关 dirty。
12. 不强推。

## 返回报告

返回：

1. 修改文件。
2. commit hash。
3. tag。
4. push 结果。
5. 最终 git status。
6. 剩余 dirty。
7. 是否建议进入下一阶段。
