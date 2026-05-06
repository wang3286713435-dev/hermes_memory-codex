# NEXT_CODEX_C_PROMPT

这是 Codex C 的下一轮真实终端复验入口。请只做 Phase 2.43d Day-1 `@主标书` alias/session 修复复验，不修改任何代码、文档、DB、facts、versions、OpenSearch、Qdrant，不上传文件，不提交 Git，不执行 repair/backfill/reindex/cleanup/delete，不进入 production rollout 或 Data Steward。

## 必读文件

执行前必须读取：

1. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_DAY1_RUN_SHEET.md`
2. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_LAUNCH_PACKET.md`
3. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
5. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## 当前背景

Day-1 Pilot 上一轮触发 `Pause`：

1. session_id：`20260506_132914_521b45`
2. `@主标书` 绑定阶段出现 `alias_bind_failed`，但同时返回正确 document/version。
3. 正式 Q1 变成 `alias_missing=true / retrieval_suppressed=true`，未进入 retrieval。
4. `@硬件清单`、`@C塔方案`、`@会议纪要` 绑定稳定。
5. Codex A 已做 bounded fix：current alias bind 在 retrieval 返回多个候选时采用 top document 完成绑定，并记录 `alias_bind_ambiguous_retrieval_document_ids`；title bind 多候选仍保持失败。
6. Codex B review 结论：bounded diff 可交真实终端复验；不能 baseline，必须先验证。

## 复验目标

确认真实 Hermes CLI 中：

1. `把当前主标书设为 @主标书` 绑定不再最终失败。
2. 同一 session 后续 Q1 不再出现 `alias_missing=true`。
3. 同一 session 后续 Q1 不再出现 `retrieval_suppressed=true`。
4. Q1 能进入 retrieval，并且 evidence 只来自 `@主标书`。
5. 不需要验证最高投标限价是否召回；限价 Missing Evidence 是已知 P1 retrieval recall 风险，不作为本轮失败。

## 环境检查

在 `/Users/Weishengsu/Hermes_memory`：

1. 检查 API `/health`；如未启动，可按既有 runbook 使用 `/Users/Weishengsu/Hermes_memory/scripts/run_local_api.sh` 启动。
2. 在 `/Users/Weishengsu/.hermes/hermes-agent` 检查 Hermes CLI：`./.venv/bin/hermes chat --help`。
3. 新建 fresh Hermes session，不复用旧 session。

## 必跑 Prompt

### Step 1：绑定主标书 alias

在 fresh session 中执行：

```text
把当前主标书设为 @主标书
```

必须记录：

1. session_id
2. `alias_resolution.status`
3. `resolved_document_id`
4. `resolved_version_id`
5. `alias_missing`
6. `retrieval_suppressed`
7. 是否出现 `alias_bind_ambiguous_retrieval_document_ids`

期望：

1. `alias_resolution.status` 为 `alias_bound` 或等价成功状态。
2. `resolved_document_id=869d4684-0a98-4825-bc72-ada65c15cfc9`
3. `resolved_version_id=43558ba9-2813-42ff-b11b-3fbb4448a5bb`
4. `alias_missing=false`
5. `retrieval_suppressed=false`

### Step 2：同 session 正式 Q1

在同一 session 中继续执行：

```text
围绕 @主标书，提取工程名称、工程地点、建设单位、代建单位、工期、最高投标限价，并列出 document_id、version_id 和 citation。
```

必须记录：

1. `alias_resolution.status`
2. `alias_missing`
3. `retrieval_suppressed`
4. `retrieval_evidence_document_ids`
5. `document_id`
6. `version_id`
7. citation / chunk id
8. `facts_as_answer`
9. `transcript_as_fact`
10. 是否有第三文件污染

期望：

1. `alias_resolution.status=alias_resolved`
2. `alias_missing=false`
3. `retrieval_suppressed=false`
4. `retrieval_evidence_document_ids` 只包含 `869d4684-0a98-4825-bc72-ada65c15cfc9`
5. citation 来自 `@主标书`
6. `facts_as_answer=false`
7. `transcript_as_fact=false`
8. 不混入第三文件

最高投标限价如果仍为 Missing Evidence，不算失败；只要没有编造金额即可。

## 可选扩展

如果 Step 1 / Step 2 均通过，可继续跑 Day-1 Q2：

```text
围绕 @主标书，提取投标资质、项目经理、联合体、业绩、人员要求，并标记哪些字段需要人工复核。
```

Q2 只用于确认 alias/session 没有再次丢失，不用于验证深层召回完全解决。

## 输出格式

请按以下结构回复：

1. API / CLI 是否可用。
2. session_id。
3. Step 1 alias 绑定表。
4. Step 2 Q1 验收表。
5. 可选 Q2 结果（如果执行）。
6. 是否仍出现 `alias_missing=true`。
7. 是否仍出现 `retrieval_suppressed=true`。
8. 是否进入 retrieval 且 evidence 仅来自 `@主标书`。
9. 是否有 facts/transcript 替代 evidence。
10. 是否有第三文件污染。
11. 是否建议恢复 Day-1 Pilot。
12. 是否建议 Phase 2.43d Git baseline。
13. 若不建议，最小阻塞点是什么。

## 判定规则

### Pass

Step 1 绑定成功，Step 2 同 session `alias_resolved`，无 `alias_missing`，无 `retrieval_suppressed`，evidence 只来自 `@主标书`。

### Partial

alias/session 已恢复，但 trace 字段展示不完整；可人工从 citation 确认只来自 `@主标书`。

### Fail

任一情况即 fail：

1. Step 1 仍 `alias_bind_failed`。
2. Step 2 仍 `alias_missing=true`。
3. Step 2 仍 `retrieval_suppressed=true`。
4. Step 2 未进入 retrieval。
5. evidence 混入第三文件。
6. facts 或 transcript 替代 retrieval evidence。

本轮复验只支持内部受控 MVP Pilot 判断，不授权 production rollout、自动审标、自动投标、自动经营决策、repair 或 Data Steward。
