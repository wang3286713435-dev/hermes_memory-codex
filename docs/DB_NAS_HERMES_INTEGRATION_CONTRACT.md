# DB / NAS 与 Hermes Agent 融合接入契约

日期：2026-05-09
版本：v2
阶段：Phase DB-0 docs-only contract freeze
面向对象：主开发 Agent、数据库 / 数字化交付平台团队、项目审查 Agent
状态：canonical contract，不是实现任务

## 0. 主开发 Agent 阅读规则

本文件是后续数据库 / NAS 接入企业 Agent 的主契约。主开发 Agent 后续规划或实现 DB/NAS 相关能力时，应优先遵守本文档，而不是临时猜测平台表结构、NAS 路径、权限模型或 MCP 用途。

当前只允许 docs-only 契约冻结；不得因为本文档存在而自动进入真实 MySQL、真实 NAS、真实 REST、真实 index 写入。

任何偏离本文档的开发计划，都必须先经过用户确认。

## 1. 总体定位

数据库 / NAS 接入是企业 Agent 的并行长期主线，不应打断当前 MVP 主线。

命名约定：

1. 后续统一把公司级企业 Agent 称为“数据管家”。
2. 数据管家不是 DB / NAS / BIM 项目的别名，而是 Hermes 企业 Agent 的产品化角色。
3. DB / NAS / TB BIM 接入只是数据管家的“资产治理 / 平台连接”能力模块之一。
4. 当前 MVP 主线继续优先落地文件、标书、会议、Excel / PPTX、上传、citation、Missing Evidence 和人工复核能力。

目标架构：

```text
NAS / 原始业务库
  -> 数字化交付平台
     -> MySQL 8 / Spring Boot / Flyway / OpenAPI
     -> ProjectAssetView / FileAssetView / ModelAssetView / AuditEventView
     -> REST API / 审计 / API Key / 项目授权
  -> Hermes_memory
     -> 只读 asset catalog sync
     -> external_asset_catalog mirror
     -> metadata / preview / selective full-text / selective semantic index
     -> permission / citation / trace / Missing Evidence
  -> Hermes Agent
     -> pre-model memory kernel 检索
     -> MCP tools 只做外围平台查询与受控动作申请
```

核心分工：

1. 数字化交付平台是 NAS / 资产治理 source of truth。
2. Hermes_memory 是 memory index / governance layer，不替代平台资产库。
3. Hermes Agent 基于 pre-model evidence 回答问题，不直接接管数据库或 NAS。
4. MCP 只是外部平台工具适配层，不替代 Hermes memory kernel。

## 2. 不变原则

主开发 Agent 不得违反以下原则：

1. 不直接扫描 NAS 作为 Hermes_memory 正式数据源。
2. 不复制 10TB NAS。
3. 不全量解析 NAS。
4. 不全量 chunk。
5. 不全量 embedding。
6. 不直接写平台 MySQL 业务底表。
7. 不直接删除、移动、覆盖、改名 NAS 文件。
8. 不让 Agent 绕过平台权限把无权限内容注入 prompt。
9. 不让 facts 替代 retrieval evidence。
10. 不把 MCP 作为企业知识主检索链路。
11. 不把 catalog-only 资产伪装成正文 citation。
12. 不在当前 DB-0 / DB-1 阶段引入 Data Steward、BIM 深度图谱、Neo4j、PostGIS、生产 scheduler。

任何真实 MySQL / NAS / REST / index 写入，都必须另开阶段并获得用户显式授权。

## 3. 已确认的平台侧接口理解

### 3.1 技术栈

已理解的平台技术路径：

1. 后端：Java / Spring Boot。
2. 数据库：MySQL 8。
3. 数据库迁移：Flyway。
4. API 契约：OpenAPI / Springdoc。
5. 缓存：Redis。
6. 对象存储：MinIO。
7. NAS 入口：SMB 挂载。
8. 当前重点目录：`/Volumes/zyzn/卓羽智能项目`。

Hermes_memory 不要求平台切换技术栈，也不要求平台将正式资产治理逻辑迁移到 Hermes_memory。

