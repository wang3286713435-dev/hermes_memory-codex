# Hermes Memory Kernel 改造点清单

## 目录

1. 文档目的
2. 推荐修改文件
3. 推荐新增模块
4. 推荐新增接口
5. 不建议修改区域
6. 高风险区域
7. Hermes_memory 合并边界
8. 实施注意事项

## 1. 文档目的

本文档列出将 Hermes_memory 从外挂式工程转向 Hermes 内建 memory kernel 所需的明确改造点、风险区域和边界策略。

## 2. 推荐修改文件

### 2.1 `run_agent.py`

推荐修改点：

1. 在 `AIAgent.__init__()` 中初始化 `self._memory_kernel`。
2. 在 `_build_system_prompt()` 中注入 memory kernel 静态说明。
3. 在 `run_conversation()` 中用户消息清洗后调用 `memory_kernel.start_turn()`。
4. 在 API messages 构造阶段注入 enterprise memory context block。
5. 在最终回答生成后调用 `memory_kernel.finish_turn()`。
6. 在 result dict 中加入 `citations`、`retrieval_trace`、`governance_trace`。

约束：

- 不应把 retrieval、citation、governance 具体实现直接写入 `run_agent.py`。
- `run_agent.py` 只负责调用 kernel façade。
- 动态检索结果不应写入 session cached system prompt。

### 2.2 `agent/memory_manager.py`

推荐修改点：

1. 增加与 `MemoryKernel` 的桥接说明或 adapter。
2. 明确该模块是 legacy/external provider manager。
3. 避免将企业知识检索逻辑继续塞入 `MemoryManager`。

### 2.3 `agent/memory_provider.py`

推荐修改点：

1. 保持兼容外部 memory provider。
2. 不将企业 memory kernel 实现为普通 `MemoryProvider`。
3. 后续可增加 deprecation 或 bridge 文档。

### 2.4 `hermes_cli/config.py`

推荐新增配置域：

```yaml
memory_kernel:
  enabled: true
  mode: enterprise
  retrieval:
    bm25_enabled: true
    dense_enabled: false
    rerank_enabled: false
    default_top_k: 8
    timeout_ms: 3000
  citation:
    required: true
  governance:
    permission_filter_required: true
  writeback:
    enabled: true
    auto_fact_write: false
```

### 2.5 `cli-config.yaml.example`

推荐同步新增 memory kernel 配置示例，明确：

- 默认 Phase 1.5 可启用 BM25
- dense/rerank/facts 默认标记为 TODO 或 disabled
- citation required
- permission filter required

### 2.6 `hermes_state.py`

推荐谨慎扩展：

- 新增 session-level metadata 保存 citation trace 可行。
- 不建议将企业文档、chunk、version、ACL 主数据放入 `SessionDB`。
- 若需要持久化 kernel trace，应新增独立表或 JSON metadata 字段，并提供迁移。

### 2.7 `model_tools.py`

推荐保持稳定。只有在需要显式暴露诊断工具或人工触发检索工具时才新增 schema。

### 2.8 `tools/registry.py`

不建议改 registry 核心逻辑。新增工具应通过现有 `registry.register()`。

## 3. 推荐新增模块

建议在 Hermes 主仓库新增：

```text
agent/memory_kernel/
  __init__.py
  kernel.py
  types.py
  query_router.py
  retrieval_orchestrator.py
  context_builder.py
  citation_engine.py
  governance.py
  writeback.py
  session_bridge.py
  config.py
  adapters/
    __init__.py
    opensearch_adapter.py
    postgres_adapter.py
    vector_adapter.py
  ingestion/
    __init__.py
    parser.py
    chunker.py
    versioning.py
```

Phase 1.5 不必一次实现所有 adapter，但目录和边界应先稳定。

## 4. 推荐新增接口

### 4.1 `MemoryKernel`

```python
class MemoryKernel:
    def start_turn(self, turn_context: TurnContext) -> KernelTurnResult: ...
    def build_context_block(self, result: KernelTurnResult) -> str: ...
    def finish_turn(self, turn_context: TurnContext, response: str, result: KernelTurnResult) -> KernelWritebackResult: ...
    def shutdown(self) -> None: ...
```

