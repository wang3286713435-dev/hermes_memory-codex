# NEXT_CODEX_A_PROMPT

## Phase 2.73 Status

Hermes v1.1 readonly adapter contract update 已由 Codex B 在主线完成本地实现与目标测试：

1. `delivery_platform.asset_views.v1.1` 已成为 Hermes 侧 readonly contract 默认版本。
2. fake adapter / readonly preflight / metadata DTO / contract tests 已同步 v1.1 字段。
3. 验证结果：`py_compile` 通过，Data Steward asset catalog target tests `73 passed`。
4. 当前仍未启用真实 Data Steward runtime、mirror、indexing 或 Agent CRUD。

## Codex A 当前行为

如果 Codex A 读到本文件：

1. 不要擅自连接真实 DB。
2. 不要执行 SQL、读取真实行、扫描 NAS、写 mirror、启用 Data Steward runtime 或实现 DB CRUD。
3. 不要做 production rollout。
4. 等待用户或 Codex B 提供新的非 DB 主线实现任务，或等待 Codex B 给出 Phase 2.74 测试机 reviewed-ref smoke prompt。

## 下一步建议

Phase 2.74：由 Codex B 直接准备测试机复验 prompt / runbook，用 reviewed ref 验证升级后的 Hermes v1.1 readonly adapter 仍满足：

1. feature flags 默认 off。
2. structure-only / redacted statistics 路径安全。
3. 无 REST/API Key `project_scope` 时 fail-closed。
4. `confidentiality_level=UNKNOWN` 不降级为低敏。
5. `index_eligibility=catalog_only` 不进入正文 evidence / semantic indexing。

## 禁止事项

任何 agent 当前都不得：

1. 写平台 DB / Hermes DB / OpenSearch / Qdrant / MinIO。
2. 扫描 NAS。
3. 执行 mirror migration。
4. 启用 Data Steward runtime feature。
5. 实现 Agent DB CRUD。
6. 修改 retrieval contract / memory kernel 主架构。
7. 进入 production rollout。
