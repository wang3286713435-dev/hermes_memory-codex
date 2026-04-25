# Phase 2.14 企业记忆回归评测集与自动化验收规划

## 1. 目标

Phase 2.14 目标是把 Phase 2.10-2.13 已通过的真实终端验收沉淀为可重复执行的回归评测集。

本阶段只规划自动化验收体系，不进入原始音频 ASR、不进入生产级 rollout、不改 retrieval contract、不改 memory kernel 主架构。

## 2. 覆盖能力

评测集先覆盖已完成能力：

1. 单文件锁定：明确文件标题或 document_id 后，只返回目标文件 evidence。
2. 同会话 A/B/A 文件切换：同一 session 内从 A 切到 B，再切回 A，不依赖新开会话。
3. file alias：覆盖 alias 绑定、使用、rebind 诊断、missing suppress retrieval。
4. A/B compare：允许两份目标文件 evidence，禁止第三份文件混入。
5. tender metadata snapshot：基础信息 query 可用 snapshot 导航，但 `snapshot_as_answer=false`。
6. Excel structured citation：返回 `sheet_name` 与 `cell_range`，缺 cell_range 时明确 fallback。
7. PPTX structured citation：返回 `slide_number` 与 `slide_title`。
8. meeting transcript：行动项、决策、风险可召回，`transcript_as_fact=false`。
9. history memory policy：历史记忆可作提示，但不得替代本轮 retrieval evidence。

## 3. 样本来源

优先使用现有真实样本池：

1. 六文件上下文治理真实池：主标书、对比标书、答疑文件、旧版交付标准、新版交付标准、会议纪要。
2. Excel 真实样本：报价表、硬件清单、结算表。
3. PPTX 真实样本：建设方案、智慧建筑脑机、数字化交付平台方案。
4. 会议纪要样本：`会议纪要汇编 (2)`。

如未来新增样本，必须先记录 title、document_id、version_id、chunk_count、document_type/source_type 与索引状态。

## 4. 评测用例分组

### 4.1 Document Scope

- 单文件标题锁定主标书。
- 同会话 `主标书 -> 交付标准 -> 主标书` 切换。
- “刚才那份文件 / 当前文件”沿用 active document。
- 标题解析失败时不得默认复用旧 active document。

### 4.2 File Alias

- `@主标书` 绑定并 scoped retrieval。
- `@会议纪要` 绑定并 scoped retrieval。
- missing alias 必须 `suppress_retrieval=true`。
- rebind alias 必须可诊断。

### 4.3 Compare 与防污染

- `@主标书` vs `@交付标准`：returned document ids 仅包含两份目标文件。
- `@会议纪要` vs `@主标书`：会议 evidence 与标书 evidence 可同时存在，但会议内容不得被当作标书条款。
- 两份大型标书对比不得混入交付标准或会议纪要。

### 4.4 Structured Citation

- Excel query 必须命中目标 Excel document_id，并返回 `sheet_name` / `cell_range`。
- PPTX query 必须命中目标 PPTX document_id，并返回 `slide_number` / `slide_title`。

### 4.5 Evidence Policy

- tender metadata snapshot 场景必须 `snapshot_as_answer=false`。
- meeting transcript 场景必须 `transcript_as_fact=false`。
- history memory 场景必须 `history_memory_as_evidence=false`。
- 本轮 retrieval 为空时必须暴露 `no_current_retrieval_evidence`，不得由历史记忆补 citation。

## 5. 指标设计

每条评测用例至少输出：

1. `case_id`
2. `prompt`
3. `pass/fail`
4. `expected_document_ids`
5. `returned_document_ids`
6. `retrieval_evidence_document_ids`
7. `citation_fields_present`
8. `contamination_flags`
9. `evidence_policy_flags`
10. `alias_resolution.status`
11. `metadata_snapshot_used`
12. `snapshot_as_answer`
13. `meeting_transcript_used`
14. `transcript_as_fact`
15. `history_memory_as_evidence`
16. `latency_ms`

失败结果必须记录最小失败原因，例如：`missing_expected_document_id`、`unexpected_document_id`、`missing_structured_citation`、`snapshot_used_as_answer`、`transcript_used_as_fact`、`history_memory_substituted_evidence`。

