# Phase 2.7 局部默认启用运行基线与小流量运行准备

## 1. 文档目的

本文档用于将 Phase 2.6 已验证通过的局部默认启用策略沉淀为可执行的运行基线，并为后续更长期的小流量运行提供统一操作手册。

本文档覆盖：

1. 当前运行基线定义
2. 当前启用范围与不启用范围
3. 开关与配置项说明
4. 观测项与异常判断入口
5. 回滚条件
6. 运行前检查清单
7. 更长期小流量运行的进入前提

本文档不覆盖：

1. 启用范围扩大
2. 全局默认启用
3. 新 reranker provider 接入
4. 更复杂 query classifier

## 2. 当前运行基线定义

### 2.1 当前 provider 基线

- `RERANK_PROVIDER=aliyun`
- `ALIYUN_RERANK_MODEL=gte-rerank-v2`
- `ALIYUN_RERANK_TIMEOUT_MS=600`

当前默认要求：

1. 真实 rerank provider 为阿里云 Text Rerank
2. timeout 统一按 `600ms` 执行
3. provider 异常、timeout、解析异常统一 fail-open

### 2.2 当前启用策略基线

当前局部默认启用策略定义为：

1. `RERANK_ENABLED=true`
2. `RERANK_DEFAULT_ENABLEMENT_ENABLED=true`
3. query 必须命中关键词集合
4. request 侧上下文必须命中目标范围：
   - `filters.source_type`
   - `route_type`
5. 候选数必须达到最小阈值

明确约束：

- 不再允许 `candidate_source_types` 单独参与放行
- `candidate_source_types` 当前仅保留为 trace 诊断字段

### 2.3 当前关键词与范围基线

当前配置基线如下：

- `RERANK_DEFAULT_ENABLEMENT_SOURCE_TYPES=tender`
- `RERANK_DEFAULT_ENABLEMENT_ROUTE_TYPES=tender,tender_qa,tender_query`
- `RERANK_DEFAULT_ENABLEMENT_KEYWORDS=资质,要求,条款,截止,联合体,投标,招标,开标,答疑,评分,保证金`
- `RERANK_DEFAULT_ENABLEMENT_MIN_CANDIDATES=2`
- `RERANK_INPUT_CAP=30`

## 3. 当前启用范围

当前默认启用 rerank 的范围保持不变，仅限：

1. 招标资料相关 query
2. 资质要求类 query
3. 条款定位类 query
4. 时间安排 / 商务条款 / 评分标准类高歧义招标 query

### 3.1 当前不启用范围

当前不默认启用 rerank 的范围包括：

1. 非招标资料 query
2. 未命中关键词的普通事实型 query
3. 候选数不足的 query
4. 全局关闭或局部关闭时的全部 query

## 4. 开关说明

### 4.1 全局开关

- `RERANK_ENABLED`

行为说明：

1. `false`：所有 query 统一回 baseline / noop
2. `true`：允许进入局部默认启用判断链路

### 4.2 局部默认启用开关

- `RERANK_DEFAULT_ENABLEMENT_ENABLED`

行为说明：

1. `false`：即使 query 命中目标范围，也不执行 rerank
2. `true`：按当前局部规则判断是否执行 rerank

### 4.3 关键运行配置

当前影响运行行为的关键配置如下：

- `RERANK_PROVIDER`
- `RERANK_ENABLED`
- `RERANK_DEFAULT_ENABLEMENT_ENABLED`
- `RERANK_DEFAULT_ENABLEMENT_SOURCE_TYPES`
- `RERANK_DEFAULT_ENABLEMENT_ROUTE_TYPES`
- `RERANK_DEFAULT_ENABLEMENT_KEYWORDS`
- `RERANK_DEFAULT_ENABLEMENT_MIN_CANDIDATES`
- `RERANK_INPUT_CAP`
- `ALIYUN_RERANK_MODEL`
- `ALIYUN_RERANK_TIMEOUT_MS`
- `QDRANT_URL`
- `OPENSEARCH_URL`

## 5. 观测项清单

运行期至少持续观测以下指标：

1. `rerank_hit_rate`
2. `rerank_skip_rate`
3. `fail_open_rate`
4. `timeout_count`
5. `latency p95`
6. `latency p99`
7. `dense_failed_count > 0` 是否出现
8. `sparse_failed_count > 0` 是否出现
9. 命中集是否漂移
10. 是否出现新的漏命中边界样本

### 5.1 规则层观测

规则层重点判断：

1. 命中集是否保持同一组目标 query
2. 误命中是否保持为 `0`
3. 是否出现新的漏命中边界样本

