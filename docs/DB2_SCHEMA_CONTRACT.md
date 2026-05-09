# DB-2 Schema Contract

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-2 schema contract handoff freeze；docs-only；未授权真实 migration / MySQL / NAS / REST / DB-3 retrieval

## 1. 当前裁决

DB-2 当前只允许：

1. fake adapter dry-run preview。
2. temporary DB proof-of-contract。
3. schema contract / field mapping / checkpoint / rollback 文档冻结。

DB-2 当前不允许：

1. 创建生产 migration。
2. 连接真实 MySQL。
3. 扫描真实 NAS。
4. 读取真实文件正文。
5. 写 `documents` / `chunks`。
6. 写 OpenSearch / Qdrant。
7. 接真实权限系统。
8. 开放 Agent 写 NAS、写业务库、删文件、移动文件。
9. 执行全量 reindex。
10. 把 catalog-only 资产送入 retrieval 或 prompt。
11. 进入 DB-3 selective indexing / evidence pack / OpenSearch / Qdrant 写入。

## 2. 已确认合同

1. 默认表名：`external_asset_catalog`。
2. 命名空间冲突时备选表名：`hermes_external_asset_catalog`。
3. 主键：`asset_uid`。
4. `asset_uid` 格式固定为 `source_system + ":" + source_view + ":" + source_id`。
5. `source_system` 当前固定为 `delivery_platform`，同一环境不得混用 `platform`。
6. 当前 `source_view` 只允许：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
7. `source_id` 是平台 View 原始 ID，不等于 `project_id`。
8. `source_id` 映射：
   - `ProjectAssetView.source_id = project_id`
   - `FileAssetView.source_id = file_id`
   - `ModelAssetView.source_id = model_id`
   - `AuditEventView.source_id = event_id`
9. 唯一约束：`UNIQUE (source_system, source_view, source_id)`。
10. `source_contract_version` 写入 catalog mirror 和 checkpoint。
11. `external_asset_sync_checkpoint` 纳入 DB-2 migration candidate schema，但 DB-2 当前不实际执行 migration。
12. `permission_status` 数据库默认值必须是 `DENIED`。
13. `permission_tags` 缺失、`project_scope` 缺失、`project_id` 缺失时，资产不得进入 prompt。
14. `confidentiality_level` 缺失时写 `UNKNOWN`，不得推断为低敏。
15. catalog-only 资产不得进入 `documents`、`chunks`、Qdrant、OpenSearch。
16. DB-2 不替代平台资产表，不成为 source of truth。

DB-1a fake adapter 既有 `asset_uid` 可能仍是 `source_system + ":" + source_id`，这是 DB-1 fake contract。真实 mirror 写入层和 DB-2 schema contract 使用本文件冻结的三段式 `asset_uid`。

## 3. `external_asset_catalog` 最终字段合同

字段类型以 MySQL 8 为默认方言。若未来兼容 PostgreSQL，`JSON` 等价为 `JSONB`；DB-2 不为双数据库兼容扩大实现范围。

