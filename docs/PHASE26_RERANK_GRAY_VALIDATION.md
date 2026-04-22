# Phase 2.6 局部默认启用真实灰度验证

## 1. 目标

本阶段用于验证以下问题：

1. 局部默认启用策略在真实灰度环境中是否按预期生效。
2. 全局关闭、局部关闭、自动 fail-open 是否真实可用。
3. trace 是否足以支撑真实运行诊断。
4. 当前灰度环境是否已经稳定到可继续扩大启用范围。

## 2. 当前灰度启用范围

当前灰度启用范围保持不变：

1. 招标资料相关 query
2. 资质要求类 query
3. 条款定位类 query
4. 高歧义、容易被相似候选干扰的 query

## 3. 当前灰度不启用范围

当前不启用范围：

1. 非招标资料 query
2. 未命中关键词的普通事实型 query
3. 候选不足的 query
4. 全局关闭或局部关闭时的全部 query

## 4. 本轮真实灰度验证方式

本轮使用：

- 48 条脱敏近真实 query
- 当前 Phase 2.5 局部默认启用规则
- 真实阿里云 Text Rerank provider
- 四组验证场景：
  - gray enabled
  - global disabled
  - local disabled
  - timeout drill

验证脚本：

- `scripts/phase26_rerank_gray_validation.py`

## 4.1 Phase 2.6 退出标准

Phase 2.6 的退出标准按两层定义。

### A. 规则层稳定

需要同时满足：

1. 命中集在最后观察窗口内不漂移。
2. 误命中保持为 `0`。
3. 不出现新的漏命中边界样本。

### B. 回退机制稳定

需要同时满足：

1. `global_disabled` 正常，全部 query 回到 baseline。
2. `local_disabled` 正常，目标 query 不再执行 rerank。
3. `timeout_drill` 正常，命中 query 统一 `failed_open`。
4. fail-open 行为与 trace 保持一致，可诊断。

### C. 延迟可接受

当前阶段采用保守工程标准：

1. 最后观察窗口内正常窗口的 `p95` 不高于 `350ms`。
2. 最后观察窗口内正常窗口的 `p99` 不高于 `400ms`。
3. 不出现继续恶化的长尾趋势。

说明：

- 单次尖峰不是绝对禁止，但若在最后观察窗口内持续重复，就不能收口。
- 异常窗口中若没有 rerank 命中，则 rerank 延迟统计不作为排序链路判定依据。

### D. 后端异常窗口可控

当前阶段采用现实可执行标准：

1. 最后观察窗口内不应再次出现 `dense_failed_count > 0` 或 `sparse_failed_count > 0` 的异常窗口。
2. 历史窗口中允许存在一次已知、已恢复的孤立异常窗口，但不能在最后观察窗口中重复出现。
3. 若异常窗口再次出现并导致目标命中集整体归零，则 Phase 2.6 不能收口。

## 5. 本轮环境预检结果

当前灰度环境预检结果：

- Qdrant：可用
- OpenSearch：可用
- 真实灰度验证脚本可完整运行

本轮排查结果表明，`rerank_hit_count=0` 的主因不是环境，而是灰度脚本没有把招标资料上下文显式传入策略判断链路。

修正内容：

1. 招标类样本请求补充 `route_type=tender_query`
2. 招标类样本请求补充 `filters.source_type=tender`
3. trace 补充 `configured_source_types`、`configured_route_types`、`configured_keywords`

修正后，局部默认启用策略开始正常命中目标 query。

后续又做了一次很小的规则收紧：

1. 局部默认启用必须由 request 侧上下文命中目标范围：
   - `filters.source_type`
   - `route_type`
2. `candidate_source_types` 不再单独参与放行
3. 关键词仍作为必要条件之一保留

这次收紧的目标是消除此前少量“非招标 query 因候选池混入 tender 结果而误命中 rerank”的情况。

## 6. 本轮观测结果

### 6.1 gray enabled

- 累计完整观察轮次：`9`
- 其中：
  - 正常窗口：`8`
  - 后端瞬时失败窗口：`1`
- total queries / run：`48`
- 正常窗口 rerank hit count：`13 / 13 / 13 / 13 / 13 / 13 / 13 / 13`
- 正常窗口 rerank hit rate：`0.2708 / 0.2708 / 0.2708 / 0.2708 / 0.2708 / 0.2708 / 0.2708 / 0.2708`
- 正常窗口 rerank skip count：`35 / 35 / 35 / 35 / 35 / 35 / 35 / 35`
- 正常窗口 rerank skip rate：`0.7292 / 0.7292 / 0.7292 / 0.7292 / 0.7292 / 0.7292 / 0.7292 / 0.7292`
- 正常窗口 fail-open count：`0 / 0 / 0 / 0 / 0 / 0 / 0 / 0`
- 正常窗口 timeout count：`0 / 0 / 0 / 0 / 0 / 0 / 0 / 0`
- 正常窗口 dense failed count：`0 / 0 / 0 / 0 / 0 / 0 / 0 / 0`
- 正常窗口 sparse failed count：`0 / 0 / 0 / 0 / 0 / 0 / 0 / 0`
- 正常窗口 latency avg：`292.399 / 309.643 / 308.633 / 322.979 / 297.234 / 297.439 / 305.022 / 296.944 ms`
- 正常窗口 latency p50：`290.711 / 295.825 / 302.986 / 299.079 / 293.302 / 296.762 / 306.682 / 305.541 ms`
- 正常窗口 latency p95：`304.302 / 322.052 / 341.721 / 347.406 / 328.119 / 317.563 / 331.919 / 311.127 ms`
- 正常窗口 latency p99：`306.839 / 465.453 / 382.525 / 566.045 / 332.406 / 337.099 / 332.471 / 316.654 ms`
- 正常窗口平均 latency：
  - avg：`303.162 ms`
  - p50：`298.861 ms`
  - p95：`325.526 ms`
  - p99：`379.937 ms`
