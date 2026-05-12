# Phase 2.71 DB v1.1 Contract Alignment Plan

日期：2026-05-11
状态：Codex B direct DB handoff planning

## 1. 背景

Phase 2.70 已完成真实 DB `structure_only` smoke 与 schema gap review：

1. DB 可达，database 匹配。
2. `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView` 四个 View 均存在。
3. `SHOW COLUMNS` 与四个 `WHERE 1 = 0` 均通过。
4. 未读取真实行、未输出 secret / 真实业务数据、未写 DB / NAS / index。

数据库团队随后给出 sanitized response，确认可推进 `delivery_platform.asset_views.v1.1` 合同评审。该回复已固化到 `docs/DB_SCHEMA_GAP_SANITIZED_RESPONSE.md`。

## 2. 当前结论

可以采纳数据库团队回复，并进入 DB v1.1 合同对齐阶段。

这仍不是完整 Data Steward 耦合：

1. 不是 DB CRUD。
2. 不是 mirror migration。
3. 不是 NAS 扫描。
4. 不是 selective indexing。
5. 不是 Agent 直接改平台数据库。

Phase 2.71 只把 v1.1 字段语义、默认安全策略、后续 smoke 顺序和双方责任写清楚。

## 3. v1.1 建议字段

### 3.1 必须优先补齐

1. `ModelAssetView.project_id`
   - 用途：模型资产直接绑定项目边界。
   - Hermes 策略：缺失时不得把 model asset 放入 prompt。

2. `permission_tags`
   - 短期只接受粗粒度标签，例如 `SOURCE_SYSTEM:delivery_platform`、`SOURCE_VIEW:<...>`、`ASSET_KIND:<...>`、`PROJECT:<project_id>`、`CONFIDENTIALITY:<UNKNOWN|INTERNAL>`、`INDEX_ELIGIBILITY:<...>`。
   - Hermes 策略：缺失或无法校验时 default deny。

3. `confidentiality_level`
   - 建议默认 `UNKNOWN`。
   - Hermes 策略：不得把 `UNKNOWN` 推断为低敏。

4. `last_seen_at`
   - 可由 `last_verified_at` 或 `updated_at` 派生。
   - Hermes 策略：标记为 derived，不等同于 NAS 实时存在证明。

5. `lifecycle_status`
   - 短期保守枚举：`active`、`archived`、`unknown`、`deleted_candidate`、`stale_unverified`。
   - 不使用 `missing` / `moved` 作为静态 View 推断。
   - Hermes 策略：`unknown` / `deleted_candidate` 不得自动进入高信任 retrieval。

6. `index_eligibility`
   - 短期默认 `catalog_only`。
   - Hermes 策略：只有显式允许时才进入 preview / full-text / semantic 后续流程。

7. `AuditEventView.event_id` checkpoint 语义
   - 已确认 `event_id_monotonic=true` 与 `checkpoint_usable=true`。
   - Hermes 策略：可作为后续 incremental sync 主游标，但本阶段不实现 sync。

8. `project_scope`
   - REST / API Key 上下文为主。
   - 静态 View 只提供资产所属 `project_id`，不得表达调用者最终可见范围。

### 3.2 不进入 v1.1 的后置项

1. 完整 ACL snapshot。
2. 用户态 `project_scope` 最终权限。
3. full-text / semantic indexing 实际开放。
4. 精确 missing / moved / stale 判定。
5. BIM component / graph / ontology 字段。
6. Agent DB CRUD / operation executor。

## 4. Hermes 安全策略

即使数据库团队补齐 v1.1 字段，Hermes 仍必须遵守：

1. `permission_tags` 缺失：deny。
2. `project_scope` 缺失：不得进入 prompt；静态 View 中的资产归属项目不等于调用者授权范围。
3. `confidentiality_level=UNKNOWN`：按敏感处理。
4. `index_eligibility=catalog_only`：只允许资产目录层展示，不进入正文 evidence。
5. catalog-only 资产不得伪装成 document chunk citation。
6. `AuditEventView.summary` 不得作为正文 evidence 或 confirmed facts。
7. 所有真实 DB 能力默认 feature flag off。

## 5. 建议执行顺序

1. 数据库团队实现或规划 `asset_views.v1.1` 字段。
2. 测试机 Codex 重新执行 structure-only smoke，验证 v1.1 字段存在。
3. 若字段存在且无 secret / raw row 输出，再由用户单独授权 `LIMIT 30` 脱敏统计 smoke。
4. `LIMIT 30` 只输出聚合统计，不保存 raw sample，不写 mirror。
5. smoke 通过后，才规划 Hermes mirror / sync preview；仍不进入真实 DB CRUD。

## 5.1 快速耦合路径

为避免数据库团队继续等待，Phase 2.71 采用两条并行交接材料：

1. `docs/CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md`
   - 发给数据库团队 Codex。
   - 用于确认 / 推进 `delivery_platform.asset_views.v1.1` 字段落点。
   - 不请求真实数据，不要求输出 raw row。

2. `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`
   - 发给测试机 Codex。
   - 仅在数据库团队确认 v1.1 完成后执行。
   - 只检查字段结构，不读取真实行，不执行 `LIMIT 30`。

该路径的目标是：数据库团队补字段完成后，测试机可以立即复验，不再重新编写 smoke prompt。

## 6. 下一步交接给数据库团队

请数据库团队先回复：

1. 是否确认推进 `delivery_platform.asset_views.v1.1`。
2. v1.1 字段预计落点：View、REST、或二者都有。
3. 是否按 `CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md` 中的 `permission_tags` 枚举落地。
4. 是否确认 `confidentiality_level` 默认值采用 `UNKNOWN`。
5. 是否确认 `lifecycle_status` 短期枚举为 `active` / `archived` / `unknown` / `deleted_candidate` / `stale_unverified`，且不静态推断 `missing` / `moved`。
6. 是否确认 `index_eligibility` 短期默认 `catalog_only`。
7. v1.1 完成后是否可重新执行 structure-only smoke。

## 7. 本阶段禁止事项

1. 不连接真实 DB 执行新 SQL。
2. 不执行 `LIMIT 30`。
3. 不读取真实行。
4. 不输出真实项目名 / 文件名 / NAS 路径 / raw row。
5. 不写 Hermes DB / 平台 DB / OpenSearch / Qdrant / MinIO。
6. 不做 mirror migration。
7. 不扫描 NAS。
8. 不启用 Data Steward runtime feature。
9. 不实现 Agent 增删改查。
10. 不进入 production rollout。
