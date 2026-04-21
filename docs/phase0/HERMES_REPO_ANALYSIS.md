# Hermes 仓库结构分析

## 目录

1. 文档目的
2. 仓库概览
3. 核心目录职责
4. 关键文件说明
5. 当前系统结构总结
6. 可复用能力盘点
7. 不确定项说明

## 1. 文档目的

本文档用于在 Phase 0 阶段基于 Hermes 主仓库真实代码结构，梳理 Hermes 当前架构、核心模块职责、启动入口、配置加载、Agent 主流程、Prompt、Tool、Memory、Session、Response、日志与 Hook 机制的位置。

本文档的结论用于指导 Hermes_memory 从“外挂式工程”转向 Hermes 内建 memory kernel 的后续改造。

## 2. 仓库概览

实际 Hermes 主仓库位置：

```text
/Users/Weishengsu/.hermes/hermes-agent
```

当前 Hermes_memory 工程位置：

```text
/Users/Weishengsu/Hermes_memory
```

Hermes 主仓库是一个 Python 工程，`pyproject.toml` 中定义了以下主要入口：

| 入口 | 指向 | 说明 |
| --- | --- | --- |
| `hermes` | `hermes_cli.main:main` | CLI 主入口 |
| `hermes-agent` | `run_agent:main` | Agent 直接运行入口 |
| `hermes-acp` | `acp_adapter.entry:main` | ACP 协议入口 |

核心形态为：多个入口最终构造或复用 `run_agent.AIAgent`，再调用 `AIAgent.run_conversation()` 完成一次用户请求。

## 3. 核心目录职责

| 目录/文件 | 职责 | Phase 0 判断 |
| --- | --- | --- |
| `run_agent.py` | Agent 主运行时。包含 `AIAgent`、Prompt 构造、模型调用、工具循环、memory provider 生命周期、最终结果组装 | 企业 memory kernel 的主接入点 |
| `agent/` | Agent 辅助模块，包括 memory、context、prompt、模型元数据、压缩等 | 应新增内建 memory kernel 子包 |
| `agent/memory_manager.py` | 当前外部 memory provider 管理器，负责 prefetch、tool schema、sync、生命周期 hook | 可作为 legacy bridge，不应等同于企业 memory kernel |
| `agent/memory_provider.py` | Memory provider 抽象接口 | 可复用接口思想，但企业内核不应实现为普通 provider 插件 |
| `tools/` | 内置工具实现与注册 | 应复用工具注册机制，但核心检索不应依赖模型主动调用工具 |
| `tools/registry.py` | 中央 ToolRegistry，负责工具注册、schema 获取、dispatch | 直接复用；避免大改 |
| `model_tools.py` | 将工具注册表桥接到模型 tool schemas，并执行普通工具调用 | 复用；仅在需要新增内核工具时轻量接入 |
| `toolsets.py` | 工具集分组、核心工具列表 | 复用；避免把企业记忆完全包装成可选 toolset |
| `tools/memory_tool.py` | 当前内置文件型 memory 工具，读写 `MEMORY.md` 和 `USER.md` | 应保留为 curated/session-like memory，不承担企业知识检索 |
| `hermes_state.py` | SQLite 会话库，保存 session、messages、FTS、system_prompt、token/cost 等 | 可扩展保存 kernel trace/citation，但 schema 改造高风险 |
| `hermes_cli/` | CLI、配置、插件、安装、界面相关逻辑 | 需要新增配置项；不应在 CLI 层实现 memory kernel |
| `hermes_cli/config.py` | 默认配置、加载、迁移、校验 | 需要新增 enterprise memory kernel 配置 |
| `hermes_cli/plugins.py` | 插件系统、插件 hook、插件工具注册 | 可用于扩展，不应作为企业 memory kernel 的主承载 |
| `plugins/memory/` | 外部 memory provider 插件 | 不应作为企业级内核记忆的最终位置 |
| `gateway/` | Gateway、多平台消息接入、事件 hook、平台适配 | 应保持入口层职责，不应复制 memory 逻辑 |
| `gateway/hooks.py` | Gateway 事件 hook 系统 | 可作为事件观测/审计补充 |
| `acp_adapter/` | ACP 协议服务和 session 管理 | 继续复用 `AIAgent.run_conversation()`；不应单独实现 memory |

