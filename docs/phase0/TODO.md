# Hermes Memory Kernel 当前待办清单

## 目录

1. 文档目的
2. 当前最高优先级待办
3. Phase 1.5 明确待办
4. 暂不推进事项

## 1. 文档目的

本文档用于固化当前阶段的明确待办事项，避免 Phase 1.5 内核接入完成后遗漏关键约束检查。

## 2. 当前最高优先级待办

1. 完成 Hermes 与 Hermes_memory 运行时依赖打通，验证 adapter 可在 Hermes 主进程中稳定加载。
2. 完成最小主链路集成验证，确认 pre-model retrieval、context 注入、citation payload 返回正常。
3. 完成 context 注入顺序专项检查。

## 3. Phase 1.5 明确待办

### 3.1 Context 注入顺序检查

当前请求上下文的注入顺序为：

1. `memory kernel context`
2. `legacy memory_manager.prefetch_all()`
3. `plugin pre_llm_call context`

该顺序为 Phase 1.5 的临时实现，不视为最终稳定结论。

进入后续开发前，必须明确完成以下检查：

- legacy memory 是否污染企业检索上下文
- plugin context 是否覆盖 memory kernel 约束
- token 超限时上下文裁剪优先级
- 最终上下文合并顺序规范

### 3.2 主链路最小闭环验证

- 验证 kernel enabled 时的正常召回
- 验证 kernel disabled 时不影响普通 Hermes 对话
- 验证 adapter 不可用时 fail-open
- 验证 citations 能随结果稳定返回

### 3.3 后续实现前置条件

- 在顺序检查完成前，不推进更复杂的上下文治理逻辑
- 在依赖打通前，不推进真实环境联调结论
- 在最小闭环验证完成前，不推进 dense/rerank/facts 等增强项

## 4. 暂不推进事项

- dense retrieval
- rerank
- facts 联查
- 复杂权限策略
- OCR
- 多 agent 协作
- 复杂后台管理功能
