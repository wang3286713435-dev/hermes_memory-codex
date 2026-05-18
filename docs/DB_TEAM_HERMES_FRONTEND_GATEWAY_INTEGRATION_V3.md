# Hermes 数据管家前端网关耦合说明 v3

日期：2026-05-18
面向对象：数字化交付平台 / 数据库 / 前端团队
适用版本：数据库团队侧 Hermes 已更新到 Phase 2.89
状态：当前可执行的前端嵌入与只读数据管家联调口径

## 0.0 Hermes 命名与风险边界

项目内企业 Agent 正式名称统一为 **Hermes**，不使用 Jarvis 作为项目文档、接口、前端文案或数据库团队交接中的正式名称。

本耦合说明必须与 `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md` 一起执行。若本文件与风险边界文档发生冲突，以更保守的边界为准：

1. Catalog metadata 不等于文件正文 evidence。
2. 只读 Catalog Tool 不等于 SQL Tool。
3. Hermes memory 不等于 NAS 内容索引。
4. 当前不得承诺理解 DWG / RVT 内容、BIM 构件级搜索、NAS 全文搜索或 NAS 语义搜索。
5. 当前不得默认返回真实 `storage_path`、raw row、真实 NAS path、secret 或文件正文。

## 0. 一句话结论

数据库团队可以基于当前 Phase 2.89 Hermes 开始做“数据管家前端嵌入 / 平台后端 Gateway / 只读资产目录联调”。

但当前不应理解为完整数据管家已经生产就绪：

1. 可以做前端入口、平台后端 Gateway、Hermes 健康检查、只读问答壳、资产目录 metadata preview、权限上下文传递和审计 trace 对齐。
2. 不可以让 Agent 直接 DB CRUD、直接扫描 NAS、直接复制 / 删除 / 移动 NAS 文件、自动写 `documents` / `chunks`、自动写 OpenSearch / Qdrant / MinIO、自动进入 production rollout。
3. 当前 Hermes 对数据库 / NAS 的定位仍是“受控只读资产治理入口 + 后续 evidence write / selective indexing 的安全门”，不是直接接管平台和 NAS。

## 1. 当前版本状态

### 1.1 数据库团队当前 Hermes 版本

数据库团队机器上的 Hermes 已更新到：

```text
phase-2.89-test-machine-runtime-preflight-handoff-baseline
```

Phase 2.89 的核心含义：

1. 已具备运行 Phase 2.88 runtime preflight runner 的交接能力。
2. 已验证可以在测试机上进入 `preflight_ready_for_operator_stop`。
3. 该状态只表示“写入前置检查链路可控”，不表示已经授权写入。
4. 该状态不授权真实 DB 写入、parser、NAS copy、index write 或 Agent answer integration。

### 1.2 Hermes 已具备的 DB / NAS 相关基础能力

当前 Hermes 主线已具备以下基础：

1. `delivery_platform.asset_views.v1.1` 只读契约已对齐。
2. `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView` 已作为稳定读模型进入 Hermes 侧契约。
3. v1.1 structure-only smoke 与 `LIMIT 30` 脱敏统计 smoke 已通过。
4. 只读 adapter / DTO / fake adapter / contract tests 已对齐 v1.1 字段形态。
5. Catalog query preview 已实现为“资产目录 metadata preview”，不是正文 evidence。
6. 缺少正文 evidence 时必须返回 `asset_catalog_only` / Missing Evidence。
7. 当前 feature flags 默认关闭，不能默认启用 Data Steward runtime、indexing、writer 或 Agent CRUD。

### 1.3 当前仍未完成的能力

当前尚未完成：

1. 前端生产级 Data Steward UI。
2. Agent 直接从 NAS 文件正文回答问题。
3. DB catalog 自动进入 `documents` / `chunks`。
4. 自动 selective indexing。
5. Agent 对 DB / NAS 的增删改查。
6. Agent answer 与 DB/NAS evidence 的完整生产链路。
7. 完整 ACL / 用户级权限快照。
8. BIM 大模型正文解析、构件级索引、图谱、空间索引。

## 2. 推荐耦合架构

前端不得直连 Hermes。推荐架构如下：

```text
企业员工浏览器
  -> 数字化交付平台前端
     -> 数字化交付平台后端 Gateway（Spring Boot）
        -> 平台鉴权 / 用户身份 / project_scope / permission proof
        -> 平台 DB / NAS / 资产库
        -> Hermes Gateway Adapter（后端内部模块）
           -> Hermes Memory / Hermes Agent（本机或内网服务）
```

核心原则：

