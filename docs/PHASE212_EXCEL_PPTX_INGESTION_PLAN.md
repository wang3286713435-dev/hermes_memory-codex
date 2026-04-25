# Phase 2.12 Excel / PPTX Ingestion MVP 立项评审

## 1. 阶段定位

Phase 2.12 是 Excel / PPTX ingestion MVP 的立项评审阶段，不是功能实现阶段。

本阶段目标：

1. 先明确依赖治理与 lockfile 策略。
2. 明确 Excel / PPTX 最小解析边界。
3. 明确样本需求、验收 query 与通过标准。
4. 防止在上下文治理刚收口后直接进入不可控的多模态扩展。

## 2. 依赖治理预检

### 2.1 当前依赖状态

当前 `pyproject.toml` 已包含：

- `openpyxl>=3.1.0`
- `python-pptx>=0.6.23`

这说明 Excel / PPTX MVP 的基础 parser 依赖已在项目声明中出现，但 `uv.lock` 当前仍为未跟踪文件。

### 2.2 uv.lock 当前判断

Phase 2.12 前置依赖治理已完成裁决：当前 `uv.lock` 适合作为项目依赖锁定文件纳入基线。

依据：

1. `uv lock --check` 在当前仓库通过，说明 lockfile 与 `pyproject.toml` 可解析一致。
2. lockfile 包含 `openpyxl`、`python-pptx`、dev extras 中的 `pytest` / `ruff` 等项目声明依赖。
3. 内容扫描未发现 token、password、private key 或本地绝对路径。
4. `source = { editable = "." }` 是项目自身 editable 源，属于正常 lockfile 表达。

### 2.3 建议 lockfile 策略

Phase 2.12 后续依赖策略：

1. 正式采用 `uv.lock` 作为当前 Python 依赖基线。
2. 后续新增 Excel / PPTX 解析依赖时，必须先改 `pyproject.toml`，再重新生成并提交 `uv.lock`。
3. lockfile 变更应与依赖变更同批提交，不应混入无关代码。
4. README / runbook 后续应补充 `uv sync` 或等价安装命令。

## 3. Excel Ingestion MVP 边界

### 3.1 最小解析对象

Excel MVP 只覆盖结构化表格文本与引用定位：

- workbook / sheet 名称
- row / column 坐标
- cell range
- 表头识别
- 原始值 / 显示值
- 金额、比例、数量、单位
- 公式文本与公式结果
- 合并单元格的归一化展示
- citation：`file -> sheet -> cell range`

### 3.2 最小输出要求

每个可检索 chunk 至少保留：

- `document_id`
- `sheet_name`
- `cell_range`
- `table_title` 或邻近标题
- `header_path`
- `text`
- `numeric_values`
- `formula_refs`
- `citation_label`

### 3.3 非目标

- 不做复杂 Excel 计算引擎。
- 不保证重算公式。
- 不解析宏。
- 不做跨 workbook 链接追踪。
- 不直接进入结构化 facts 层。

## 4. PPTX Ingestion MVP 边界

### 4.1 最小解析对象

PPTX MVP 只覆盖可审计页面文本与引用定位：

- slide number
- slide title
- body text
- speaker notes
- shape text
- table text
- chart title / chart caption / data label 文本
- image placeholder 信息
- OCR 后置，不在 MVP 实现
- citation：`file -> slide -> shape / notes / chart`

### 4.2 最小输出要求

每个可检索 chunk 至少保留：

- `document_id`
- `slide_number`
- `slide_title`
- `shape_type`
- `shape_name` 或位置描述
- `text`
- `notes_text`
- `chart_caption`
- `citation_label`

### 4.3 非目标

- 不做完整 OCR。
- 不做图片语义理解。
- 不做复杂图表数据还原。
- 不做动画、母版、版式还原。
- 不直接进入结构化 facts 层。

## 5. 样本需求

实现前需要用户提供：

1. 2-3 个真实 Excel：
   - 报价汇总表
   - 进度计划表
   - 付款节点 / 成本测算表
2. 2-3 个真实 PPTX：
   - 项目汇报 PPT
   - 实施方案 PPT
   - 数字化交付 / BIM / CIM 方案 PPT

样本要求：

- 优先脱敏或低敏。
- 文件需允许本地入库与检索验证。
- 每类文件至少包含一个可人工确认的标准答案区域。

## 6. 验收 Query 与通过标准

### 6.1 Excel 验收 Query

1. `报价汇总表中的投标总价是多少？`
2. `请找出安装工程费所在 sheet 和 cell range。`
3. `付款计划表中第 3 期付款比例是多少？`
4. `进度计划表里计划开工日期和计划完工日期是什么？`
5. `哪个表格列出了暂列金额？金额是多少？`
6. `请引用材料单价表中钢筋单价的单元格范围。`
7. `公式单元格 F20 的公式文本是什么？`
8. `哪些 sheet 与报价测算有关？`

通过标准：

- 返回正确 `document_id`。
- 返回正确 `sheet_name`。
- 返回可核验 `cell_range`。
- 答案必须来自 retrieval evidence，不得只来自文件名或历史记忆。

### 6.2 PPTX 验收 Query

1. `项目汇报 PPT 中哪一页介绍总体建设目标？`
2. `哪一页提到 BIM/CIM 平台能力？`
3. `请引用包含实施计划甘特图的 slide。`
4. `第 8 页备注里有哪些交付风险？`
5. `哪一页展示项目组织架构？`
6. `方案 PPT 中哪些页面提到运维服务？`
7. `图表标题中是否出现年度目标？在哪一页？`
8. `请列出与数字化交付标准相关的 slide。`

通过标准：

- 返回正确 `document_id`。
- 返回正确 `slide_number`。
- 返回 slide title / shape / notes 来源。
- citation 能定位到具体 slide，不得只返回整份文件。

## 7. 非目标

Phase 2.12 MVP 不做：

- 完整 OCR。
- 音频 ASR。
- facts 主线。
- 权限大改。
- production rollout。
- retrieval contract 重构。
- memory kernel 主架构重构。

## 8. 建议结论

建议进入 Phase 2.12 MVP 实现前，先完成依赖治理小任务。

若依赖策略明确，Phase 2.12 的实现顺序建议为：

1. Excel parser MVP。
2. Excel citation / retrieval 验收。
3. PPTX parser MVP。
4. PPTX citation / retrieval 验收。
5. 再决定是否进入 OCR 或更复杂多模态能力。
