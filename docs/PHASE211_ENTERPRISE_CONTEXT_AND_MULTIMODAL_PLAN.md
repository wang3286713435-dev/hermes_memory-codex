# Phase 2.11 企业上下文治理与多模态规划

## 1. 阶段定位

Phase 2.11 是 Phase 2.10 之后的规划阶段，不是功能大扩展阶段。

本阶段目标是把企业会话上下文治理、多模态文件摄取、会议音频记忆的架构边界、验收标准和后续实施顺序写清楚，为后续实现提供可审计输入。

## 2. 对齐 PRD / Roadmap / Technical Design

- PRD 要求 Hermes 从文档检索器演进为企业长期记忆系统，但当前仍处于文档知识层与会话作用域能力增强阶段。
- Roadmap 将多模态资料和会议记忆列为 Phase 2 / Phase 3 的后续能力，不应在底座未完全稳定前一次性展开。
- Technical Design 要求多模态能力先进入可审计长期记忆，再进入 Agent 推理；会议、音频和经营分析必须保留来源、转写、决策依据和人工确认边界。

## 3. Phase 2.11 范围

### 3.1 企业会话上下文治理继续增强

规划以下能力，不在本阶段直接大改实现：

- active document scope 从单文件切换扩展到更清晰的任务 / 项目 / 多文件上下文治理。
- 明确当前检索 evidence、历史会话记忆、用户临时指令之间的优先级。
- 继续加强上下文防污染：当前文件、对比文件、历史引用、旧会话摘要必须可区分。
- 规划 trace / audit 字段，用于诊断 scope 变化、证据来源和上下文注入来源。

### 3.2 Excel / PPTX 摄取规划

本阶段只定义架构与验收标准：

- Excel 应保留 sheet、表头、行列坐标、合并单元格、公式、金额、单位和 cell range citation。
- PPTX 应保留 slide number、页面标题、正文、备注、图表说明、图片 OCR 和 slide-level citation。
- 解析结果应进入文档知识层，可检索、可引用、可权限过滤、可评测。

### 3.3 音频与会议记忆规划

本阶段只定义会议记忆闭环，不直接实现：

- 会议音频应先生成可审计转写文本，保留时间戳、发言人、议题和来源文件。
- 决策点、行动项、风险、后续跟进必须支持人工确认后再进入长期记忆。
- 会议记忆应能关联项目、客户、合同、文档和结构化事实，但不得跳过权限和审计。

## 4. 详细设计草案

### 4.1 企业上下文治理

#### 4.1.1 Scope 优先级

1. 当前 turn 显式 `document_id` 或文件标题点名最高优先级。
2. compare scope 高于单一 active document；进入 compare mode 后临时旁路 active document。
3. active document 仅在用户未点名新文件，或明确说 `刚才那份文件` / `当前文件` 时生效。
4. project scope 作为文档集合边界，只能扩大到同一项目内，不得覆盖显式 document scope。
5. history memory 只能作为低优先级上下文提示，不得替代本轮 retrieval evidence。
6. 普通检索只在没有有效 document / compare / project scope 时启用。

#### 4.1.2 防污染规则

- active document 存在时，prompt evidence 只允许同 `document_id`。
- compare scope 存在时，prompt evidence 只允许 compare list 内的 document ids。
- project scope 存在时，prompt evidence 只允许同 `project_id` 且仍需满足权限过滤。
- history memory 必须独立标记为 `history_memory`，不能伪装成本轮检索引用。
- 当标题解析失败且用户未说 `刚才/当前` 时，不得沿用旧 active document。
- 若 retrieval evidence 与 history memory 冲突，默认以本轮检索 evidence 为准，并在 trace 标记冲突。

#### 4.1.3 建议 trace / audit 字段

- `scope_type`: `document` / `compare` / `project` / `unscoped`
- `scope_source`: `explicit_filter` / `title_inference` / `active_document` / `project_context` / `history_memory`
- `active_document_id`
- `compare_document_ids`
- `project_id`
- `returned_document_ids`
- `history_memory_used`
- `scope_conflict_detected`
- `evidence_filtered_out_count`

### 4.2 Excel Ingestion 规划

#### 4.2.1 数据模型草案

- `document`: 原始 Excel 文件、版本、权限、项目、上传人。
- `sheet`: sheet 名称、顺序、可见状态、使用范围。
- `table_region`: 表格区域、标题、表头行、数据范围。
- `cell_range`: 起止单元格、原始值、显示值、数据类型。
- `formula`: 公式文本、引用区域、计算值、失败状态。
- `numeric_value`: 金额、比例、数量、单位、币种。
- `citation`: `file -> sheet -> cell_range`，例如 `报价表.xlsx / 清单汇总 / B12:D18`。

#### 4.2.2 验收 query 样本

1. `报价汇总表中的投标总价是多少？`
2. `清单明细里土建工程费对应哪个单元格范围？`
3. `请引用材料单价表中钢筋单价的 sheet 和 cell range。`
4. `付款计划表里第 3 期付款比例是多少？`
5. `公式单元格 F20 是怎么计算出来的？`
6. `最高限价表中安装工程费和暂列金额分别是多少？`
7. `找出金额单位为万元的所有合计项。`
8. `这个 Excel 中哪些 sheet 与报价测算有关？`

### 4.3 PPTX Ingestion 规划

#### 4.3.1 数据模型草案

- `document`: 原始 PPTX 文件、版本、权限、项目、上传人。
- `slide`: slide number、标题、版式、备注、缩略图引用。
- `shape`: 文本框、表格、图片、图表、SmartArt、位置与层级。
- `notes`: 演讲者备注、页码、段落。
- `chart`: 图表标题、系列、坐标轴、数据标签。
- `image_ocr`: 图片 OCR 文本、置信度、区域位置。
- `citation`: `file -> slide -> shape/notes/chart/image region`。

