# Memory Kernel 内核级集成方案

## 目录

1. 文档目的
2. 核心结论
3. 设计原则
4. 总体架构
5. 模块职责
6. 请求流设计
7. Phase 1.5 当前上下文注入顺序说明
8. 数据流设计
9. 与 Hermes_memory 的关系
10. 集成方式
11. 推荐结论

## 1. 文档目的

本文档定义企业长期记忆系统如何从独立 Hermes_memory 工程，升级为 Hermes 内建 memory kernel，并深度参与 query routing、context building、retrieval orchestration、citation generation、governance 和 memory writeback。

## 2. 核心结论

企业长期记忆系统不应作为 Hermes 的普通插件、外部 provider 或模型可选工具存在。

推荐方案是：

1. 在 Hermes 主仓库新增内建子系统 `agent/memory_kernel/`。
2. 在 `AIAgent.__init__()` 中初始化 `MemoryKernel`。
3. 在 `AIAgent.run_conversation()` 的主请求链路中显式调用 kernel。
4. 将 Hermes_memory 当前文档摄取、chunking、OpenSearch、citation 能力归位为 kernel 依赖的内部服务模块。
5. 保持“逻辑上内核化，工程上模块化”：主链路内建，存储、索引、解析、检索实现模块化。

## 3. 设计原则

### 3.1 不能只做纯向量检索

企业长期记忆不能只依赖 vector database，原因包括：

- 企业查询常包含编号、合同号、项目名、客户名、金额、日期、版本号，BM25/sparse search 更稳定。
- 纯向量检索难以保证权限过滤先于召回。
- 纯向量检索难以解释命中原因和生成可追溯 citation。
- 版本治理、增量更新、结构化事实查询不是向量库职责。
- 向量相似度不能替代结构化 metadata filter、rerank 和 policy enforcement。
- 企业场景更担心“检索不到、答无依据、版本混乱、权限失控”，不是单纯上下文窗口不足。

### 3.2 企业长期记忆至少包含五层

| 层级 | 说明 |
| --- | --- |
| 文档知识层 | 文档、版本、chunk、source、citation、索引 |
| 结构化事实层 | 企业事实、实体、关系、指标、时间有效性 |
| 会话记忆层 | 用户偏好、项目上下文、历史任务状态、对话摘要 |
| 检索层 | query rewrite、metadata filter、BM25、dense、hybrid、rerank |
| 权限治理层 | tenant、user、role、resource ACL、审计、策略执行 |

向量数据库只是检索层的一部分，不是完整记忆系统。

## 4. 总体架构

```text
Hermes Entrypoints
  CLI / ACP / Gateway / API
        |
        v
run_agent.AIAgent
        |
        +-- MemoryKernel
        |     +-- QueryRouter
        |     +-- GovernanceHooks
        |     +-- RetrievalOrchestrator
        |     |     +-- BM25 Retriever
        |     |     +-- Dense Retriever
        |     |     +-- Metadata Filter
        |     |     +-- Reranker
        |     +-- ContextBuilder
        |     +-- CitationEngine
        |     +-- StructuredFactsAccessLayer
        |     +-- SessionMemoryBridge
        |     +-- MemoryWriteback
        |
        +-- Existing MemoryManager
        |     +-- Legacy / external memory providers
        |
        +-- ToolRegistry / ModelTools
        +-- SessionDB
        +-- ContextEngine
        |
        v
Model Provider
```

## 5. 模块职责

### 5.1 `MemoryKernel`

内建企业记忆总协调器，职责：

- 读取 kernel 配置
- 接收当前 turn 上下文
- 调用 query router
- 调用 governance pre-check
- 协调 retrieval
- 构建注入模型的 context block
- 生成 citation payload
- 执行 memory writeback
- 输出 retrieval/governance/citation trace

### 5.2 `QueryRouter`

职责：

- 判断查询类型：知识问答、事实查询、会话回忆、任务执行、混合查询
- 决定是否需要检索
- 决定检索范围：文档知识、结构化事实、会话记忆
- 生成 query plan

执行阶段：请求清洗后，模型调用前。

### 5.3 `RetrievalOrchestrator`

职责：

- 执行 metadata filter
- 调用 BM25/sparse retriever
- 调用 dense retriever
- 合并结果
- 调用 rerank
- 输出标准化 retrieval results

Phase 1.5 应先保证 BM25 + metadata filter + citation 稳定；dense 与 rerank 可在 Phase 2 完善。

### 5.4 `ContextBuilder`

职责：

- 将 retrieval results 转换为模型可消费的 context block
- 控制 token budget
- 去重与合并相邻 chunk
- 保留 citation markers
- 避免污染用户原始输入

执行位置：API messages 构造前，注入当前用户消息。

### 5.5 `CitationEngine`

职责：

- 将 chunk 命中转成标准 citation
- 保留 document、version、chunk、heading、page_range、source、score
- 生成回答引用所需的 stable citation id
- 在 result dict 中返回 citation payload

### 5.6 `GovernanceHooks`

职责：

- 权限上下文解析
- tenant/user/role/resource 过滤
- 检索前 ACL filter
- 回答前 citation 可见性校验
- 审计事件生成

Phase 1.5 先实现接口和基础过滤；Phase 2 接入完整权限策略。

### 5.7 `MemoryWriteback`

职责：

- 记录用户 query、answer、citation、retrieval trace
- 将可沉淀的会话信息写入会话记忆
- 将人工确认或高置信事实写入结构化事实层
- 避免未经确认的模型输出自动污染企业知识库