1. 平台后端是唯一 Gateway。
2. 前端不直接访问 Hermes。
3. 前端不持有 Hermes token、DB 凭据、NAS 凭据或 `.env`。
4. 平台后端负责用户身份、权限、project_scope、API Key、审计和速率限制。
5. Hermes 只消费平台后端传入的已校验上下文。
6. Hermes 不绕过平台权限访问 DB / NAS。

## 3. 平台后端 Gateway 职责

数据库 / 平台后端团队应优先实现一个 Hermes Gateway Adapter。

### 3.1 Gateway 必须负责

1. 用户登录态校验。
2. 用户项目权限校验。
3. 生成本次请求的 `project_scope` 或等价 permission proof。
4. 将用户问题、项目范围、资产过滤条件和 trace_id 转发给 Hermes。
5. 对 Hermes 返回进行二次安全检查。
6. 写平台侧审计日志。
7. 控制超时、重试、速率限制、熔断。
8. 对前端隐藏 Hermes 内部错误、环境变量和路径。

### 3.2 Gateway 不应做

1. 不把前端请求原样透传给 Hermes。
2. 不把 DB password / API key / `.env` 暴露给浏览器。
3. 不让 Hermes 返回的本地路径直接展示给用户。
4. 不允许前端通过 Hermes 触发 DB 写入、NAS scan、parser、indexing 或 rollout。
5. 不把 catalog-only metadata 标记成文件正文 evidence。

## 4. 建议平台侧接口

以下接口名是建议，数据库团队可按现有后端路由规范调整。

### 4.1 健康检查

```http
GET /api/data-steward/hermes/health
```

Gateway 行为：

1. 调用 Hermes `/health` 或等价健康检查。
2. 返回 Hermes 可用性、版本、当前模式。
3. 不返回内部路径、secret、`.env`、DB 连接串。

建议返回：

```json
{
  "status": "ok",
  "hermes_available": true,
  "mode": "read_only_gateway",
  "contract_version": "delivery_platform.asset_views.v1.1",
  "runtime_write_enabled": false,
  "agent_answer_integration_enabled": false
}
```

### 4.2 数据管家聊天入口

```http
POST /api/data-steward/chat
```

前端请求到平台后端：

```json
{
  "session_id": "frontend-session-id",
  "message": "帮我查一下 C 塔项目有哪些模型文件",
  "project_filters": ["project-id-or-code"],
  "mode": "catalog_lookup"
}
```

平台后端转给 Hermes 前必须补齐：

```json
{
  "request_id": "platform-trace-id",
  "user_context": {
    "user_id": "platform-user-id",
    "roles": ["role-code"],
    "department_id": "department-id"
  },
  "permission_context": {
    "project_scope": {
      "type": "SPECIFIC_PROJECTS",
      "project_ids": ["project-id"]
    },
    "permission_tags": ["PROJECT:<project_id>", "CONFIDENTIALITY:UNKNOWN"],
    "confidentiality_clearance": "INTERNAL_OR_UNKNOWN",
    "source": "platform_gateway"
  },
  "query": {
    "text": "帮我查一下 C 塔项目有哪些模型文件",
    "mode": "catalog_lookup",
    "asset_filters": {
      "asset_kinds": ["MODEL", "FILE"],
      "contract_version": "delivery_platform.asset_views.v1.1"
    }
  }
}
```

Hermes 返回给 Gateway 的推荐结构：

```json
{
  "answer_type": "asset_catalog_preview",
  "answer": "这是资产目录层面的查询结果，不代表文件正文已被读取。",
  "asset_catalog_only": true,
  "content_evidence_available": false,
  "missing_evidence": [
    {
      "reason": "asset_catalog_only",
      "message": "当前仅有资产目录元数据，尚无文件正文 evidence。"
    }
  ],
  "catalog_results": [
    {
      "asset_ref": "redacted-or-platform-asset-ref",
      "asset_kind": "MODEL",
      "project_id": "project-id",
      "file_ext": "rvt",
      "lifecycle_status": "active",
      "index_eligibility": "catalog_only",
      "permission_status": "allowed_by_gateway_scope"
    }
  ],
  "citations": [],
  "guardrails": {
    "metadata_as_answer": false,
    "facts_as_answer": false,
    "snapshot_as_answer": false,
    "requires_retrieval_evidence_for_content_answer": true
  },
  "trace": {
    "platform_trace_id": "platform-trace-id",
    "hermes_trace_id": "hermes-trace-id"
  },
  "requires_human_review": true
}
```

### 4.3 资产目录搜索

```http
POST /api/data-steward/catalog/search
```

用途：

