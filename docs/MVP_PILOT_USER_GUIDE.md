# MVP Pilot User Guide

## 1. 适用对象

本指南面向内部受控 MVP Pilot 使用者、人工复核人、记录人和技术值守。

Hermes 当前是企业文件 Agent 试用版本，不是自动审标系统或自动经营决策系统。

## 2. 使用前检查

每次试用前确认：

1. Hermes_memory API `/health` 正常。
2. Hermes CLI 可启动。
3. 本轮使用的文件已入库。
4. 当前 session 内已绑定 alias。
5. 当前使用目标属于内部受控 Pilot，不是 production rollout。

## 3. 推荐 Alias

首轮建议使用：

1. `@主标书`
2. `@会议纪要`
3. `@硬件清单`
4. `@C塔方案`

绑定后检查：

1. `alias_resolution` 是否成功。
2. `resolved_document_id` 是否正确。
3. `version_id` 是否符合目标文件。
4. 后续 query 是否仍为 `alias_resolved`。

## 4. 标书审查使用方式

推荐 query：

```text
围绕 @主标书，提取工程名称、工程地点、建设单位、代建单位、工期、最高投标限价。
请按字段输出结论、evidence / citation、是否需要人工确认。
如果当前召回中没有找到，请明确写“未在当前召回中找到”。
```

复核重点：

1. 是否命中 `@主标书` document_id。
2. 每个字段是否有 citation。
3. 最高投标限价、业绩要求、付款节点是否标记人工复核。
4. Missing Evidence 是否被保留。

## 5. 文件提取使用方式

Excel query 应要求返回：

1. `sheet_name`
2. `cell_range`
3. document_id / version_id
4. 降级说明，如果只有 row / column

PPTX query 应要求返回：

1. `slide_number`
2. `slide_title`
3. document_id / version_id

会议纪要 query 应要求返回：

1. action items / decisions / risks
2. citation
3. `transcript_as_fact=false`

## 6. 方向分析使用方式

方向分析必须要求 Hermes 按以下分区输出：

1. Evidence
2. Interpretation
3. Recommendation
4. Risk / Assumption
5. Missing Evidence

硬规则：

1. Recommendation 是辅助建议。
2. 必须人工决策。
3. 无 evidence 的内容放入 Missing Evidence 或 Assumption。
4. `facts_as_answer=false`。

## 7. 人工复核 Checklist

每条输出至少检查：

1. document_id / version_id 是否正确。
2. citation 是否完整。
3. `facts_as_answer=false`。
4. `transcript_as_fact=false`。
5. 是否存在 `contamination_flags`。
6. 是否明确列出 Missing Evidence。
7. partial 是否已标记人工复核。

## 8. 禁止事项

1. 不把 Hermes 输出当最终审标结论。
2. 不把 Hermes 输出当自动经营决策。
3. 不要求 Hermes 自动 repair、delete、cleanup、backfill 或 reindex。
4. 不把 facts 当 retrieval evidence。
5. 不把会议纪要当招标文件条款。
6. 不把内部 Pilot 当 production rollout。
