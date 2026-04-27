# Next Codex A Prompt

这是 Codex A 的下一轮固定任务入口。请读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.30a / 2.30b Practical MVP Pilot 收口与双仓库 Git baseline。

Codex C 已复跑 12 条 Pilot query，结论如下：

1. Alias/session 修复有效。
2. 四个 alias 在同一 session 后续 query 中均稳定 `alias_resolved`：
   - `@主标书`
   - `@会议纪要`
   - `@硬件清单`
   - `@C塔方案`
3. 未再出现 `alias_missing`。
4. 未出现 `retrieval_suppressed` 误阻断。
5. `facts_as_answer=false` 全部稳定。
6. `transcript_as_fact=false` 全部稳定。
7. compare 场景未混入第三文件。
8. 12 条 query：`10/12 pass, 2/12 partial, 0 failed`。
9. partial 均为召回质量尾项，不是 alias/session 修复失败。

本轮只做 Git baseline，不做新功能。

## 当前基线

Hermes_memory：

1. 当前 HEAD：`7060d38`。
2. 当前 dirty 包含 Phase 2.30a Pilot 文档、Phase 2.30b 状态同步、`NEXT_CODEX_A_PROMPT.md`。
3. `reports/agent_runs/latest.json` 是 ignored 本地状态文件，不提交。

Hermes 主仓库：

1. 当前 HEAD：`801b5621`。
2. 当前 Phase 2.30b 相关 dirty：
   - `agent/memory_kernel/session_document_scope.py`
   - `tests/agent/test_session_document_scope.py`
   - `docs/TODO.md`
   - `docs/DEV_LOG.md`
3. 既存无关 dirty 必须保留，不得 stage：
   - `uv.lock`
   - `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
   - `tests/agent/test_memory_kernel_adapter_reload.py`

## Codex C 验收摘要

API / CLI：

1. Hermes_memory `/health`：通过，`200 OK`。
2. Hermes CLI：通过，`hermes chat --help` 可用。
3. Session：`20260428_015219_f923ca`。
4. 未修改代码、未改文档、未上传、未提交、未写 DB/facts/versions。

Alias：

1. `@主标书`：已绑定，Q1-Q4 均 `alias_resolved`。
2. `@会议纪要`：`alias_bound`，后续稳定。
3. `@硬件清单`：`alias_bound`，后续稳定。
4. `@C塔方案`：`alias_bound`，后续稳定。

12 条 query：

1. `@主标书` 基础信息：partial，最高投标限价未召回。
2. `@主标书` 资质 / 经理 / 联合体 / 业绩 / 人员：partial，业绩要求未被当前召回覆盖。
3. `@主标书` 合同 / 商务风险：pass。
4. `@主标书` 不存在风险点：pass。
5. `@硬件清单` GPU 服务器金额 / 单位：pass，Excel citation 含 `sheet=开始`、`A3:P24`、Row 7 / `H7:P7`。
6. `@C塔方案` PPTX 主题 / 首页：pass，含 slide citation。
7. `@会议纪要` 行动项：pass。
8. `@会议纪要` 决策：pass。
9. `@会议纪要` 风险：pass。
10. `@会议纪要 vs @主标书` compare：pass，两份 document 均命中，无第三文件。
11. confirmed facts 不替代 evidence：pass。
12. 公司发展方向辅助分析：pass，四个 alias 均命中，输出 Evidence / Interpretation / Recommendation / Risk / Missing Evidence。

## 允许 stage / commit 的文件

Hermes_memory 仅允许：

1. `docs/PHASE230_PRACTICAL_MVP_PILOT_PLAN.md`
2. `docs/MVP_PILOT_RUNBOOK.md`
3. `docs/MVP_TENDER_REVIEW_PLAYBOOK.md`
4. `docs/MVP_FILE_EXTRACTION_PLAYBOOK.md`
5. `docs/MVP_STRATEGY_ANALYSIS_PLAYBOOK.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/NIGHTLY_SPRINT_QUEUE.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`
10. `docs/ACTIVE_PHASE.md`
11. `docs/HANDOFF_LOG.md`
12. `docs/PHASE_BACKLOG.md`

Hermes 主仓库仅允许：

1. `agent/memory_kernel/session_document_scope.py`
2. `tests/agent/test_session_document_scope.py`
3. `docs/TODO.md`
4. `docs/DEV_LOG.md`

禁止 stage：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/.hermes/hermes-agent/uv.lock`
3. `/Users/Weishengsu/.hermes/hermes-agent/docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
4. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_memory_kernel_adapter_reload.py`
5. 任何真实 reports / reviews / agent run JSON。

## Baseline 前验证

Hermes 主仓库：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
python3 -m py_compile agent/memory_kernel/session_document_scope.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py agent/memory_kernel/context_builder.py agent/memory_kernel/adapters/hermes_memory_adapter.py
```

然后尝试：

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m pytest tests/agent/test_session_document_scope.py tests/agent/test_phase214b_cli_smoke_eval.py -q
```

如果 pytest 仍不可用，按既有方式直接执行测试函数断言，并报告数量；当前已知 direct assertion tests 为 `53 passed`。

Hermes_memory：

```bash
cd /Users/Weishengsu/Hermes_memory
python3 -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
```

确认 `git status --short` 仅包含本阶段允许文件。

## Commit / Tag / Push

Hermes 主仓库：

1. commit message：`fix: stabilize practical MVP alias binding`
2. tag：`phase-2.30b-practical-mvp-pilot-baseline`
3. push 目标：可写远端 `backup2` 当前工作分支与 tag。不要推 origin。

Hermes_memory：

1. commit message：`docs: baseline practical MVP pilot`
2. tag：`phase-2.30b-practical-mvp-pilot-baseline`
3. push 目标：`origin/main` 与 tag。

## 硬禁止

1. 不写新功能。
2. 不改 retrieval contract。
3. 不改 memory kernel 主架构。
4. 不改 parser / ingestion / chunking。
5. 不写业务 DB。
6. 不修改 facts / document_versions / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete。
8. 不进入 production rollout。
9. 不创建 production cron / scheduler。
10. 不处理召回质量尾项。

## Nightly Sprint 规则

用户已要求开启 Codex A 夜间自动模式，但本轮是 Yellow Lane baseline。

执行规则：

1. 可以执行本 baseline。
2. baseline 成功后必须停止。
3. 不得继续自动进入 Phase 2.31。
4. 不得在夜间自动做 rollout、repair、DB mutation 或新功能。

## 返回报告

请返回：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 是否建议进入内部受控 MVP Pilot。
8. 是否建议进入下一阶段规划。
9. 保留 known risks：
   - 深层字段召回仍需人工复核。
   - 公司方向建议必须人工决策。
   - 当前不是 production rollout。
