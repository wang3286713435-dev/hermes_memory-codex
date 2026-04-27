# Phase 2.31 Internal Controlled MVP Pilot Operations Plan

## 1. 目标

Phase 2.31 目标是让公司内部可以安全开始受控 MVP Pilot 试用。

本阶段只建立试用流程、人工复核机制、反馈模板和 known risk checklist，不新增功能，不进入 production rollout。

## 2. Pilot 范围

本次内部试用只覆盖三类场景：

1. 标书审查 / 风险提取。
2. 企业文件内容提取与 citation 定位。
3. 公司未来发展方向辅助分析。

本次内部试用不覆盖：

1. production rollout。
2. 自动审标定论。
3. 自动经营决策。
4. repair executor。
5. facts 自动抽取。
6. facts 替代 retrieval evidence。
7. 完整 RBAC / ABAC / SSO。

## 3. 试用角色

### 3.1 使用者

职责：

1. 按 runbook 绑定 alias。
2. 提出业务 query。
3. 保存 Hermes 输出。
4. 不把 Hermes 输出直接当最终业务结论。

### 3.2 人工复核人

职责：

1. 检查 evidence / citation 是否存在。
2. 检查 document_id / version_id 是否符合目标文件。
3. 检查 `facts_as_answer=false`。
4. 检查 `transcript_as_fact=false`。
5. 标记 partial、missing evidence 和需要人工确认的结论。

### 3.3 记录人

职责：

1. 收集 query、输出和复核结果。
2. 记录 pass / partial / fail。
3. 归类问题类型。
4. 汇总 1-2 天试用报告。

### 3.4 技术值守

职责：

1. 只处理 API / CLI / alias / citation / session scope 问题。
2. 不修改业务结论。
3. 不执行 repair、backfill、reindex、cleanup 或 delete。
4. 遇到数据修改需求时停止并升级为单独 Phase。

## 4. 每次使用流程

1. 检查 Hermes_memory API `/health`。
2. 启动 Hermes CLI 并建立新 session。
3. 在同一 session 内绑定必要 alias：
   - `@主标书`
   - `@会议纪要`
   - `@硬件清单`
   - `@C塔方案`
4. 运行业务 query。
5. 保存完整输出。
6. 人工检查以下字段：
   - document_id / version_id
   - citation / chunk / sheet / cell / slide
   - `facts_as_answer=false`
   - `transcript_as_fact=false`
   - `contamination_flags`
   - Missing Evidence
7. 在 feedback template 中记录结果。

## 5. 人工复核标准

1. 无 citation 不采信。
2. Missing Evidence 必须保留，不得补脑。
3. partial 不等于 fail，但必须标记人工复核。
4. 经营建议只能作为辅助建议，必须人工决策。
5. 标书深层字段必须人工复核，尤其是最高投标限价、业绩要求、付款节点、工期节点和质保 / 违约条款。
6. 会议纪要只能作为 retrieval evidence，不是原始录音铁证。
7. confirmed facts 只能作为辅助上下文，不得替代当前 retrieval evidence。
8. compare 场景必须确认只返回目标 A/B 文件，不混入第三文件。

## 6. 试用节奏

建议首轮试用周期为 1-2 天。

每日最小动作：

1. 每位使用者运行 3-5 条真实 query。
2. 每条 query 都保存输出和人工复核结果。
3. 记录人当天汇总 pass / partial / fail。
4. 技术值守只整理问题，不现场改数据或改功能。

## 7. 成功判定

1. Alias/session 不再成为主要阻塞。
2. 标书审查高频问题可稳定输出 citation 或明确 Missing Evidence。
3. Excel / PPTX / 会议纪要 extraction 可稳定定位。
4. 使用者能明确区分 Evidence / Interpretation / Recommendation。
5. 所有 partial / Missing Evidence 都能被记录。
6. 试用期间未出现 facts 替代 retrieval evidence。
7. 试用期间未出现会议纪要被标记为 confirmed fact。

## 8. 失败或暂停条件

出现以下情况应暂停试用并回到 Phase 规划：

1. alias/session 再次成为主要阻塞。
2. 多次出现无 citation 但给确定结论。
3. compare 场景频繁混入第三文件。
4. `facts_as_answer=true`。
5. `transcript_as_fact=true`。
6. 使用者要求自动执行业务决策、repair 或 rollout。
7. 需要修改真实业务数据。

## 9. 当前结论

Phase 2.31 建议进入内部受控 MVP Pilot 试用，但必须保持人工复核和非 rollout 边界。

本阶段不建议进入 production rollout。