### 3.2 稳定读模型

Hermes_memory 短期只消费平台稳定 View / Read Model。

允许读取：

| View | 用途 |
|---|---|
| `ProjectAssetView` | 项目级资产总览、项目过滤、项目范围内文件查询 |
| `FileAssetView` | 文件资产目录、路径、类型、大小、更新时间、checksum 状态 |
| `ModelAssetView` | BIM / 模型资产目录、格式、专业、版本、预览状态、轻量化状态 |
| `AuditEventView` | 增量同步、事件回放、审计追踪、trace 对齐 |

禁止直接依赖：

1. `data_file_resources`
2. `data_asset_scan_candidates`
3. `data_asset_import_jobs`
4. `data_asset_import_rows`
5. 其他平台正式业务表、候选表、任务表、导入临时表

如果 View 不能满足需求，优先由平台扩展 View 或 REST API，而不是让 Hermes_memory 读取底表。

## 4. View Contract 与字段分级

平台侧应提供版本化 View contract。Hermes_memory adapter 必须绑定 contract version，不自行推断字段含义。

契约要求：

1. 每个 View 提供 contract version。
2. 字段新增可以兼容。
3. 字段删除、改名、改义必须走评审。
4. 字段类型、主键、更新时间、事件顺序语义需要写入 contract。
5. SQL View 本身不负责分页；DB 直读 View 时由 Hermes_memory adapter 负责 `limit` / cursor / checkpoint。
6. REST API 由平台提供分页参数。
7. 大规模同步必须按 checkpoint 拉取，不允许一次性全量拉大表。

### 4.1 P0：当前可对接字段

P0 字段用于 DB-1 / DB-2 fake adapter、sync preview 和 asset catalog mirror 的最小闭环。

| 字段 | 说明 |
|---|---|
| `project_id` / project identifier | 项目边界与最小权限过滤依据 |
| `file_id` / platform asset id | 平台文件资产标识 |
| `source_path` / storage path | 文件路径或平台存储路径 |
| `file_name` | 文件名 |
| `file_ext` / file type | 文件扩展名或类型 |
| `file_size` | 文件大小 |
| `created_at` | 平台记录创建时间 |
| `updated_at` | 平台记录更新时间，仅辅助判断 |
| model format / discipline / version fields | `ModelAssetView` 模型元数据 |
| audit event id / created_at | `AuditEventView` 增量同步候选依据 |

注意：`updated_at` 只能作为辅助字段，不作为唯一增量依据。

### 4.2 P1：需要平台补充字段

P1 字段不是 DB-1 / DB-2 阻塞项，但进入真实只读联调、权限过滤和后续 indexing 前需要逐步补齐。

| 字段 | 用途 |
|---|---|
| `permission_tags` | Hermes_memory pre-model 权限过滤 |
| `project_scope` | 服务级同步后的用户请求范围过滤 |
| `lifecycle_status` | 排除 deleted / archived / unavailable 资产 |
| `content_hash` / checksum | 内容变更、移动识别、索引失效 |
| NAS `modified_at` | 原始文件 mtime，辅助判断内容变化 |
| `last_seen_at` | 判断 missing / stale / moved |
| missing / stale / moved status | 文件缺失、过期、疑似移动状态 |
| index eligibility fields | 是否可 preview / full-text / semantic indexing |

### 4.3 P2：后续权限 / 密级 / 版本治理字段

P2 字段属于后置治理能力，不作为 DB-1 / DB-2 阻塞项。

| 字段 | 用途 |
|---|---|
| `confidentiality_level` | 密级过滤 |
| full ACL snapshot | 用户 / 部门 / 角色 / 密级完整映射 |
| owner / department / customer | 企业治理维度 |
| `is_latest` | 多版本资产选择 |
| version lineage | 版本链、历史版本、回滚定位 |
| retention / archive policy | 归档与保留策略 |

## 5. 权限模型

只读 MySQL View 适合平台到 Hermes_memory 的 asset catalog 同步，但只读服务账号不代表终端用户可见全部内容。

