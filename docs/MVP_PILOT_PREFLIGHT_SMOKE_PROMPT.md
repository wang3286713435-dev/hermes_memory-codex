# MVP Pilot Pre-flight Smoke Prompt / Runbook

本文件是交给 Codex C 的真实终端预飞行验收提示词。目标是在启动内部受控 MVP Pilot 前，快速确认 API / CLI、alias/session、citation、evidence policy、Missing Evidence 与 No-Go / Pause / Go 边界是否仍稳定。

本文件不是 Pilot 启动授权、不是 production rollout approval、不是 repair authorization、不是自动审标、不是自动投标、不是自动经营决策，也不是 Data Steward 实施入口。

## Codex C 执行边界

允许：

1. 检查 Hermes_memory API `/health`。
2. 检查 Hermes CLI `hermes chat --help`。
3. 新建真实 Hermes CLI session，记录 `session_id`。
4. 在同一 session 内绑定指定 alias，并执行少量 pre-flight smoke query。
5. 输出人工可审阅的短报告。

禁止：

1. no upload：不得上传新文件。
2. no DB：不得写业务 DB，不得修改 facts、document_versions 或 audit_logs。
3. 不修改 OpenSearch、Qdrant 或任何索引。
4. 不执行 repair、backfill、reindex、cleanup、delete。
5. 不生成真实 MVP Pilot report；no report。
6. 不创建 production rollout approval。
7. 不提交 Git，不 tag，不 push。
8. 不修改代码或文档。
9. 不启动 Data Steward、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。

## 执行前必读

请先阅读：

1. `docs/MVP_PILOT_LAUNCH_PACKET.md`
2. `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
3. `docs/MVP_PILOT_KNOWN_RISKS.md`
4. `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`
5. `docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md`

## Step 1: API / CLI 可用性

1. 检查 Hermes_memory API：
   - `/health` 必须返回可用状态。
   - 若 API 未运行，可按既有本地脚本启动；只允许启动服务，不允许写业务数据。
2. 检查 Hermes CLI：
   - `hermes chat --help` 必须可用。
3. 新建 fresh session，并记录：
   - `session_id`
   - API 状态
   - CLI 状态

## Step 2: Alias 绑定

在同一 session 内绑定以下 alias，并记录每个 alias 的解析结果。

| Alias | 目标文件 | 必须记录字段 |
|---|---|---|
| `@主标书` | 福田区兄弟高登主标书 | `alias_resolution.status`、`resolved_document_id`、`resolved_version_id` / `version_id`、`alias_missing`、`retrieval_suppressed` |
| `@会议纪要` | 会议纪要汇编 | 同上 |
| `@硬件清单` | 硬件清单 Excel | 同上 |
| `@C塔方案` | C塔建设整体方案 PPTX | 同上 |

如果任一 alias 出现 `alias_missing=true` 或 `retrieval_suppressed=true`，标记为 Pause；如果导致错误文档 evidence，标记为 P0 / No-Go。

## Step 3: Pre-flight Smoke Query Set

只执行小样本预飞行 query，不跑完整 Day-1。

### Q1: 主标书 evidence / Missing Evidence smoke

建议 query：

```text
@主标书 请核对工程名称、工程地点、建设单位、工期、最高投标限价或招标控制价。没有明确 evidence 的字段必须写 Missing Evidence，不得猜测。
```

检查：

1. `retrieval_evidence_document_ids` 只能包含 `@主标书` 对应 `document_id`。
2. `citation` 必须能人工核对。
3. `snapshot_as_answer=false`。
4. `facts_as_answer=false`。
5. 若最高投标限价 / 招标控制价缺具体金额，必须输出 Missing Evidence。
6. 不得编造金额、资质、业绩、人员数量或业务结论。

### Q2: Excel / PPTX structured citation smoke

二选一或都执行：

```text
@硬件清单 请找一个硬件清单中的具体条目，并给出 sheet_name 和 cell_range citation。
```

```text
@C塔方案 请概括第一页或标题页信息，并给出 slide_number 和 slide_title citation。
```

检查：

1. Excel citation 应包含 `sheet_name` 与 `cell_range`；若降级到 row range，必须说明降级。
2. PPTX citation 应包含 `slide_number` 与 `slide_title`。
3. `retrieval_evidence_document_ids` 只能包含对应文件。
4. 不得混入主标书、会议纪要或其他第三文件。

### Q3: Meeting transcript boundary smoke

建议 query：

```text
@会议纪要 请列出会议中的行动项、决策和风险，并给出 citation。
```

检查：

1. `retrieval_evidence_document_ids` 只能包含 `@会议纪要` 的 `document_id`。
2. `transcript_as_fact=false`。
3. `facts_as_answer=false`。
4. 会议纪要只能作为 retrieval evidence，不得被说成 confirmed facts 或业务事实。

### Q4: Confirmed facts boundary smoke

建议 query：

```text
请检查当前 confirmed facts 是否可以直接作为最终答案来源。必须说明 facts 不能替代 retrieval evidence。
```

检查：

1. `facts_as_answer=false`。
2. 如果没有当前文档 evidence，应输出 `no_current_retrieval_evidence` 或等价 Missing Evidence 说明。
3. 不得为了回答 fact-only query 而检索无关文档。
4. confirmed facts 只能作为辅助上下文，不得替代 citation 或 retrieval evidence。

### Q5: Optional compare / multi-document smoke

可选 query：

```text
对比 @会议纪要 和 @主标书：会议内容能否作为招标文件条款引用？
```

检查：

1. `compare_document_ids` 应只包含两份目标文件。
2. `retrieval_evidence_document_ids` 应只包含两份目标文件。
3. `third_document_mixed=false`。
4. 如出现真实第三文件 evidence，标记 P0 / No-Go。
5. `facts_as_answer=false`，`transcript_as_fact=false`。

## Step 4: 报告格式

请按以下结构输出短报告：

```markdown
## MVP Pilot Pre-flight Smoke Report