| 字段 | 类型 | Null / 默认值 | 来源 View 字段 | 当前已有 | DB-2 fake / proof 填充 | 后续真实阶段补齐方 |
|---|---|---|---|---|---|---|
| `asset_uid` | `VARCHAR(256)` | `NOT NULL`, PK | 派生：`source_system:source_view:source_id` | 已有派生规则 | 由 fake adapter / mirror preview 生成 | Hermes mirror writer |
| `source_system` | `VARCHAR(64)` | `NOT NULL`, 默认写入 `delivery_platform` | 平台来源配置 | 已确认 | 固定写 `delivery_platform` | Hermes 配置 + 平台团队确认 |
| `source_view` | `VARCHAR(64)` | `NOT NULL` | View 名称 | 已确认 | fake fixture view name | 平台 View contract |
| `source_id` | `VARCHAR(128)` | `NOT NULL` | `project_id` / `file_id` / `model_id` / `event_id` | 已有 | 按 View 映射 | 平台 View contract |
| `source_contract_version` | `VARCHAR(64)` | `NOT NULL` | View contract version | 待平台稳定版本号 | proof 写 `DB2_SCHEMA_V1` 或 fixture version | 平台 + Hermes contract review |
| `source_path` | `TEXT` | `NULL` | `logical_path` / `storage_path` | File / Model 部分已有 | 优先 `logical_path`，否则 `storage_path` | 平台 View |
| `storage_location` | `TEXT` | `NULL` | `storage_provider` + `storage_path` | File 有，Model 部分有 | 拼接或复制 storage path，不读文件 | 平台 View |
| `file_name` | `VARCHAR(512)` | `NULL` | `file_name` / `model_name` / `project_name` | 部分已有 | File 用 `file_name`，Model 用 `model_name`，Project 用 `project_name` | 平台 View |
| `file_ext` | `VARCHAR(32)` | `NULL` | `file_ext` / `model_format` | File / Model 部分已有 | File 用 `file_ext`，Model 可用 `model_format` | 平台 View |
| `mime_type` | `VARCHAR(128)` | `NULL` | 当前 View 未稳定提供 | 当前没有 | 由扩展名粗略派生或留空，标记 derived | 平台后续字段或 Hermes metadata 派生 |
| `file_size` | `BIGINT` | `NULL` | `size_bytes` / `total_size_bytes` | File / Project 已有 | File 用 `size_bytes`，Project 用 `total_size_bytes`，其余留空 | 平台 View |
| `content_hash` | `VARCHAR(128)` | `NULL` | `checksum` | File 已有 | File 用 `checksum`，缺失留空 | 平台 View |
| `created_at` | `TIMESTAMP` | `NULL` | `created_at` | File / Audit 已有 | 有源字段则映射；缺失留空 | 平台 View |
| `modified_at` | `TIMESTAMP` | `NULL` | `updated_at` / `last_asset_updated_at` / `created_at` | 部分已有 | 缺 `source_modified_at` 时优先用 `updated_at`，并标记 derived | 平台后续明确 `source_modified_at` |
| `last_seen_at` | `TIMESTAMP` | `NULL` | 当前 View 未稳定提供 | 当前没有 | proof 阶段用同步时间，并标记 `SYNC_DERIVED` | Hermes sync 或平台扫描任务 |
| `owner` | `VARCHAR(255)` | `NULL` | `manager_name` / `owner_org_name` / `operator_id` | Project / Audit 部分已有 | 可映射可用字段；不可用留空 | 平台组织 / 权限团队 |
| `department_id` | `VARCHAR(128)` | `NULL` | 当前 View 未稳定提供 | 当前没有 | 留空 | 平台组织 / 权限团队 |
| `project_id` | `VARCHAR(128)` | `NULL` | `project_id` | Project / File / Audit 已有，Model 当前缺失 | 有则映射；Model 可暂留空或后续由 file_id 关联补齐 | 平台 View |
| `customer_id` | `VARCHAR(128)` | `NULL` | 当前 View 未稳定提供 | 当前没有 | 留空 | 平台客户主数据 |
| `project_scope` | `JSON` | `NULL` | 当前 View 未稳定提供 | 当前没有 | fixture 可提供；否则留空并 `DENIED` | 平台权限系统 / Hermes 权限同步 |
| `permission_tags` | `JSON` | `NULL` | 当前 View 未稳定提供 | 当前没有 | fixture 可提供；缺失时留空并 `DENIED` | 平台权限系统 / Hermes 权限同步 |
| `permission_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'DENIED'` | 权限同步结果 | 当前没有稳定 View 字段 | 缺权限字段、缺项目、缺 scope 均写 `DENIED` | Hermes permission filter |
| `confidentiality_level` | `VARCHAR(32)` | `NOT NULL DEFAULT 'UNKNOWN'` | 当前 View 未稳定提供 | 当前没有 | 缺失写 `UNKNOWN` | 平台密级 / 权限团队 |
| `version_key` | `VARCHAR(128)` | `NULL` | `version_no` | File / Model 已有 | 映射 `version_no` | 平台 View |
| `is_latest` | `BOOLEAN` | `NULL` | 当前 View 未稳定提供 | 当前没有 | 不自行推断；留空 | 平台版本服务 |
| `parent_asset_uid` | `VARCHAR(256)` | `NULL` | `project_id` / `file_id` | 部分可派生 | File 可指向 Project；Model 可指向 File；缺字段留空 | Hermes mirror writer |
| `index_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'CATALOG_ONLY'` | Hermes 状态 | 已确认 | 固定 `CATALOG_ONLY` | DB-3+ indexing pipeline |
| `parse_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'NOT_REQUESTED'` | Hermes 状态 | 已确认 | 固定 `NOT_REQUESTED` | DB-3+ parser |
| `semantic_index_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'NOT_REQUESTED'` | Hermes 状态 | 已确认 | 固定 `NOT_REQUESTED` | DB-3+ vector pipeline |
| `citation_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'NOT_REQUESTED'` | Hermes 状态 | 已确认 | 固定 `NOT_REQUESTED` | DB-3+ citation builder |
| `lifecycle_status` | `VARCHAR(32)` | `NOT NULL DEFAULT 'ACTIVE'` | `asset_status` / `process_status` / future lifecycle field | 当前只有部分状态字段 | 未明确时 `ACTIVE`；缺失只写 candidate flag，不判定删除 | 平台事件 / 连续扫描证据 |
| `data_quality_flags` | `JSON` | `NULL` | Hermes 派生 | 当前没有 | 记录 `candidate_missing`、`missing_permission_tags`、`missing_modified_at` 等 | Hermes sync + 平台补充 |
| `derived_metadata_source` | `VARCHAR(64)` | `NOT NULL DEFAULT 'SOURCE_VIEW'` | Hermes 派生 | 当前没有 | `SOURCE_VIEW` / `SYNC_DERIVED` / `FALLBACK_DERIVED` / `UNKNOWN` | Hermes mirror writer |
| `created_at_utc` | `TIMESTAMP` | `NOT NULL` | Hermes mirror row created time | Hermes 可生成 | 同步创建时间，UTC | Hermes mirror writer |
| `updated_at_utc` | `TIMESTAMP` | `NOT NULL` | Hermes mirror row updated time | Hermes 可生成 | 同步更新时间，UTC | Hermes mirror writer |

