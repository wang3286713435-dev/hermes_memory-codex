# DB v1.1 Deployment Blocker Status

日期：2026-05-12
状态：Go for Hermes structure-only smoke

## 1. 当前判断

`delivery_platform.asset_views.v1.1` 已完成目标环境部署，可以进入 Hermes 测试机 v1.1 structure-only smoke。

此前阻塞点在数据库平台侧：v1.1 migration / REST contract 已完成静态补丁，但尚未应用到目标 DB / 后端服务。数据库团队现已回传脱敏部署报告，阻塞解除。

## 2. 数据库团队回传依据

数据库团队 Codex 回传：

1. 本地交接文档仍标记 `v1_1_db_apply_status: NOT_APPLIED_BY_THIS_TASK`。
2. 相关 V17 migration / REST 合同文件仍处于本地补丁状态。
3. 测试机 env 文件存在且权限为 `600`，但 contract version 尚未确认为 `delivery_platform.asset_views.v1.1`。
4. 数据库团队没有更新 env，也没有重跑 smoke，避免把未部署状态误标为可用。

已完成的平台侧静态收口：

1. View migration：`/Users/vc/Documents/数字化交付平台/backend/delivery-app/src/main/resources/db/migration/V17__asset_views_v1_1.sql`
2. REST DTO / repository / Agent API 返回结构已补齐 v1.1 字段。
3. 文档已标注 v1.1 需要目标 DB 应用迁移和部署后，再执行 structure-only smoke。

验证结果：

1. `./mvnw -q -DskipTests compile` 通过。
2. 静态字段检查通过。
3. 未连接 DB。
4. 未读取真实行。
5. 未执行 `LIMIT 30`。
6. 未输出 secret / raw row / 真实项目名 / 文件名 / NAS 路径。
7. 未写 DB / NAS / Hermes Memory / OpenSearch / Qdrant / MinIO。

## 2.1 部署完成回传

数据库团队后续回传：

```yaml
v1_1_db_apply_status: APPLIED_TO_TARGET_DB
backend_deploy_status: DEPLOYED_TO_TEST_MACHINE_OR_TARGET_ENV
contract_version_available: delivery_platform.asset_views.v1.1
env_contract_version_update_allowed: true
structure_only_smoke_allowed: true
real_rows_allowed: false
writes_allowed: false
```

脱敏部署报告要点：

1. `V17__asset_views_v1_1.sql` 已由 Flyway 应用成功，目标 DB 记录为 version `17` success。
2. 四个 View 均已包含 v1.1 字段。
3. 后端测试实例已启动，健康检查 `UP`。
4. 运行态使用 lazy initialization，避免启动后台任务 worker 主动轮询业务任务。
5. Hermes 测试机安全 env 中 contract version key 已更新并确认 present，权限仍为 `600`。
6. 四个 View 的 `WHERE 1 = 0` structure-only 验证已通过。
7. 未读取真实业务行，未输出 secret / raw row / 真实项目名 / 文件名 / NAS 路径。
8. 未写 Hermes Memory、OpenSearch、Qdrant、MinIO，未扫描 NAS，未触发 mirror migration / indexing / Agent CRUD。

## 3. Hermes 当前策略

Hermes 侧可以进入测试机 v1.1 structure-only smoke：

1. 测试机 contract env 已由安全渠道更新为 v1.1，且未输出真值。
2. 可以执行 `CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`。
3. 不执行 `LIMIT 30`。
4. 不读取真实行。
5. 不启用 Data Steward runtime features。
6. 不写 mirror / documents / chunks / OpenSearch / Qdrant。
7. 不实现 Agent DB CRUD。

## 4. 下一步 Go 条件

数据库团队已回传以下信息，Go 条件满足：

```yaml
v1_1_db_apply_status: APPLIED_TO_TARGET_DB
backend_deploy_status: DEPLOYED_TO_TEST_MACHINE_OR_TARGET_ENV
contract_version_available: delivery_platform.asset_views.v1.1
env_contract_version_update_allowed: true
structure_only_smoke_allowed: true
real_rows_allowed: false
writes_allowed: false
```

测试机 operator / Codex 下一步：

1. 执行 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`。
2. 只做 structure-only 字段复验。
3. 返回 sanitized report。

## 5. 当前不做

当前仍不应执行 `LIMIT 30` 或任何真实行读取。

正确下一步是：测试机执行 v1.1 structure-only smoke。
