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
