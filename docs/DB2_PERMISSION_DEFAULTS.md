# DB-2 Permission Defaults

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-2 permission fail-closed contract；docs-only

## 1. 核心规则

DB-2 权限默认策略是 fail closed。

也就是：不知道有没有权限时，一律当作没有权限。

## 2. 数据库默认值

`external_asset_catalog` 必须包含：

```sql
permission_status VARCHAR(32) NOT NULL DEFAULT 'DENIED'
project_scope JSON NULL
permission_tags JSON NULL
confidentiality_level VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN'
```

`permission_status` 枚举：

1. `ALLOWED`
2. `DENIED`
3. `UNKNOWN`
4. `STALE`

DB-2 fake / proof 阶段默认写 `DENIED`，只有 fixture 明确提供可见权限并通过项目 scope 检查时，才允许标记为 `ALLOWED`。

## 3. 缺字段处理

| 场景 | DB-2 处理 |
|---|---|
| 缺 `permission_tags` | `permission_status=DENIED` |
| 缺 `project_scope` | `permission_status=DENIED`，不得进入 prompt |
| 缺 `project_id` | 不进入用户检索上下文 |
| 缺 `confidentiality_level` | 写 `UNKNOWN` |
| 服务级 DB 账号可读 | 不代表终端用户可见 |
| NAS ACL snapshot 未接入 | 不阻塞 DB-2，但不得扩大可见性 |

## 4. Retrieval 边界

DB-2 不实现 retrieval，但冻结未来边界：

1. pre-model retrieval 必须先做权限过滤。
2. catalog-only 资产不得作为正文 evidence。
3. catalog-only 资产不得写入 prompt 作为可回答内容。
4. 用户问正文、条款、图纸内容、BIM 构件语义时，catalog-only 必须返回 Missing Evidence。
5. 建议 Missing Evidence reason：`asset_catalog_only`。

## 5. Catalog-only 状态

DB-2 默认状态：

1. `index_status=CATALOG_ONLY`
2. `parse_status=NOT_REQUESTED`
3. `semantic_index_status=NOT_REQUESTED`
4. `citation_status=NOT_REQUESTED`

这些状态不能被解释为“可正文回答”。

## 6. Agent 写操作边界

当前阶段 Agent 不允许：

1. 写 NAS。
2. 改平台业务库。
3. 删除文件。
4. 移动文件。
5. 改真实权限系统。
6. 触发全量 reindex。
7. 把 catalog-only 资产送入 retrieval。

## 7. 验收口径

权限测试至少覆盖：

1. 缺 `permission_tags` 默认 `DENIED`。
2. 缺 `project_scope` 不进入 prompt。
3. 缺 `project_id` 不进入检索上下文。
4. `permission_status` 数据库默认值为 `DENIED`。
5. catalog-only 对正文问题返回 Missing Evidence。
6. 服务账号可读不等于用户可见。
