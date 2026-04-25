# Phase 2.13 Meeting Transcript Ingestion MVP 规划

## 1. 阶段定位

Phase 2.13 建议优先做会议纪要 / 转写文本 ingestion MVP。

本阶段不直接进入原始音频 ASR。当前更稳的切口是先处理已经存在的 `.docx` / `.txt` / `.md` 会议纪要或转写文本，把会议类资料纳入可检索、可引用、可诊断的企业记忆链路。

## 2. Phase 2.12 后置核对结论

Hermes 主仓库 Phase 2.12 baseline 已在当前有效备份远端固化：

- 主仓库 `origin` 指向 `https://github.com/NousResearch/hermes-agent.git`，属于上游开源仓库。
- 本地向 `origin` 推送失败的直接原因是 GitHub HTTPS 凭证不可读：`could not read Username for 'https://github.com': Device not configured`。
- 主仓库 `backup2` 指向 `git@github.com:wang3286713435-dev/hermes_repo.git`，是当前可写备份远端。
- `backup2` 上已存在 Phase 2.12 baseline 分支与 tag，均指向 `2f9e623a`：
  - branch: `codex/phase-2.11d-context-regression-baseline`
  - tag: `phase-2.12-structured-file-ingestion-baseline`

因此当前不需要为了 Phase 2.12 单独补 primary remote 对齐；继续把 `backup2` 视为当前有效可回滚基线即可。若后续要对齐 `origin`，应单独处理 GitHub upstream / fork / credential 策略，不应混入功能阶段。

## 3. MVP 范围

### 3.1 输入文件类型

Phase 2.13 MVP 只覆盖文本化会议资料：

- `.docx` 会议纪要。
- `.txt` 会议转写文本。
- `.md` / markdown 会议记录。

### 3.2 最小解析对象

每份会议资料至少尝试抽取：

- `meeting_title`
- `meeting_date`
- `attendees`
- `speaker`
- `timestamp`
- `agenda`
- `decision`
- `action_item`
- `owner`
- `due_date`
- `risk`
- `open_question`

### 3.3 Citation 要求

会议类 chunk 必须保留可审计引用位置：

- 文件标题 / `document_id`
- chunk id
- speaker
- timestamp 或段落范围
- 原文 excerpt
- 若无法识别 timestamp，应明确标记为 `timestamp_missing`

### 3.4 Trace 要求

建议 trace 至少包含：

- `meeting_transcript_used`
- `meeting_fields_matched`
- `speaker_detected`
- `timestamp_detected`
- `action_items_detected`
- `decisions_detected`
- `risks_detected`
- `transcript_as_fact=false`
- `evidence_required=true`

## 4. 非目标

Phase 2.13 MVP 不做：

- 原始音频 ASR。
- speaker diarization 模型接入。
- 完整 facts 主线。
- 权限体系大改。
- 审计系统闭环。
- production rollout。
- retrieval contract 重构。
- memory kernel 主架构重构。

会议资料可以作为 retrieval evidence，但会议结论、行动项、风险在进入结构化事实或长期承诺前仍需要人工确认。

## 5. 样本需求

实现前建议准备 3-5 份低敏或脱敏会议资料：

1. 项目例会纪要 `.docx`。
2. 招投标评审会议纪要 `.docx`。
3. 客户沟通会议转写 `.txt`。
4. 内部技术评审会议记录 `.md`。
5. 包含行动项和负责人表格的会议纪要。

每份样本应至少有一个人工可核验答案，例如明确决策、负责人、截止时间或风险事项。

## 6. 验收 Query 与通过标准

### 6.1 验收 Query

1. `这次会议做出了哪些决策？请引用原文位置。`
2. `谁负责跟进数字化交付标准？截止时间是什么？`
3. `会议中提到的主要风险有哪些？`
4. `客户提出了哪些待确认问题？`
5. `请列出本次会议的行动项、负责人和截止时间。`
6. `某位发言人提到了什么关键意见？`
7. `会议纪要里是否确认了 BIM 应用范围？`
8. `请按议题整理会议结论。`
9. `哪些事项还没有明确负责人？`
10. `把会议行动项与对应项目文件关联起来回答。`

### 6.2 通过标准

- 返回正确 `document_id`。
- 返回正确 meeting chunk。
- citation 能显示 speaker / timestamp / 段落位置。
- action item、decision、risk 不得脱离 retrieval evidence。
- 无 timestamp 时必须诊断为 `timestamp_missing`，不得伪造时间。
- 不得把未确认会议内容写成已确认事实。

