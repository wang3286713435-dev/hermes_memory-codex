# DB Schema Gap Sanitized Response

日期：2026-05-11
回复方：数字化交付平台数据库团队 Codex
范围：仅基于当前仓库 schema / migration / View 定义做脱敏评审；未连接数据库、未读取真实行、未输出 secret / 真实项目名 / 文件名 / NAS 路径 / `asset_uid` / `source_id` / raw row。

## 1. P1 字段短期可补评审

| 字段 | 短期结论 | 建议落点 | 说明 |
|---|---|---|---|
| `permission_tags` | 可短期补“粗粒度标签”，不可作为完整 ACL | View v1.1 + REST contract | 可派生 `PROJECT:<project_id>`、`SOURCE:<source_type>`、`CONFIDENTIALITY:INTERNAL_DEFAULT` 等非用户态标签；不能表达用户级权限。Hermes 仍必须 fail closed。 |
| `project_scope` | 可短期补 | REST contract 优先，View 可补粗粒度 | REST / API Key 层可返回 `ALL_PROJECTS` / `SPECIFIC_PROJECTS` / project id list；View 层只能暴露资产所属 project，不应表达调用者可见范围。 |
| `confidentiality_level` | 可短期补默认值 | View v1.1 + REST contract | 当前没有正式密级表。可先给 `INTERNAL` 或 `UNKNOWN`。建议默认 `UNKNOWN` 更保守；Hermes 不得推断为低敏。 |
| `ModelAssetView.project_id` | 可短期补 | View v1.1 | 当前源表两条分支都具备项目 ID 来源：模型集成分支有 `mi.project_id`，NAS 文件分支有 `f.project_id`。建议尽快补。 |
| `last_seen_at` | 可短期补“派生字段” | View v1.1 | `data_file_resources.last_verified_at` 已存在，可作为文件最近验证时间；为空时可降级使用 `updated_at`，但字段语义应标注为 derived，不等同于 NAS 实时存在证明。 |
| `lifecycle / missing / moved / stale` | 可短期补保守版，完整语义后置 | REST contract 优先，View 可先给 `lifecycle_status` | 当前可安全表达 `active` / `unknown` / `deleted_candidate` 等保守状态；`missing`、`moved`、`stale` 需要扫描报告、路径验证策略和时间阈值确认后再稳定。 |
| `index_eligibility` | 可短期补保守版 | View v1.1 + REST contract | 建议短期默认 `catalog_only`。`preview_allowed`、`full_text_allowed`、`semantic_allowed` 需结合权限、密级、文件类型和数据负责人策略后再开放。 |

## 2. 建议后置字段与原因

1. 完整 `permission_tags` / full ACL snapshot：当前 View 是稳定资产读模型，不带调用者身份上下文；完整权限需要 API Key、用户项目授权、角色权限或 ACL 快照共同决定。
2. 完整 `project_scope` 用户可见范围：这是调用者 / API Key 维度的授权问题，不是资产静态字段；建议通过 REST permission contract 或 Hermes precondition 配置注入。
3. 精确 `confidentiality_level`：当前没有正式密级来源表或业务确认规则；短期只能 `UNKNOWN` / `INTERNAL_DEFAULT`，不能当作真实密级。
4. 精确 `missing` / `moved` / `stale` 生命周期：需要 NAS 路径复验、扫描任务状态、路径变更规则、stale 时间阈值和人工确认机制。
5. `full_text_allowed` / `semantic_allowed` 级别的 `index_eligibility`：会进入 DB-3 retrieval / indexing 范围，需要数据负责人审批、外部持久化策略、权限过滤和脱敏策略共同确认。
6. `is_latest`、version lineage、retention / archive policy、BIM component / ontology / graph 字段：属于版本治理、归档治理和二 / 三期 BIM 语义能力，不进入 DB-2 View 合同。

## 3. `AuditEventView.event_id` 语义确认

当前 `AuditEventView.event_id` 来源于 `core_audit_logs.id`，该字段在当前 schema 中定义为 `BIGINT PRIMARY KEY AUTO_INCREMENT`。

数据库团队结论：

```yaml
event_id_monotonic: true
checkpoint_usable: true
recommended_checkpoint: "AuditEventView.event_id"
```

使用约束：

