# Phase 2.2 Rerank 前置结构

## 1. 范围

Phase 2.2 只固定 rerank 前置结构，不接入真实 reranker 模型。

本阶段不改变 retrieval contract 主语义，不新增 retrieval mode，不推进 facts、OCR、多 agent、复杂权限，也不修改 Hermes 主仓库主链路。

## 2. Candidate Pool

Candidate pool 是 Hermes_memory retrieval service 内部结构，位于 dense/sparse/hybrid 召回之后、rerank hook 之前。

职责：

- 汇总 dense 与 sparse 候选
- hybrid 模式下按 `chunk_id` 去重
- 记录候选来源分布
- 为 rerank hook 提供统一候选输入

Candidate pool 不作为 ContextBuilder 或 citation 输入。下游仍只消费最终 `SearchResponse.results`。

## 3. Rerank Hook

rerank hook 固定在以下位置：

1. dense / sparse retrieval
2. hybrid merge
3. candidate pool build
4. rerank hook
5. final results
6. context_builder / citation

## 4. Rerank Contract

`RerankRequest` 包含：

- `query`
- `candidates`
- `top_k`
- `retrieval_mode`
- `trace_id`

`RerankOutcome` 包含：

- `results`
- `status`
- `provider`
- `trace`

## 5. NoopReranker

当前实现仅为可诊断 noop：

- 不调用模型
- 不改变 score-desc 排序语义
- 返回 `status=skipped`
- trace 中记录 provider、reason_if_skipped、elapsed_ms、fail_open、candidate_count_in、candidate_count_out、top_k、retrieval_mode

## 6. Fail-open

rerank 异常时必须 fail-open：

- 捕获异常
- 记录 `rerank_status=failed_open`
- 返回 candidate pool 的 score-desc top_k
- 不影响 dense/sparse/hybrid 检索结果输出

## 7. 当前未完成

- 真实 reranker 模型
- rerank 模型服务配置
- rerank 质量评测集
- rerank latency / cost 评估
- rerank 与权限策略的联合治理
