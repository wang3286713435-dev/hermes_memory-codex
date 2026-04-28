# Phase 2.32 MVP Pilot Feedback Intake Plan

## 1. 目标

Phase 2.32 目标是建立内部 MVP Pilot 反馈收集、分诊和优先级闭环。

本阶段只做流程规划，不写功能代码，不创建自动 issue，不写业务 DB，不进入 rollout。

## 2. 输入来源

反馈来源限定为：

1. `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md` 填写结果。
2. 真实 Hermes 输出。
3. 人工复核结论。
4. Codex C 真实终端复验记录。
5. 使用者补充的业务影响说明。

不得把未复核的口头结论直接作为修复任务。

## 3. Intake 字段

每条反馈至少记录：

1. feedback_id。
2. 日期 / 使用人 / 复核人。
3. 使用场景：
   - 标书审查 / 风险提取。
   - 文件内容提取与 citation 定位。
   - 公司未来发展方向辅助分析。
4. query 原文。
5. 期望答案。
6. 实际答案摘要。
7. pass / partial / fail。
8. document_id / version_id。
9. citation 是否完整。
10. 问题类型。
11. 业务影响。
12. 建议优先级。
13. 是否需要 Codex C 复验。
14. 是否需要新 phase。

## 4. 问题类型

问题类型固定为：

1. alias/session。
2. retrieval recall。
3. citation。
4. contamination。
5. facts boundary。
6. transcript boundary。
7. UX / prompt。
8. latency / runtime。
9. environment。
10. other。

## 5. 优先级定义

### P0

满足任一条件：

1. facts 替代 retrieval evidence。
2. transcript 被标为 fact。
3. compare 场景混入第三文件且未被标记。
4. 无 citation 仍输出确定业务结论。
5. alias/session 大面积失效，阻塞试用。

处理要求：

1. 暂停相关场景试用。
2. 需要 Codex B 重新规划。
3. 需要 Codex C 复验。

### P1

满足任一条件：

1. 高频业务字段召回 partial 或漏召回。
2. citation 缺字段但仍能定位。
3. 用户无法稳定复现推荐流程。
4. 影响试用效率但未触发安全边界。

处理要求：

1. 进入下一轮 bounded phase 候选。
2. 需要人工复核样例。

### P2

满足任一条件：

1. 低频字段召回不稳。
2. 输出格式可读性不足。
3. feedback 表单字段需要补充。
4. runbook 文案需要澄清。

处理要求：

1. 可批量进入 docs / UX polish。
2. 不阻塞试用。

### P3

满足任一条件：

1. 长期优化建议。
2. 非当前 Pilot 场景需求。
3. 需要新样本、新密钥或新业务判断。

处理要求：

1. 放入 backlog。
2. 不进入当前 sprint。

## 6. Go / No-Go 规则

可以继续试用：

1. P0 为 0。
2. P1 可人工规避并已记录。
3. 所有 partial / Missing Evidence 均可追踪。
4. 用户能区分 Evidence / Interpretation / Recommendation。

必须暂停或降级：

1. 出现任一 P0。
2. 同一场景连续出现 3 条以上未解释 fail。
3. 使用者无法识别 Missing Evidence。
4. 试用中出现自动决策、repair、DB mutation 或 rollout 诉求。

## 7. 分诊流程

1. 记录人收集 feedback template。
2. 人工复核人确认证据与问题类型。
3. 技术值守只判断是否属于 alias / retrieval / citation / contamination / boundary 问题。
4. Codex B 将反馈归并为 bounded phase 候选。
5. Codex A 只执行明确批准的单一 phase 子任务。
6. Codex C 对需要真实终端的 P0 / P1 做复验。

## 8. 非目标

本阶段不做：

1. 自动修复。
2. 自动写 DB。
3. 自动创建 Linear / GitHub issue。
4. 自动生成 repair plan。
5. production rollout。
6. facts 自动抽取。
7. facts 替代 retrieval evidence。
8. 修改 retrieval contract。
9. 修改 memory kernel 主架构。

## 9. 输出物建议

首轮可以用人工维护的表格或 markdown 汇总，不新增系统功能。

建议字段：

1. feedback_id。
2. priority。
3. issue_type。
4. scenario。
5. query。
6. expected / actual。
7. evidence status。
8. proposed next phase。
9. owner。
10. status。

## 10. 当前结论

Phase 2.32 建议先由 Codex B review 本规划，再决定是否做文档基线或最小本地 intake 表模板。

当前不建议进入自动 issue 创建、repair executor 或 rollout。