1. 可作为 Hermes checkpoint / incremental sync 主游标。
2. 推荐按 `event_id > :last_event_id ORDER BY event_id ASC LIMIT :limit` 拉取。
3. `created_at` 只能作为 overlap window 辅助字段，不应单独作为 checkpoint。
4. 如果未来发生跨库合并、审计表重建、数据导入重排，需要重新评审 checkpoint 语义。

## 4. 后续 `LIMIT 30` 脱敏统计 smoke 授权口径

数据库团队同意后续执行，但仅限“脱敏统计 smoke”，不得输出 raw row。

允许输出：

1. `row_count`
2. `null_count_by_field`
3. `distinct_count_by_safe_enum_field`
4. `min/max timestamp`
5. `field_presence`
6. `type compatibility`

禁止输出：

1. 真实项目名
2. 真实文件名
3. 真实 NAS 路径
4. `asset_uid`
5. `source_id`
6. raw row
7. secret
8. 任何可反推出业务内容的明细值

建议 smoke 模式：

```yaml
limit_30_desensitized_stats_smoke: allowed
raw_row_output: forbidden
external_persistence: forbidden
```

## 5. Contract Version 建议

建议新增合同版本：

```text
delivery_platform.asset_views.v1.1
```

建议 v1.1 范围：

1. `ModelAssetView.project_id`
2. `permission_tags` 粗粒度派生标签
3. `confidentiality_level` 保守默认值
4. `last_seen_at` 派生字段
5. `lifecycle_status` 保守枚举
6. `index_eligibility` 保守枚举，默认 `catalog_only`
7. 明确 `AuditEventView.event_id` 为 checkpoint 主游标

不建议在 v1.1 中承诺：

1. 完整 ACL snapshot
2. 用户态 `project_scope` 最终权限
3. full-text / semantic indexing 可用性
4. 精确 missing / moved / stale 判定
5. BIM component / graph / ontology 字段

最终建议：DB-2 可以推进 `asset_views.v1.1` 的结构合同评审，但 Hermes mirror 在权限字段未形成强证明前仍必须默认 `DENIED`。

## 6. 第 6 节确认回复

数据库团队后续确认：

```yaml
contract_version_next: delivery_platform.asset_views.v1.1
status: approved_for_structure_contract_design
data_access_scope: structure_only
raw_rows_allowed: false
```

字段落点：

| 字段 | 落点 | 说明 |
|---|---|---|
| `permission_tags` | View + REST | View 提供静态粗粒度标签；REST 可叠加调用者 / API Key 授权上下文。 |
| `project_scope` | REST 为主 | 调用者授权范围，不建议在静态 View 中表达为“可见范围”；View 只补资产所属 `project_id`。 |
| `confidentiality_level` | View + REST | v1.1 先给保守默认值。 |
| `ModelAssetView.project_id` | View + REST | 短期补入 View，REST 同步返回。 |
| `last_seen_at` | View + REST | 从已有验证 / 更新时间字段派生，语义标注为 derived。 |
| `lifecycle_status` | View + REST | 短期保守枚举，复杂 missing / moved 精判后置。 |
| `index_eligibility` | View + REST | v1.1 默认 `catalog_only`。 |

`permission_tags` 固定为以下格式，仅表达静态资产治理标签，不表达最终用户权限：

```text
SOURCE_SYSTEM:delivery_platform
SOURCE_VIEW:<ProjectAssetView|FileAssetView|ModelAssetView|AuditEventView>
ASSET_KIND:<PROJECT|FILE|MODEL|AUDIT_EVENT>
PROJECT:<project_id>
CONFIDENTIALITY:<UNKNOWN|INTERNAL>
INDEX_ELIGIBILITY:<catalog_only|preview_allowed|full_text_allowed|semantic_allowed>
```

`confidentiality_level` 默认值采用 `UNKNOWN`。

`lifecycle_status` 短期枚举：

```text
active
archived
unknown
deleted_candidate
stale_unverified
```

短期不确认静态精确枚举：

```text
missing
moved
```

`index_eligibility` 短期默认 `catalog_only`，保留 `preview_allowed` / `full_text_allowed` / `semantic_allowed` 枚举空间，但未授权 DB-3 / indexing 前不得自动升级。

v1.1 完成后允许重新执行 structure-only smoke，范围仅限 `SHOW COLUMNS`、`WHERE 1 = 0`、字段存在性校验、类型兼容校验和 contract version 校验。

仍禁止 `LIMIT 30`、真实行读取、DB 写入、NAS scan、mirror migration、OpenSearch / Qdrant / MinIO 写入、indexing 和 Agent CRUD。
