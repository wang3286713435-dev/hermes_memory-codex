# Data Steward Branch Roadmap

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-1 baseline 前 roadmap

## 1. 产品定位

“数据管家”是 Hermes 企业 Agent 的产品名。DB / NAS / BIM 不是另一个独立产品，而是数据管家的资产治理模块。

当前 MVP 主线仍优先服务企业文件、标书、会议、Excel / PPTX、小文件上传、citation、Missing Evidence 与人工复核。DB 分支是并行前置路线，用于把企业资产目录、NAS 元数据、BIM / 模型资产和后续平台连接边界先定义清楚，避免以后把真实 DB、NAS、索引和 memory kernel 混在一起推进。

## 2. 最终产品全貌

数据管家的长期目标是成为 Hermes 企业 Agent 的资产治理与 evidence answer 层。它不是“全量扫描 10TB NAS 后全部 embedding”的系统，而是受控的企业资产目录、索引授权、证据分层和人工审批流程。

最终能力包括：

1. 企业资产目录：
   - 项目文件、交付物、模型、扫描候选、归档资产的统一 catalog。
   - 记录 `asset_uid`、source system、source id、路径、文件类型、大小、checksum、更新时间、状态和来源 View。
   - 资产目录默认是 metadata / catalog evidence，不等同于正文 evidence。
2. BIM / 模型资产目录：
   - 管理 IFC、RVT、NWD、CAD、点云、轻量化模型等模型资产的登记状态。
   - 记录模型格式、专业、版本、预览状态、轻量化状态和索引资格。
   - 大模型 / 原生 BIM 文件默认 catalog-only，不默认进入全文解析或 semantic indexing。
3. 项目 / 楼栋 / 楼层 / 空间 / 设备索引：
   - 后续可在平台侧或 Hermes catalog mirror 中承载项目结构、楼栋、楼层、空间、设备与资产关系。
   - 该索引用于定位、过滤和治理，不自动替代文件正文证据。
   - 空间 / 设备级能力进入前必须先完成权限、状态、citation 和人工授权边界。
4. 权限过滤：
   - 服务账号同步权限不等于终端用户可见权限。
   - `project_scope`、`permission_tags`、生命周期状态、密级和 ACL snapshot 逐步用于 pre-model 过滤。
   - `permission_tags` 缺失默认 deny。
5. Evidence answer：
   - 可回答资产目录类问题，例如某项目有哪些文件、某模型是否登记、某文件路径 / 大小 / checksum / 更新时间 / 项目归属。
   - 文件正文、条款解释、图纸内容、模型语义分析必须依赖可 citation 的 preview / full-text / semantic index。
   - metadata 不得被伪装成正文 evidence。
6. Missing Evidence：
   - 当只有 catalog evidence、没有正文索引时，必须返回 `asset_catalog_only` 类 Missing Evidence。
   - 当用户无权限、权限标签缺失或资产状态异常时，不得返回敏感路径、正文片段或可推断内容。
7. 人工审批：
   - NAS 扫描、checksum、selective indexing、删除、移动、归档、重建索引和资产注释必须走人工授权或平台审批。
   - Hermes 可以生成 operation plan，但不能直接执行破坏性动作。
8. 后续子 Agent 监控：
   - 后续可有只读监控 Agent 关注资产状态、缺失 checksum、stale / moved / missing、权限标签缺失和索引授权候选。
   - 子 Agent 输出应是 diagnostics / preview / approval request，不是自动修复结果。
   - 任何自动化监控都必须有 feature flag、审计记录和人工复核边界。

## 3. DB-0 到 DB-6 阶段路线

### DB-0：契约冻结

目标：

1. 固化平台稳定 View / REST contract。
2. 明确 Hermes_memory 不读取平台底表。
3. 明确 DB / NAS / BIM 接入属于数据管家资产治理模块。
4. 明确 asset catalog 与 document content evidence 分层。
5. 明确 `asset_uid = source_system + ":" + source_id`。
6. 明确 `permission_tags` 缺失默认 deny。
7. 明确 DB-0 / DB-1 不连接真实 MySQL / NAS。

完成形态：

1. `DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
2. `DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
3. DB branch plan / acceptance / roadmap 文档。

### DB-1：Fake View Adapter

目标：

1. 使用 fake JSON fixtures 模拟平台 View。
2. 实现只读 fake adapter。
3. 通过 contract tests 固化最小字段、分页、cursor、contract version、asset uid、权限缺失 deny 和异常状态。

当前 DB-1 范围仅包括：

1. `ProjectAssetView`
2. `FileAssetView`
3. `ModelAssetView`
4. `AuditEventView`
5. fake adapter contract tests。

当前 DB-1 明确不做：

1. 不连接真实 MySQL。
2. 不连接或扫描真实 NAS。
3. 不扫描 `/Volumes/zyzn/卓羽智能项目`。
4. 不写 `documents` / `chunks`。
5. 不写 OpenSearch / Qdrant。
6. 不做正文解析。
7. 不写 migration。
8. 不改 retrieval contract。
9. 不改 memory kernel 主架构。

### DB-2：Asset Catalog Mirror

后续目标：

1. 建立 Hermes_memory 独立 `external_asset_catalog` mirror 或等价 catalog mirror。
2. 保存平台 View 规范化元数据、checkpoint、`project_scope`、`permission_tags` 和状态字段。
3. 支持 dry-run sync preview。