## 7. 推荐结论

建议进入 Phase 2.13 最小规划与样本确认。

优先切口为会议纪要 / 转写文本 ingestion MVP，而不是原始音频 ASR。这样可以复用当前文档 ingestion、chunk、OpenSearch、citation 和 Hermes 上层 evidence 治理能力，同时避免过早引入 ASR、说话人分离和音频质量问题。

## 8. 首轮最小实现结果

Phase 2.13 首轮最小实现已完成：

1. 新增轻量会议文本 metadata 提取层，复用现有 `.docx` / `.txt` / `.md` parser，不重写 docx parser。
2. ingestion 时对会议类文档写入 `meeting_transcript` metadata，包含 speaker、timestamp、topic、decision、action_item、owner、deadline、risk、source_location、source_chunk_id、confidence。
3. retrieval 时对历史已入库会议纪要动态补齐 meeting metadata，因此无需重复上传既有真实样本。
4. trace 增加 `meeting_transcript_used`、`meeting_fields_matched`、`speaker_detected`、`timestamp_detected`、`action_items_detected`、`decisions_detected`、`risks_detected`、`transcript_as_fact=false`、`evidence_required=true`。
5. snapshot / metadata 仅作为检索导航与诊断，不替代 retrieval evidence。

### 8.1 真实样本验证

已使用既有真实样本验证，未重复上传：

- title: `会议纪要汇编 (2)`
- document_id: `92051cc6-56b5-4930-bdf0-119163c83a75`
- source_type: `meeting`
- document_type: `meeting`
- chunks: `17`

验证结果：

1. `会议里有哪些行动项？` 命中会议纪要，`meeting_transcript_used=true`，`action_items_detected > 0`。
2. `会议里形成了哪些决策？` 命中会议纪要，`decisions_detected > 0`。
3. `会议中提到哪些风险？` 命中会议纪要问题 / 风险相关 chunk，`risks_detected > 0`。
4. 对比会议纪要与主标书时，会议作用域只返回会议 document_id，主标书作用域只返回主标书 document_id，未出现证据混用。

### 8.2 降级项

1. 本轮不做原始音频 ASR。
2. 不做 speaker diarization 模型，仅基于文本模式识别 speaker。
3. 未将会议结论写入 facts；`transcript_as_fact=false`。
4. 对历史已入库会议纪要采用 retrieval-time metadata 动态补齐，不做数据迁移。

## 9. 真实终端 trace 语义修正

Phase 2.13 真实终端验收曾发现：会议纪要检索 evidence 可用，但输出中多次出现 `transcript_as_fact=true`。

当前已修正为：

1. `meeting_transcript_used=true` 只表示本轮 retrieval 命中了会议纪要 / 转写文本 evidence。
2. `transcript_as_fact` 必须恒为 `false`，行动项、决策、风险命中不会改变该语义。
3. 会议纪要 answer evidence 必须来自 `retrieval_evidence_document_ids` / `meeting_source_chunk_ids` 对应 chunk。
4. 会议纪要内容进入 facts 或长期承诺前仍需人工确认；本阶段不做 facts 写入。

## 10. 真实终端验收收口

Phase 2.13 真实终端复验已通过：

1. `@主标书` 绑定通过，`document_id=869d4684-0a98-4825-bc72-ada65c15cfc9`，retrieval evidence 仅来自主标书，`contamination_flags=[]`。
2. `@会议纪要` 绑定通过，`document_id=92051cc6-56b5-4930-bdf0-119163c83a75`，`meeting_transcript_used=true`、`transcript_as_fact=false`、`evidence_required=true`。
3. 行动项 / 决策 / 风险提取通过：`action_items_detected=4`、`decisions_detected=3`、`risks_detected=2`，且 `transcript_as_fact=false`。
4. `@会议纪要` 与 `@主标书` 对比通过，`compare_document_ids` 同时包含会议纪要与主标书，retrieval evidence 同时包含两份文件。
5. 对比场景中的 `topicmismatch` / `mutualunawareness` 属于合理隔离诊断，不视为失败。
6. 会议内容不得当标书条款已通过：主标书检索未混入会议纪要，未把“真实族库 / 推动行业标准 / 认证体系”等会议内容误引用为招标条款。

当前 Phase 2.13 可收口为：会议纪要 / 转写文本 ingestion MVP 已完成最小闭环，但仍不包含原始音频 ASR、speaker diarization 模型、facts 写入或生产级 rollout。
