# Hermes 请求调用链分析

## 目录

1. 文档目的
2. 请求入口
3. 单次请求生命周期
4. Prompt / Tool / Memory / Response 顺序
5. 关键函数与模块定位
6. Memory Kernel 可插入点
7. 不确定项说明

## 1. 文档目的

本文档描述 Hermes 当前一次用户请求从进入系统到生成回答的真实调用链，并明确 memory kernel 应插入的请求前、中、后阶段。

## 2. 请求入口

Hermes 当前存在多个入口，但核心收敛点是 `run_agent.AIAgent.run_conversation()`。

| 入口 | 关键位置 | 调用链结论 |
| --- | --- | --- |
| CLI | `hermes_cli.main:main` | CLI 入口最终构造或复用 `AIAgent` 并调用 `run_conversation()` |
| Direct Agent | `run_agent:main` | 直接进入 Agent 运行流程 |
| ACP | `acp_adapter/server.py` 的 `HermesACPServer.prompt()` | 明确调用 `agent.run_conversation()` |
| Gateway | `gateway/run.py` | 存在多处 `agent.run_conversation()` 调用 |
| API Server | `gateway/platforms/api_server.py` | 存在 `agent.run_conversation()` 调用 |

因此，企业 memory kernel 不应分别写入 CLI、ACP、Gateway、API 层，而应进入 `AIAgent` 主链路。

## 3. 单次请求生命周期

### 3.1 入口层

入口层负责：

- 接收用户输入
- 解析 session 标识
- 准备 conversation history
- 创建或获取 `AIAgent`
- 将请求传递给 `AIAgent.run_conversation()`

以 ACP 为例，`acp_adapter/server.py` 的 `prompt()` 方法会：

1. 取得 `SessionState`
2. 提取用户文本
3. 处理 slash command
4. 设置 tool、thinking、approval、message callbacks
5. 调用 `agent.run_conversation(user_message=user_text, conversation_history=state.history, task_id=session_id)`
6. 将结果写回 session history
7. 输出最终 response

### 3.2 Agent 初始化阶段

`AIAgent.__init__()` 负责初始化：

- 模型配置
- session 信息
- callback
- tool definitions
- valid tool names
- 内置 `MemoryStore`
- 外部 `MemoryManager`
- memory provider tool schemas
- context compressor / context engine
- platform / gateway metadata

当前外部 memory provider 初始化逻辑包括：

1. 读取配置中的 `memory.provider`
2. 通过 `plugins.memory.load_memory_provider()` 加载 provider
3. 创建 `MemoryManager`
4. 将 provider 加入 manager
5. 调用 `initialize_all()`
6. 将 provider tool schemas 添加到模型工具列表

### 3.3 请求开始阶段

`run_conversation()` 开始后执行：

1. 清洗当前用户消息中的 memory context 泄漏标记
2. 复制 `conversation_history`
3. 追加当前用户消息
4. 加载或构建 system prompt
5. 根据 session 状态决定是否缓存或复用 system prompt
6. 执行可能的 compression preflight
7. 调用 plugin `pre_llm_call`
8. 调用 memory provider `on_turn_start()`
9. 调用 memory provider `prefetch_all()`

### 3.4 Prompt 和上下文构建阶段

`_build_system_prompt()` 负责构建静态 system prompt，主要层次包括：

1. Agent identity
2. tool guidance
3. model/tool use guidance
4. 用户传入 system message
5. 内置 `MEMORY.md`
6. 内置 `USER.md`
7. 外部 memory provider system prompt
8. skills prompt
9. context files prompt
10. timestamp / session / model / provider 信息
11. environment hints

动态 memory prefetch 不写入 system prompt，而是在 API message 构造时注入当前用户消息。

### 3.5 模型调用阶段

在构造发送给模型的 messages 时，当前逻辑会：

1. 放入 system prompt
2. 转换 conversation messages
3. 对当前用户消息追加 memory prefetch block
4. 对当前用户消息追加 plugin `pre_llm_call` 返回的上下文
5. 调用模型 provider API

这一阶段是企业 retrieval context 和 citation hints 的最佳动态注入点。

### 3.6 Tool 调用阶段

模型返回 tool calls 后，Hermes 进入工具循环：

1. `_execute_tool_calls*()` 根据策略并发或串行执行工具
2. `_invoke_tool()` 处理特殊工具
3. 普通工具进入 `model_tools.handle_function_call()`
4. `model_tools.handle_function_call()` 通过 `ToolRegistry.dispatch()` 调用具体工具
5. plugin `pre_tool_call` / `post_tool_call` / `transform_tool_result` 参与工具生命周期
6. tool result 回填给模型继续推理

