# Phase 2.17 Rerank Smoke Audit 与 dense/hybrid eval 扩展

## 1. 阶段目标

Phase 2.17 只做 Rerank Smoke Audit 与 dense/hybrid eval 扩展。

本阶段不改 retrieval contract，不改 memory kernel 主架构，不改 rerank 策略，不进入 rollout。

## 2. 当前 rerank 状态判断

### 2.1 provider 配置项

当前默认配置：

1. `rerank_provider=noop`
2. `rerank_enabled=false`
3. `rerank_default_enablement_enabled=false`
4. `rerank_default_enablement_source_types=tender`
5. `rerank_default_enablement_route_types=tender,tender_qa,tender_query`
6. `rerank_default_enablement_keywords=资质,要求,条款,截止,联合体,投标,招标,开标,答疑,评分,保证金`
7. `rerank_default_enablement_min_candidates=2`
8. `rerank_input_cap=30`
9. `aliyun_rerank_model=gte-rerank-v2`
10. `aliyun_rerank_timeout_ms=600`

### 2.2 触发条件

真实 rerank 只有同时满足以下条件才会进入 Aliyun provider：

1. `rerank_enabled=true`
2. `rerank_provider=aliyun`
3. `rerank_default_enablement_enabled=true`
4. 候选数量达到 `rerank_default_enablement_min_candidates`
5. query 命中配置关键词
6. request 侧 `filters.source_type` 命中配置 source type，或 request `route_type` 命中配置 route type

若不满足，则使用 `NoopReranker`，trace 中 `rerank_status=skipped`。

### 2.3 是否真实调用模型

当前代码具备 Aliyun Text Rerank adapter，真实调用路径为：

`/api/v1/services/rerank/text-rerank/text-rerank`

API key 优先级：

1. `ALIYUN_RERANK_API_KEY`
2. `ALIYUN_EMBEDDING_API_KEY` fallback

Phase 2.9d 曾完成首轮 provider smoke：embedding 与 rerank 真调用通过，rerank 使用 embedding key fallback。Phase 2.17 仍需重新审计当前环境下是否真实调用发生，而不是只复用历史结论。

### 2.4 fail-open 与 trace

已有可观测字段：

1. `rerank_status`
2. `rerank.provider`
3. `rerank.model`
4. `rerank.elapsed_ms`
5. `rerank.timeout_ms`
6. `rerank.fail_open`
7. `rerank.error_type`
8. `rerank.api_key_source`
9. `rerank.remote_request_id`
10. `rerank_policy.reason`
11. `rerank_policy.matched_keywords`
12. `rerank_policy.candidate_count`

Rerank provider 异常、timeout、缺 key、空候选、异常响应均应 fail-open 到 candidate pool，不应阻断 retrieval。

## 3. Rerank Smoke Audit 方案

### 3.1 样本范围

建议首轮 5 条真实 query：

1. 主标书：`总工期和关键节点有什么要求？`
2. 主标书：`施工总承包资质等级要求是什么？`
3. Excel：`投标总价和付款比例是什么？`
4. PPTX：`智慧建筑脑机系统这一页讲了什么？`
5. 会议纪要：`会议里有哪些行动项和风险？`

### 3.2 必须输出字段

每条 smoke 记录：

1. `case_id`
2. `document_id`
3. `query`
4. `rerank_status`
5. `rerank_provider`
6. `rerank_model`
7. `rerank_returned`
8. `rerank_latency_ms`
9. `fail_open`
10. `fail_open_reason`
11. `error_type`
12. `api_key_source`
13. `policy_reason`
14. `matched_keywords`
15. `candidate_count`
16. `result_document_ids`

### 3.3 通过标准

1. 目标 tender query 应能触发 policy matched，并在可用 key 下真实调用 provider。
2. Excel/PPTX/会议纪要 query 如果不满足当前局部默认启用条件，可以判定为合理 skipped，但必须 trace 清晰。
3. provider 失败时必须 `failed_open`，结果仍来自 candidate pool。
4. latency 与 timeout 必须可观测。
5. 不要求 rerank 排序优于 sparse/dense，只验证真实调用、跳过、fail-open 可诊断。

