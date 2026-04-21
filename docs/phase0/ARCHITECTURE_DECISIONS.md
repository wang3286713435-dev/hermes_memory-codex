# Hermes Memory Kernel 架构决策记录

## 目录

1. 文档目的
2. ADR-001：企业记忆必须内建为 Memory Kernel
3. ADR-002：主检索链路不依赖模型主动调用工具
4. ADR-003：动态检索上下文注入当前用户消息而非 system prompt
5. ADR-004：保留 MemoryManager 作为 Legacy Bridge
6. ADR-005：Hermes_memory 逻辑内核化、工程模块化
7. ADR-006：Phase 1.5 先接 BM25 与 Citation，不提前扩展 Dense/Rerank
8. ADR-007：企业知识主数据不进入 SessionDB
9. ADR-008：Citation 由 Kernel 生成，不交给模型自由生成
10. ADR-009：Phase 1.5 上下文注入顺序为临时实现，后续必须专项复核

## 1. 文档目的

本文档记录 Phase 0 阶段确认的关键架构决策，作为后续 Phase 1.5 / Phase 2 开发依据。

## 2. ADR-001：企业记忆必须内建为 Memory Kernel

### 决策

企业长期记忆系统应作为 Hermes 主仓库内建 `MemoryKernel` 子系统，而不是普通插件、外部 provider 或外挂服务。

### 原因

- 企业记忆需要参与 query routing、context building、retrieval orchestration、citation、governance、writeback。
- 这些能力位于请求主链路，不能依赖外围 hook 或模型主动调用。
- 权限过滤、版本治理、引用生成必须在模型回答前稳定执行。

### 可选方案

| 方案 | 评价 |
| --- | --- |
| 普通 plugin | 易接入，但生命周期弱，治理能力不足 |
| 外部 HTTP 服务 | 工程解耦，但 query-time 容易退化为外挂 |
| MemoryProvider 实现 | 兼容现有接口，但抽象不足以承载企业治理 |
| 内建 MemoryKernel | 符合目标，改造成本较高 |

### 最终方案

采用内建 MemoryKernel。

## 3. ADR-002：主检索链路不依赖模型主动调用工具

### 决策

企业知识检索应在模型调用前由 `MemoryKernel` 自动执行，不应等待模型选择 memory/search tool。

### 原因

- 企业 QA 需要稳定召回依据。
- 模型可能不调用工具或调用错误工具。
- 权限和 citation 需要前置。
- 评测系统需要稳定可重放的 retrieval trace。

### 暂不采纳方案

不采纳“把企业检索做成一个 search_memory tool，由模型自行决定是否调用”的方案。

## 4. ADR-003：动态检索上下文注入当前用户消息而非 system prompt

### 决策

动态 retrieval context 注入当前用户消息附近，类似当前 `build_memory_context_block()` 的模式；system prompt 只放静态说明。

### 原因

- Hermes 当前存在 system prompt cache。
- 动态检索结果写入 system prompt 会造成跨轮污染。
- 当前 memory provider prefetch 已采用当前用户消息注入方式，符合现有模式。

### 最终方案

`_build_system_prompt()` 只加入 kernel static guidance，`run_conversation()` API message 构造阶段注入 enterprise memory context block。

## 5. ADR-004：保留 MemoryManager 作为 Legacy Bridge

### 决策

保留 `agent/memory_manager.py` 与 `agent/memory_provider.py`，但不把企业 memory kernel 建成普通 provider。

### 原因

- Hermes 已有外部 memory provider 插件生态。
- 直接替换会破坏兼容性。
- `MemoryManager` 缺少 enterprise retrieval/citation/governance 抽象。

### 最终方案

`MemoryKernel` 与 `MemoryManager` 并存。`MemoryKernel` 是企业主链路，`MemoryManager` 是 legacy/external memory bridge。

## 6. ADR-005：Hermes_memory 逻辑内核化、工程模块化

### 决策

Hermes_memory 不应继续作为外部外挂系统发展。其核心能力应归位到 Hermes 内建 memory kernel；摄取、索引、存储 adapter 可保持工程模块化。

### 原因

- 查询主链路必须内核化。
- 文档摄取与索引适合后台服务化。
- 工程上完全揉成一个巨型文件会不可维护。

### 最终方案

采用“逻辑上内核化，工程上模块化”：

- Query-time kernel 在 Hermes 主仓库内建。
- Ingestion/indexing/storage 作为内部子系统或服务。
- 所有能力由 kernel 配置、治理和引用标准统一管理。

## 7. ADR-006：Phase 1.5 先接 BM25 与 Citation，不提前扩展 Dense/Rerank

### 决策

Phase 1.5 聚焦 Hermes 主链路接入、BM25 retrieval、metadata filter、citation，不扩展 dense/rerank/facts/OCR。

### 原因

- 当前最大风险是架构方向和主链路接入，不是算法丰富度。
- 提前扩展 dense/rerank 会放大外挂式架构返工。
- BM25 对中文企业文档、编号、项目名、合同号具有现实价值。

### 最终方案

Phase 1.5：内核接入优先。

Phase 2：再做 hybrid、rerank、facts、permission policy。

## 8. ADR-007：企业知识主数据不进入 SessionDB

### 决策

企业文档、版本、chunk、ACL、ingestion job 主数据不存入 Hermes `SessionDB`。

### 原因

- `SessionDB` 是会话存储，适合 messages、system_prompt、session metadata。
- 企业知识库需要 PostgreSQL、OpenSearch、对象存储等专用存储。
- 混入 SQLite 会造成扩展性、权限治理、索引、备份、迁移问题。

### 最终方案

`SessionDB` 保存 session trace、kernel trace 引用或 citation snapshot；企业知识主数据保留在企业知识存储。

## 9. ADR-008：Citation 由 Kernel 生成，不交给模型自由生成

### 决策

Citation payload 由 `CitationEngine` 基于检索命中生成，并随 result 返回。模型可使用 citation markers，但不能自由编造引用。

### 原因

- 企业回答需要可追溯。
- 模型生成引用容易幻觉。
- citation 需要包含 document、version、chunk、heading、page_range、source、permission context。

### 最终方案

`CitationEngine` 是 memory kernel 的核心模块。回答层只引用 kernel 提供的 citation id。

## 10. ADR-009：Phase 1.5 上下文注入顺序为临时实现，后续必须专项复核

### 决策

Phase 1.5 当前请求上下文的注入顺序定义为：

1. `memory kernel context`
2. `legacy memory_manager.prefetch_all()`
3. `plugin pre_llm_call context`

该顺序仅作为当前阶段的临时实现，用于完成内核接入闭环，不视为最终稳定架构结论。

### 原因

- Phase 1.5 的首要目标是将企业检索主链路接入 Hermes 核心请求路径。
- 当前 Hermes 已存在 legacy memory 与 plugin context 注入机制，完全重构其顺序与裁剪策略会扩大本阶段改造范围。
- 如果不显式记录该顺序的临时性质，后续容易将当前实现误当作最终规范。

### 必须专项复核的事项

- legacy memory 是否污染企业检索上下文
- plugin context 是否覆盖 memory kernel 约束
- token 超限时上下文裁剪优先级
- 最终上下文合并顺序规范

### 最终方案

当前保留该顺序作为 Phase 1.5 临时实现，并将“context 注入顺序检查”列为进入下一阶段前的明确待办。