### 5.8 `StructuredFactsAccessLayer`

职责：

- 提供结构化事实查询接口
- 支持实体、指标、关系、时间有效性
- 与文档检索结果合并为统一 context

Phase 2 再实现实际 facts 联查。

### 5.9 `SessionMemoryBridge`

职责：

- 连接 `SessionDB`、现有 `MemoryStore`、外部 `MemoryManager`
- 对齐会话历史、用户偏好、项目上下文
- 防止 legacy memory 与 enterprise memory 重复注入或冲突

## 6. 请求流设计

```text
run_conversation()
  |
  +-- sanitize_context()
  +-- append current user message
  +-- build/reuse system prompt
  |
  +-- memory_kernel.start_turn()
        +-- QueryRouter.route()
        +-- GovernanceHooks.before_retrieval()
        +-- RetrievalOrchestrator.retrieve()
        +-- ContextBuilder.build()
        +-- CitationEngine.build()
  |
  +-- legacy plugin pre_llm_call
  +-- legacy memory_manager.prefetch_all()
  |
  +-- construct API messages
        +-- system prompt
        +-- conversation history
        +-- current user message
              +-- enterprise memory context block
              +-- legacy memory prefetch block
              +-- plugin context block
  |
  +-- model/tool loop
  |
  +-- final response
  |
  +-- memory_kernel.finish_turn()
        +-- GovernanceHooks.after_response()
        +-- MemoryWriteback.capture()
        +-- audit trace
  |
  +-- legacy memory_manager.sync_all()
  +-- return result with citations
```

## 7. Phase 1.5 当前上下文注入顺序说明

Phase 1.5 当前请求上下文的注入顺序为：

1. `memory kernel context`
2. `legacy memory_manager.prefetch_all()`
3. `plugin pre_llm_call context`

该顺序用于完成当前阶段的最小内核接入闭环，不视为最终稳定结论。

后续必须专项检查以下问题：

- legacy memory 是否污染企业检索上下文
- plugin context 是否覆盖 memory kernel 约束
- token 超限时上下文裁剪优先级
- 最终上下文合并顺序规范

在上述问题完成专项检查前，不应将当前注入顺序固化为长期接口规范。

## 8. 数据流设计

### 7.1 Query-time 数据流

```text
User Query
  -> QueryPlan
  -> Permission Context
  -> Filtered Retrieval Request
  -> Retrieval Results
  -> Reranked Results
  -> Context Blocks
  -> Citation Payload
  -> Model Input
  -> Answer + Citations + Trace
```

### 7.2 Ingestion 数据流

```text
Document Source
  -> Parser
  -> Cleaner
  -> Version Resolver
  -> Structured Chunker
  -> PostgreSQL Metadata
  -> Object Storage
  -> OpenSearch BM25 Index
  -> Vector Index
  -> Ingestion Audit
```

Ingestion 可以保持为独立服务或后台 worker，但其查询侧必须由 Hermes 内建 `MemoryKernel` 调用。

## 9. 与 Hermes_memory 的关系

当前 Hermes_memory 已形成文档上传、解析、chunking、OpenSearch 检索、citation 等能力雏形。推荐归位方式：

| Hermes_memory 模块 | 归位建议 |
| --- | --- |
| FastAPI 上传接口 | 可保留为内部管理/摄取 API，不作为 Agent 查询主路径 |
| 文档解析 | 并入 memory kernel ingestion 子系统 |
| chunking | 并入 memory kernel indexing 子系统 |
| OpenSearch 检索 | 作为 `RetrievalOrchestrator` 的 retriever adapter |
| citation | 并入 `CitationEngine` |
| 数据模型 | 企业长期知识存储保留 PostgreSQL，不进入 Hermes `SessionDB` |
| memory_kernel prototype | 迁入 Hermes 主仓库 `agent/memory_kernel/` 并重构为内建模块 |

## 10. 集成方式

### 9.1 应驻留 Hermes 主仓库的模块

- `agent/memory_kernel/kernel.py`
- `agent/memory_kernel/query_router.py`
- `agent/memory_kernel/retrieval_orchestrator.py`
- `agent/memory_kernel/context_builder.py`
- `agent/memory_kernel/citation_engine.py`
- `agent/memory_kernel/governance.py`
- `agent/memory_kernel/writeback.py`
- `agent/memory_kernel/session_bridge.py`
- `agent/memory_kernel/types.py`

### 9.2 可保持相对独立的模块

- 文档摄取 API
- 后台 ingestion worker
- OpenSearch/PostgreSQL/MinIO adapter
- OCR pipeline
- admin console
- offline evaluation jobs

这些模块可以作为内部子系统或独立进程部署，但必须由 Hermes memory kernel 统一治理，而不是作为普通插件松散接入。

## 11. 推荐结论

推荐采用“主链路内建 + 子系统模块化”的方案：

1. 在 Hermes 主仓库新增 `agent/memory_kernel/`。
2. 保留 `MemoryManager` 作为 legacy memory provider bridge。
3. 在 `run_agent.AIAgent` 中显式调用 `MemoryKernel`。
4. 动态检索上下文注入当前用户消息，不写入缓存 system prompt。
5. citation、retrieval trace、governance trace 随 result 返回。
6. Hermes_memory 当前能力逐步迁入或被 kernel adapter 调用。
7. Phase 1.5 前暂停新增 dense/rerank/facts/复杂权限实现，先完成内核接入框架和主链路稳定性。
8. 在进入下一阶段前，必须完成 context 注入顺序专项检查并形成稳定合并规范。
