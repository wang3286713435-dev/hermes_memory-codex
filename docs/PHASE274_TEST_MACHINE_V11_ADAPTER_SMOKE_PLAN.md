# Phase 2.74 Test-machine v1.1 Adapter Smoke Plan

## 目标

在 Hermes 侧 v1.1 readonly adapter contract update 完成后，让测试机 Codex 在 reviewed ref 上复验：

1. Hermes 代码版本包含 Phase 2.73 v1.1 adapter 更新。
2. Data Steward / asset catalog feature flags 默认关闭。
3. v1.1 structure-only smoke 仍为 `Go`。
4. 经明确授权后，`LIMIT 30` 脱敏统计 smoke 仍为 `Go`。
5. 无 REST / API Key `project_scope` 证明时仍 fail-closed，不把 `permission_tags` 当最终权限。

## 当前边界

本阶段只准备测试机复验 prompt / runbook，不在开发机连接真实 DB，不执行 SQL，不读取真实行，不写任何系统。

## 允许

- 测试机 reviewed ref / dirty 状态检查。
- 安全 env key 名称存在性检查，不输出值。
- `structure_only` SQL。
- 用户明确授权后的 `LIMIT 30` 脱敏聚合统计。
- 只输出 sanitized report。

## 禁止

- 输出 secret / `.env` 真值。
- 输出真实项目名、文件名、NAS 路径、raw row、ID 原值、`permission_tags` 原值。
- 写平台 DB / Hermes DB / OpenSearch / Qdrant / MinIO。
- 扫描 NAS。
- 执行 mirror migration。
- 启用 Data Steward runtime features。
- 执行 Agent DB CRUD。
- 执行 repair / cleanup / backfill / reindex / delete / migration。
- 进入 production rollout。

## Go 条件

1. Hermes_memory 在测试机 checkout 到包含 Phase 2.73 的 reviewed ref。
2. Worktree clean。
3. `platform_asset_readonly_db_contract_version` 或等价配置为 `delivery_platform.asset_views.v1.1`。
4. `structure_only` smoke Go。
5. 如执行 redacted statistics smoke，则 `raw_rows_output=false`、`secret_printed=false`、`true_business_data_output=false`、`writes_performed=false`。
6. 报告明确 `hermes_default_without_rest_scope=DENIED`。

## Pause 条件

1. 测试机未更新到 reviewed ref。
2. env key 不完整。
3. contract version 仍是 v1。
4. MySQL client / Hermes readonly tooling 不可用。
5. 不能保证脱敏输出。

## No-Go 条件

1. 读取或输出 raw row。
2. 输出 secret 或真实业务数据。
3. 发生任何写操作。
4. 启用 Data Steward runtime、mirror、indexing 或 Agent CRUD。

## 下一步

将 `docs/CODEX_TEST_MACHINE_V11_ADAPTER_SMOKE_PROMPT.md` 交给测试机 Codex。测试机返回 Go 后，再决定是否做 Data Steward 接入基线与后续 catalog query preview。
