# Phase 2.4 Rerank 默认启用策略评估

## 1. 目标

本文档用于回答以下问题：

1. 真实 reranker 是否已经值得进入默认启用实施阶段。
2. 如果值得，应该先在什么范围启用。
3. timeout、fail-open、rollback 应如何落地。
4. 当前仍不应做什么。

本阶段是策略评估，不是默认启用实施。

## 2. 当前评测基础

当前已具备的证据：

- 阿里云 Text Rerank API 已真实打通。
- `gte-rerank-v2` 已完成真实请求验证。
- `ALIYUN_EMBEDDING_API_KEY` 可作为 rerank key fallback。
- rerank hook、candidate pool、trace、fail-open 已在主链路中落地。
- 48 条脱敏近真实中文企业 query 已完成 baseline vs experiment 对比。

当前 48 条样本覆盖：

- 招标资料：19
- 公司文档：4
- 公众号文章：8
- 制度文件：4
- 合同条款：4
- 项目文档：4
- 方案文档：5

## 3. 当前评测结果

Baseline（`NoopReranker`）：

- top-1 hit：`0.9583`
- top-3 hit：`1.0`
- top-5 hit：`1.0`
- latency avg：`0.002 ms`
- latency p50：`0.002 ms`
- latency p95：`0.004 ms`
- fail-open count：`0`

Experiment（`AliyunTextReranker` / `gte-rerank-v2`）：

- top-1 hit：`1.0`
- top-3 hit：`1.0`
- top-5 hit：`1.0`
- latency avg：`358.34 ms`
- latency p50：`353.478 ms`
- latency p95：`458.05 ms`
- fail-open count：`0`

收益观察：

- top-1 改进：`2` 条
- top-1 回归：`0` 条
- 当前收益集中在招标资料中的资质要求 / 条款定位类问题

## 4. 默认启用范围建议

### 4.1 建议优先默认启用的范围

建议优先在以下 query 范围默认启用 rerank：

1. 招标资料相关 query。
2. 资质要求类 query。
3. 条款定位类 query。
4. 容易被相似候选干扰的 query，例如：
   - “是否要求 ISO9001”
   - “资质要求有哪些”
   - “某条款写了什么”
   - “付款安排 / 评分标准 / 时间安排”

### 4.2 暂不建议默认启用的范围

以下范围暂不建议默认启用：

1. 已知 baseline top-1 已长期稳定的简单事实型 query。
2. 公众号文章中的直接措辞定位类 query。
3. 制度、合同、项目文档中词面高度唯一、baseline 已无明显误排的 query。

### 4.3 启用方式建议

当前更推荐：

1. 按 query 类型启用。
2. 按 route_type 或检索场景启用。
3. 保留全局 config flag，支持快速关闭。

当前不建议：

1. 对所有 query 全局默认启用。
2. 只按 provider 可用与否就统一打开。

## 5. timeout / fail-open / rollback 策略建议

### 5.1 timeout 建议

建议初始 timeout：

- `timeout_ms = 600`

原因：

- 当前 p95 约 `458 ms`
- 若设置为 `600 ms`，可覆盖当前观测区间并保留少量抖动余量
- 再高会让“默认启用”对整体响应时间的影响过于明显

### 5.2 fail-open 策略

当前建议直接保留现有 fail-open 机制：

1. timeout 直接回 baseline 排序结果。
2. provider HTTP 异常直接 fail-open。
3. response 解析异常直接 fail-open。
4. key 问题直接 fail-open。

必须记录 trace：

- provider
- model
- elapsed_ms
- timeout_ms
- fail_open
- error_type
- remote_request_id（若可得）

### 5.3 rollback 策略

必须保留全局快速关闭开关：

- `RERANK_ENABLED=false`

建议的回滚触发条件：

1. fail-open rate 持续高于 `1%`
2. rerank p95 持续高于 `600 ms`
3. 小流量灰度中 top-1 收益不稳定或出现明显回归
4. provider 成本或配额超出预算

## 6. 成本与延迟预算判断

### 6.1 当前延迟是否可接受

当前延迟在以下条件下可接受：

1. 只对高价值 query 类型启用。
2. 仅在 hybrid candidate pool 已形成后执行一次 rerank。
3. 用户场景更重视答案正确性和条款定位，而不是最低延迟。

当前延迟在以下情况下不建议接受：

1. 全量 query 全局默认启用。
2. 低价值、低歧义、baseline 已足够稳定的 query。
3. 高并发且对响应时间极度敏感的流量。

### 6.2 默认启用前仍需补的观测

1. 更大一批真实业务 query 的分类统计。
2. 分 query 类型的收益与回归对比。
3. 小流量灰度下的真实 fail-open rate。
4. 更稳定的 latency p95 / p99 观测。

## 7. 是否值得进入默认启用实施阶段

结论：

可以进入默认启用实施阶段，但应以“局部默认启用 + 可快速回退”的方式进入，而不是全局默认启用。

建议进入方式：

1. 第一阶段只对招标资料相关 query 默认启用。
2. 第一阶段重点覆盖资质要求类、条款定位类 query。
3. 保持 `RERANK_ENABLED` 全局开关可即时关闭。
4. 保持 timeout 和 fail-open 严格生效。
5. 默认启用实施阶段仍应以灰度启用为主，不做全量直接放开。

## 8. 当前仍不应做的内容

1. 不应默认对所有 query 启用 rerank。
2. 不应同时并行多个 reranker provider。
3. 不应在本阶段引入 qwen3-rerank、BGE 或 cross-encoder 本地部署。
4. 不应在本阶段重写 candidate pool 策略或 retrieval contract。
5. 不应把当前评测结果包装成“已完成生产验证”。
