# Phase 1.5 / Phase 1.5b Baseline Audit

## 1. 当前基线说明

本文档记录 Hermes 企业级 memory kernel 项目在进入 Phase 2 前的基线审计结果。

审计目标是确认 Phase 1.5 与 Phase 1.5b 的工程变更边界，区分以下内容：

- 应作为 memory kernel 主线保留的改动。
- Phase 0 文档与 Phase 1 工程骨架中已有的项目资产。
- 历史遗留、实验性或暂不纳入当前主线的 dirty files。
- 进入 Phase 2 前需要人工确认或排除的边界项。

本次审计不新增业务能力，不引入 dense retrieval、rerank、facts 联查、复杂权限、OCR、多 agent 或 citation 文本渲染增强。

## 2. 检查范围

### 2.1 Hermes 主仓库

仓库路径：

`/Users/Weishengsu/.hermes/hermes-agent`

检查方式：

- `git status --short`
- `git diff --name-only`
- `git ls-files --others --exclude-standard`
- 关键文件内容抽查

### 2.2 Hermes_memory 工程

工程路径：

`/Users/Weishengsu/Hermes_memory`

检查方式：

- 文件树扫描
- 关键目录与关键实现文件抽查
- 基于项目阶段与文件职责进行归类

说明：`/Users/Weishengsu/Hermes_memory` 当前不是 Git 仓库，无法通过 `git status` 区分 tracked / untracked / modified。本文档对 Hermes_memory 的归类基于实际文件职责、阶段来源与当前工作内容判断。

## 3. Hermes 主仓库变更清单

### 3.1 已修改文件

| 文件 | 阶段归属 | 建议 | 说明 |
|---|---|---|---|
| `run_agent.py` | Phase 1.5 / Phase 1.5b | 保留 | 在 `AIAgent.run_conversation()` 中接入 memory kernel pre-model retrieval，并在当前请求用户消息中通过 merge policy 注入上下文。 |
| `hermes_cli/config.py` | Phase 1.5 | 保留 | 新增 `memory_kernel` 默认配置。 |
| `cli-config.yaml.example` | Phase 1.5 | 保留 | 新增 `memory_kernel` 示例配置。 |
| `pyproject.toml` | 无关 / 待排除 | 暂不纳入 | 新增 `chromadb>=1.5.8`，与 Phase 1.5/1.5b 明确约束不符。当前阶段未实现 dense retrieval，不应引入该依赖作为主线基线。 |
| `uv.lock` | 无关 / 待排除 | 暂不纳入 | 由 `chromadb` 或其他依赖变更引入大量锁文件变化，同时包含 `atroposlib`、`tinker`、`yc-bench` 等版本来源变化，超出 memory kernel Phase 1.5/1.5b 范围。 |

### 3.2 新增文件

| 文件 | 阶段归属 | 建议 | 说明 |
|---|---|---|---|
| `agent/memory_kernel/__init__.py` | Phase 1.5 | 保留 | Hermes 内建 memory kernel 包入口。 |
| `agent/memory_kernel/config.py` | Phase 1.5 | 保留 | memory kernel 配置对象与配置加载。 |
| `agent/memory_kernel/interfaces.py` | Phase 1.5 | 保留 | Query route、retrieval item、citation、kernel request/result 等核心接口。 |
| `agent/memory_kernel/router.py` | Phase 1.5 | 保留 | 最小 query router。 |
| `agent/memory_kernel/orchestrator.py` | Phase 1.5 | 保留 | pre-model retrieval orchestration。 |
| `agent/memory_kernel/context_builder.py` | Phase 1.5 | 保留 | request-scoped enterprise memory context 构建。 |
| `agent/memory_kernel/citation_engine.py` | Phase 1.5 | 保留 | 最小 citation 结构归一化。 |
| `agent/memory_kernel/kernel.py` | Phase 1.5 | 保留 | memory kernel façade，组织 route / retrieve / context / citation。 |
| `agent/memory_kernel/adapters/__init__.py` | Phase 1.5 | 保留 | adapter 包入口。 |
| `agent/memory_kernel/adapters/hermes_memory_adapter.py` | Phase 1.5 | 保留 | Hermes 主仓库到 Hermes_memory 现有 retrieval 能力的最小 adapter。 |
| `agent/memory_kernel/merge_policy.py` | Phase 1.5b | 保留 | 最小稳定 context merge policy。 |
| `tests/agent/test_memory_kernel_integration.py` | 测试 / Phase 1.5b | 保留 | AIAgent 级无模型集成测试。 |
| `tools/vector_db_tool.py` | 无关 / 待排除 | 暂不纳入 | 独立 DashScope + SQLite 向量工具，属于模型主动 tool 路径，与当前 memory kernel pre-model retrieval 路线冲突。 |
| `vector_store.py` | 无关 / 待排除 | 暂不纳入 | 独立轻量向量存储实验，不属于 Phase 1.5/1.5b 内核接入基线。 |

