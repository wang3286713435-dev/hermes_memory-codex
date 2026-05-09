# Phase DB-0 数据管家资产治理并行分支计划

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-0 contract baseline

## 1. 定位

“数据管家”是 Hermes 企业 Agent 的产品化名称。DB / NAS / TB BIM 接入不是另一个独立产品，而是数据管家的资产治理 / 平台连接能力模块。

当前 MVP 主线继续优先落地本地企业文件、标书、会议、Excel / PPTX、小文件上传、citation、Missing Evidence 与人工复核能力。DB-0 分支只做并行前置，不抢当前 MVP 资源。

## 2. 分支职责

本分支负责：

1. 固化 DB / NAS / BIM 接入契约。
2. 明确平台 View / REST 是唯一短期读取面。
3. 设计 fake View adapter 与 contract tests 的后续入口。
4. 保持 asset catalog 与 document content evidence 分层。
5. 保证后续能无损合回主线。

本分支不负责：

1. 真实 MySQL 连接。
2. 真实 NAS 扫描。
3. 真实 REST 写入。
4. 写 `documents` / `chunks`。
5. 写 OpenSearch / Qdrant。
6. 全量 BIM / CAD / 点云解析。
7. Neo4j / PostGIS / 空间索引实现。
8. production scheduler / rollout。

## 3. 合回主线条件

合回主线前必须满足：

1. 所有 DB / NAS 能力默认 feature flag off。
2. fake adapter 与真实平台 client 分离。
3. catalog-only 资产不进入现有 `documents` / `chunks`。
4. catalog retrieval 与 document content retrieval 明确分层。
5. Missing Evidence 可区分 `asset_catalog_only`。
6. `permission_tags` 缺失默认 deny。
7. contract tests 通过。
8. Codex B review 通过。

## 4. DB 分支阶段

### DB-0a Contract Baseline

固化：

1. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
2. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
3. 本分支计划文档。

### DB-1a Fake View Fixtures

后续新增 fake JSON fixtures：

1. `ProjectAssetView`
2. `FileAssetView`
3. `ModelAssetView`
4. `AuditEventView`

覆盖项目：

1. `101-C塔`
2. `98-深圳口岸项目`
3. `99-丰图既有建模项目`

### DB-1b Fake Adapter Contract Tests

后续实现只读 fake adapter，并测试：

1. pagination / limit / cursor。
2. `contract_version`。
3. `asset_uid = source_system + ":" + source_id`。
4. `permission_tags` missing deny。
5. stale / moved / missing / checksum missing。

### DB-2 Planning Only

规划 `external_asset_catalog` mirror。DB-2 前不得写 migration。

## 5. 当前结论

本分支可以安全并行推进 DB-0 / DB-1 前置工作，不影响当前 MVP 主线。真实 DB / NAS / REST / index 写入仍需用户后续显式授权。
