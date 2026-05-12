# DB Schema Gap Request To Database Team

日期：2026-05-11
状态：draft for database team review

## 1. 背景

Hermes / 数据管家已完成真实 DB `structure_only` smoke：

1. 四个 View 存在。
2. 字段结构可读。
3. `WHERE 1 = 0` 空结构查询通过。
4. 未读取真实行。
5. 未输出 secret 或真实业务数据。
6. 未写任何 DB / index / NAS。

本文件仅用于字段缺口评审，不请求任何真实数据。

## 2. 当前可用字段

### ProjectAssetView

已具备项目级基本字段：

`project_id`, `project_code`, `project_name`, `project_stage`, `discipline_scope`, `manager_name`, `owner_org_name`, `asset_status`, `model_file_count`, `total_size_bytes`, `last_asset_updated_at`

### FileAssetView

已具备文件级基础字段：

`file_id`, `project_id`, `project_code`, `project_name`, `file_name`, `file_ext`, `file_kind`, `discipline`, `version_no`, `size_bytes`, `checksum`, `storage_provider`, `storage_path`, `logical_path`, `source_type`, `process_status`, `created_at`, `updated_at`

### ModelAssetView

已具备模型级基础字段：

`model_id`, `file_id`, `project_code`, `model_name`, `model_format`, `discipline`, `version_no`, `preview_available`, `lightweight_status`, `component_index_status`, `storage_path`, `updated_at`

### AuditEventView

已具备事件级基础字段：

`event_id`, `project_id`, `module_code`, `action_code`, `target_type`, `target_id`, `operator_id`, `summary`, `created_at`

## 3. P1 缺口：进入 mirror / retrieval 前建议补齐

请数据库团队评估是否可在 View 或 REST contract 中补充：

1. `permission_tags`
   - 用途：Hermes pre-model 权限过滤。
   - 当前策略：缺失默认 deny。

2. `project_scope`
   - 用途：限制用户请求范围与项目访问边界。
   - 当前策略：缺失不得进入 prompt。

3. `confidentiality_level`
   - 用途：密级过滤。
   - 当前策略：缺失写 `UNKNOWN`，不得推断为低敏。

4. `ModelAssetView.project_id`
   - 用途：模型资产直接绑定项目权限边界。
   - 当前风险：仅有 `project_code` 和 `file_id`，Hermes 不应在 prompt 阶段隐式猜 project 权限。

5. `last_seen_at`
   - 用途：判断资产是否仍存在。
   - 当前策略：缺失只能使用 sync time 标记为 derived，不做删除判断。

6. explicit `lifecycle_status`
   - 建议枚举：`active`, `archived`, `missing`, `moved`, `deleted_candidate`。
   - 用途：排除不可用资产。

7. `index_eligibility`
   - 建议枚举：`catalog_only`, `preview_allowed`, `full_text_allowed`, `semantic_allowed`。
   - 用途：明确哪些资产可进入后续 preview / full-text / semantic indexing。

8. `AuditEventView.event_id` 单调递增语义确认
   - 用途：Hermes checkpoint / incremental sync。
   - 请确认是否可作为稳定 checkpoint；若不保证单调，是否有其他 event sequence 字段。

## 4. P2 后置字段

后续可规划：

1. full ACL snapshot。
2. `is_latest`。
3. version lineage。
4. owner department / customer id。
5. retention / archive policy。
6. spatial metadata eligibility。
7. BIM component / ontology / graph 相关字段。

## 5. 当前不请求

当前不请求：

1. 真实项目名。
2. 文件名样本。
3. NAS 路径样本。
4. raw rows。
5. `LIMIT 30` 样本。
6. 任何 secret。
7. 任何 DB 写入。
8. 任何 NAS scan。

## 6. 需要数据库团队回复

请只回复脱敏评审结论：

1. P1 字段哪些可以短期加入 View / REST contract。
2. 哪些字段需要后置。
3. `ModelAssetView.project_id` 是否可以补。
4. `AuditEventView.event_id` 是否单调递增。
5. 是否同意后续做 `LIMIT 30` 脱敏样本 smoke，只输出统计，不输出 raw row。

不得回复 secret、真实项目名、真实文件名、NAS 路径或 raw row。