边界：

1. DB-2 必须在 DB-1 baseline 和用户显式授权后才能进入。
2. 未授权前不得写 migration。
3. catalog-only 资产不得进入 `documents` / `chunks`。
4. catalog-only 资产不得进入 OpenSearch / Qdrant。
5. mirror 写入只能写 Hermes_memory 自有 catalog mirror，不写平台 DB。
6. 真实 MySQL / NAS / REST 联调仍需单独授权。

### DB-3：Catalog Retrieval

后续目标：

1. 支持项目 / 文件 / 模型目录类问题。
2. 对正文问题返回 Missing Evidence。
3. 完成 pre-model 权限过滤。
4. 在 context 中区分 `asset_catalog_evidence`、`document_content_evidence`、`semantic_index_evidence`。

边界：

1. DB-3 必须在 DB-2 baseline 和用户显式授权后才能进入。
2. 不改变现有 retrieval request / response contract 语义。
3. 不让 catalog retrieval 替代 document content retrieval。
4. metadata-only 结果不能被当作正文 citation。
5. 无权限、权限标签缺失、项目不匹配或状态异常时不得进入 prompt。

### DB-4：MCP Query Tools

后续目标：

1. 提供只读查询工具，例如 `search_project_assets`、`search_file_assets`、`get_model_assets`、`get_asset_events`。
2. 先接 fake adapter 或只读 View。
3. 返回 `source_view`、`trace_id`、`permission_status`、`citation_status`、`project_scope`、`contract_version`。

边界：

1. MCP 是外围工具层，不替代 memory kernel。
2. MCP tools 不直接写 MySQL 正式表。
3. MCP tools 不直接删除、移动、改名 NAS 文件。
4. 动作类 tools 必须后置，且先走 fake REST / approval preview。

### DB-5：Selective Indexing

后续目标：

1. 只对授权、高价值、可解析、citation 可定位的资产建立 preview / full-text / semantic index。
2. 支持 indexing request preview 和人工授权记录。
3. 记录 parser version、embedding model、citation capability、授权范围和过期策略。

边界：

1. 不全量解析 10TB NAS。
2. 不全量 chunk。
3. 不全量 embedding。
4. BIM / CAD / 点云 / 音视频 / 大压缩包默认 catalog-only。
5. 投标、合同、报价、内部评审、人事、财务、法务、客户敏感资料默认 excluded，除非后续有明确授权和权限模型。

### DB-6：Operation Plan / Approval

后续目标：

1. 生成受控 operation plan。
2. 通过平台 REST / OpenAPI 提交人工审批申请。
3. 支持资产修复、补 checksum、申请索引、标注、归档、删除申请等工作流。
4. 为后续子 Agent 监控提供审批入口。

边界：

1. operation plan 是建议，不是执行结果。
2. 删除、移动、权限修改、批量重建索引必须标记 high-risk。
3. plan 必须记录 evidence、影响范围、回滚建议和审批人。
4. Hermes 不直接执行破坏性动作。
5. 真实平台写入必须用户和平台共同授权。

## 4. DB-1 当前状态

DB-1 当前只做 fake View adapter / contract tests。它的作用是把平台 View contract 的最低可用语义固定下来，而不是接入真实平台。

当前 DB-1 可声明：

1. fake fixtures 覆盖 `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView`。
2. fake fixtures 覆盖 `101-C塔`、`98-深圳口岸项目`、`99-丰图既有建模项目`。
3. fake adapter 是只读 adapter。
4. contract tests 覆盖 pagination / cursor、`contract_version`、`asset_uid`、`permission_tags` missing deny、moved / stale / missing / checksum missing。
5. 所有 Data Steward / DB / NAS 能力默认 feature flag off。

当前 DB-1 不可声明：

1. 已连接真实 MySQL。
2. 已扫描真实 NAS。
3. 已建立 asset catalog mirror。
4. 已支持 catalog retrieval。
5. 已支持 BIM / 空间 / 设备深度索引。
6. 已支持 selective indexing。
7. 已支持平台 REST 写入或人工审批。

## 5. 合回主线条件

DB 分支合回主线前必须满足：

1. 所有 DB / NAS / Data Steward 能力默认 feature flag off。
2. fake adapter 与真实平台 client 分离。
3. catalog-only 资产不进入现有 `documents` / `chunks`。
4. catalog-only 资产不写 OpenSearch / Qdrant。
5. catalog-only evidence 与 document content evidence 分层清晰。
6. Missing Evidence 可区分 `asset_catalog_only`。
7. `permission_tags` 缺失默认 deny。
8. `asset_uid = source_system + ":" + source_id` 规则稳定。
9. contract tests 通过。
10. 不改 retrieval contract 语义。
11. 不改 memory kernel 主架构。
12. 不含真实 MySQL / NAS / REST credential、scan output 或平台审计写入产物。
13. Codex B review 通过。
14. 用户确认可以合回主线。

## 6. 当前停止线

本 roadmap 是继续后续开发前的路线说明，不是 baseline，也不是 DB-2 implementation prompt。

当前必须停止于：

1. 不写功能代码。
2. 不进入 DB-2。
3. 不新增 migration。
4. 不连接真实 MySQL / NAS。
5. 不扫描 `/Volumes/zyzn/卓羽智能项目`。
6. 不写 `documents` / `chunks` / OpenSearch / Qdrant。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。
9. 不做 baseline。