必须遵守：

1. DB 只读账号是服务级同步账号，不是终端用户权限。
2. Hermes_memory mirror 必须保存 `project_scope` / `permission_tags` / 最小可行权限标签，后续再扩展 ACL snapshot。
3. Hermes_memory retrieval 阶段必须按用户、项目、权限标签、密级状态做 pre-model 权限过滤。
4. 无 `project_id`、无权限标签、权限不匹配、生命周期状态不允许的资产，不得进入 prompt。
5. answer guard 必须检查 citation 是否来自用户可见资产。

短期最小可行权限方案：

1. 按 `project_id` / `project_scope` 做访问边界。
2. 未归属项目的文件默认不可进入 prompt。
3. 敏感目录、投标、合同、报价、内部评审默认不进入正文索引。
4. 后续再补 `permission_tags`、`confidentiality_level`、ACL snapshot。

`permission_tags` 缺失时，Hermes_memory 默认策略为 deny。

## 6. 增量同步与变化识别

短期增量同步优先使用 `AuditEventView` / 事件流。

约束：

1. `updated_at` 只能作为辅助，不作为唯一增量依据。
2. NAS 原始 `modified_at`、`last_seen_at`、missing / stale / moved 状态需要平台后续补充或通过 API 暴露。
3. Hermes_memory 不应只靠路径和 `updated_at` 判断内容变化。
4. 大规模同步必须按 checkpoint 拉取，不允许一次性全量拉大表。

checkpoint 策略：

1. 优先使用单调递增的 `event_id`。
2. 如果只能使用 `created_at`，必须同时记录 tie-breaker，例如 `event_id` 或 source id。
3. 对乱序事件保留 overlap window，并按 asset key 幂等 upsert。
4. checkpoint 记录在 Hermes_memory 本地 mirror，不覆盖平台 checkpoint。

路径 / 内容变化处理：

1. 路径变化但 checksum 相同：标记为 moved，更新 catalog 当前路径，旧路径标记 stale，不重复建立 semantic index。
2. 路径相同但 checksum 变化：标记为 content_changed，失效旧 preview / full-text / semantic index，等待重新授权或重新 indexing。
3. 路径缺失且 `last_seen_at` 过期：标记为 missing / stale，不进入 prompt。
4. checksum 缺失时：只能作为疑似变化，不得静默复用旧正文 evidence。

## 7. Hermes_memory 内部实现契约

### 7.1 默认 feature flags

后续新增能力必须默认关闭：

```env
PLATFORM_ASSET_CATALOG_ENABLED=false
PLATFORM_ASSET_SYNC_WRITE_ENABLED=false
PLATFORM_ASSET_MCP_ENABLED=false
PLATFORM_ASSET_SEMANTIC_INDEX_ENABLED=false
```

### 7.2 内部抽象

后续可新增以下抽象，但 DB-0 不实现代码：

| 抽象 | 职责 |
|---|---|
| `PlatformAssetCatalogClient` | 读取平台稳定 View / 后续 REST read API |
| `AssetCatalogSyncService` | 只读同步 asset catalog 与 sync checkpoint |
| `AssetCatalogQueryService` | 提供资产目录查询与 evidence 构建 |
| `AssetIndexPlanner` | 判断资产是否可进入 preview / full-text / semantic index |
| `OperationPlanService` | 生成需人工审批的操作计划 |

### 7.3 Asset key

Hermes_memory mirror 不直接假设平台 `file_id` 全局唯一。建议使用组合键：

```text
asset_uid = source_system + ":" + source_id
```

其中 `source_id` 可映射平台 `file_id`。即使平台确认 `file_id` 全局稳定唯一，Hermes_memory 仍应保留 `source_system` 作为跨系统隔离前缀。

### 7.4 Catalog-only mirror 草案

后续 DB-2 可新增独立 mirror，例如 `external_asset_catalog`。

草案字段：

