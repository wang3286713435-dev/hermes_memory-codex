# Phase 2.72 DB v1.1 Structure-only Smoke Result

日期：2026-05-12
状态：Go

## 1. 结果摘要

测试机已完成 `delivery_platform.asset_views.v1.1` structure-only smoke，结果为 `Go`。

该结果代表：

1. DB 可达。
2. database name 匹配预期。
3. 四个 View 均存在：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
4. v1.1 字段存在性校验通过。
5. 四个 View 的 `WHERE 1 = 0` 均通过。
6. 未读取真实行。
7. 未输出 secret / 真实业务数据。
8. 未执行任何写操作。

这表示 Hermes 与真实 DB 已完成 v1.1 只读结构级耦合。

## 2. v1.1 字段验证结果

### ProjectAssetView

已确认字段：

1. `permission_tags`
2. `confidentiality_level`
3. `last_seen_at`
4. `lifecycle_status`
5. `index_eligibility`

### FileAssetView

已确认字段：

1. `permission_tags`
2. `confidentiality_level`
3. `last_seen_at`
4. `lifecycle_status`
5. `index_eligibility`

### ModelAssetView

已确认字段：

1. `project_id`
2. `permission_tags`
3. `confidentiality_level`
4. `last_seen_at`
5. `lifecycle_status`
6. `index_eligibility`

### AuditEventView

已确认字段：

1. `event_id`
2. `created_at`

## 3. 权限 / checkpoint 语义

测试机报告确认：

```yaml
project_scope_static_view_expected: false
project_scope_rest_contract_required: true
event_id_checkpoint_expected: true
event_id_monotonic_claim_source: database_team_sanitized_response
```

Hermes 侧解释：

1. `project_scope` 不应被误解为静态 View 可见范围。
2. 调用者授权仍应来自 REST / API Key / caller context。
3. `AuditEventView.event_id` 可作为后续 checkpoint 规划依据。

## 4. 安全确认

测试机报告确认：

```yaml
secret_printed: false
real_rows_read: false
true_business_data_output: false
writes_performed: false
```

本轮没有：

1. `LIMIT 30`
2. 真实行读取
3. secret 输出
4. raw row 输出
5. 真实项目名 / 文件名 / NAS 路径输出
6. Hermes Memory DB 写入
7. OpenSearch / Qdrant / MinIO 写入
8. NAS scan
9. mirror migration
10. indexing
11. Agent CRUD
12. production rollout

## 5. 当前结论

v1.1 structure-only DB smoke passed。

这仍不等于完整 Data Steward 耦合完成。当前完成的是“真实 DB v1.1 结构级只读耦合”。

下一步候选：

1. `LIMIT 30` 脱敏统计 smoke：验证字段值形态、空值率、枚举分布、timestamp coverage；仍不输出 raw row。
2. Hermes 侧 v1.1 readonly adapter contract planning：根据 v1.1 字段更新 fake adapter / contract tests / DTO 预期；仍默认 feature flags off。

建议优先：先做 `LIMIT 30` 脱敏统计 smoke planning / prompt，不立即执行，继续要求用户显式授权。