### 3.3 直接相关文件

以下文件属于 memory kernel 主线，应作为 Phase 2 起点的一部分保留：

- `run_agent.py`
- `hermes_cli/config.py`
- `cli-config.yaml.example`
- `agent/memory_kernel/**`
- `tests/agent/test_memory_kernel_integration.py`

### 3.4 无关或暂不纳入文件

以下文件不建议纳入 Phase 1.5 / Phase 1.5b 基线：

- `pyproject.toml`
- `uv.lock`
- `tools/vector_db_tool.py`
- `vector_store.py`

原因：

- 当前阶段明确不做 dense retrieval。
- 当前主线设计要求 query-time retrieval 由 memory kernel 在模型调用前执行，不走模型主动调用 tool。
- 这些文件引入 DashScope/SQLite/Chroma 方向的实验性向量检索路径，容易造成架构边界混乱。
- `uv.lock` 包含大量与本项目无关的依赖解析变化，提交风险较高。

## 4. Hermes_memory 工程变更归类

由于 Hermes_memory 当前不是 Git 仓库，本节按工程职责和阶段来源归类。

### 4.1 Phase 0 文档分析相关

| 文件 | 建议 | 说明 |
|---|---|---|
| `docs/phase0/HERMES_REPO_ANALYSIS.md` | 保留 | Hermes 仓库结构分析。 |
| `docs/phase0/HERMES_CALL_FLOW.md` | 保留 | Hermes 请求调用链分析。 |
| `docs/phase0/MEMORY_KERNEL_INTEGRATION_PLAN.md` | 保留 | memory kernel 内核级集成方案。 |
| `docs/phase0/PATCH_POINTS.md` | 保留 | 改造点与风险点清单。 |
| `docs/phase0/DEVELOPMENT_GUIDE.md` | 保留 | 阶段定义与开发边界。 |
| `docs/phase0/ARCHITECTURE_DECISIONS.md` | 保留 | Phase 0 / Phase 1.5 架构决策。 |
| `docs/phase0/TODO.md` | 保留 | 当前上下文注入顺序检查与后续待办。 |

### 4.2 项目立项与总体设计文档

| 文件 | 建议 | 说明 |
|---|---|---|
| `docs/PRD.md` | 保留 | 项目需求文档。 |
| `docs/TECHNICAL_DESIGN.md` | 保留 | 技术方案文档。 |
| `docs/ROADMAP.md` | 保留 | 分阶段路线图。 |
| `docs/ARCHITECTURE_DECISION_RECORD.md` | 保留 | 关键技术选型与取舍记录。 |

### 4.3 Phase 1 / Phase 1.5 可复用工程资产

| 文件或目录 | 建议 | 说明 |
|---|---|---|
| `app/memory_kernel/**` | 保留 | Hermes_memory 侧 memory kernel 雏形，当前由 Hermes 主仓库 adapter 复用。 |
| `app/services/retrieval/service.py` | 保留 | Phase 1 retrieval 服务，Phase 1.5b 已增强数据库 fallback query simplification。 |
| `app/services/citation/**` | 保留 | citation 标准化能力。 |
| `app/services/ingestion/**` | 保留 | 文档接入骨架。 |
| `app/services/parsing/**` | 保留 | 文档解析骨架。 |
| `app/services/chunking/**` | 保留 | 结构化 chunking 骨架。 |
| `app/services/indexing/**` | 保留 | OpenSearch indexing 骨架。 |
| `app/models/**` | 保留 | 文档、版本、chunk、citation、retrieval log 等数据模型。 |
| `app/schemas/**` | 保留 | API 与服务层 schema。 |
| `migrations/versions/0001_phase1_core_schema.py` | 保留 | Phase 1 核心 schema migration。 |
| `tests/test_retrieval_fallback.py` | 保留 | Phase 1.5b fallback query simplification 单元测试。 |

### 4.4 运行与开发环境资产

| 文件或目录 | 建议 | 说明 |
|---|---|---|
| `.env.example` | 保留 | 本地与部署配置模板。 |
| `README.md` | 保留 | 当前工程运行说明。 |
| `Dockerfile` | 保留 | 服务容器构建。 |
| `docker-compose.yml` | 保留 | PostgreSQL / OpenSearch / MinIO 等本地依赖编排。 |
| `pyproject.toml` | 保留 | Hermes_memory 工程依赖定义。 |
| `alembic.ini`、`migrations/**` | 保留 | 数据库迁移配置。 |

### 4.5 本地生成物与应排除项

以下内容不应进入项目基线或后续提交：

