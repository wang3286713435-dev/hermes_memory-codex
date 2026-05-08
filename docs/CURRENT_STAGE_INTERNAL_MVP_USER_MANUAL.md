# 当前阶段内部受控 MVP 使用说明书

## 1. 这份说明书给谁看

这份说明书面向当前阶段会实际使用 Hermes 的人，包括：

1. 内部试用人员。
2. 人工复核人。
3. 测试机操作员。
4. 技术值守人员。

这份说明书的目标是提供一个统一入口，让人类读者在一份文档里就能理解：

1. 当前项目是什么。
2. 当前项目能做什么。
3. 当前项目不能做什么。
4. 当前应该怎么在测试机上使用。
5. 出现什么情况必须暂停。

## 2. 当前项目是什么

Hermes 当前阶段是一个内部受控的企业文件 Agent MVP。

它的定位是：

1. 企业文件问答与证据检索工具。
2. 标书、会议纪要、Excel、PPTX 等资料的辅助分析工具。
3. 带引用、带来源定位、带人工复核边界的内部试用系统。

它不是：

1. production rollout 系统。
2. 自动审标系统。
3. 自动投标系统。
4. 自动经营决策系统。
5. 自动合同、采购或法务决策系统。
6. 自动 repair、cleanup、backfill、reindex、delete 系统。

## 3. 当前架构怎么理解

当前“应用”分成两层：

1. `Hermes_memory`
   - 负责文件上传、解析、切分、入库、索引、检索、citation、facts 和 API。
2. `hermes-agent`
   - 负责 CLI、会话、alias、用户交互和会话式使用体验。

对使用者来说，这意味着：

1. 只启动 `Hermes_memory`，你会得到后端能力和 API。
2. 同时接通 `hermes-agent`，你才会得到更完整的会话式体验，比如 `@主标书`、`@会议纪要` 这类 alias 使用方式。

## 4. 当前能力边界

### 4.1 目前已经具备

1. 文件入库与版本治理
   - 支持 `txt`、`md`、`html`、`pdf`、`docx`、`xlsx`、`pptx` 上传和入库。
   - 支持同一 document 下的 version 管理。
   - 能识别重复上传。
2. 检索与引用
   - 支持 sparse retrieval。
   - 支持 dense retrieval。
   - 支持 hybrid retrieval。
   - 能返回 `document_id`、`version_id`、citation 和结构化来源定位。
3. 结构化文件引用
   - Excel 可返回 `sheet_name`、`cell_range` 或降级定位信息。
   - PPTX 可返回 `slide_number`、`slide_title`。
   - 会议纪要可提取 action items、decisions、risks，并保留来源边界。
4. 受控会话使用
   - `hermes-agent` 可在 session 中绑定 alias。
   - 同一 session 可围绕指定文档持续提问。

### 4.2 当前明确不能当成已完成能力

1. 最终业务答案生成
   - 当前系统更适合提供 evidence、citation 和 answer basis，不应被当成最终自动结论机。
2. 生产级权限治理
   - 当前不是完整 IAM、SSO、RBAC、ABAC 方案。
3. 自动业务决策
   - 不允许把 Hermes 输出直接当自动审标、自动经营、自动采购、自动合同决策。
4. 自动数据修复和自动运维闭环
   - 当前不授权 repair、cleanup、backfill、reindex、delete、destructive migration。
5. 全量企业资料开放式使用
   - 当前更适合内部受控、小批量、人工监督式试用。

### 4.3 当前必须始终保持的边界

1. `facts_as_answer=false`
2. `transcript_as_fact=false`
3. 没有 evidence 时必须显式写出 `Missing Evidence`
4. Recommendation 只能作为辅助建议，最终判断必须由人完成

## 5. 当前最适合怎么用

当前最适合的使用场景是：

1. 内部受控的企业文件问答与证据检索。
2. 标书基础字段提取与风险点定位。
3. Excel / PPTX / 会议纪要类资料的结构化引用和人工复核辅助。
4. 有人工 reviewer 在场的方向分析和资料核对。

