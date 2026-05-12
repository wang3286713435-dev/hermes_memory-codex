# CODEX DB v1.1 Field Confirmation Prompt

用途：发给数据库团队 Codex，用于按已确认口径推进 `delivery_platform.asset_views.v1.1` 字段落点。

## 背景

Hermes / 数据管家已经完成真实 DB `structure_only` smoke：

1. DB reachable。
2. database name matches expected。
3. `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView` 四个 View 存在。
4. `SHOW COLUMNS` 与 `WHERE 1 = 0` 均通过。
5. 未读取真实行、未输出 secret / 真实业务数据、未写任何系统。

数据库团队已返回 sanitized response，建议推进：

```text
delivery_platform.asset_views.v1.1
```

## 当前目标

数据库团队已确认推进 `delivery_platform.asset_views.v1.1`。请按以下 v1.1 口径推进 View / REST contract 修改，并返回脱敏执行报告。

本 prompt 不要求输出真实数据，不要求读取真实行。

## 已确认的 v1.1 口径

```yaml
contract_version_next: delivery_platform.asset_views.v1.1
status: approved_for_structure_contract_design
data_access_scope: structure_only
raw_rows_allowed: false
```

v1.1 只作为 View / REST contract 结构演进，不代表授权真实样例读取、索引写入、mirror migration 或 Agent CRUD。

## 字段落点

请按以下落点实现或确认：

| 字段 | 落点 | 要求 |
|---|---|---|
| `permission_tags` | View + REST | View 提供静态粗粒度标签；REST 可叠加调用者 / API Key 授权上下文。 |
| `project_scope` | REST 为主 | 调用者授权范围，不建议在静态 View 中表达为“可见范围”；View 只补资产所属 `project_id`。 |
| `confidentiality_level` | View + REST | 默认值采用 `UNKNOWN`。 |
| `ModelAssetView.project_id` | View + REST | 必须补入 View，REST 同步返回。 |
| `last_seen_at` | View + REST | 可由已有验证 / 更新时间字段派生，语义标注为 derived。 |
| `lifecycle_status` | View + REST | 使用短期保守枚举。 |
| `index_eligibility` | View + REST | 默认 `catalog_only`。 |

## `permission_tags` 枚举

v1.1 固定为以下格式，仅表达静态资产治理标签，不表达最终用户权限：

```text
SOURCE_SYSTEM:delivery_platform
SOURCE_VIEW:<ProjectAssetView|FileAssetView|ModelAssetView|AuditEventView>
ASSET_KIND:<PROJECT|FILE|MODEL|AUDIT_EVENT>
PROJECT:<project_id>
CONFIDENTIALITY:<UNKNOWN|INTERNAL>
INDEX_ELIGIBILITY:<catalog_only|preview_allowed|full_text_allowed|semantic_allowed>
```

约束：

1. 不使用真实项目名、项目编码、文件名、路径作为 tag。
2. `PROJECT:<project_id>` 只表示资产归属项目，不表示调用者有权访问。
3. Hermes mirror 仍必须 fail closed：没有 REST / API Key 权限证明时默认 `DENIED`。

## 字段默认值 / 枚举

### `confidentiality_level`

默认值采用：

```text
UNKNOWN
```

不得默认 `INTERNAL`，避免误解为“已完成内部可见性判定”。

### `lifecycle_status`

短期枚举确认如下：

```text
active
archived
unknown
deleted_candidate
stale_unverified
```

暂不使用短期精确枚举：

```text
missing
moved
```

原因：`missing` / `moved` 需要 NAS 路径复验、扫描任务报告、移动判定规则和人工确认机制；当前不应仅由 View 静态字段推断。

### `index_eligibility`

短期默认值：

```text
catalog_only
```

v1.1 可保留枚举空间：

```text
catalog_only
preview_allowed
full_text_allowed
semantic_allowed
```

除非后续单独授权 DB-3 / indexing，实际返回应默认 `catalog_only`。不得因为文件类型可解析就自动升级到 full-text 或 semantic。

## 执行后请返回

如果本轮你们会改数据库 View / migration，请只输出脱敏执行报告：

1. changed files
2. migration / View name
3. validation command
4. sanitized result
5. 是否未读取真实行
6. 是否未输出 secret / raw row / 真实项目名 / 文件名 / NAS 路径
7. 是否确认 Hermes 测试机可重新执行 `structure_only` smoke

## 严格禁止输出

1. secret / token / password / API key / `.env` 真值。
2. 真实项目名。
3. 真实文件名。
4. NAS 路径。
5. `asset_uid` / `source_id`。
6. raw row。
7. 任何可反推出真实业务内容的明细值。

## 严格禁止动作

除非数据库团队内部已明确授权，否则不要：

1. 输出真实行。
2. 执行 `LIMIT 30` 真实样本报告。
3. 扫描 NAS。
4. 写 Hermes Memory DB。
5. 写 OpenSearch / Qdrant / MinIO。
6. 触发 Hermes mirror / indexing。
7. 实现 Agent DB CRUD。
8. 进入 production rollout。

## Hermes 接收标准

Hermes 侧会按以下规则接收 v1.1：

1. `permission_tags` 缺失：deny。
2. `project_scope` / caller scope 缺失：不得进入 prompt。
3. `confidentiality_level=UNKNOWN`：按敏感处理。
4. `index_eligibility=catalog_only`：只允许资产目录展示，不作为正文 evidence。
5. `AuditEventView.summary` 不得作为正文 evidence 或 confirmed facts。
6. `project_scope` 的最终调用者授权以 REST / API Key 上下文为准；静态 View 只提供资产归属。
7. v1.1 完成后，先重跑 structure-only smoke；通过后才考虑是否另行授权 `LIMIT 30` 脱敏统计 smoke。
