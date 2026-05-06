# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.43d `@主标书` alias/session 修复 Git baseline。

本轮不写新功能、不改代码逻辑、不进入 Phase 2.44、不启动 Pilot 新一轮、不运行 production rollout、不 repair、不 backfill、不 reindex、不 cleanup、不 delete、不做 Data Steward 实现。

## 必读文件

执行前必须读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
8. `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
9. `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

## Baseline 依据

Phase 2.43d 已满足 baseline gate：

1. 当前 phase 有明确验收结果：Day-1 `@主标书` alias/session blocker 已修复。
2. Codex B review 已通过：bounded diff 只影响 current alias bind fallback，未放宽 title bind 多候选失败语义。
3. Codex C 真实终端复验已通过：
   - session_id：`20260506_143354_d4ad05`
   - `@主标书`：同 session Q1-Q2 均 resolved，`alias_missing=false`，`retrieval_suppressed=false`
   - `@硬件清单`、`@C塔方案`、`@会议纪要`：alias bound 且 stable
   - Day-1 10 条 query：`6 pass / 4 partial / 0 fail`
   - P0：0
   - Decision：`Go`
4. 文档状态已同步：ACTIVE_PHASE / PHASE_BACKLOG / TODO / DEV_LOG / HANDOFF_LOG / latest.json 已记录 Codex C 结果。
5. 下一步将切换回内部受控 MVP Pilot continuation / issue intake，因此应先 baseline Phase 2.43d。

## 当前保留风险

这些是已知 Pilot 尾项，不是本轮 baseline 阻塞：

1. P1：`@主标书` 最高投标限价 / 招标控制价仍 Missing Evidence。
2. P1：`@主标书` 资质 / 项目经理 / 联合体 / 业绩 / 人员等深层字段仍需人工复核。
3. P1：Excel 硬件清单部分 cell citation 降级为 row / range。
4. P1/P2：公司方向分析仍必须人工决策，部分风险 / 行业判断需人工复核。
5. P2：会议风险解释 / strategy trace 展示尾项。

这些尾项不得在本轮顺手修。

## Git baseline 范围

### Hermes 主仓库

工作目录：`/Users/Weishengsu/.hermes/hermes-agent`

只允许 stage / commit 以下文件：

1. `agent/memory_kernel/session_document_scope.py`
2. `tests/agent/test_session_document_scope.py`
3. `docs/TODO.md`
4. `docs/DEV_LOG.md`

不得 stage / commit 以下既有无关 dirty：

1. `agent/memory_kernel/adapters/hermes_memory_adapter.py`
2. `uv.lock`
3. `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `tests/agent/test_memory_kernel_adapter_reload.py`

commit message：

```text
fix: stabilize main tender alias session binding
```

### Hermes_memory

工作目录：`/Users/Weishengsu/Hermes_memory`

只允许 stage / commit 以下文件：

1. `docs/NEXT_CODEX_A_PROMPT.md`
2. `docs/NEXT_CODEX_C_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`（ignored 本地状态）

commit message：

```text
docs: record phase 2.43d alias session validation
```

## Tag

两仓库都打同一个 tag：

```text
phase-2.43d-main-tender-alias-session-baseline
```

## 验证命令

### Hermes 主仓库

在 `/Users/Weishengsu/.hermes/hermes-agent` 执行：

```bash
./.venv/bin/python -m py_compile \
  agent/memory_kernel/session_document_scope.py \
  agent/memory_kernel/kernel.py \
  agent/memory_kernel/orchestrator.py \
  agent/memory_kernel/context_builder.py \
  agent/memory_kernel/adapters/hermes_memory_adapter.py

./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py -q

git diff --check
git status --short
```

### Hermes_memory

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

## Stage / commit / push 规则

1. 必须 selective staging，只 stage 白名单文件。
2. staged 后必须检查 `git diff --cached --name-only`。
3. 若 staged 文件超出白名单，必须 unstage 并停止。
4. Hermes 主仓库不得推 origin；按既定策略推可写远端 `backup2` 当前工作分支与 tag。
5. Hermes_memory 推 `origin/main` 与 tag。
6. baseline 后必须停止，不得进入 Phase 2.44，不得继续执行 Pilot，不得自动发起 Codex C。

## 完成报告必须包含

1. 两仓库 commit hash。
2. tag 是否创建并指向当前 HEAD。
3. push 结果。
4. 最终 `git status --short`。
5. 是否只 stage / commit 白名单文件。
6. 是否保留无关 dirty：
   - Hermes 主仓库：`agent/memory_kernel/adapters/hermes_memory_adapter.py`、`uv.lock`、`docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`、`tests/agent/test_memory_kernel_adapter_reload.py`
   - Hermes_memory：`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
7. 是否写 DB / facts / document_versions / OpenSearch / Qdrant（必须为否）。
8. 是否进入 rollout / repair / Data Steward（必须为否）。
9. 下一步建议：恢复内部受控 MVP Pilot continuation / issue intake，不进入 production rollout。