特殊工具包括：

- `memory`
- `session_search`
- `todo`
- `clarify`
- `delegate_task`
- context engine tools
- memory provider tools

企业 memory kernel 的主检索不应放在“模型选择某个 memory tool 后才执行”的路径中。主检索必须在模型回答前稳定执行。

### 3.7 最终回答阶段

当模型生成最终回答后：

1. 组装 `final_response`
2. 计算 token / cost / timing
3. 保存 messages
4. 调用 memory provider `sync_all(original_user_message, final_response)`
5. 调用 memory provider `queue_prefetch_all(original_user_message)`
6. 触发 session end / hooks / callbacks
7. 返回 result dict 给入口层

Memory writeback 的推荐接入点位于 final response 后、session result 返回前。

## 4. Prompt / Tool / Memory / Response 顺序

当前顺序可抽象为：

```text
用户请求
  |
  v
入口层获取 session / history
  |
  v
AIAgent.run_conversation()
  |
  +-- sanitize_context()
  +-- messages append current user message
  +-- build or reuse system prompt
  +-- compression preflight
  +-- plugin pre_llm_call
  +-- memory_manager.on_turn_start()
  +-- memory_manager.prefetch_all()
  |
  v
API messages 构造
  |
  +-- system prompt
  +-- conversation history
  +-- current user message
        +-- memory context block
        +-- plugin context block
  |
  v
模型调用
  |
  +-- final answer
  或
  +-- tool calls
        +-- _invoke_tool()
        +-- model_tools.handle_function_call()
        +-- ToolRegistry.dispatch()
        +-- tool results
        +-- 下一轮模型调用
  |
  v
最终回答
  |
  +-- memory_manager.sync_all()
  +-- memory_manager.queue_prefetch_all()
  +-- session persistence
  +-- result 返回
```

## 5. 关键函数与模块定位

| 能力 | 文件 | 关键函数/类 |
| --- | --- | --- |
| Agent 主类 | `run_agent.py` | `AIAgent` |
| 单次请求 | `run_agent.py` | `AIAgent.run_conversation()` |
| System prompt | `run_agent.py` | `AIAgent._build_system_prompt()` |
| 特殊工具调用 | `run_agent.py` | `_invoke_tool()` |
| 工具 schema | `model_tools.py` | `get_tool_definitions()` |
| 普通工具调用 | `model_tools.py` | `handle_function_call()` |
| 工具注册 | `tools/registry.py` | `ToolRegistry` |
| 文件型 memory | `tools/memory_tool.py` | `MemoryStore` |
| 外部 memory 管理 | `agent/memory_manager.py` | `MemoryManager` |
| memory provider 抽象 | `agent/memory_provider.py` | `MemoryProvider` |
| Session store | `hermes_state.py` | `SessionDB` |
| 配置 | `hermes_cli/config.py` | `DEFAULT_CONFIG`, `load_config()` |
| 插件 hook | `hermes_cli/plugins.py` | plugin hook manager |
| Gateway hook | `gateway/hooks.py` | `HookRegistry` |

## 6. Memory Kernel 可插入点

| 阶段 | 插入点 | 建议接入方式 |
| --- | --- | --- |
| Agent 初始化 | `AIAgent.__init__()` | 初始化 `MemoryKernel`，加载配置、客户端、策略 |
| System prompt 构建 | `_build_system_prompt()` | 注入静态 kernel guidance，不注入动态检索结果 |
| 请求清洗后 | `run_conversation()` 中 `original_user_message` 确定后 | 调用 `QueryRouter.route()` 和 governance pre-check |
| 模型调用前 | API messages 构造前 | 调用 `RetrievalOrchestrator.retrieve()` 与 `ContextBuilder.build()` |
| 当前用户消息注入 | 当前 memory prefetch block 附近 | 注入 enterprise memory context block |
| 工具执行前 | `_invoke_tool()` 或 `model_tools.handle_function_call()` 前 | 可选接入 governance hooks，Phase 1.5 后实施 |
| 最终回答后 | `sync_all()` 附近 | 调用 `MemoryWriteback.capture_turn()` |
| 返回 result 前 | result dict 组装处 | 写入 citations / retrieval trace / governance trace |

## 7. 不确定项说明

1. 不同模型 provider 的 API message 细节需在实现 citation block 时继续逐个验证。
2. Gateway 多平台入口是否携带完整 user identity、tenant、permission context，需要进一步审计平台适配层。
3. Session persistence 的 exact write timing 需要在引入 citation snapshot 前进一步验证，避免 citation 与 message 不一致。

