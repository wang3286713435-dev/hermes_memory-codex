# Phase 2.30a Practical MVP Pilot Plan

## 1. 目标

Phase 2.30a 目标是把已有企业长期记忆能力整理成公司内部受控 MVP Pilot Pack。

本阶段重点不是继续堆治理功能，而是让真实同事可以在人工监督下使用 Hermes 完成三类高价值任务：

1. 标书审查 / 风险提取。
2. 企业文件内容提取与引用定位。
3. 基于公司资料的未来发展方向辅助分析。

## 2. MVP 定义

本 MVP 是：

1. 公司内部受控试运行版本。
2. 人工监督的企业文件 Agent。
3. 可用于审查标书、提取文件内容、辅助公司方向分析。
4. 所有结论必须带 retrieval evidence / citation / source reference。
5. 默认不自动决策，不自动修复数据，不进入 production rollout。

本 MVP 不是：

1. 生产级全面发布。
2. 自动审标系统。
3. 自动经营决策系统。
4. repair executor。
5. facts 自动抽取或 facts 替代 retrieval evidence。
6. 完整 RBAC / ABAC / SSO。

## 3. Pilot 使用角色

建议首轮只面向小范围内部用户：

1. 投标 / 商务人员：审查标书、合同风险与投标资格。
2. 技术 / 方案人员：提取方案、清单、交付标准与 PPTX 内容。
3. 管理层 / 项目负责人：基于会议纪要、方案、标书、清单和 confirmed facts 做方向辅助分析。

所有用户必须理解：Hermes 输出是辅助判断，最终结论需人工确认。

## 4. 三个 Pilot 场景

### 4.1 标书审查 / 风险提取

目标：

1. 快速提取项目基础信息。
2. 快速定位投标资格要求。
3. 快速发现商务 / 合同风险。
4. 明确缺失 evidence 的事项。

必须输出：

1. 结论。
2. 证据来源。
3. 风险等级。
4. 待人工确认项。

### 4.2 文件内容提取与引用定位

目标：

1. 对 PDF / Word / 标书返回 document_id 与 chunk citation。
2. 对 Excel 返回 sheet_name 与 cell_range / row / column。
3. 对 PPTX 返回 slide_number 与 slide_title。
4. 对会议纪要返回 action items / decisions / risks，且 `transcript_as_fact=false`。
5. 对比两个文件时不混入第三份文件。

### 4.3 公司未来发展方向辅助分析

目标：

1. 从会议纪要、PPT、Excel、标书、confirmed facts 中提取可引用 evidence。
2. 区分 Evidence、Interpretation、Recommendation、Risk / Assumption、Missing Evidence。
3. 给出辅助建议，但明确需要人工决策。

硬规则：

1. confirmed facts 只能作为辅助上下文。
2. `facts_as_answer=false` 必须保持。
3. 没有 retrieval evidence 时不得凭 facts 或历史记忆作答。
4. 发展方向建议必须标明“辅助建议，需人工决策”。

## 5. Pilot 验收 Query 清单

建议首轮真实终端验收覆盖 12 条：

1. 围绕 `@主标书` 提取工程名称、工程地点、建设单位、代建单位、工期、最高投标限价。
2. 围绕 `@主标书` 提取投标资质、项目经理、联合体、业绩和人员要求。
3. 围绕 `@主标书` 提取付款、质保、工期、违约、结算、变更、索赔风险。
4. 围绕 `@主标书` 查询一个不存在或未召回的风险点，要求输出“未在当前召回中找到”。
5. 围绕 Excel 清单查询指定设备 / 金额 / 单位，要求返回 sheet_name 与 cell_range。
6. 围绕 PPTX 查询方案第一页或指定主题，要求返回 slide_number 与 slide_title。
7. 围绕 `@会议纪要` 提取行动项。
8. 围绕 `@会议纪要` 提取决策。
9. 围绕 `@会议纪要` 提取风险，并确认 `transcript_as_fact=false`。
10. 对比 `@会议纪要` 与 `@主标书`，确认 evidence 同时来自两份文件且无第三文件。
11. 查询 confirmed facts 辅助上下文，确认 `facts_as_answer=false` 且不替代 retrieval evidence。
12. 要求 Hermes 基于现有资料给出公司未来发展方向辅助分析，并按 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分区。

## 6. Codex C 真实终端验收要求

Codex C 复验时应回传：

1. API health / CLI 可用性。
2. 每条 query 的 document_id / version_id。
3. citation 字段。
4. `facts_as_answer`。
5. `transcript_as_fact`。
6. `contamination_flags`。
7. 是否存在 no_current_retrieval_evidence。
8. 是否出现无关文档混入。
9. 是否出现 facts 替代 retrieval evidence。

通过标准：

1. 关键查询必须有 retrieval evidence 或明确缺 evidence。
2. facts 不得作为最终答案来源。
3. meeting transcript 不得被标为 fact。
4. 文件对比不得混入第三份文件。
5. Excel / PPTX 必须展示结构化 citation。

失败标准：

1. 无 evidence 仍给确定结论。
2. facts_as_answer 为 true。
3. transcript_as_fact 为 true。
4. compare 场景混入第三份文件。
5. Excel / PPTX citation 缺失。

## 7. Pilot 操作边界

允许：

1. 内部试用。
2. 手动上传 / 绑定 alias。
3. 手动执行 Hermes CLI / API query。
4. 人工检查 citation 与 evidence。
5. 记录问题和改进项。

禁止：

1. production rollout。
2. repair executor。
3. 自动修改 facts / versions / indexes。
4. facts 自动抽取。
5. facts 替代 retrieval evidence。
6. 默认扫描真实 reports / reviews。
7. 生产 cron / scheduler。

## 8. 规划结论

Phase 2.30a 可以进入内部 MVP Pilot Pack review。

建议下一步：

1. Codex B 审核 pilot pack 文档。
2. Codex C 按 12 条 query 做真实终端抽样验收。
3. 验收通过后再做 Phase 2.30a docs baseline。

当前不建议直接进入 production rollout。