- policy reasons：
  - `local_default_enablement_matched`：`13`
  - `local_default_enablement_not_matched`：`35`

### 6.1.1 后端瞬时失败窗口专项记录

截至当前累计观察窗口：

- `dense_failed_count > 0` 的窗口数：`1`
- `sparse_failed_count > 0` 的窗口数：`0`
- 异常窗口占比：`1 / 9`

已记录的异常窗口表现：

- `dense_failed_count = 48`
- `sparse_failed_count = 0`
- `rerank_hit_count = 0`
- `candidate_pool_below_min_threshold = 48`
- 目标命中集整体归零
- 误命中仍为 `0`

恢复情况：

- 紧随其后的下一次完整复跑已自动恢复到正常命中状态
- 当前没有看到异常窗口连续出现

### 6.1.2 最后观察窗口（3 次完整观察）

本轮将最后观察窗口固定为 `3` 次完整观察，结果如下：

- `run1`
  - `rerank_hit_count = 13`
  - `dense_failed_count = 0`
  - `sparse_failed_count = 0`
  - `fail_open_count = 0`
  - `latency avg = 300.924 ms`
  - `latency p95 = 317.043 ms`
  - `latency p99 = 325.816 ms`
- `run2`
  - `rerank_hit_count = 13`
  - `dense_failed_count = 0`
  - `sparse_failed_count = 0`
  - `fail_open_count = 0`
  - `latency avg = 303.952 ms`
  - `latency p95 = 316.446 ms`
  - `latency p99 = 319.692 ms`
- `run3`
  - `rerank_hit_count = 13`
  - `dense_failed_count = 0`
  - `sparse_failed_count = 0`
  - `fail_open_count = 0`
  - `latency avg = 310.335 ms`
  - `latency p95 = 329.705 ms`
  - `latency p99 = 346.974 ms`

最后观察窗口汇总：

- 命中集：`13 / 13 / 13`，完全一致
- 误命中：`0 / 0 / 0`
- 漏命中：`0 / 0 / 0`
- `global_disabled`：三次均正常
- `local_disabled`：三次均正常
- `timeout_drill`：三次均正常
- `dense_failed_count > 0`：`0` 次
- `sparse_failed_count > 0`：`0` 次
- `p95 mean = 321.065 ms`
- `p99 mean = 330.827 ms`

### 6.2 global disabled

- total queries：`48`
- rerank hit count：`0`
- rerank skip count：`48`
- policy reason：`rerank_globally_disabled`

### 6.3 local disabled

- total queries：`48`
- rerank hit count：`0`
- rerank skip count：`48`
- policy reason：`local_default_enablement_disabled`

### 6.4 timeout drill

- total queries：`48`
- rerank hit count：`0 / 0 / 0 / 0 / 0`
- rerank policy hit count：`13 / 13 / 13 / 13 / 13`
- rerank skip count：`35 / 35 / 35 / 35 / 35`
- fail-open count：`13 / 13 / 13 / 13 / 13`
- fail-open rate：`0.2708 / 0.2708 / 0.2708 / 0.2708 / 0.2708`
- timeout count：`13 / 13 / 13 / 13 / 13`
- policy reasons：
  - `local_default_enablement_matched`：`13`
  - `local_default_enablement_not_matched`：`35`

## 7. 结果解释

本轮验证结论：

1. 当前局部默认启用策略已经在真实灰度环境中稳定命中目标 query。
2. 当前目标 query 命中率为 `13 / 48 = 27.08%`。
3. 规则层面的正常窗口在 8 次完整观察中结果一致，说明命中 / 跳过 / 回退链路具备稳定性。
4. 全局关闭、局部关闭、超时 fail-open 均真实可验证。
5. 这次规则收紧后，之前观察到的两条误命中已经消失。

### 7.1 命中质量与覆盖范围

当前命中 query 仍主要集中在：

- 资质要求类
- 条款定位类
- 时间安排 / 商务条款 / 评分标准类招标 query

本轮复跑结果显示：

- 之前的误命中 `rq-018`、`rq-022` 已经消失
- 当前未再观察到非招标 query 被误命中
- 目标招标类 query 仍保持稳定命中

说明当前“必须由 request 侧 `source_type / route_type` 命中目标范围”的收紧方向是有效的。

