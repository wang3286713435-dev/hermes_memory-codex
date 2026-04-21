# Phase 1.5 / Phase 1.5b Closeout

## 1. 收尾范围

本次收尾覆盖 Hermes enterprise memory kernel 项目的 Phase 0、Phase 1、Phase 1.5 与 Phase 1.5b 主线成果。

本轮只进行基线固化、Git 提交边界整理与 GitHub 备份，不开发 Phase 2 新功能。

## 2. Git 提交边界

### 2.1 Hermes 主仓库

纳入基线的内容包括：

- Hermes `AIAgent.run_conversation()` 内核级 memory kernel 接入。
- `agent/memory_kernel/` 内建模块。
- request-scoped context merge policy。
- memory kernel 配置项。
- AIAgent 级无模型集成测试。

排除在本轮之外的内容包括：

- 与 Phase 1.5 / Phase 1.5b 无关的向量实验文件。
- 锁文件与依赖变更中未确认属于 memory kernel 主线的部分。
- 本地缓存、虚拟环境、测试缓存和系统生成物。

### 2.2 Hermes_memory 工程

纳入基线的内容包括：

- Phase 0 分析文档。
- PRD、技术方案、路线图与架构决策。
- Phase 1 工程骨架。
- 文档摄取、解析、chunking、retrieval、citation 与 memory kernel 子系统雏形。
- 数据模型、migration、运行配置与本地开发编排。
- Phase 1.5b fallback query simplification 测试。
- Phase 1.5 baseline audit。

排除在本轮之外的内容包括：

- `.venv*`
- `.pytest_cache/`
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.egg-info/`
- `.DS_Store`
- IDE 缓存和其他本地生成物。

## 3. GitHub 备份目标

Hermes 主仓库备份 remote：

`git@github.com:wang3286713435-dev/hermes_main.git`

Hermes_memory remote：

`git@github.com:wang3286713435-dev/hermes_memory-codex.git`

## 4. Tag 规划

Hermes 主仓库：

- `phase-1.5-memory-kernel-baseline`
- `phase-1.5b-closed`

Hermes_memory：

- `phase-0-complete`
- `phase-1.5-baseline`
- `phase-1.5b-closed`

## 5. 当前基线说明

当前基线确认以下能力已经完成：

- Hermes memory kernel 已作为内建核心层接入 Hermes 主请求链路。
- Query-time retrieval 已成为 pre-model 行为，不依赖模型主动调用 tool。
- 动态 enterprise memory context 只注入当前请求，不写入缓存 system prompt。
- context merge policy 已从临时顺序收口为最小稳定策略。
- AIAgent 级无模型集成测试已覆盖实际注入顺序、降级行为与 result payload。
- Hermes_memory 数据库 fallback 已具备最小长问句关键词降级能力。

## 6. 进入 Phase 2 的条件

当前具备进入 Phase 2 的工程前置条件：

- Phase 0 分析与架构文档已经收口。
- Phase 1 / Phase 1.5 / Phase 1.5b 主线代码与测试已整理为可追踪基线。
- 无关向量实验改动未纳入本轮基线。
- 本地生成物已通过 `.gitignore` 排除。
- GitHub 备份目标已明确。

## 7. 进入 Phase 2 前仍然不做的事项

以下事项不属于本次收尾，也不应在未进入 Phase 2 设计拆解前直接推进：

- dense retrieval adapter 正式实现。
- rerank。
- facts 联查。
- 复杂权限策略。
- OCR。
- 多 agent 协作。
- citation 文本渲染增强。
- 将实验性向量 tool 路径混入 memory kernel 主线。

## 8. Phase 2 起点建议

Phase 2 建议从最小 hybrid retrieval 与 metadata filter 起步。

推荐顺序：

1. 先固化 retrieval request / filter / result contract。
2. 接入 metadata filter，确保权限与版本治理后续可挂载。
3. 再实现 dense retrieval adapter，并与现有 BM25 fallback 形成可观测 hybrid 路径。
4. 最后引入 rerank。

不建议一开始直接做复杂 facts 联查、OCR、多 agent 或完整权限策略。
