# MVP Pilot Runbook

## 1. 使用目标

本 runbook 用于公司内部受控 MVP Pilot。

Hermes 当前可作为人工监督下的企业文件 Agent，用于：

1. 标书审查 / 风险提取。
2. 文件内容提取与引用定位。
3. 公司未来发展方向辅助分析。

## 2. 启动前检查

Codex C 或内部试用人员应先确认：

1. Hermes_memory API `/health` 返回正常。
2. Hermes CLI 可启动。
3. 目标文件已入库并可检索。
4. 需要使用 alias 的文件已在同一会话中绑定。
5. 当前不是 production rollout。

## 3. Alias 建议

建议首轮 pilot 使用以下 alias：

1. `@主标书`
2. `@对比标书`
3. `@答疑文件`
4. `@交付标准旧版`
5. `@交付标准新版`
6. `@会议纪要`

绑定后必须确认：

1. alias_resolution 成功。
2. resolved_document_id 正确。
3. retrieval_evidence_document_ids 不混入非目标文件。

## 4. 通用回答要求

每个业务回答必须包含：

1. 结论。
2. Evidence / citation。
3. 不确定或缺 evidence 的说明。
4. 待人工确认项。

禁止：

1. 无 evidence 给确定结论。
2. confirmed facts 替代 retrieval evidence。
3. history memory 替代 retrieval evidence。
4. meeting transcript 被标记为 confirmed fact。

## 5. Codex C 验收 Prompt

### 5.1 API / CLI 检查

```text
请检查 Hermes_memory API /health 是否可用，并确认 Hermes CLI 可以启动。
返回 API 状态、CLI 状态、当前 session_id。
```

### 5.2 Alias 绑定

```text
请在同一 Hermes 会话中绑定：
把当前主标书设为 @主标书。
把会议纪要文件设为 @会议纪要。
如需要 Excel / PPTX / 交付标准，也分别绑定 alias。
返回 alias_resolution、resolved_document_id、version_id。
```

### 5.3 业务 Query 执行

执行 `PHASE230_PRACTICAL_MVP_PILOT_PLAN.md` 中 12 条验收 query。

每条 query 回传：

1. query 文本。
2. pass / fail。
3. document_id / version_id。
4. citation 字段。
5. `facts_as_answer`。
6. `transcript_as_fact`。
7. `contamination_flags`。
8. 是否缺 evidence。
9. 失败原因。

## 6. 通过标准

1. 标书基础信息、资质、合同风险能返回目标文件 evidence 或明确缺 evidence。
2. Excel 返回 sheet / cell citation。
3. PPTX 返回 slide citation。
4. 会议纪要返回行动项、决策、风险，且 `transcript_as_fact=false`。
5. facts 辅助上下文保持 `facts_as_answer=false`。
6. compare 场景无第三文件污染。

## 7. 失败后处理

失败后只记录问题，不自动修复。

记录字段：

1. query。
2. 预期。
3. 实际 document_id / citation。
4. trace flags。
5. 是否疑似 retrieval、context、alias、citation 或 facts 语义问题。

需要修复时另起 phase，不在 pilot runbook 中直接修改代码或数据。