当前收益范围与策略设计一致：

- 主要命中招标资料中的资质要求、时间安排、商务条款、评分标准类 query
- 不会对所有 query 全量执行 rerank
- 当前误命中已消失，但仍应继续在当前范围内观察，不应直接扩大启用范围

### 7.2 规则层与运行层分层观察

#### A. 规则层

当前规则层可以确认：

- `request` 侧 `source_type / route_type + 关键词` 的收紧规则已稳定生效
- 正常窗口下命中集保持同一组 `13` 条目标 query，不漂移
- 当前误命中继续为 `0`
- 正常窗口下未观察到新的漏命中边界样本

#### B. 运行层

当前运行层可以确认：

- 后端瞬时失败窗口仍然存在，但目前只观察到 `1` 次
- 该窗口会直接导致：
  - `dense_failed_count = 48`
  - 目标命中集临时整体归零
  - `candidate_pool_below_min_threshold = 48`
- 紧随其后的下一窗口已恢复正常，说明当前风险更像“瞬时波动”而不是“持续失效”
- 当前阶段的主要阻塞点已经从规则本身转移为检索后端瞬时失败窗口

## 8. 回滚演练结论

### 8.1 全局关闭

已验证：

- `RERANK_ENABLED=false` 时，policy reason 明确为 `rerank_globally_disabled`
- query 全部回 baseline / noop

### 8.2 局部关闭

已验证：

- `RERANK_DEFAULT_ENABLEMENT_ENABLED=false` 时，policy reason 明确为 `local_default_enablement_disabled`
- 目标 query 也不会执行 rerank

### 8.3 自动回退

代码与真实灰度脚本均已验证：

- timeout / provider error / 解析异常时统一 `failed_open`
- 本轮 `timeout_drill` 中：
  - policy hit count：`13`
  - fail-open count：`13`
  - timeout count：`13`
- trace 中保留 `error_type`、`fail_open`、`policy_reason`

## 9. Trace 复核结果

当前 trace 足以支撑灰度问题排查，至少可看出：

1. 是否命中局部默认启用规则
2. 命中的原因
3. 匹配的关键词
4. source_type / route_type 是否匹配
5. 候选数是否达到阈值
6. rerank 是否真正执行
7. 是否发生 `failed_open`
8. provider / model / timeout / error_type

## 10. 当前阶段结论

当前“局部默认启用 + 灰度 + 可快速回退”的策略已经在真实灰度环境中完成更长一点的稳定性观察。

当前可确认：

- 策略能命中目标 query
- 全局关闭可用
- 局部关闭可用
- timeout fail-open 可用
- trace 足以定位未命中与回退原因
- 收紧后误命中已消失
- 正常窗口中命中集保持不变

当前同时应明确：

- 大部分非目标 query 会稳定跳过；
- 当前未再观察到误命中；
- 正常窗口延迟落在约 `303ms avg / 326ms p95 / 380ms p99` 的观察区间；
- 异常窗口中没有 rerank 命中，延迟统计对 rerank 本身失去意义；
- 当前已确认存在 `1` 次后端瞬时失败窗口：`dense_failed_count=48`，导致全部 query 落到 `candidate_pool_below_min_threshold`，目标命中集临时归零；
- 紧随其后的窗口已恢复到正常状态，说明当前更值得关注的是检索后端瞬时波动，而不是局部默认启用规则漂移；
- 但仍缺少更长时间窗口和更接近真实流量的灰度观测数据。

## 11. 退出标准判定

基于最后观察窗口的 `3` 次完整观察，Phase 2.6 的退出标准判定如下：

### A. 规则层稳定：满足

- 命中集不漂移：满足
- 误命中保持为 `0`：满足
- 无新增漏命中边界样本：满足

### B. 回退机制稳定：满足

- `global_disabled` 正常：满足
- `local_disabled` 正常：满足
- `timeout_drill` 正常：满足
- fail-open 与 trace 行为符合预期：满足

### C. 延迟可接受：满足

- 最后观察窗口 `p95 = 317.043 / 316.446 / 329.705 ms`：满足当前标准
- 最后观察窗口 `p99 = 325.816 / 319.692 / 346.974 ms`：满足当前标准
- 未观察到继续恶化的长尾趋势：满足

### D. 后端异常窗口可控：满足

- 最后观察窗口内未再次出现 `dense_failed_count > 0`：满足
- 最后观察窗口内未出现 `sparse_failed_count > 0`：满足
- 历史上仅有 `1` 次已恢复的孤立异常窗口：可接受

## 12. 收口结论

Phase 2.6 可以正式收口。

当前收口依据：

1. 规则层已稳定。
2. 回退机制已稳定。
3. 最后观察窗口内延迟满足当前阶段标准。
4. 历史上的后端异常窗口未在最后观察窗口内重复出现，可视为当前阶段可控。

下一阶段建议名称：

- `Phase 2.7：局部默认启用运行基线收口与小流量运行准备`

该阶段应关注：

- 将当前 Phase 2.6 的结论沉淀为运行基线
- 准备更长期的小流量运行手册与观测面板
- 继续保持当前启用范围，不做范围扩大