### 4.2 `QueryRouter`

```python
class QueryRouter:
    def route(self, request: QueryRouteRequest) -> QueryPlan: ...
```

### 4.3 `RetrievalOrchestrator`

```python
class RetrievalOrchestrator:
    def retrieve(self, plan: QueryPlan, context: RetrievalContext) -> RetrievalResult: ...
```

### 4.4 `CitationEngine`

```python
class CitationEngine:
    def build(self, retrieval_result: RetrievalResult) -> list[Citation]: ...
```

### 4.5 `GovernanceHooks`

```python
class GovernanceHooks:
    def before_retrieval(self, context: TurnContext, plan: QueryPlan) -> GovernanceDecision: ...
    def after_response(self, context: TurnContext, response: str, citations: list[Citation]) -> GovernanceDecision: ...
```

## 5. 不建议修改区域

| 区域 | 原因 |
| --- | --- |
| `tools/registry.py` 核心注册/dispatch 逻辑 | 已是稳定中心能力，改动会影响全部工具 |
| `model_tools.py` 主工具 dispatch 行为 | 容易破坏工具调用、plugin hook、tool result 兼容性 |
| 各入口层重复加 memory 逻辑 | 会造成 CLI/ACP/Gateway/API 行为不一致 |
| `plugins/memory/` 作为企业内核主体 | 会退化为外挂式记忆系统 |
| system prompt 缓存策略 | 动态检索上下文写入缓存会导致版本污染和上下文串扰 |
| `SessionDB` 承载企业知识库 | SQLite session store 不适合作为企业文档知识层主存储 |

## 6. 高风险区域

| 风险区域 | 风险说明 | 控制策略 |
| --- | --- | --- |
| `run_agent.py` | 文件体量大，包含大量模型/工具/流式细节 | 只增加 façade 调用，核心逻辑下沉到新模块 |
| Prompt 注入 | 可能污染用户消息或破坏模型行为 | 使用独立 enterprise memory context block |
| system prompt cache | 动态上下文写入会导致跨轮污染 | 只放静态 kernel guidance |
| Tool 循环 | governance 若接入过深会影响全部工具 | Phase 1.5 先只做 retrieval governance |
| SessionDB 迁移 | 老会话兼容风险 | 新表/metadata 增量迁移，避免改老字段语义 |
| 权限过滤 | 若在 retrieval 后过滤，可能泄漏命中信息 | metadata filter 和 ACL filter 必须前置 |
| Citation | 如果只由模型生成，无法保证可追溯 | citation payload 由 kernel 生成并返回 |
| Context compression | 可能压缩掉 citation anchors | citation snapshot 独立保存 |

## 7. Hermes_memory 合并边界

### 7.1 应并入 Hermes 主体的能力

- Query Router
- Retrieval Orchestrator
- Context Builder
- Citation Engine
- Governance Hooks
- Memory Writeback
- Session Memory Bridge

### 7.2 可作为内部子系统保留的能力

- FastAPI ingestion 管理接口
- 文档上传
- 文档解析
- chunking
- OpenSearch/PostgreSQL/MinIO adapter
- ingestion job
- evaluation job

### 7.3 不应保留的形态

- Agent 通过外部 HTTP 插件临时调用 Hermes_memory
- 模型主动调用 `search_memory` tool 才触发企业知识检索
- 权限过滤由检索结果返回后再手工筛选
- citation 由模型自由编造

## 8. 实施注意事项

1. 先做 Phase 0 文档收口，再做 Phase 1.5 内核接入。
2. Phase 1.5 的目标不是扩展更多检索算法，而是把 query-time 主链路放入 Hermes。
3. 任何新增 retrieval/facts/rerank 功能，都必须通过 `MemoryKernel` 进入主请求链路。
4. 保留 legacy memory provider 兼容性，避免破坏已有 Hermes 用户。
5. 对 Hermes 原版升级冲突最高的文件是 `run_agent.py`，因此 patch 必须小而集中。

