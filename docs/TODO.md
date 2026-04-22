# Hermes Memory 当前待办清单

## 1. Phase 2.1-Qdrant 未确认项

1. Qdrant 是否需要 `QDRANT_API_KEY`、以及 `api-key` header 是否生效尚未确认；当前仅验证了无鉴权的本地容器路径。
2. Dockerfile 依赖 `python:3.11-slim` 拉取在部分网络环境可能超时（docker.io oauth token timeout），导致 `docker compose build api` 失败；若团队主路径依赖容器构建，需准备镜像源/网络策略或提供替代运行方式。

## 2. 暂不推进事项

- 真实 `rerank` 模型接入
- `facts` 联查
- OCR
- 多 agent 协作
- 复杂权限策略
- 大规模 ingestion 改造

## 3. Phase 2.2 后续待办

1. 真实 reranker 模型尚未接入。当前仅完成 `NoopReranker` 与 rerank hook 结构，不能视为排序质量增强已完成；需在后续 rerank 实现阶段处理。
2. rerank 质量评测集尚未建立。当前只有最小评测入口，不能衡量真实召回排序收益；需在 evaluation 阶段补充标注样本与指标。
3. rerank 延迟、成本、超时策略尚未验证。当前仅验证 fail-open 行为，真实模型服务接入后需专项压测。
4. 真实 reranker adapter 尚未选型。下一阶段应先在 API 型 reranker 与轻量 cross-encoder 服务之间选择一条主路线，不应并行扩展多个 provider。
5. candidate pool 内部候选扩大策略尚未实现。当前仍沿用 request `top_k` 召回，后续若要提升 rerank 收益，应增加内部 candidate cap，但不能改变公开 `top_k` 语义。

## 4. Phase 2.3 待办

1. 当前黄金 query 已扩到 48 条，但样本仍以脱敏近真实评测语料为主，不是完整真实企业知识库；进入更大范围 rollout 前仍需补更大范围的真实业务 query 集。
2. rerank candidate 扩大策略尚未进入代码。当前只使用 `RERANK_INPUT_CAP` 截断，未实现 dense/sparse 内部 candidate target 扩大。
3. BGE / cross-encoder 只作为备选路线记录，当前不实现。
4. 当前 baseline vs experiment 已覆盖 48 条小规模样本，top-1 有提升且无回归，已足以支持“默认启用策略评估”，但仍不足以直接作为全局默认启用依据。
5. 默认启用实施前仍需补充 rollout policy 落地：按 query 类型灰度、超时阈值、成本观测和回退开关。
6. Phase 2.5 已落地局部默认启用规则，但当前只覆盖招标资料中的高收益 query；扩大范围前仍需更大规模真实 query 复测。
7. 需要补最小运行手册：灰度开关切换、timeout 观察、fail-open 监控与回滚步骤。
8. Phase 2.6 环境阻塞已解除：Docker daemon、Qdrant、OpenSearch 已恢复，灰度验证脚本可正常运行。
9. Phase 2.6 已修正灰度脚本的 request 上下文传递，当前局部默认启用可命中目标 query；后续应继续观察真实灰度下的 fail-open rate、p95/p99 与收益稳定性。
10. Phase 2.6 已完成退出标准判定并可收口：最后观察窗口的 3 次完整观察均满足规则层稳定、回退机制稳定、延迟可接受、后端异常窗口可控。后续重点转入下一阶段的运行基线收口与小流量运行准备，而不是继续开放式观察。
