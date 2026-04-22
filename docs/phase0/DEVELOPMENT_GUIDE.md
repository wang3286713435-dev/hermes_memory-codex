# Hermes Memory Kernel 开发指南

## 目录

1. 文档目的
2. 阶段定义
3. 当前暂停事项
4. 可继续推进事项
5. Phase 1.5 当前上下文注入顺序约束
6. 阶段交付物
7. 阶段依赖关系
8. 验收标准
9. 当前优先级建议
10. 下一步开发顺序

## 1. 文档目的

本文档用于重构 Hermes_memory 的阶段规划，使项目从“外挂式长期记忆服务”转向“企业内核型魔改版 Hermes”。

## 2. 阶段定义

### 2.1 Phase 0：Hermes 结构分析与内核集成设计

目标：

- 理解 Hermes 主仓库真实结构
- 明确请求调用链
- 明确 memory kernel 插入点
- 明确 Hermes 与 Hermes_memory 边界
- 修正开发路线
- 输出正式工程文档

Phase 0 不新增业务能力代码。

### 2.2 Phase 1：最小知识链路闭环

真实定位：

- 建立文档上传、解析、chunking、存储、BM25 检索、citation 的最小闭环
- 验证企业知识层基础数据模型
- 为内核接入提供可调用能力

Phase 1 可以作为内部子系统开发，但不代表最终架构已经内核化。

### 2.3 Phase 1.5：Memory Kernel 主链路接入

目标：

- 在 Hermes 主仓库新增 `agent/memory_kernel/`
- 在 `AIAgent` 主链路接入 kernel
- 实现 QueryRouter、RetrievalOrchestrator、ContextBuilder、CitationEngine 的最小版
- 将 Phase 1 的 BM25 检索能力接入 Agent query-time
- 返回 citation payload
- 保留 legacy MemoryManager 兼容

Phase 1.5 是从外挂式工程转为内核型 Hermes 的关键阶段。

### 2.4 Phase 2：企业治理与混合检索增强

目标：

- dense retrieval
- hybrid search
- rerank
- permission control
- structured facts access
- evaluation
- retrieval trace
- audit logs
- version-aware retrieval

Phase 2 不应在 Phase 1.5 主链路稳定前提前展开。

### 2.5 Phase 3：企业化运营与系统扩展

目标：

- 多企业系统接入
- 后台管理
- OCR
- 公众号全量采集
- 招标资料专项 pipeline
- 多租户治理
- 可视化评测
- 生命周期治理
- 灰度发布与回滚

## 3. 当前暂停事项

以下事项应暂停，直到 Phase 0 文档收口且 Phase 1.5 集成方案确认：

- dense retrieval 实现
- vector adapter 完整实现
- rerank 实现
- facts 联查实现
- 复杂 permission policy
- OCR
- 多 agent 协作
- 复杂后台管理功能
- 将 Hermes_memory 继续做成独立外挂服务的 query-time 能力

## 4. 可继续推进事项

以下事项可以继续，但必须服务于内核化路线：

- 修复 Phase 1 最小闭环 bug
- 补齐 ingestion/retrieval/citation 的接口稳定性
- 增加最小测试和样例验证
- 明确 API schema
- 编写 adapter，使 Hermes memory kernel 可以调用现有能力
- 准备 OpenSearch/PostgreSQL/MinIO 本地验证环境

## 5. Phase 1.5 当前上下文注入顺序约束

Phase 1.5 当前请求上下文的注入顺序为：

1. `memory kernel context`
2. `legacy memory_manager.prefetch_all()`
3. `plugin pre_llm_call context`

该顺序是 Phase 1.5 的临时实现，用于完成 Hermes 主链路内建接入，不视为最终稳定结论。

在继续推进后续开发前，必须专项检查以下事项：

- legacy memory 是否污染企业检索上下文
- plugin context 是否覆盖 memory kernel 约束
- token 超限时上下文裁剪优先级
- 最终上下文合并顺序规范

该事项属于后续开发前的明确待办，不得视为“已设计完成”而跳过。

## 6. 阶段交付物

| 阶段 | 交付物 |
| --- | --- |
| Phase 0 | 6 份结构分析与集成设计文档 |
| Phase 1 | 可运行 ingestion -> BM25 retrieval -> citation 最小闭环 |
| Phase 1.5 | Hermes 主链路内建 memory kernel，query-time 自动检索与引用返回 |
| Phase 2 | hybrid search、rerank、权限治理、facts、评测、审计 |
| Phase 3 | 企业系统扩展、管理界面、OCR、运营治理 |

## 7. 阶段依赖关系

```text
Phase 0
  -> Phase 1 收口
  -> Phase 1.5 内核接入
  -> Phase 2 企业能力增强
  -> Phase 3 规模化运营
```

Phase 1 与 Phase 0 可部分并行，但 Phase 1.5 必须依赖 Phase 0 的调用链和 patch point 结论。

## 8. 验收标准

### 7.1 Phase 0 验收标准

- 明确 Hermes 仓库目录职责
- 明确请求调用链
- 明确 Prompt、Tool、Memory、Response 位置
- 明确 memory kernel 插入点
- 明确 Hermes_memory 归位方案
- 明确暂停项与可继续项
- 形成 6 份正式文档