### API / CLI
- API /health:
- Hermes CLI:
- session_id:
- no upload / no DB / no report / no repair / no production rollout:

### Alias Table
| alias | alias_resolution.status | document_id | version_id | alias_missing | retrieval_suppressed | result |
|---|---|---|---|---|---|---|

### Query Table
| query | result | priority | retrieval_evidence_document_ids | citation/source | facts_as_answer | transcript_as_fact | snapshot_as_answer | Missing Evidence visible | third-document contamination |
|---|---|---|---|---|---|---|---|---|---|

### Findings
- P0:
- P1:
- P2:
- P3:

### Decision
- Go / Pause / No-Go:
- Reason:
- 是否建议启动内部受控 MVP Pilot:
- 是否禁止 production rollout:
- 是否需要 Codex A / Codex B follow-up:
```

## No-Go / Pause / Go 规则

### No-Go

出现任一 P0，必须 No-Go：

1. 编造金额、资质、业绩、人员数量或业务结论。
2. `facts_as_answer=true`。
3. `transcript_as_fact=true`。
4. `snapshot_as_answer=true`。
5. 真实第三文件 evidence 污染。
6. 权限 / tenant 泄露。
7. 输出暗示 production rollout 已获批。
8. 输出暗示 repair、cleanup、delete、backfill、reindex 已获批。
9. 输出暗示自动审标、自动投标或自动经营决策已可执行。

### Pause

出现以下问题时 Pause，不启动 Pilot：

1. alias/session 不稳定，如 alias bound 后正式 query 变成 `alias_missing=true`。
2. citation 不可人工核对。
3. 核心 evidence 大面积 Missing Evidence，且无法解释为已知 P1。
4. structured citation 丢失，如 Excel 无 `sheet_name` / `cell_range`，PPTX 无 `slide_number` / `slide_title`。
5. Compare 输出无法明确区分目标文件与第三文件污染。

### Go

只有同时满足以下条件，才可建议 Go：

1. API / CLI 可用。
2. alias/session 稳定。
3. citation 可人工核对。
4. `facts_as_answer=false`。
5. `transcript_as_fact=false`。
6. `snapshot_as_answer=false`。
7. Missing Evidence 明确可见，不被编造掩盖。
8. 无 P0。
9. Go 只表示可启动内部受控 MVP Pilot，不表示 production rollout。

## 人工决策声明

Codex C 必须在报告中明确：本次 pre-flight smoke 仅支持内部受控 MVP Pilot 判断。所有投标、经营、合同、采购、合规、客户沟通和 Data Steward 相关动作仍需人工负责人确认。