## 4. 关键文件说明

### 4.1 `run_agent.py`

`run_agent.py` 是当前 Hermes Agent 的主控文件。关键位置如下：

| 位置 | 说明 |
| --- | --- |
| `class AIAgent` | Agent 主类 |
| `AIAgent.__init__()` | 初始化模型、工具、memory provider、context engine、session、回调等 |
| `_build_system_prompt()` | 系统 Prompt 构建中心 |
| `run_conversation()` | 单次请求主流程 |
| `_invoke_tool()` | 特殊工具与普通工具调用分发 |
| `_execute_tool_calls*()` | 并发/串行工具调用执行 |
| `shutdown_memory_provider()` / `commit_memory_session()` | memory provider 会话结束与提交 |

当前 memory 相关位置：

| 代码位置 | 当前职责 |
| --- | --- |
| `from agent.memory_manager import build_memory_context_block, sanitize_context` | 引入 memory 上下文封装与输入清洗 |
| `self._memory_store` | 文件型内置 memory，来自 `tools.memory_tool.MemoryStore` |
| `self._memory_manager` | 外部 memory provider 管理器 |
| `_build_system_prompt()` | 注入 `MEMORY.md`、`USER.md`、memory provider system prompt |
| `run_conversation()` | 调用 provider `on_turn_start()`、`prefetch_all()`，并将 prefetch 结果注入当前用户消息 |
| final response 后 | 调用 `sync_all()` 和 `queue_prefetch_all()` |

### 4.2 `agent/memory_manager.py`

当前 `MemoryManager` 提供：

- `sanitize_context()`
- `build_memory_context_block()`
- `add_provider()`
- `initialize_all()`
- `build_system_prompt()`
- `prefetch_all()`
- `queue_prefetch_all()`
- `sync_all()`
- `get_all_tool_schemas()`
- `handle_tool_call()`
- `on_turn_start()`
- `on_session_end()`
- `on_pre_compress()`
- `on_memory_write()`
- `on_delegation()`

该模块适合作为已有 memory provider 的兼容层，但不适合作为企业长期记忆系统的完整内核。原因是它的抽象是 provider/plugin 级别，缺少 query routing、retrieval orchestration、citation、governance、structured facts、versioning、permission filtering 等核心企业能力。

### 4.3 `agent/memory_provider.py`

`MemoryProvider` 是当前外部 memory provider 的抽象接口，主要方法包括：

- `initialize()`
- `system_prompt_block`
- `prefetch()`
- `queue_prefetch()`
- `sync_turn()`
- `get_tool_schemas()`
- `handle_tool_call()`
- `shutdown()`
- `on_turn_start()`
- `on_session_end()`
- `on_pre_compress()`
- `on_memory_write()`
- `on_delegation()`

该抽象可复用其生命周期设计，但企业 memory kernel 不应降级为某个 provider 实现。

### 4.4 `tools/registry.py` 与 `model_tools.py`

`tools/registry.py` 定义中央工具注册表 `ToolRegistry`，负责工具注册、schema 获取、dispatch、alias、toolset 管理。

`model_tools.py` 负责：

- `get_tool_definitions()`：从 registry 获取模型可见工具 schema
- `handle_function_call()`：执行普通工具调用，并触发 plugin hook

企业 memory kernel 可以复用工具机制暴露少量诊断或显式查询工具，但主检索链路不应依赖模型主动选择 tool。核心原因是企业知识召回必须在回答前稳定发生，并受权限、版本、引用和评测约束治理。

### 4.5 `hermes_state.py`

`SessionDB` 使用 SQLite 保存会话、消息、system prompt、FTS、模型配置、token、cost、标题等。它是当前 session store 和 session search 的基础。

企业 memory kernel 可在未来保存：

- 每轮 query route 结果
- retrieval trace
- citation snapshot
- governance decision
- memory writeback event

但不建议直接把企业文档知识库、chunk、版本、权限矩阵塞入 `SessionDB`。企业长期知识层应使用 PostgreSQL/OpenSearch/对象存储等独立企业级存储。

### 4.6 `hermes_cli/config.py`