当前不适合的使用场景是：

1. 对外客户交付。
2. 无人监督的大规模业务决策。
3. 全公司敏感资料一次性全量导入。
4. 把输出直接提交给客户、招标方、法务、采购或经营管理层作为最终结论。

## 6. 测试机当前的推荐使用方式

### 6.1 使用前检查

每次开始前至少确认：

1. `Hermes_memory` 的 `/health` 正常。
2. `hermes chat --help` 正常。
3. `HERMES_MEMORY_KERNEL_ENABLED=1`。
4. `HERMES_MEMORY_PATH` 指向本机的 `Hermes_memory` 仓库。
5. 当前使用的文件已经入库。
6. 当前属于内部受控 MVP 试用，不是 production rollout。

### 6.2 第一批推荐导入

建议先从 4 类代表性文件开始：

1. `@主标书`
2. `@硬件清单`
3. `@C塔方案`
4. `@会议纪要`

推荐元数据：

1. 主标书：`source_type=tender`
2. 硬件清单：`source_type=tender`
3. C 塔方案：`source_type=tender`
4. 会议纪要：`source_type=meeting_minutes`

### 6.3 导入后怎么检查

每个文件导入后至少记录：

1. 文件名。
2. `title`
3. `source_type`
4. `document_type`
5. `document_id`
6. `version_id`
7. `chunk_count`
8. `indexed_count`

如果当前文件无法形成正常索引，先暂停，不要继续堆更多文件。

## 7. 人类使用时的推荐流程

### 7.1 第一步：绑定 alias

建议在同一 session 中绑定：

1. `@主标书`
2. `@硬件清单`
3. `@C塔方案`
4. `@会议纪要`

当前阶段更稳的绑定说法是：

1. `把《主标书》设为 @主标书`
2. `把《会议纪要》设为 @会议纪要`
3. `把《硬件清单》设为 @硬件清单`
4. `把《C塔方案》设为 @C塔方案`

如果已经先围绕某个文件问过问题，也可以使用：

1. `把当前主标书设为 @主标书`
2. `请把上一轮已锁定的当前文件设为 @主标书`

但这类说法依赖当前 session 里已经存在 active document，所以在人类现场试用时，优先推荐“把《标题》设为 @alias”的显式说法。

绑定后检查：

1. `alias_resolution.status`
2. `resolved_document_id`
3. `resolved_version_id`
4. 是否存在异常的 retrieval suppression

### 7.2 第二步：跑最小问题集

推荐至少验证以下 4 类问题：

1. 标书基础字段提取
   - 例如工程名称、工程地点、建设单位、工期、最高投标限价。
2. Excel 结构化定位
   - 例如要求返回 `sheet_name` 和 `cell_range`。
3. PPTX 页面定位
   - 例如要求返回 `slide_number` 和 `slide_title`。
4. 会议纪要边界验证
   - 例如要求返回 action items、decisions、risks，并明确 `transcript_as_fact=false`。

### 7.3 第三步：人工复核

每条输出至少检查：

1. `document_id` / `version_id` 是否正确。
2. citation 是否能人工回到原文件核对。
3. `facts_as_answer=false`
4. `transcript_as_fact=false`
5. 是否存在第三文件污染。
6. 没有证据时是否明确写出 `Missing Evidence`。

## 8. 当前建议怎样提问

### 8.1 标书类

推荐问法：

```text
围绕 @主标书，提取工程名称、工程地点、建设单位、工期、最高投标限价。
请按字段输出结论、evidence / citation、是否需要人工确认。
如果当前召回中没有找到，请明确写 Missing Evidence。
```

### 8.2 Excel 类

推荐要求返回：

1. `sheet_name`
2. `cell_range`
3. `document_id`
4. `version_id`
5. 如果只能降级定位，要明确说明

### 8.3 PPTX 类

推荐要求返回：