| 字段 | 说明 |
|---|---|
| `asset_uid` | Hermes_memory 内部资产唯一键 |
| `source_system` | 例如 `delivery_platform` |
| `source_id` | 平台 `file_id` / model id |
| `source_view` | 来源 View |
| `project_id` | 项目边界 |
| `project_scope` | 权限范围 |
| `source_path` | 当前路径 |
| `file_name` | 文件名 |
| `file_ext` | 扩展名 |
| `file_size` | 文件大小 |
| `created_at` | 平台创建时间 |
| `updated_at` | 平台更新时间 |
| `modified_at` | NAS mtime，P1 |
| `last_seen_at` | 最近扫描看到时间，P1 |
| `content_hash` | checksum，P1 |
| `lifecycle_status` | 生命周期状态，P1 |
| `permission_tags` | 权限标签，P1 |
| `confidentiality_level` | 密级，P2 |
| `index_status` | catalog / preview / full_text / semantic |
| `citation_status` | none / metadata_only / content_citable |
| `sync_status` | active / moved / stale / missing |
| `contract_version` | View contract version |
| `last_event_id` | 同步事件 |
| `last_synced_at` | Hermes_memory 同步时间 |

catalog-only 资产不得写入现有 `documents` / `chunks`，不得写入 Qdrant / OpenSearch。

## 8. Retrieval / Evidence 契约

后续 DB-3 可新增 asset catalog retrieval provider，但不得破坏现有 retrieval contract。

允许回答：

1. 某项目有哪些文件。
2. 某模型是否登记。
3. 某文件路径 / 大小 / checksum / 更新时间 / 项目归属。
4. 某资产是否已 preview / full-text / semantic indexed。

必须 Missing Evidence：

1. 用户询问文件正文内容，但该 asset 只有 catalog。
2. 用户要求依据文件作结论，但该 asset 未进入可 citation 的索引层。
3. 用户无项目权限或资产无权限标签。

context 必须区分：

1. `asset_catalog_evidence`
2. `document_content_evidence`
3. `semantic_index_evidence`

Missing Evidence 标准响应：

```json
{
  "status": "missing_evidence",
  "reason": "asset_catalog_only",
  "asset_uid": "<source_system:source_id>",
  "available_evidence": "asset_catalog",
  "required_evidence": ["preview_index", "full_text_index", "semantic_index"],
  "deep_index_required": true,
  "permission_status": "allowed_or_denied",
  "citation_status": "metadata_only",
  "next_action": "request_selective_indexing_authorization"
}
```

如果用户无权限，则 `permission_status=denied`，不得返回敏感路径、正文片段或可推断内容。

## 9. MCP Server 契约

MCP Server 是外围工具适配层，不是 memory kernel 主链路。

DB-4 查询 tools：

| Tool | 数据源 / 接口 | 权限 |
|---|---|---|
| `search_project_assets` | `ProjectAssetView` | 只读 |
| `search_file_assets` | `FileAssetView` | 只读 |
| `get_model_assets` | `ModelAssetView` | 只读 |
| `get_asset_events` | `AuditEventView` | 只读 |

动作 tools 后置，先接 fake REST：

| Tool | 接口 | 边界 |
|---|---|---|
| `trigger_nas_scan` | REST / OpenAPI | 需授权 |
| `trigger_checksum` | REST / OpenAPI | 需授权 |
| `submit_asset_annotation` | REST / OpenAPI | 需人工审核 |
| `submit_delete_request` | REST / OpenAPI | 只提交申请 |

MCP tool 返回结果必须包含：

1. `source_view`
2. `trace_id`
3. `permission_status`
4. `citation_status`
5. `project_scope`
6. `contract_version`

MCP Server 禁止：

1. 直接写 MySQL 正式表。
2. 直接读平台业务底表。
3. 直接删除、移动、改名 NAS 文件。
4. 绕过 API Key、项目授权和平台审计。
5. 把工具查询结果当作 memory kernel 主证据链替代品。

## 10. Selective Indexing 契约

默认索引状态：