## 4. dense/hybrid eval 扩展方案

### 4.1 Phase 2.14 eval 扩展字段

建议在 Phase 2.14 API deterministic eval 中增加：

1. `required_dense_status`
2. `min_dense_returned`
3. `required_sparse_status`
4. `min_sparse_returned`
5. `required_candidate_pool_fields`
6. `forbidden_dense_document_ids`
7. `forbidden_hybrid_document_ids`

### 4.2 检查目标

1. dense 链路真实执行。
2. Qdrant 返回候选。
3. hybrid candidate pool 同时包含 dense / sparse 计数。
4. 结果 document_id 不漂移、不污染。
5. 不要求 dense 排名优于 sparse。
6. 不改变现有 eval 对 citation、trace、document scope 的断言。

### 4.3 首轮建议覆盖

1. 主标书基础信息 query。
2. 对比标书工期 query。
3. 答疑文件 query。
4. 交付标准旧版 query。
5. 交付标准新版 query。
6. 会议纪要 action / decision / risk query。

## 5. 非目标

1. 不调 rerank 策略。
2. 不改排序权重。
3. 不做 query rewrite。
4. 不做 rollout。
5. 不改变 retrieval contract。
6. 不改变 memory kernel 主架构。
7. 不要求 rerank 或 dense 在质量上立刻超过 sparse。

## 6. 最小实现结果

### 6.1 Rerank Smoke Audit runner

已新增 `scripts/phase217_rerank_smoke_audit.py`：

1. runner 仅通过进程内显式启用 `rerank_enabled=true`、`rerank_provider=aliyun`、`rerank_default_enablement_enabled=true` 执行 smoke，不改变默认配置。
2. 输出 JSON summary，包含 `total`、`executed`、`skipped`、`failed`、provider、model、returned、latency、fail-open、error_type、api_key_source 与 policy diagnostics。
3. 覆盖 5 条真实 query：主标书基础信息、主标书工期/关键节点、答疑文件临时性紧急工作、Excel structured query、会议纪要 action/decision/risk。

本地 live smoke 结果：

1. `total=5`
2. `passed=5`
3. `failed=0`
4. `executed=3`
5. `skipped=2`
6. `failed_open=0`

其中 3 条 tender 文本类 query 真实调用 `aliyun_text_rerank` / `gte-rerank-v2`，`api_key_source=ALIYUN_EMBEDDING_API_KEY`；Excel 与会议纪要因当前局部默认启用规则不匹配而 `skipped`，skip reason 可诊断。

### 6.2 Phase 2.14 dense/hybrid eval 扩展

已扩展 `scripts/phase214_regression_eval.py`：

1. `EvalCase` 支持 `required_dense_status`、`min_dense_returned`、`required_sparse_status`、`min_sparse_returned`、`required_candidate_pool_fields`。
2. `EvalResult` 新增 `failed_dense_hybrid_checks`。
3. 已在主标书、对比标书、答疑文件与会议纪要 smoke case 中检查 dense / sparse / candidate pool 字段。
4. 不要求 dense 排名优于 sparse，只验证 dense/hybrid 链路真实执行且 returned document_ids 不污染。

本地 live eval 结果：

1. `total=12`
2. `passed=11`
3. `failed=0`
4. `skipped=1`
5. `p50=16.291ms`
6. `p95=928.611ms`

`missing_alias_suppress_cli_only` 仍保持 CLI-only skipped；其余 API deterministic eval 与 dense/hybrid 扩展均通过。

### 6.3 测试结果

已通过：

```bash
uv run pytest tests/test_phase214_regression_eval.py tests/test_phase217_rerank_smoke_audit.py tests/test_rerank_hook.py tests/test_aliyun_reranker.py -q
```

结果：`26 passed`。

## 7. 当前建议

建议进入 Phase 2.17 Git baseline：

1. Rerank Smoke Audit runner 已可观测真实调用、合理 skipped 与 fail-open 结果。
2. Phase 2.14 eval 已覆盖 dense/hybrid 基本执行与无污染检查。
3. 后续若要做排序质量评测，应另起阶段，不应混入本阶段 smoke audit。