支持字段也允许保留在 schema 中：`project_code`、`project_name`、`asset_kind`、`storage_provider`、`storage_path`、`logical_path`、`sync_status`、`last_event_id`、`raw_payload`、`previous_source_path`。这些字段不保存正文、chunk、embedding 或 citation 正文。

## 4. View 字段映射

详细映射以 `docs/DB2_VIEW_FIELD_MAPPING.md` 为准。本合同冻结以下处理原则：

1. `ProjectAssetView` 是项目级 catalog 资产，不代表文件正文。
2. `FileAssetView` 是文件级 catalog 资产，不读取真实文件内容。
3. `ModelAssetView` 是 BIM / 模型级 catalog 资产，不解析模型构件或语义。
4. `AuditEventView` 是同步事件资产 / checkpoint 辅助来源，不作为正文 evidence。
5. 当前缺少 `permission_tags`、`project_scope`、`confidentiality_level` 时 fail closed。
6. 当前缺少 moved / stale / missing 明确状态时，只允许写 `candidate_missing` 或 `UNKNOWN`，不得自动删除或判定真实删除。

## 5. 逻辑 SQL 草案

真实 SQL 方言等用户授权 migration 后再生成；本节只冻结目标结构。

```sql
CREATE TABLE external_asset_catalog (
    asset_uid VARCHAR(256) PRIMARY KEY,
    source_system VARCHAR(64) NOT NULL,
    source_view VARCHAR(64) NOT NULL,
    source_id VARCHAR(128) NOT NULL,
    source_contract_version VARCHAR(64) NOT NULL,

    project_id VARCHAR(128) NULL,
    project_code VARCHAR(128) NULL,
    project_name VARCHAR(255) NULL,
    customer_id VARCHAR(128) NULL,
    department_id VARCHAR(128) NULL,
    owner VARCHAR(255) NULL,

    asset_kind VARCHAR(64) NULL,
    file_name VARCHAR(512) NULL,
    file_ext VARCHAR(32) NULL,
    mime_type VARCHAR(128) NULL,
    source_path TEXT NULL,
    storage_location TEXT NULL,
    storage_provider VARCHAR(64) NULL,
    storage_path TEXT NULL,
    logical_path TEXT NULL,

    file_size BIGINT NULL,
    content_hash VARCHAR(128) NULL,
    version_key VARCHAR(128) NULL,
    is_latest BOOLEAN NULL,
    parent_asset_uid VARCHAR(256) NULL,

    permission_status VARCHAR(32) NOT NULL DEFAULT 'DENIED',
    project_scope JSON NULL,
    permission_tags JSON NULL,
    confidentiality_level VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN',

    lifecycle_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    data_quality_flags JSON NULL,
    previous_source_path TEXT NULL,
    derived_metadata_source VARCHAR(64) NOT NULL DEFAULT 'SOURCE_VIEW',

    sync_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    index_status VARCHAR(32) NOT NULL DEFAULT 'CATALOG_ONLY',
    parse_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',
    semantic_index_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',
    citation_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',

    last_event_id BIGINT NULL,
    created_at TIMESTAMP NULL,
    modified_at TIMESTAMP NULL,
    last_seen_at TIMESTAMP NULL,
    created_at_utc TIMESTAMP NOT NULL,
    updated_at_utc TIMESTAMP NOT NULL,

    raw_payload JSON NULL,

    UNIQUE KEY uk_external_asset_source (source_system, source_view, source_id)
);
```