1. `slide_number`
2. `slide_title`
3. `document_id`
4. `version_id`

### 8.4 会议纪要类

推荐要求返回：

1. action items
2. decisions
3. risks
4. citation
5. `transcript_as_fact=false`

### 8.5 方向分析类

必须要求按以下结构输出：

1. Evidence
2. Interpretation
3. Recommendation
4. Risk / Assumption
5. Missing Evidence

同时必须强调：

1. Recommendation 只是辅助建议。
2. 最终经营判断必须由人做。

## 9. 当前禁止事项

在当前阶段，使用者和操作员都不应：

1. 把 Hermes 输出当最终审标结论。
2. 把 Hermes 输出当自动经营决策。
3. 把会议纪要当正式招标文件条款。
4. 把 facts 当 retrieval evidence 的替代品。
5. 要求系统执行 repair、cleanup、backfill、reindex、delete 或 destructive migration。
6. 在测试机上临时修改业务代码绕过问题。
7. 把测试机当开发机长期手改代码。
8. 未经小样本验证就一次性导入大批量敏感企业资料。

## 10. 什么时候必须暂停

出现以下任一情况应暂停使用并记录问题：

1. `/health` 不通过。
2. Hermes CLI 不可用。
3. alias 解析错误或频繁不稳定。
4. 输出没有 citation 却给出确定性结论。
5. `facts_as_answer=true`
6. `transcript_as_fact=true`
7. compare 或多文档场景混入第三文件。
8. 使用者开始把系统当自动决策系统。
9. 下一步需要 repair、cleanup、backfill、reindex、delete、migration 才能继续。

## 11. 热更新和运维纪律

测试机上的更新纪律必须保持简单和受控：

1. 开发在开发机完成。
2. 经 review 后 push 到远端。
3. 测试机只做 `git pull --ff-only`、重启、health check、最小 smoke。
4. 不在测试机上做主线功能开发。
5. 更新失败时回退到上一个已知可用版本，不在现场临时打补丁绕过。

## 12. 当前是否达到可用标准

如果同时满足以下条件，可以认为达到了“内部受控 MVP 可用标准”：

1. `Hermes_memory` `/health` 正常。
2. `hermes-agent` CLI 正常。
3. embedding key 已就绪。
4. alias 可绑定并稳定解析。
5. 至少一轮小样本导入和检索验证通过。
6. 使用者理解人工复核边界。

这仍然不等于：

1. production rollout
2. 全量企业落地
3. 自动业务决策上线

## 13. 当前已知易用性尾项

当前阶段已经可用，但文件绑定体验仍有一项明确的后续优化点：

1. 后续应由 Hermes 主仓 main agent 优化 alias / 当前文件绑定的人性化体验。
2. 目标是降低 `把当前主标书设为 @主标书` 这类说法对 active document、session resume 和唯一检索命中的隐式依赖。
3. 后续更理想的体验应包括：
   - 更稳定的标题直绑。
   - 更明确的“当前文件”提示与恢复提示。
   - 绑定失败时更清楚的诊断与下一步建议。

## 14. 推荐配套阅读

如果只读一份，先读本说明书。

需要更细的辅助材料时，再按用途补读：

1. [MVP Pilot User Guide](./MVP_PILOT_USER_GUIDE.md)
   - 更短的试用者操作视角。
2. [MVP Pilot Known Risks](./MVP_PILOT_KNOWN_RISKS.md)
   - 风险和边界总表。
3. [MVP Pilot Launch Packet](./MVP_PILOT_LAUNCH_PACKET.md)
   - 角色分工、Go/Pause/No-Go、试用前 checklist。
4. [Phase 2.51 Mac Mini Internal MVP Operator Runbook](./PHASE251_MAC_MINI_INTERNAL_MVP_OPERATOR_RUNBOOK.md)
   - Mac mini 操作员的值守、更新、回退纪律。
5. [Mac mini 最小 MVP 部署指南](./MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md)
   - 测试机部署与架构说明。
