# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`

## 当前状态

Phase 2.36c 已通过 Codex B review 与 Codex C 真实终端复验。

已确认：

1. Step 1 一步 alias binding 通过：
   - `alias_resolution.status=alias_bound`
   - `resolved_document_id=869d4684-0a98-4825-bc72-ada65c15cfc9`
   - `resolved_version_id=43558ba9-2813-42ff-b11b-3fbb4448a5bb`
   - `alias_missing=false`
   - `retrieval_suppressed=false`
2. Q1 限价 diagnostics 与 Missing Evidence 已一致：
   - `deep_field_missing_reason=missing_concrete_price_amount`
   - `concrete_evidence_present=false`
   - `concrete_evidence_missing_fields=["price_ceiling"]`
   - 未编造最高投标限价 / 招标控制价 / 投标报价上限金额。
3. Q2 项目经理等级边界通过：
   - `project_manager_level_explicit=false`
   - 电子证书 / 证照格式 / 材料要求未被推断为“项目经理=一级注册建造师”。
4. 安全边界稳定：
   - `snapshot_as_answer=false`
   - `facts_as_answer=false`
   - `transcript_as_fact=false`
   - `retrieval_evidence_document_ids` 仅主标书 document_id，无第三文件污染。
5. 仍保留非阻塞尾项：
   - Q1 组合查询包含工期时 profile 可能显示 `schedule_scope`，但 price aliases / missing reason / diagnostics 已正确透出。
   - 真实限价金额、资质具体等级 / 类别、业绩、人员数量仍可能是源文件缺字段或深层召回尾项，必须继续 Missing Evidence / 人工复核。

## 本轮目标

Phase 2.36c deep-field diagnostics semantic consistency 收口与 Git baseline。

只做 baseline，不继续写功能代码。

## 允许修改文件

只允许纳入以下 Phase 2.36 / 2.36c 文件：

1. `app/services/retrieval/tender_metadata.py`
2. `app/services/retrieval/service.py`
3. `tests/test_phase236_tender_deep_field_trace.py`
4. `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/PHASE_BACKLOG.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`
10. `docs/NEXT_CODEX_A_PROMPT.md`

`reports/agent_runs/latest.json` 是 ignored 本地状态文件，可以更新但不得 staged / committed。

## Baseline 前复核

执行以下轻量验证：

1. `UV_CACHE_DIR=.uv-cache uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py`
2. `UV_CACHE_DIR=.uv-cache uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q`
3. `git diff --check`
4. `git status --short`

要求：

1. pytest 应为 `33 passed` 或等价全通过。
2. dirty 文件必须只包含“允许修改文件”范围。
3. 不得出现 `.uv-cache`、`reports/agent_runs/latest.json` 或其他 ignored/local 文件被 staged。

## Git baseline

若验证通过：

1. stage 仅允许修改文件中的 tracked / new docs / tests / code 文件。
2. commit message：
   - `chore: baseline phase 2.36c tender deep-field diagnostics`
3. tag：
   - `phase-2.36c-tender-deep-field-diagnostics-baseline`
4. push：
   - `origin/main`
   - tag

baseline 后必须停止，不得自动进入 Phase 2.37。

## 文档同步要求

提交前确保文档写明：

1. Phase 2.36c Codex C 复验通过。
2. diagnostics 与 Missing Evidence 语义一致。
3. 电子证书格式 / 材料条款不得推断为项目经理等级。
4. deep-field recall 仍 partial，真实限价 / 资质等级 / 业绩 / 人员数量仍为后续尾项。
5. 当前不是自动审标，不是 rollout。

## 硬边界

1. 不写业务 DB / facts / document_versions。
2. 不修改 OpenSearch / Qdrant 数据。
3. 不执行 repair / backfill / reindex / cleanup / delete。
4. 不做自动审标结论。
5. 不隐藏 Missing Evidence。
6. 不编造最高投标限价、资质等级、业绩或人员数量。
7. 不修改 retrieval contract。
8. 不修改 memory kernel 主架构。
9. 不纳入无关 dirty。

## 输出要求

返回精简报告：

1. 修改文件。
2. 测试结果。
3. Codex C 复验结论是否已写入文档。
4. commit hash。
5. tag。
6. push 结果。
7. 最终 `git status --short`。
8. 阻塞点 / 风险点。
9. 是否建议进入下一阶段规划。
