# Phase 2.70 DB Schema Contract Gap Review

日期：2026-05-11
状态：Codex B direct DB handoff planning

## 1. 背景

测试机 DB `structure_only` smoke 已返回 `Go`：

1. `SELECT 1` 通过。
2. `SELECT DATABASE()` 匹配预期 database。
3. 四个 View 均存在：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
4. 四个 View 的 `SHOW COLUMNS` 成功。
5. 四个 View 的 `WHERE 1 = 0` 空结构查询成功。
6. 未输出 secret、真实项目名、文件名、NAS 路径、`asset_uid`、`source_id`、raw row。
7. 未读取真实业务行。
8. 未写任何 DB / index / object storage。

这代表 Hermes 与真实 DB 完成了第一阶段只读结构级耦合，但还不是完整 Data Steward 耦合。

## 2. 本阶段目标

Phase 2.70 只做 schema contract gap review：

1. 将真实 View 字段对照 `DB_NAS_HERMES_INTEGRATION_CONTRACT.md`。
2. 标出 P0 可直接映射字段。
3. 标出 P1 进入 mirror / retrieval 前必须补齐或 fail-closed 的字段。
4. 标出 P2 后置治理字段。
5. 给数据库团队一份最小补字段建议。
6. 判断是否具备进入后续 `LIMIT 30` 脱敏样本 smoke 的条件。

本阶段不读取真实行，不执行 `LIMIT 30`，不写 migration，不写 mirror，不启用 Data Steward runtime features。

## 3. 真实 View 字段摘要

### ProjectAssetView

已存在字段：

`project_id`, `project_code`, `project_name`, `project_stage`, `discipline_scope`, `manager_name`, `owner_org_name`, `asset_status`, `model_file_count`, `total_size_bytes`, `last_asset_updated_at`

P0 可用：

1. `project_id`
2. `project_code`
3. `project_name`
4. `project_stage`
5. `discipline_scope`
6. `manager_name`
7. `owner_org_name`
8. `asset_status`
9. `model_file_count`
10. `total_size_bytes`
11. `last_asset_updated_at`

主要缺口：

1. `permission_tags`
2. `project_scope`
3. `confidentiality_level`
4. 明确 lifecycle / archived / deleted 语义

### FileAssetView

已存在字段：

`file_id`, `project_id`, `project_code`, `project_name`, `file_name`, `file_ext`, `file_kind`, `discipline`, `version_no`, `size_bytes`, `checksum`, `storage_provider`, `storage_path`, `logical_path`, `source_type`, `process_status`, `created_at`, `updated_at`

P0 可用：

1. `file_id`
2. `project_id`
3. `project_code`
4. `project_name`
5. `file_name`
6. `file_ext`
7. `file_kind`
8. `discipline`
9. `version_no`
10. `size_bytes`
11. `checksum`
12. `storage_provider`
13. `storage_path`
14. `logical_path`
15. `source_type`
16. `process_status`
17. `created_at`
18. `updated_at`

主要缺口：

1. `permission_tags`
2. `project_scope`
3. `confidentiality_level`
4. `last_seen_at`
5. explicit `missing` / `moved` / `stale` status
6. index eligibility fields

### ModelAssetView

已存在字段：

`model_id`, `file_id`, `project_code`, `model_name`, `model_format`, `discipline`, `version_no`, `preview_available`, `lightweight_status`, `component_index_status`, `storage_path`, `updated_at`

P0 可用：

1. `model_id`
2. `file_id`
3. `project_code`
4. `model_name`
5. `model_format`
6. `discipline`
7. `version_no`
8. `preview_available`
9. `lightweight_status`
10. `component_index_status`
11. `storage_path`
12. `updated_at`

主要缺口：

1. `project_id` 缺失。短期可通过 `file_id` -> `FileAssetView.project_id` 间接关联，但 mirror / retrieval 阶段必须 fail-closed 或显式 join。
2. `permission_tags`
3. `project_scope`
4. `confidentiality_level`
5. `content_hash` / model checksum
6. `last_seen_at`
7. explicit lifecycle / missing / moved / stale