1. `catalog_only`
2. `metadata_indexed`
3. `preview_indexed`
4. `full_text_indexed`
5. `semantic_indexed`
6. `curated_memory`
7. `archived`
8. `excluded`

默认规则：

1. 10TB NAS 不做全量正文解析。
2. 10TB NAS 不做全量 chunk。
3. 10TB NAS 不做全量 embedding。
4. BIM / CAD / 音视频 / 大压缩包短期只做 catalog / metadata。
5. 只有高价值、已授权、结构可解析、citation 可定位的文件可进入 semantic indexing。

selective indexing 的人工授权入口后续优先走平台 REST / OpenAPI 的申请流程；在平台接口固化前，Hermes_memory 只生成本地 index request preview，不执行真实 indexing。

授权记录至少需要：

1. `asset_uid`
2. `source_path`
3. `content_hash`
4. `project_id`
5. 授权人
6. 授权范围
7. 允许的索引等级：preview / full-text / semantic
8. citation capability
9. parser version
10. embedding model
11. 过期或撤销策略

默认 excluded：

1. 未归属项目文件。
2. 权限标签缺失且未人工授权文件。
3. 投标、合同、报价、内部评审目录。
4. 人事、财务、法务、客户敏感资料。
5. 大压缩包、音视频、CAD / BIM 原生大文件。
6. 临时文件、缓存文件、隐藏文件、系统文件。
7. 路径或 checksum 状态异常文件。

## 11. Trace 与审计契约

当前 DB-0 / DB-1 只定义 trace 对齐字段，不真实写平台审计。

边界：

1. Hermes_memory 可保留本地 trace。
2. 联调阶段设计 Hermes_memory `trace_id` 与平台 trace_id / event_id 的映射。
3. 平台 agent trace 写入、API Key、项目范围授权属于后续批次能力。
4. 后续 Batch 3 固化 API Key 与 agent audit API 后，再接入平台 audit / trace write。
5. 在 API 固化前，Hermes_memory 不向平台写 agent trace。

## 12. Operation Plan 契约

Hermes Agent 可以生成 operation plan，但当前不能直接执行真实修复、删除、归档、重建索引。

约束：

1. operation plan 是建议，不是执行结果。
2. operation plan 写入平台前必须有人工确认。
3. 涉及删除、移动、权限修改、批量重建索引的 plan 必须标记 high-risk。
4. plan 必须记录 evidence、影响范围、回滚建议和审批人。
5. plan 默认不触发 DB / NAS / index 写入。

## 13. 真实 NAS 试点范围

DB-1 / DB-2 可以先使用 fake View fixtures 模拟以下三个项目：

1. `101-C塔`
2. `98-深圳口岸项目`
3. `99-丰图既有建模项目`

边界：

1. 真实 NAS 连接必须等待平台和用户授权。
2. 不直接扫描 `/Volumes/zyzn/卓羽智能项目` 作为 Hermes_memory 的正式数据源。
3. fake fixtures 可以模拟项目、文件、模型、事件、权限标签缺失、checksum 缺失、moved / stale 等状态。
4. 真实联调前必须明确目录白名单、敏感目录黑名单、账号权限和审计要求。

## 14. Phase Gate

以下 phase gate 属于独立 DB 分支路线，可与当前 MVP 主线并行推进。进入任何下一阶段前都必须 Codex B review，不得自动跨阶段。

### DB-0：契约冻结

目标：

1. 对齐 View 清单、字段含义、权限边界、trace_id、事件同步方式。
2. 不连接真实 MySQL。
3. 不连接真实 NAS。

### DB-1：Fake View Adapter

目标：

1. 使用 fake / fixture 实现 `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView` adapter。
2. 不写 Qdrant / OpenSearch。
3. 不做正文解析。

### DB-2：Asset Catalog Mirror

目标：

1. 建立 Hermes_memory 独立 asset catalog mirror。
2. 保存平台 View 的规范化元数据、checkpoint、`project_scope`、`permission_tags` 占位。
3. catalog-only 不进入 `documents` / `chunks`。

### DB-3：Catalog Retrieval

目标：