禁止保存：

1. 文件正文。
2. chunk。
3. embedding。
4. citation 正文。
5. 平台正式资产表的 source of truth。
6. NAS ACL 原文快照中的敏感全文。

## 6. 索引与约束

DB-2 建议最小索引：

1. `PRIMARY KEY (asset_uid)`
2. `UNIQUE KEY uk_external_asset_source (source_system, source_view, source_id)`
3. `INDEX idx_external_asset_source_view (source_system, source_view)`
4. `INDEX idx_external_asset_project (project_id)`
5. `INDEX idx_external_asset_project_code (project_code)`
6. `INDEX idx_external_asset_lifecycle (lifecycle_status)`
7. `INDEX idx_external_asset_index_status (index_status)`
8. `INDEX idx_external_asset_permission (permission_status)`
9. `INDEX idx_external_asset_sync (sync_status)`
10. `INDEX idx_external_asset_event (last_event_id)`
11. `INDEX idx_external_asset_seen (last_seen_at)`
12. `INDEX idx_external_asset_updated_utc (updated_at_utc)`
13. `INDEX idx_external_asset_kind (asset_kind)`

MySQL 8 约束：

1. `JSON` 字段使用 MySQL `JSON` 类型，不用 `TEXT` 代替。
2. 初版不依赖 JSON 内部索引。
3. 使用 `utf8mb4`，注意唯一键长度和索引名长度。
4. `source_path`、`storage_path`、`logical_path`、`storage_location` 为 `TEXT`，不建普通索引。

PostgreSQL 说明：

1. 等价 JSON 字段可用 `JSONB`。
2. JSONB + GIN 属于后续评估，不扩大 DB-2 实现范围。

## 7. Checkpoint 与 rollback

`external_asset_sync_checkpoint` 的最终合同见 `docs/DB2_CHECKPOINT_AND_ROLLBACK_CONTRACT.md`。

核心冻结点：

1. checkpoint 粒度默认 `source_system + ":" + source_view`。
2. 未来可扩展为 `source_system + ":" + source_view + ":" + project_id`。
3. 每次 sync run 必须有 `run_id`。
4. 失败恢复必须从上一个成功 checkpoint + overlap window 继续。
5. checkpoint rollback 只影响下一次同步游标，不影响 NAS、平台 MySQL、`documents`、`chunks`、Qdrant、OpenSearch 或 memory kernel。

## 8. 权限默认值

权限默认值合同见 `docs/DB2_PERMISSION_DEFAULTS.md`。

冻结规则：

1. `permission_status` 缺省 `DENIED`。
2. `permission_tags` 缺失时 `DENIED`。
3. `project_scope` 缺失时不得进入 prompt。
4. 无 `project_id` 的资产默认不得进入用户检索上下文。
5. 服务级 DB 账号可读不等于终端用户有权查看全部资产。
6. catalog-only 资产在正文回答场景必须返回 Missing Evidence，建议 reason 为 `asset_catalog_only`。

## 9. DB-3 前置门槛

在以下条件满足前，不进入 DB-3：

1. DB-2 schema contract 已冻结。
2. View 字段映射已冻结。
3. checkpoint / rollback 合同已冻结。
4. fake fixture acceptance case 通过。
5. temporary DB proof-of-contract 通过。
6. 权限默认 `DENIED` 规则通过测试。
7. catalog-only 不进入 retrieval 通过测试。
8. 数据库 / NAS 团队单独授权进入真实平台对接。
9. 用户单独授权 DB-3 范围。

DB-3 才允许讨论 selective indexing、preview index、full text、semantic index、Hermes_memory evidence pack 与 OpenSearch / Qdrant 写入。DB-3 不自动继承 DB-2 的授权。