#### 4.3.2 验收 query 样本

1. `第 5 页的项目架构图表达了什么？`
2. `方案 PPT 中哪里提到 BIM/CIM 平台能力？`
3. `请引用包含实施计划甘特图的 slide。`
4. `第 8 页备注里有哪些交付风险？`
5. `哪一页展示了客户案例列表？`
6. `图表中 2025 年收入目标是多少？`
7. `图片 OCR 中是否出现“数字化交付标准”？`
8. `请列出 PPT 中所有与运维服务有关的页面。`

### 4.4 Meeting Audio Memory 规划

#### 4.4.1 处理链路草案

1. 上传会议音频或转写文本。
2. 生成可审计 transcript，保留 timestamp、speaker、source file。
3. 切分议题，标记议题开始/结束时间。
4. 抽取决策点、行动项、风险、待确认事项。
5. 进入人工确认队列。
6. 仅将人工确认后的内容写入长期记忆或结构化事实层。
7. 与项目、客户、合同、文档建立关联。

#### 4.4.2 写入边界

- 未确认 transcript 可检索但必须标记为 `unverified_transcript`。
- 决策、行动项、风险在人工确认前不得作为确定事实回答。
- speaker attribution 低置信度时必须标记 `speaker_uncertain`。
- 会议记忆不能自动替代审批、法务、财务或投标最终决策。

#### 4.4.3 验收 query 样本

1. `上周项目例会决定了哪些事项？`
2. `谁负责跟进数字化交付标准的确认？`
3. `会议中提到的最大风险是什么？请引用时间戳。`
4. `关于付款节点，会议里有哪些待确认问题？`
5. `列出本次会议的行动项、负责人和截止时间。`
6. `客户在会议中是否确认了 BIM 应用范围？`
7. `哪些会议结论还没有人工确认？`
8. `把这次会议和对应招标文件中的工期要求关联起来。`

## 5. 非目标

- 不实现完整 multimodal ingestion。
- 不改 retrieval contract。
- 不改 memory kernel 主架构。
- 不推进 dense ingestion 主线。
- 不实现 facts、权限大改、OCR、完整会议记忆、完整 AI 审标自动化或生产级 rollout。

## 6. 最小验收标准

### 6.1 企业上下文治理

- 能明确区分 active document、multi-document compare、历史会话记忆和当前检索 evidence。
- 能定义上下文污染判定规则：错误文件、第三方文件、旧会话内容替代本轮检索均应可诊断。
- 能列出后续实现所需 trace 字段和测试场景。

### 6.2 Excel / PPTX

- 完成数据模型草案：source document、sheet/slide、block、cell/shape、citation location。
- 完成 parser provider 选择标准和失败降级策略。
- 完成 5-10 条代表性验收 query 设计。

### 6.3 会议音频

- 完成会议音频处理链路草案：上传、转写、说话人、议题、决策、行动项、人工确认、写入长期记忆。
- 完成 timestamp citation 和 speaker attribution 的验收定义。
- 完成会议记忆不得直接替代人工决策的边界说明。

## 7. 当前阶段判断

Phase 2.11 详细设计与验收样本已具备进入评审的基础，但仍不建议直接开始完整实现。

下一步建议先评审 MVP 边界：优先选择企业上下文治理增强或 Excel/PPTX ingestion MVP 中的一个最小切口，避免同时展开多模态、会议记忆和权限治理。

## 8. MVP 最小切口评审

### 8.1 候选切口 A：企业上下文治理增强

建议优先选择 A。

原因：

- 多模态接入前必须先降低上下文污染风险；否则 Excel、PPTX、会议转写进入后，会放大错误文件、旧记忆、跨项目 evidence 混入问题。
- Phase 2.10 只解决了 document scope，包括 active document、文件切换和 A/B compare；尚未解决 project scope、task scope、history memory、本轮 retrieval evidence 的完整优先级。
- 企业 Agent 长期能力依赖上下文治理底座；没有稳定 scope / evidence / history 优先级，多模态 ingestion 只会增加数据复杂度，而不能提升可信回答能力。

### 8.2 候选切口 B：Excel/PPTX ingestion MVP

暂不建议优先选择 B。

原因：

- Excel/PPTX 需要新增 parser、结构化块、引用位置和失败降级，实施面更大。
- 当前文档和会话上下文治理仍未覆盖 project/task/history/evidence 优先级。
- 若先接入多模态文件，容易把检索污染、历史记忆污染和引用不清晰问题扩大到更多文件类型。

## 9. Phase 2.11a 最小实现边界

### 9.1 目标

Phase 2.11a 只做企业上下文治理增强，不做多模态 parser。

### 9.2 Scope 优先级

1. 显式 `document_id` / 明确文件标题。
2. compare scope。
3. active document。
4. project scope。
5. task scope。
6. history memory。
7. 普通 retrieval。

### 9.3 最小能力

- 增加 project scope / task scope 的轻量状态表达，不改变 retrieval contract。
- 明确 active document、compare scope、project scope、task scope 的冲突处理。
- 增加 evidence source trace，区分 `retrieval_evidence`、`history_memory`、`plugin_context`、`user_instruction`。
- 明确 history memory 不得替代本轮 retrieval evidence。
- 增加上下文污染诊断规则：错误 document、错误 project、第三方 compare 文件、旧会话记忆替代本轮 retrieval evidence。

### 9.4 Phase 2.11a 非目标

- 不实现 Excel/PPTX parser。
- 不实现 OCR / ASR。
- 不推进 facts、权限大改或 rollout。
- 不改 retrieval contract。
- 不改 memory kernel 主架构。