1. 支持项目 / 文件 / 模型目录类问题。
2. 对正文问题返回 Missing Evidence。
3. 完成 pre-model 权限过滤。

### DB-4：MCP Query Tools

目标：

1. 实现 `search_project_assets`、`search_file_assets`、`get_model_assets`、`get_asset_events`。
2. 只读工具先接 fake adapter 或只读 View。
3. 动作 tools 先使用 fake REST，不触发真实扫描 / checksum / delete。

### DB-5：Selective Indexing

目标：

1. 只对授权、高价值、可解析、citation 可定位文件建立 preview / full-text / semantic index。
2. 不全量 embedding。

### DB-6：Operation Plan / Approval

目标：

1. 生成受控操作计划。
2. 通过平台 REST 提交人工审批申请。
3. 不直接执行破坏性动作。

每个 phase 的停止条件：

1. 不自动进入下一 phase。
2. baseline 前必须 Codex B review。
3. 任何真实 MySQL / NAS / REST / index 写入必须用户显式授权。
4. 任何真实 NAS 删除、移动、覆盖保持禁止。

## 15. 主开发 Agent 第一批允许做的事

当用户明确授权进入 DB-1 时，主开发 Agent 第一批只允许做：

1. 新建 fake / fixture 数据，不连接真实 MySQL。
2. 实现 `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView` 的 fake adapter。
3. 输出 sync preview，不写 Hermes_memory DB。
4. 不写 Qdrant / OpenSearch。
5. 不做正文解析。
6. 不改 memory kernel 主架构。
7. 不改 retrieval contract 语义。
8. 补最小 contract tests。

## 16. DB-0 验收

本阶段完成条件：

1. 对接契约文档存在且边界清晰。
2. 明确平台稳定 View 是唯一短期读取面。
3. 明确字段分为 P0 / P1 / P2，不把目标字段误判为当前可用字段。
4. 明确动作必须走 REST / OpenAPI，且 DB-0 / DB-1 不真实写平台审计。
5. 明确 Hermes_memory 不依赖平台底表。
6. 明确 MCP 是外围工具层，不替代 memory kernel。
7. 明确 10TB NAS 默认 catalog / metadata，不全量 embedding。
8. 明确 `permission_tags` 缺失默认 deny。
9. 明确不影响当前内部 MVP 主线。

本阶段不需要：

1. 代码实现。
2. 数据库迁移。
3. MCP Server。
4. 真实 MySQL 连接。
5. 真实 NAS 读取。
6. Qdrant / OpenSearch 写入。
7. API / CLI smoke。

## 17. 禁止事项总表

主开发 Agent 后续不得把当前对接改成：

1. Hermes_memory 直接扫描 NAS 作为正式数据源。
2. Hermes_memory 直接写平台业务表。
3. Hermes Agent 通过 MCP 直接操作数据库正式表。
4. Agent 默认全量解析 NAS。
5. Agent 默认全量 embedding。
6. Agent 绕过平台权限把无权限内容注入 prompt。
7. Agent 直接执行删除、移动、覆盖、权限修改。
8. 当前阶段引入 Data Steward / BIM 深度图谱 / Neo4j / PostGIS / 生产 scheduler 作为前置依赖。

## 18. 对后续耦合的最终声明

Hermes Agent 项目会把数据库 / NAS 平台接口纳入企业 Agent 长期路线，但接入方式保持渐进、可审计、低耦合：

1. 平台继续作为资产与 NAS 治理的 source of truth。
2. Hermes_memory 只消费稳定 View / REST 契约，不绑定平台底表。
3. Agent 通过 memory kernel 获取 pre-model evidence，不绕过权限直接访问数据。
4. MCP 只封装平台查询和受控动作申请，不替代记忆内核。
5. 所有真实写入、索引、动作申请都必须具备 trace、权限、审计和人工授权边界。

只要平台侧维护版本化 View / REST contract，后续 Hermes Agent 与企业数据库 / NAS 的耦合可以渐进扩展，不需要推倒重来，也不会与当前 Hermes_memory 主线重复建设。