- `.DS_Store`
- `docs/.DS_Store`
- `.pytest_cache/**`
- `.venv-integration/**`
- `__pycache__/**`
- `*.pyc`
- `hermes_memory.egg-info/**`

说明：

- `.venv-integration` 是 Phase 1.5 / 1.5b 联调时创建的共享运行时环境，仅作为本机验证资产，不属于项目源代码。
- `hermes_memory.egg-info` 是本地打包/安装生成物，应由 `.gitignore` 排除。
- 缓存与字节码文件不应纳入任何阶段基线。

## 5. 阶段归属分类

### 5.1 Phase 0 文档分析相关

- `docs/phase0/HERMES_REPO_ANALYSIS.md`
- `docs/phase0/HERMES_CALL_FLOW.md`
- `docs/phase0/MEMORY_KERNEL_INTEGRATION_PLAN.md`
- `docs/phase0/PATCH_POINTS.md`
- `docs/phase0/DEVELOPMENT_GUIDE.md`
- `docs/phase0/ARCHITECTURE_DECISIONS.md`
- `docs/phase0/TODO.md`

### 5.2 Phase 1.5 内核接入相关

- Hermes 主仓库：
  - `run_agent.py`
  - `hermes_cli/config.py`
  - `cli-config.yaml.example`
  - `agent/memory_kernel/__init__.py`
  - `agent/memory_kernel/config.py`
  - `agent/memory_kernel/interfaces.py`
  - `agent/memory_kernel/router.py`
  - `agent/memory_kernel/orchestrator.py`
  - `agent/memory_kernel/context_builder.py`
  - `agent/memory_kernel/citation_engine.py`
  - `agent/memory_kernel/kernel.py`
  - `agent/memory_kernel/adapters/__init__.py`
  - `agent/memory_kernel/adapters/hermes_memory_adapter.py`
- Hermes_memory：
  - `app/memory_kernel/**`
  - `app/services/retrieval/**`
  - `app/services/citation/**`

### 5.3 Phase 1.5b 行为收口相关

- Hermes 主仓库：
  - `agent/memory_kernel/merge_policy.py`
  - `run_agent.py` 中 request-scoped context merge policy 接入
- Hermes_memory：
  - `app/services/retrieval/service.py` 中 `_simplify_query_terms()` 与数据库 fallback 查询增强

### 5.4 测试相关

- Hermes 主仓库：
  - `tests/agent/test_memory_kernel_integration.py`
- Hermes_memory：
  - `tests/test_retrieval_fallback.py`

### 5.5 文档相关

- `docs/PRD.md`
- `docs/TECHNICAL_DESIGN.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE_DECISION_RECORD.md`
- `docs/phase0/**`
- `docs/PHASE15_BASELINE_AUDIT.md`

### 5.6 无关 / 待排除改动

- Hermes 主仓库：
  - `pyproject.toml`
  - `uv.lock`
  - `tools/vector_db_tool.py`
  - `vector_store.py`
- Hermes_memory 本地生成物：
  - `.DS_Store`
  - `docs/.DS_Store`
  - `.pytest_cache/**`
  - `.venv-integration/**`
  - `__pycache__/**`
  - `*.pyc`
  - `hermes_memory.egg-info/**`

## 6. 提交边界风险

### 6.1 是否存在无关 dirty files

存在。

Hermes 主仓库中的以下文件不属于当前 memory kernel 主线：

- `pyproject.toml`
- `uv.lock`
- `tools/vector_db_tool.py`
- `vector_store.py`

这些文件与向量检索实验或依赖解析有关，不应混入 Phase 1.5 / Phase 1.5b 基线提交。

### 6.2 是否存在同一文件混入无关改动

当前已确认：

- `run_agent.py` 的 diff 主要集中在 memory kernel 初始化、pre-model retrieval、context merge policy、result payload、finish_turn hook，属于本项目主线。
- `hermes_cli/config.py` 和 `cli-config.yaml.example` 的 diff 仅包含 `memory_kernel` 配置，属于本项目主线。
- `pyproject.toml` 和 `uv.lock` 的改动不属于本项目当前阶段，应排除。

需要注意：

- `run_agent.py` 是 Hermes 核心长文件，后续升级原版 Hermes 时极易冲突。建议 Phase 2 前将 memory kernel 接入点保持小而集中，并在文档中记录插入位置。

### 6.3 后续合并高冲突区域

高冲突区域包括：

- `run_agent.py`
  - `AIAgent.__init__()`
  - `_build_system_prompt()`
  - `AIAgent.run_conversation()`
  - result payload 组装区域
- `hermes_cli/config.py`
  - `DEFAULT_CONFIG`
- `cli-config.yaml.example`
  - 配置模板区域