### AuditEventView

已存在字段：

`event_id`, `project_id`, `module_code`, `action_code`, `target_type`, `target_id`, `operator_id`, `summary`, `created_at`

P0 可用：

1. `event_id`
2. `project_id`
3. `module_code`
4. `action_code`
5. `target_type`
6. `target_id`
7. `operator_id`
8. `created_at`

谨慎字段：

1. `summary` 为 JSON，但不得作为正文 evidence 或长期 fact；只能作为事件摘要元数据。

主要缺口：

1. 事件顺序 / checkpoint 语义需确认：`event_id` 是否单调递增。
2. 是否存在事件类型白名单 / 数据变更类型映射。
3. `summary` 是否可能包含敏感信息；默认不得输出。

## 4. P0 / P1 / P2 判定

### P0：足够进入下一步脱敏样本 smoke 的基础

当前已具备：

1. 四个 View 存在。
2. 项目 / 文件 / 模型 / 审计事件核心 ID 字段存在。
3. 文件路径、大小、版本、checksum、创建 / 更新时间字段基本存在。
4. 模型格式、专业、轻量化 / 构件索引状态字段存在。
5. 审计事件 `event_id`、`created_at`、`target_type`、`target_id` 存在。

### P1：进入 mirror / retrieval 前必须处理

1. `permission_tags` 缺失。
2. `project_scope` 缺失。
3. `confidentiality_level` 缺失。
4. `ModelAssetView.project_id` 缺失。
5. `last_seen_at` 缺失。
6. explicit missing / moved / stale lifecycle 缺失。
7. index eligibility 字段缺失。

默认策略：

1. 权限字段缺失时 fail-closed / deny。
2. 无 `project_id` 的 ModelAsset 不得进入 prompt。
3. 无 lifecycle 明确信息时不得自动判定 deleted / moved / stale。
4. catalog-only 不得作为正文 citation。

### P2：后置治理字段

1. full ACL snapshot。
2. `is_latest` / version lineage。
3. retention / archive policy。
4. department / customer / owner 完整主数据。
5. spatial index eligibility。
6. BIM component-level / graph / ontology 字段。

## 5. 给数据库团队的最小补字段建议

优先级 P1：

1. 在所有 asset View 增加或暴露 `permission_tags`。
2. 增加或暴露 `project_scope`。
3. 增加或暴露 `confidentiality_level`。
4. 在 `ModelAssetView` 增加 `project_id`，避免 Hermes 通过 `file_id` 二次推断权限边界。
5. 增加 `last_seen_at`。
6. 增加 explicit `lifecycle_status`，至少覆盖 `active` / `archived` / `missing` / `moved` / `deleted_candidate`。
7. 增加 `index_eligibility` 或等价字段，区分 `catalog_only` / `preview_allowed` / `full_text_allowed` / `semantic_allowed`。
8. 确认 `AuditEventView.event_id` 是否单调递增，可作为 checkpoint。

优先级 P2：

1. `is_latest`
2. `version_lineage`
3. `owner_department`
4. `customer_id`
5. `retention_policy`
6. spatial metadata eligibility

## 6. 是否建议进入 LIMIT 30 脱敏样本 smoke

谨慎建议：可以规划，但不要立即执行。

进入 `LIMIT 30` 脱敏样本 smoke 前需要用户再次显式授权，并要求：

1. 只输出脱敏统计，不输出真实项目名、文件名、路径、raw row。
2. 可输出字段覆盖率、null count、状态分布、格式分布、数量统计。
3. `summary` JSON 不直接输出。
4. 样本读取只用于验证字段可用性和权限 fail-closed，不进入 Hermes retrieval / prompt。
5. 不写 mirror，不写 index。

## 7. 下一步

Codex B 可直接给数据库团队 / 测试机 Codex 输出两类材料：

1. `schema_contract_gap_summary`：给数据库团队确认 P1 字段缺口。
2. `limit_30_redacted_smoke_plan`：待用户明确授权后执行。

当前不建议进入 mirror migration、selective indexing、DB CRUD 或 NAS scan。