1. 前端资产页调用。
2. 只返回用户有权看到的资产 metadata。
3. 不返回 raw DB row。
4. 不把结果当成文档正文 evidence。

请求建议：

```json
{
  "query": "C塔 结构 RVT",
  "project_scope": {
    "type": "SPECIFIC_PROJECTS",
    "project_ids": ["project-id"]
  },
  "filters": {
    "asset_kind": ["MODEL", "FILE"],
    "file_ext": ["rvt", "dwg", "pdf"],
    "lifecycle_status": ["active"],
    "index_eligibility": ["catalog_only"]
  },
  "page": {
    "limit": 20,
    "cursor": null
  }
}
```

响应建议：

```json
{
  "results": [
    {
      "asset_ref": "platform-asset-ref",
      "asset_kind": "MODEL",
      "project_id": "project-id",
      "file_ext": "rvt",
      "size_bucket": "gte_1gb",
      "lifecycle_status": "active",
      "index_eligibility": "catalog_only",
      "content_evidence_available": false
    }
  ],
  "next_cursor": null,
  "safety": {
    "raw_rows_output": false,
    "true_nas_path_output": false,
    "secret_printed": false
  }
}
```

## 5. 当前允许的前端能力

数据库团队现在可以做以下 P0 / P1 前半段功能。

### 5.1 P0：可以立即做

1. 前端增加“数据管家”入口。
2. 后端增加 Hermes Gateway Adapter。
3. Gateway 调 Hermes health。
4. Gateway 统一包装用户身份、project_scope、trace_id。
5. 前端展示 Hermes 只读回答。
6. 前端展示 catalog-only 结果，并明确标注“目录元数据，不是正文内容”。
7. 前端展示 Missing Evidence。
8. 平台审计记录用户问题、trace_id、项目范围、Hermes decision。

### 5.2 P1：可以并行设计，但需灰度开关

1. 资产目录自然语言搜索。
2. 项目内文件 / 模型分类问答。
3. 基于 platform asset ref 的跳转。
4. 前端展示“可读 / 不可读 / 需要申请权限 / 仅目录可见”状态。
5. 审计面板展示 Hermes trace 与平台 trace 关联。

### 5.3 当前不应做

1. 前端按钮触发 Agent 删除 / 移动 / 改名 NAS 文件。
2. 前端按钮触发 Agent 直接写平台 DB。
3. 前端按钮触发 Agent 自动扫描 NAS。
4. 前端按钮触发 Agent 自动解析大批文件。
5. 前端将 Agent 回答作为自动审批、自动设计审查、自动算量、自动投标或经营决策依据。

## 6. 权限与安全要求

### 6.1 Fail Closed

以下任一条件缺失，Hermes 必须拒绝或返回 Missing Evidence：

1. 无用户身份。
2. 无 project_scope。
3. 无 permission proof。
4. 资产无 project_id。
5. 资产 lifecycle 不允许。
6. 资产仅 catalog-only，但用户要求正文回答。
7. 权限标签不匹配。
8. 密级未知且无法确认可见性。

### 6.2 前端展示规则

前端必须区分：

1. `asset_catalog_preview`：资产目录结果。
2. `document_content_answer`：正文 evidence 回答。
3. `missing_evidence`：证据不足。
4. `permission_denied`：无权限。
5. `requires_human_review`：需要人工确认。

不得把 `asset_catalog_preview` 显示成“已读取文件内容”。

### 6.3 NAS 路径展示

默认不由 Hermes 输出真实 NAS 路径。

如果平台前端需要展示路径：

1. 应由平台后端基于用户权限自行返回。
2. 不应让 Hermes 在回答文本中直接输出真实 NAS 路径。
3. 不应把 NAS 路径写入公开日志或前端错误提示。

## 7. Feature Flag 建议

当前默认：

```text
PLATFORM_ASSET_CATALOG_ENABLED=false
PLATFORM_ASSET_SYNC_WRITE_ENABLED=false
PLATFORM_ASSET_MCP_ENABLED=false
PLATFORM_ASSET_SEMANTIC_INDEX_ENABLED=false
PLATFORM_ASSET_READONLY_DB_ENABLED=false
PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false
PLATFORM_ASSET_BATCH_COPY_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=false
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED=false
PLATFORM_ASSET_INDEX_WRITE_ENABLED=false
PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED=false
```

前端 P0 联调建议：

1. Gateway 自己可启用前端入口。
2. Hermes runtime 写入相关 flag 必须保持 false。
3. 如需开启只读 catalog preview，必须先确认部署侧配置、权限证明和只读 smoke 已通过。
4. 不得为了前端展示临时打开 write / index / parser / Agent answer integration。

