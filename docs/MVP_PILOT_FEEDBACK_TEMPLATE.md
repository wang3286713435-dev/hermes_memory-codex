# MVP Pilot Feedback Template

## 1. 基础信息

- 日期：
- 使用人：
- 人工复核人：
- 记录人：
- Hermes session_id：
- 使用场景：
  - 标书审查 / 风险提取
  - 文件内容提取与 citation 定位
  - 公司未来发展方向辅助分析
  - 其他：

## 2. Query 记录

- query 原文：
- 期望答案：
- 实际答案摘要：
- document_id：
- version_id：
- citation 是否完整：是 / 否 / 部分
- 结构化 citation：
  - chunk_id：
  - sheet_name：
  - cell_range：
  - slide_number：
  - slide_title：

## 3. 结果判定

- 结果：pass / partial / fail
- partial / fail 原因：
- 是否存在 Missing Evidence：是 / 否
- 是否需要人工复核：是 / 否
- 是否已人工复核：是 / 否

## 4. Trace / 边界字段

- alias_resolution：
- retrieval_evidence_document_ids：
- compare_document_ids：
- contamination_flags：
- facts_as_answer：
- transcript_as_fact：
- no_current_retrieval_evidence：

## 5. 问题类型

可多选：

1. alias/session
2. retrieval recall
3. citation
4. contamination
5. facts boundary
6. transcript boundary
7. UX / prompt
8. latency / runtime
9. other

## 6. 业务影响

- 影响等级：高 / 中 / 低
- 影响说明：
- 是否阻塞当前业务使用：是 / 否

## 7. 建议优先级

- 优先级：P0 / P1 / P2 / P3
- 建议下一步：
- 是否需要 Codex B review：是 / 否
- 是否需要 Codex C 复验：是 / 否

## 8. 记录原则

1. partial 必须记录，不得当作 pass。
2. Missing Evidence 必须保留。
3. 业务建议必须标记“需人工决策”。
4. 不在反馈表中要求自动修复数据。