### 7.2 Phase 1 验收标准

- 可上传文档
- 可解析 txt/md/html/pdf/docx 中至少基础文本
- 可结构化 chunk
- 可写入数据库
- 可写入 OpenSearch BM25 index
- 可通过 API 检索 chunk
- 返回标准 citation

### 7.3 Phase 1.5 验收标准

- Hermes 主仓库内存在 `agent/memory_kernel/`
- `AIAgent.run_conversation()` 自动调用 memory kernel
- 不依赖模型主动调用工具即可执行企业知识检索
- 当前用户消息中注入 enterprise memory context block
- final result 返回 citations
- legacy MemoryManager 不被破坏
- 可配置启停 memory kernel
- 明确记录当前上下文注入顺序及其“临时实现”属性
- 将顺序检查列入进入下一阶段前的显式待办

### 7.4 Phase 2 验收标准

Phase 2 拆分为小阶段推进。Phase 2 第一小阶段仅验收检索契约与双路召回骨架：

- 固化 retrieval request / filter / result contract
- 支持 `source_type`、`document_id`、`document_type`、`is_latest` metadata filter
- unsupported filter 必须进入 `ignored_filters`，不得静默吞掉
- 接入现有 1024 维向量库 dense retrieval adapter
- 支持最小 dense + sparse hybrid retrieval
- trace 能区分 dense、sparse、fallback 与 hybrid merge
- rerank 仅预留接口位置，本小阶段不实现

Phase 2 后续小阶段再推进：

- rerank
- structured facts
- retrieval evaluation
- audit logs
- version-aware citation

### 7.5 Phase 2.1 状态

Phase 2.1 聚焦 dense backend 接通与真实 hybrid 验证：

- 已固化 dense `/search` request / response contract
- 已通过本地 HTTP vector backend 集成测试验证 dense-only 路径
- 已通过本地 HTTP dense + controlled sparse 验证 hybrid 去重与 score merge
- 已验证 dense backend 异常时 hybrid fail-open，sparse 检索继续返回
- 生产级外部 `VECTOR_STORE_URL` 尚未配置，真实外部向量库验证待执行
- rerank、facts、OCR、多 agent、复杂权限、citation 文本渲染增强仍不进入本阶段

### 7.6 Phase 2.1-Qdrant 状态

Phase 2.1-Qdrant 将 dense backend 主路线从临时 HTTP `/search` contract 切换为 Qdrant：

- 默认 `VECTOR_STORE_PROVIDER=qdrant`
- 新增 `QDRANT_URL`、`QDRANT_API_KEY`、`QDRANT_COLLECTION`、`QDRANT_VECTOR_SIZE=1024`
- 新增阿里云 `text-embedding-v3` 查询向量客户端，维度固定为 1024
- Qdrant point payload 映射到既有 `SearchResult` contract
- metadata filter 当前支持 `source_type`、`document_id`、`document_type`、`is_latest`
- hybrid 仍保持 dense + sparse 双路召回、`chunk_id` 去重、简单 score sum 融合
- Qdrant 异常或 embedding 不可用时，hybrid 必须 fail-open 到 sparse

当前验证状态：

- 已通过 fake Qdrant HTTP server 测试 collection、upsert、search、filter、normalization、hybrid 与 fail-open
- 已通过 context_builder / citation 对 dense-only、sparse-only、hybrid 的统一 contract 消费检查
- 当前机器无 `docker`，且未配置 `ALIYUN_EMBEDDING_API_KEY`，真实 Qdrant 容器与阿里云 embedding 调用仍是 TODO

## 9. 当前优先级建议

当前应优先完成 Phase 0，而不是继续扩展检索能力。原因：

1. 项目目标已经从外部长期记忆服务调整为企业内核型 Hermes。
2. 若继续按外挂式服务扩展，后续接入 Hermes 主链路时会产生大量返工。
3. 权限、citation、versioning、writeback 必须在主请求链路中被治理，而不是外围补丁。
4. Hermes 已存在 memory、session、plugin、tool、hook 能力，必须先复用和规避冲突。

## 10. 下一步开发顺序

推荐顺序：

1. 完成 Phase 0 文档评审。
2. 冻结 Hermes_memory Phase 1 对外接口：ingestion、retrieval、citation。
3. 在 Hermes 主仓库新增 `agent/memory_kernel/` 空骨架和类型定义。
4. 在 `AIAgent` 中接入 kernel façade，但默认可配置关闭。
5. 将 Phase 1 BM25 检索以 adapter 方式接入 `RetrievalOrchestrator`。
6. 实现 context block 注入和 citation payload 返回。
7. 对当前上下文注入顺序进行专项检查，确认合并顺序与裁剪策略。
8. 增加主链路最小集成测试。
9. 进入 Phase 2 第一小阶段：先固化 retrieval contract、metadata filter、dense adapter 和最小 hybrid。
10. Phase 2.1-Qdrant 真实环境补验：配置 Qdrant 与阿里云 embedding key 后，执行真实 dense-only 与 hybrid gate。
10. 在 contract 与 hybrid 骨架稳定后，再进入 rerank、permission、facts 等后续小阶段。