`DEFAULT_CONFIG` 和 `load_config()` 位于该文件。当前配置已经包含 memory、plugins、platform toolsets、context 等配置域。

后续应新增 `enterprise_memory` 或 `memory_kernel` 配置域，包含：

- enabled
- storage
- retrieval
- governance
- citation
- writeback
- timeout
- fallback_policy

### 4.7 `hermes_cli/plugins.py`

插件系统支持 hook，包括：

- `pre_llm_call`
- `post_llm_call`
- `pre_tool_call`
- `post_tool_call`
- `transform_tool_result`
- `on_session_start`
- `on_session_end`
- `on_session_finalize`
- `on_session_reset`

这些机制适合作为扩展、观测、集成点，但不适合作为企业 memory kernel 的主实现方式。将企业长期记忆做成插件会导致其生命周期、权限治理、上下文构建和 citation 变成外围能力，不符合“内核型 Hermes”的目标。

## 5. 当前系统结构总结

Hermes 当前结构可以概括为：

```text
入口层
  CLI / ACP / Gateway / API
      |
      v
Agent 主运行时
  run_agent.AIAgent
      |
      +-- 配置加载 hermes_cli.config
      +-- SessionDB hermes_state.py
      +-- Prompt 构建 _build_system_prompt()
      +-- Tool schema 构建 model_tools.get_tool_definitions()
      +-- Tool dispatch model_tools.handle_function_call()
      +-- 内置 memory tools.memory_tool.MemoryStore
      +-- 外部 memory provider agent.memory_manager.MemoryManager
      +-- Context compression / context engine
      |
      v
模型调用与工具循环
      |
      v
Response / session persistence / hooks / callbacks
```

当前 memory 是“多点接入”：

- 静态 curated memory 注入 system prompt
- 外部 provider prefetch 注入当前用户消息
- 外部 provider 工具暴露给模型
- final response 后执行 sync/writeback

这为企业 memory kernel 提供了可复用插入点，但现有结构尚未形成企业级长期记忆内核。

## 6. 可复用能力盘点

| 能力 | 当前位置 | 复用建议 |
| --- | --- | --- |
| Agent 主生命周期 | `run_agent.AIAgent.run_conversation()` | 必须复用，memory kernel 应接入此链路 |
| Prompt 构建 | `AIAgent._build_system_prompt()` | 复用静态说明，动态知识上下文不应写入缓存 system prompt |
| 当前用户消息动态注入 | `run_conversation()` 中 API message 构造处 | 适合注入 retrieval context 与 citation hints |
| Tool registry | `tools/registry.py` | 复用，不重复造工具注册系统 |
| Tool dispatch | `model_tools.py` | 复用，核心检索不依赖模型主动调用 |
| Session store | `hermes_state.py` | 复用会话记录；企业知识存储另建 |
| Memory provider lifecycle | `agent/memory_manager.py` / `agent/memory_provider.py` | 作为 legacy bridge 或扩展接口，不作为企业内核主体 |
| Plugin hook | `hermes_cli/plugins.py` | 作为扩展和观测，不作为核心 memory 主路径 |
| Gateway hook | `gateway/hooks.py` | 用于事件审计和平台观测 |
| Config system | `hermes_cli/config.py` | 新增 memory kernel 配置域 |
| Context engine | `agent/context_engine.py` | 与 kernel context builder 协同，避免压缩丢失引用信息 |

## 7. 不确定项说明

以下内容需要在后续实施前进一步确认：

1. CLI 交互主循环在 `hermes_cli.main` 与 `cli.py` 中的完整路径尚未逐行审计；已确认最终会进入 `AIAgent.run_conversation()`。
2. Gateway 各平台适配器未全部逐行审计；已确认 `gateway/run.py` 与 `gateway/platforms/api_server.py` 存在 `run_conversation()` 调用。
3. 各模型 provider 适配分支未全部逐行审计；本阶段重点确认 memory、prompt、tool 和 response 主链路。
4. `plugins/memory/` 下各 provider 实现未全部审计；已审计公共抽象与加载方式。
5. Context engine 的具体运行策略需在 Phase 1.5 设计 citation 与 compression 保真时继续审计。