- `uv.lock`
  - 锁文件体积大，且当前包含无关依赖变更，不建议纳入本阶段。

### 6.4 是否应拆分提交

建议拆分提交。

推荐提交边界：

1. `docs: add phase0 and phase15 baseline docs`
   - `docs/PRD.md`
   - `docs/TECHNICAL_DESIGN.md`
   - `docs/ROADMAP.md`
   - `docs/ARCHITECTURE_DECISION_RECORD.md`
   - `docs/phase0/**`
   - `docs/PHASE15_BASELINE_AUDIT.md`

2. `feat(memory-kernel): add Hermes core memory kernel integration`
   - `agent/memory_kernel/**`
   - `run_agent.py`
   - `hermes_cli/config.py`
   - `cli-config.yaml.example`

3. `test(memory-kernel): add request context and fallback tests`
   - `tests/agent/test_memory_kernel_integration.py`
   - `tests/test_retrieval_fallback.py`

4. `fix(retrieval): improve database fallback query simplification`
   - `app/services/retrieval/service.py`

不建议纳入上述提交：

- `pyproject.toml`
- `uv.lock`
- `tools/vector_db_tool.py`
- `vector_store.py`
- 本地缓存、虚拟环境、egg-info、`.DS_Store`

## 7. 验证记录

Phase 1.5b 复核时已完成以下验证：

- Hermes_memory fallback 单元测试：
  - `2 passed`
- Hermes 主仓库 AIAgent 级无模型集成测试：
  - `3 passed`
- 语法检查：
  - `py_compile` 通过
- 额外 SQLite fallback 长问句验证：
  - `database_fallback 1 chunk-1`

验证结论：

- context merge policy 已落地并被 AIAgent 级测试覆盖。
- kernel disabled / retrieval unavailable 不破坏普通对话。
- 数据库 fallback 对长问句已具备最小关键词降级能力。

## 8. 是否适合作为 Phase 2 起点

当前具备进入 Phase 2 的技术前置条件，但尚未形成完全干净的提交基线。

进入 Phase 2 前应先完成以下整理：

1. 从 Phase 1.5 / Phase 1.5b 基线中排除 Hermes 主仓库的无关向量实验改动：
   - `pyproject.toml`
   - `uv.lock`
   - `tools/vector_db_tool.py`
   - `vector_store.py`

2. 确认 Hermes_memory 是否需要初始化为 Git 仓库或纳入统一 monorepo 管理。

3. 清理或确保忽略本地生成物：
   - `.venv-integration/**`
   - `.pytest_cache/**`
   - `__pycache__/**`
   - `*.pyc`
   - `hermes_memory.egg-info/**`
   - `.DS_Store`

4. 将 Phase 1.5 / Phase 1.5b 主线改动按推荐提交边界拆分。

完成以上整理后，可以将当前基线作为 Phase 2 起点。

## 9. 需要人工确认的边界项

| 项目 | 需要确认的问题 | 默认建议 |
|---|---|---|
| `pyproject.toml` 中 `chromadb` 依赖 | 是否来自其他并行开发任务，是否必须保留 | 暂不纳入 Phase 1.5/1.5b 基线 |
| `uv.lock` 大量依赖变化 | 是否由其他任务生成，是否已有独立目的 | 暂不纳入 Phase 1.5/1.5b 基线 |
| `tools/vector_db_tool.py` | 是否为其他实验性 memory tool | 暂不纳入当前 memory kernel 主线 |
| `vector_store.py` | 是否为其他实验性向量存储 | 暂不纳入当前 memory kernel 主线 |
| Hermes_memory 是否 Git 化 | 是否需要独立版本控制或并入 Hermes 主仓库 | 建议先初始化版本控制或明确纳入主仓库策略 |
| `.venv-integration` | 是否保留作为本机联调环境 | 可保留在本机，但不得进入提交基线 |

## 10. 基线结论

Phase 1.5 / Phase 1.5b 的核心目标已经完成：

- Hermes memory kernel 已内建接入 `AIAgent.run_conversation()`。
- Query-time retrieval 已成为 pre-model 行为。
- 动态 retrieval context 仅注入当前请求，不写入缓存 system prompt。
- context merge policy 已从临时顺序收口为最小稳定策略。
- AIAgent 级无模型集成测试已覆盖实际注入顺序与降级行为。
- 数据库 fallback 已具备最小长问句关键词降级能力。

但当前工作区还不是完全干净的 Phase 2 起点。

建议结论：

- 可以确认 Phase 1.5 / Phase 1.5b 功能基线成立。
- 不建议在排除无关 dirty files 前直接进入 Phase 2。
- 建议先完成提交边界整理，再进入 Phase 2 的 hybrid retrieval、rerank、facts、permissions 等能力建设。