## 8. 测试用例清单

数据库团队接入时至少跑以下用例。

### 8.1 Health / Gateway

1. Hermes health 正常。
2. Hermes 不可用时，前端显示“数据管家暂不可用”，不暴露内部错误。
3. 浏览器不能直接访问 Hermes 内部地址。
4. Gateway 日志不输出 secret / `.env` / DB password。

### 8.2 权限

1. 无登录态：拒绝。
2. 无 project_scope：拒绝。
3. project_scope 不含目标项目：拒绝。
4. 有 project_scope 且目标资产属于项目：允许 catalog preview。
5. catalog-only 内容问题：返回 Missing Evidence，不编造。

### 8.3 数据边界

1. 查询“有哪些模型文件”：可以返回目录 metadata。
2. 查询“打开 / 删除 / 移动某文件”：拒绝或生成人工申请，不执行。
3. 查询“总结某 RVT 模型正文内容”：如果没有正文 evidence，返回 Missing Evidence。
4. 查询“输出 NAS 路径”：默认不由 Hermes 输出；如平台要展示，走平台权限控制。

### 8.4 审计

1. 每次请求有 platform trace_id。
2. Hermes response 带 hermes_trace_id 或等价字段。
3. 审计记录不含 raw row、NAS path、secret。
4. 拒绝动作也写审计。

## 9. 数据库团队当前可以推进的任务

建议数据库团队立即推进：

1. 前端“数据管家”入口 UI。
2. 平台后端 Hermes Gateway Adapter。
3. project_scope / permission proof DTO。
4. Gateway 到 Hermes 的 health 调用。
5. Gateway 到 Hermes 的只读 chat / catalog search 调用壳。
6. 前端展示 `asset_catalog_preview` / `missing_evidence` / `permission_denied` / `requires_human_review`。
7. 平台审计 trace 对齐。
8. P0 测试用例与灰度开关。

暂缓：

1. Agent 直接写平台 DB。
2. Agent 直接写 Hermes `documents` / `chunks`。
3. Agent 直接扫描 / 操作 NAS。
4. 自动 selective indexing。
5. BIM 深解析、构件级图谱、空间索引。
6. production rollout。

## 10. 与 Phase 2.91 的关系

Phase 2.91 正在推进 runtime evidence writer smoke gate。

这对数据库团队的影响：

1. 不阻塞前端 P0 Gateway / 只读 catalog integration。
2. 会影响后续“把 NAS 派生内容写入 Hermes evidence tables”的能力。
3. 在 Phase 2.91 通过 Codex B review、后续测试机 writer smoke 通过之前，不应把 Agent 写入能力接入前端。
4. 前端可以先做只读壳和目录查询，等 writer / indexing / Agent answer integration 后续稳定后再逐步打开。

## 11. 当前 Go / Pause / No-Go

### Go

允许数据库团队开始：

1. 前端内嵌数据管家入口。
2. 平台后端 Gateway。
3. 只读资产目录查询。
4. 权限上下文传递。
5. Catalog-only / Missing Evidence 展示。
6. 审计 trace 对齐。

### Pause

以下内容需暂停，等待 Hermes 后续阶段：

1. 写入 Hermes evidence tables。
2. 让 Agent 读取 NAS 文件正文并生成正式 evidence。
3. selective full-text / semantic indexing。
4. Agent answer integration 到生产前端。

### No-Go

以下内容当前明确禁止：

1. Agent DB CRUD。
2. Agent NAS CRUD。
3. 自动删除 / 移动 / 覆盖 NAS 文件。
4. 自动全量扫描 1TB / 10TB NAS。
5. 自动 BIM 大模型解析。
6. 真实写 DB / OpenSearch / Qdrant / MinIO。
7. production rollout。

## 12. 给数据库团队的执行口径

请按以下口径推进：

1. 当前 Hermes 2.89 可作为“只读数据管家 Gateway 联调版本”。
2. 前端只接平台后端 Gateway，不直连 Hermes。
3. Gateway 必须带用户身份、project_scope、permission proof。
4. Hermes 当前优先返回 catalog preview / Missing Evidence / 权限拒绝，不承诺正文读取。
5. 任何写入、索引、NAS 文件读取、Agent CRUD、production rollout 都等后续 Hermes 阶段明确授权。

这版文档是 v3 增量对接说明，不废弃 v2 契约；v2 继续作为 DB / NAS / Hermes 长期低耦合总原则，v3 用于当前数据库团队把 Hermes 嵌入前端作为数据管家的实际联调。
