# MVP Pilot Known Risks

## 1. 当前风险总览

Phase 2.31 内部受控 MVP Pilot 已具备试用条件，但仍不是 production rollout。

所有输出必须保留 evidence / citation / Missing Evidence 与人工复核边界。

## 2. 标书深层召回风险

已知仍需人工复核的字段：

1. 最高投标限价。
2. 业绩要求。
3. 付款节点 / 支付比例。
4. 工期节点 / 关键节点。
5. 质保 / 缺陷责任期。
6. 违约责任 / 延期赔偿。

风险说明：

1. 部分 query 可能命中邻近章节而非目标条款。
2. partial 不等于 fail，但必须人工复核。
3. 无 citation 的字段不得采信。

## 3. 发展方向分析风险

公司未来发展方向分析可能存在：

1. evidence 覆盖不足。
2. 部分文件只有间接 evidence。
3. 会议纪要反映讨论过程，不等于最终经营决策。
4. confirmed facts 可能存在 stale_source_version。
5. 推荐建议可能依赖缺失的市场、财务、客户反馈或竞品资料。

处理原则：

1. Recommendation 只能作为辅助建议。
2. 必须人工决策。
3. 缺失资料必须列入 Missing Evidence。

## 4. Facts 边界风险

当前 facts 只能辅助，不是 final answer 来源。

必须保持：

1. `facts_as_answer=false`
2. facts 不替代 retrieval evidence
3. stale fact source 必须提示
4. 无 retrieval evidence 时不得只靠 facts 作答

## 5. 会议纪要风险

会议纪要是转写文本或整理文本，不是原始录音铁证。

必须保持：

1. `transcript_as_fact=false`
2. 会议纪要不得作为招标文件条款引用
3. 会议行动项 / 决策 / 风险需要人工确认

## 6. 权限与审计风险

当前权限仍是 soft policy placeholder，不是完整 RBAC / ABAC。

当前不覆盖：

1. 企业 IAM / SSO。
2. 完整部门 / 岗位 / 项目权限模型。
3. 管理后台。
4. 生产级审计报表。

## 7. 运维边界风险

当前不进入 production rollout。

禁止：

1. repair executor。
2. delete / cleanup。
3. migration。
4. backfill / reindex。
5. production cron / scheduler。
6. 自动 facts 抽取。
7. 自动经营决策。

## 8. 试用 Go / Pause 判断

可继续试用：

1. alias/session 稳定。
2. citation 可定位。
3. partial / Missing Evidence 可记录。
4. 用户能理解人工复核边界。

应暂停试用：

1. facts 替代 evidence。
2. 会议纪要被标为 fact。
3. compare 混入第三文件。
4. 使用者要求自动决策或自动修复。
5. 深层字段多次无 citation 但输出确定结论。
