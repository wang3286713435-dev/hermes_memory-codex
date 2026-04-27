# MVP Strategy Analysis Playbook

## 1. 适用范围

用于内部试运行阶段的公司未来发展方向辅助分析。

该能力只做辅助建议，不做自动决策。

## 2. 强制输出格式

每次分析必须按以下结构输出：

1. Evidence
2. Interpretation
3. Recommendation
4. Risk / Assumption
5. Missing Evidence

## 3. Evidence

Evidence 只能来自：

1. 会议纪要 retrieval evidence。
2. PPTX / 方案文档 citation。
3. Excel / 清单 citation。
4. 标书 / 项目资料 citation。
5. confirmed facts auxiliary context，但必须保留 source_document_id / source_version_id / source_chunk_id。

## 4. Interpretation

Interpretation 是基于 evidence 的分析。

必须写清：

1. 哪些判断直接来自 evidence。
2. 哪些判断是推断。
3. 推断的不确定性。

## 5. Recommendation

Recommendation 必须标明：

1. 这是辅助建议。
2. 需人工决策。
3. 不应自动执行。

## 6. Risk / Assumption

至少列出：

1. evidence 覆盖不足风险。
2. 旧版本资料风险。
3. 会议纪要只是 retrieval evidence，不等于 confirmed fact。
4. confirmed facts 可能存在 stale_source_version。

## 7. Missing Evidence

必须列出还需要补充的资料，例如：

1. 最新经营数据。
2. 客户反馈。
3. 项目交付复盘。
4. 市场竞品信息。
5. 财务 / 成本测算。

## 8. 示例 Prompt

```text
请基于 @会议纪要、@主标书、相关 PPTX 和 confirmed facts，分析公司未来 6-12 个月可以优先投入的方向。
必须按 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分区。
facts_as_answer 必须为 false。
没有 retrieval evidence 的结论请放入 Missing Evidence 或 Assumption，不要当作事实。
```

## 9. 硬规则

1. facts 不得直接作为 final answer。
2. `facts_as_answer=false`。
3. 没有 retrieval evidence 时不得凭 facts 或历史记忆作答。
4. 发展方向建议必须标明“辅助建议，需人工决策”。