## 6. 执行方式评审

### A. API-level deterministic eval

优点：

- 可直接断言 trace、document_id、citation metadata 与 latency。
- 适合作为 CI / 本地回归基础。
- 对 LLM 表述不敏感，误差更小。

不足：

- 不能完全覆盖 Hermes CLI 的 prompt 注入、alias 会话状态与最终回答展示。

### B. Hermes CLI black-box eval

优点：

- 更接近真实用户终端体验。
- 能发现 context 注入、答案格式、模型误读 trace 等问题。

不足：

- 依赖模型输出，稳定性与成本较差。
- 自动判定难度更高，不适合作为大规模基础回归。

### C. 两者结合

推荐顺序：

1. 先实现 API-level deterministic eval，覆盖主干能力与核心 trace。
2. 再补少量 Hermes CLI smoke，覆盖 alias 会话流、A/B compare、structured citation 展示、meeting transcript 非 fact 语义。

## 7. 最小实现边界

Phase 2.14 最小实现建议包括：

1. 新增评测用例配置文件，记录 prompt、filters、expected ids、expected trace flags。
2. 新增 API-level eval runner，调用 Hermes_memory retrieval 或 Hermes memory kernel 可控入口。
3. 输出 JSON / Markdown 评测报告。
4. 支持按 case group 运行：document_scope、alias、compare、structured_citation、meeting、evidence_policy。
5. CLI smoke 只保留 3-5 条高价值真实终端用例。

## 8. 非目标

Phase 2.14 不做：

1. 原始音频 ASR。
2. OCR。
3. facts 写入。
4. 权限治理大改。
5. 生产级 rollout。
6. retrieval contract 重构。
7. memory kernel 主架构重构。

## 9. 规划结论

建议开始 Phase 2.14 最小实现。

优先实现 API-level deterministic eval，再补少量 Hermes CLI smoke。这样可以把当前越来越重的人工终端验收转化为可重复、可审计、可自动对比的回归证据，同时避免过早进入 rollout 或多模态大扩展。

## 10. 最小实现结果

Phase 2.14 API-level deterministic eval runner 已完成首轮最小实现：

1. 新增 `scripts/phase214_regression_eval.py`。
2. 支持内置 Python list eval cases。
3. 每个 case 覆盖 `id`、`query`、`filters`、`expected_document_ids`、`forbidden_document_ids`、`required_trace_flags`、`required_citation_fields`。
4. 直接调用 `RetrievalService`，用于本地 / CI 可重复回归；不依赖 Hermes CLI 黑盒。
5. 输出 JSON summary，包含 total、passed、failed、skipped、latency p50/p95 与逐 case 诊断。
6. 依赖检查会明确区分 DB 与 OpenSearch 不可用层级。

### 10.1 首轮内置 case

当前内置 `11` 条 case：

1. 主标书基础信息 metadata snapshot。
2. 答疑补遗文件单文件锁定。
3. 附件十一交付标准单文件锁定。
4. 主标书工期 query 防对比标书污染。
5. 对比标书工期 query 防主标书污染。
6. Excel sheet / cell citation。
7. PPTX slide citation。
8. 会议纪要 action item。
9. 会议纪要 decision。
10. 会议纪要 risk。
11. missing alias suppress：标记为 CLI-only skipped，不强行纳入 API eval。

### 10.2 本地运行结果

使用 localhost DB / OpenSearch 环境运行：

- total: `11`
- passed: `10`
- failed: `0`
- skipped: `1`
- skipped case: `missing_alias_suppress_cli_only`
- latency p50 / p95: `74.042 ms / 784.776 ms`

默认环境若指向 Docker 内部 hostname 而本机无法解析，runner 会输出：

- `db=failed`
- `opensearch=failed`
- `errors[].layer=db/opensearch`

### 10.3 限制

1. 当前 runner 覆盖 API-level deterministic eval，不替代 Hermes CLI 会话态 smoke。
2. alias missing / suppress retrieval 属于 Hermes session layer，当前只标记为 CLI-only skipped。
3. 评测依赖既有真实数据已入库，不负责重复上传样本。