### 5.2 运行层观测

运行层重点判断：

1. 是否再次出现 `dense_failed_count > 0`
2. 是否再次出现 `sparse_failed_count > 0`
3. 异常窗口是否导致：
   - `candidate_pool_below_min_threshold`
   - `rerank_hit_count=0`
   - 目标命中集整体归零
4. 异常窗口后是否自动恢复

## 6. Trace 与排查入口

### 6.1 规则层排查入口

优先看以下 trace 字段：

1. `rerank_policy.enabled`
2. `rerank_policy.reason`
3. `rerank_policy.matched_keywords`
4. `rerank_policy.applied_source_type`
5. `rerank_policy.route_type`
6. `rerank_policy.source_type_match`
7. `rerank_policy.route_type_match`
8. `rerank_policy.min_candidates_met`
9. `rerank_policy.candidate_count`

### 6.2 运行层排查入口

优先看以下 trace / 统计：

1. `rerank.status`
2. `rerank.fail_open`
3. `rerank.error_type`
4. `dense.status`
5. `sparse.status`
6. `candidate_pool` 相关计数
7. `dense_failed_count`
8. `sparse_failed_count`

### 6.3 常见判断路径

#### 规则问题

若出现以下现象，更可能是规则问题：

1. request 侧 `source_type / route_type` 未命中
2. `matched_keywords` 为空
3. `local_default_enablement_not_matched` 持续出现
4. 正常检索可用，但命中集开始漂移

#### 后端问题

若出现以下现象，更可能是后端问题：

1. `dense_failed_count > 0`
2. `sparse_failed_count > 0`
3. 目标 query 集体落到 `candidate_pool_below_min_threshold`
4. 命中集临时整体归零，但后续窗口自动恢复

## 7. 回滚条件

### 7.1 触发全局关闭的条件

满足任一条件应优先考虑全局关闭：

1. `dense_failed_count > 0` 或 `sparse_failed_count > 0` 在连续窗口重复出现
2. `fail_open_rate` 明显抬升且持续
3. `p99` 持续恶化并超过当前阶段预算
4. 出现大面积目标命中集整体归零

### 7.2 触发局部关闭的条件

满足任一条件应优先考虑局部关闭：

1. 命中集开始漂移
2. 新的误命中开始出现
3. 新的漏命中边界样本开始出现
4. 仅在当前局部启用范围内观察到明显收益下降或不稳定

### 7.3 停止小流量运行的条件

满足以下条件之一应暂停更长期小流量运行：

1. 后端异常窗口开始重复出现
2. 当前运行窗口中出现第二次“目标命中集整体归零”
3. 当前观察指标无法再支撑规则层与运行层分离判断

## 8. 运行前检查清单

进入更长期小流量运行前，至少完成以下检查：

1. Qdrant 可用
2. OpenSearch 可用
3. rerank key 可用
4. 当前 provider 正常
5. `ALIYUN_RERANK_TIMEOUT_MS=600`
6. 当前启用范围配置正确
7. `RERANK_ENABLED` 可切换
8. `RERANK_DEFAULT_ENABLEMENT_ENABLED` 可切换
9. 灰度验证脚本可运行
10. 双仓库可回滚基线已完成

## 9. 更长期小流量运行前提

进入更长期小流量运行前，当前必须满足：

1. 当前规则不再改动
2. 当前启用范围不再扩大
3. 当前运行基线文档完整
4. 回滚条件明确
5. 观测项明确
6. 双仓库可回滚基线已完成
7. Phase 2.6 退出标准已满足
8. 当前没有新增阻塞问题

## 10. 当前阶段结论

当前局部默认启用策略已经沉淀成一套：

1. 可执行
2. 可关闭
3. 可观测
4. 可回退

的运行基线。

当前已经具备进入“更长期小流量运行准备”的条件，但仍不应：

1. 扩大启用范围
2. 全局默认启用
3. 引入新的 provider 或 classifier

## 11. Phase 2.8 运行观察衔接

Phase 2.8 的运行观察继续严格沿用本 runbook，不新增变量。

当前运行期重点观察项保持为：

1. `rerank_hit_rate`
2. `rerank_skip_rate`
3. `fail_open_rate`
4. `timeout_count`
5. `latency p95`
6. `latency p99`
7. `dense_failed_count > 0`
8. `sparse_failed_count > 0`
9. 命中集是否漂移
10. 是否出现新的漏命中边界样本

当前判断原则：

1. 规则层稳定，不再改规则
2. 继续保持当前启用范围不变
3. 若后端异常窗口再次出现，应优先按运行层问题处理，而不是回退到规则修改
