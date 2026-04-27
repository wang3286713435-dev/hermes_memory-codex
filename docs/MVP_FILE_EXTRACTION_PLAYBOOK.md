# MVP File Extraction Playbook

## 1. 适用范围

用于内部试运行阶段的企业文件内容提取与引用定位。

覆盖：

1. 标书 / PDF / Word。
2. Excel。
3. PPTX。
4. 会议纪要 / transcript。
5. 两文件对比。

## 2. 标书 / PDF / Word 模板

```text
围绕 @目标文件，提取【目标内容】。
请返回：
- 结论
- document_id
- version_id
- citation / chunk 信息
- 是否缺 evidence
```

## 3. Excel 模板

```text
围绕 @Excel文件，查询【设备 / 金额 / 单位 / 清单项】。
请返回：
- sheet_name
- cell_range，若没有则返回 row / column 降级说明
- document_id
- version_id
- 结论
```

## 4. PPTX 模板

```text
围绕 @PPT文件，提取【方案要点 / 指定页内容】。
请返回：
- slide_number
- slide_title
- document_id
- version_id
- 结论
```

## 5. 会议纪要模板

```text
围绕 @会议纪要，提取行动项、决策、风险。
请返回：
- action items / decisions / risks
- evidence / citation
- transcript_as_fact=false
- 不得把会议纪要标为 confirmed fact
```

## 6. 对比模板

```text
对比 @文件A 和 @文件B 的差异。
请分别列出两份文件的 evidence。
不得混入第三份文件。
请返回 compare_document_ids、retrieval_evidence_document_ids、contamination_flags。
```

## 7. 防污染规则

1. 单文件查询只允许目标 document_id evidence。
2. A/B compare 只允许 A/B 两份文件 evidence。
3. missing alias 时必须 suppress retrieval，不得回退旧 active document。
4. 无 evidence 时必须明确 no_current_retrieval_evidence。
