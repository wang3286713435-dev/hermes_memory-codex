# DB-4A Readonly DB Preflight Skeleton

日期：2026-05-09

## 目标

DB-4A 把数据库团队的连接合同落到 Hermes_memory 侧的本地预检接口中，但仍不连接真实 MySQL。当前阶段只验证四个只读 View 的字段合同、source identity、权限 fail-closed 和 checkpoint candidate 能否稳定归一化到 catalog preview DTO。

## 已吸收的数据库团队合同

1. `source_system` 固定为 `delivery_platform`。
2. `source_contract_version` 固定为 `delivery_platform.asset_views.v1`。
3. 当前只允许四个 View：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
4. `asset_uid` 使用三段式：`source_system + ":" + source_view + ":" + source_id`。
5. `AuditEventView.event_id` 是主 checkpoint candidate。
6. `created_at` overlap window 后续保留为 DB-4B/DB-4C 真实只读 smoke 的输入要求。
7. `permission_tags`、`project_scope`、`confidentiality_level` 当前没有稳定 View 字段，Hermes 必须默认 deny。

## 当前实现

新增 `AssetCatalogReadonlyPreflightValidator`。它接收已经在内存中的 View rows，不打开数据库连接，不读取 NAS，不触发 REST，不写任何 mirror/index/retrieval 表。

预检输出：

1. `AssetCatalogReadonlyPreflightResult`
2. `AssetCatalogMirrorPreview`
3. 每行 `AssetCatalogMirrorPreviewItem`
4. 字段缺失或合同漂移 findings

默认行为：

1. 缺权限字段时 `permission_status = denied`。
2. 每个 preview item 的 `action = would_deny`。
3. `reason = missing_permission_contract`。
4. `citation_status = metadata_only`。
5. `evidence_kind = asset_catalog_evidence`。
6. `content_evidence_available = false`。
7. 所有 write flags 均为 `false`。

## 安全配置

新增配置默认值：

1. `platform_asset_readonly_db_enabled = false`
2. `platform_asset_readonly_db_dsn = None`
3. `platform_asset_readonly_db_user = None`
4. `platform_asset_readonly_db_contract_version = delivery_platform.asset_views.v1`

这些配置只是 DB-4B 真实只读 smoke 的显式门槛。DB-4A 不使用 DSN，也不连接数据库。

## 禁止范围

DB-4A 不做：

1. 不连接真实 MySQL。
2. 不创建 migration。
3. 不写 `external_asset_catalog`。
4. 不扫描真实 NAS。
5. 不读真实文件正文。
6. 不触发平台 REST。
7. 不写 `documents` / `chunks`。
8. 不写 OpenSearch / Qdrant。
9. 不创建 embedding。
10. 不进入真实 retrieval/indexing。
11. 不开放 Agent 写操作。

## DB-4B 前置门槛

进入真实只读 staging smoke 前必须满足：

1. 用户单独授权 DB-4B。
2. 平台/运维提供 staging 或 dev 联调 DSN。
3. 提供企业 Agent 专用只读账号，不使用应用主账号。
4. 只读账号只能 SELECT 四个 View。
5. 不授予业务底表 SELECT。
6. 不授予 INSERT / UPDATE / DELETE / DROP / ALTER。
7. 明确是否允许暴露样例中的真实 NAS 路径和项目名。
8. DB-4A 本地预检、lint、py_compile、boundary grep 通过。

DB-4B 也仍然只允许只读 smoke：查询小样本、归一化为 preview DTO、fail closed。mirror write、migration、NAS scan、documents/chunks、OpenSearch/Qdrant、selective indexing 继续后置。
