# Phase 2.5 局部默认启用实施（灰度版）

## 1. 目标

本阶段将 Phase 2.4 的策略评估落地为可运行逻辑，但范围只限局部默认启用，不做全局默认启用。

当前目标：

1. 对高收益范围默认启用真实 rerank。
2. 保留全局关闭、局部关闭、timeout fail-open 和快速回退。
3. 让 trace 能明确反映本次是否命中局部启用规则。

## 2. 当前默认启用范围

第一版局部默认启用规则采用可解释的简单规则，不引入复杂分类器。

当前命中条件：

1. `RERANK_ENABLED=true`
2. `RERANK_PROVIDER=aliyun`
3. `RERANK_DEFAULT_ENABLEMENT_ENABLED=true`
4. 候选集数量达到最小阈值，默认 `2`
5. query 命中高收益关键词
6. 且命中目标范围：
   - `source_type=tender`
   - 或 `route_type in {tender, tender_qa, tender_query}`

默认关键词：

- `资质`
- `要求`
- `条款`
- `截止`
- `联合体`
- `投标`
- `招标`
- `开标`
- `答疑`
- `评分`
- `保证金`

## 3. 当前不启用范围

以下场景当前不默认启用：

1. 非招标资料范围的普通 query
2. 未命中高收益关键词的普通事实型 query
3. 候选数低于阈值的 query
4. 全局关闭或 provider 不匹配时的全部 query

## 4. timeout / fail-open / rollback

### 4.1 timeout

当前默认：

- `ALIYUN_RERANK_TIMEOUT_MS=600`

### 4.2 fail-open

以下情况统一 `failed_open`：

1. timeout
2. provider HTTP 异常
3. provider 返回解析异常
4. key 缺失
5. provider 运行时异常

fail-open 后回退到未 rerank 的 candidate pool 排序结果。

### 4.3 rollback

当前回退方式：

1. 全局快速关闭：`RERANK_ENABLED=false`
2. 局部默认启用关闭：`RERANK_DEFAULT_ENABLEMENT_ENABLED=false`
3. provider 切回 noop：`RERANK_PROVIDER=noop`

建议回退触发条件：

1. fail-open rate 持续高于 `1%`
2. rerank p95 持续高于 `600ms`
3. 灰度流量中出现明显 top-1 回归
4. provider 成本或配额超预算

## 5. Trace 观察点

当前 trace 中应重点观察：

### 5.1 `trace.rerank_policy`

- `strategy`
- `strategy_active`
- `enabled`
- `reason`
- `global_enabled`
- `local_default_enablement_enabled`
- `route_type`
- `applied_source_type`
- `candidate_source_types`
- `matched_keywords`
- `source_type_match`
- `route_type_match`
- `min_candidates_met`
- `candidate_count`

### 5.2 `trace.rerank`

- `provider`
- `status`
- `reason`
- `fail_open`
- `elapsed_ms`
- `timeout_ms`
- `error_type`
- `policy_enabled`
- `policy_reason`

## 6. 为什么当前仍不全局启用

原因仍然成立：

1. 当前收益主要集中在招标资料中的资质要求 / 条款定位类 query。
2. 其他 query 类型目前更多体现为“无回归”，而不是“显著提升”。
3. rerank 平均延迟与 p95 延迟已明显高于 noop。
4. 当前还没有更大规模真实流量统计支撑全量默认启用。

## 7. 进入下一步前需要满足的条件

若要扩大默认启用范围，至少需要满足：

1. 在更大真实 query 集上分类型复测收益。
2. 低回归、低 fail-open、可接受 latency 持续稳定。
3. 灰度运行结果能支撑扩大范围，而不是只在离线 spike 中表现良好。
4. 运行手册与回退手册已落实到配置和操作流程。
