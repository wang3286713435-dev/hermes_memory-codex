# Hermes Data Steward Agent Risk Boundary

日期：2026-05-18
状态：Data Steward / NAS / DB catalog-only 后续开发风险边界
命名约定：本项目企业 Agent 统一称为 **Hermes**，不使用 Jarvis 作为项目内正式名称。

## 1. 定位

本文用于固化 Hermes 在接入 Data Steward / NAS / DB catalog-only 能力时的风险边界。

当前结论：

1. Hermes 当前架构整体健康，不需要因 catalog-only 接入而重构 memory kernel。
2. Hermes 适合通过低侵入的只读 Catalog Tool 接入 `FileAssetView` / `ModelAssetView` / 平台 Gateway API。
3. 当前不新增生产级 NAS 向量库。
4. 当前不把 NAS catalog rows、DWG / RVT 内容、真实 NAS 路径或 raw row 写入 Hermes long-term memory。
5. 本文不是立即开发所有能力的实现指令，而是后续 prompt、tool、Gateway、前端文案和测试验收的安全边界。

## 2. 当前 Hermes 能力口径

当前 Hermes 应定位为：

```text
Catalog Query Agent / 资产目录查询助手
```

当前可以承诺：

1. 查找 DWG / RVT / PDF / Office 等资产记录。
2. 按项目、专业、类型、状态、时间、权限标签筛选。
3. 返回 `file_id` / `model_id` / `project_id` / `source_view` 等目录信息。
4. 解释当前能力边界。
5. 对正文、构件、工程语义类问题返回 Missing Evidence。

当前不得承诺：

1. 理解 DWG 图纸内容。
2. 解析 RVT 模型构件。
3. 做 BIM 构件级搜索。
4. 做 NAS 全文搜索。
5. 做 NAS 语义搜索。
6. 读取任意 NAS 文件正文。
7. 长期记住 NAS 文件内容。

## 3. 推荐接入方式

推荐链路：

```text
Frontend / Platform Gateway
  -> Hermes
     -> Read-only Catalog Tool
        -> FileAssetView / ModelAssetView / REST Contract
```

不推荐链路：

```text
Hermes -> data_file_resources 底表
Hermes -> 自由生成 SQL
Hermes -> DB / NAS 写操作
Hermes -> NAS 文件正文持久化
Hermes -> catalog rows 写入 documents / chunks / Qdrant / OpenSearch
```

## 4. 高优先级风险边界

### 4.1 Catalog metadata 不等于正文 evidence

Catalog-only 查询返回的是资产目录信息，不是文件正文、工程语义或构件 evidence。

当用户问：

```text
这个 RVT 模型里是否有地下室构件？
```

Hermes 只能回答：

```text
目录信息显示该资产可能属于某项目 / 某专业 / 某文件类型。
当前没有文件正文或构件级 evidence，不能确认模型内容。
```

Hermes 不得回答：

```text
图纸内容包含……
模型构件包含……
文件正文写明……
```

正文类、构件类、工程语义类问题必须返回 Missing Evidence，并说明当前仅支持目录级查询。

### 4.2 Hermes memory 不得被 NAS catalog 或文件内容污染

允许写入 Hermes memory 的内容应限制为低敏关系和偏好：

1. `related_file_ids`
2. `query_id`
3. `project_id`
4. 用户确认过的目标结果引用
5. 用户偏好的专业、目录或项目范围
6. 反馈标签

禁止写入 Hermes memory：

1. 真实 `storage_path`
2. raw catalog row
3. 文件正文
4. DWG / RVT 解析内容
5. 客户敏感数据
6. NAS 文件内容

原则：

```text
Hermes memory 可以记 related_file_ids；
不能记 NAS 文件正文、raw row 和真实路径。
```

### 4.3 不允许模型生成 SQL 或直接访问底表

Hermes 只能使用受控只读工具：

```text
asset_catalog_search
asset_catalog_detail
```

工具必须满足：

1. 只读。
2. fail-closed。
3. 固定 schema。
4. 固定 filter。
5. 不执行写操作。
6. 不允许任意 SQL。
7. 不返回 raw row。
8. 不返回 raw `storage_path`。

### 4.4 真实 storage path 默认不得外泄

以下位置均不得默认输出真实 NAS 路径：

1. Hermes 最终回答。
2. Tool result。
3. Trace log。
4. Memory。
5. Debug log。
6. Frontend display。
7. 错误信息。

Catalog Tool 默认不得返回：

```text
storage_path
storage_uri
raw NAS path
```

默认返回应是脱敏字段：

```text
display_path
path_hint
locator
project_scope
授权打开入口
```

如果未来需要敏感路径输出，控制权必须在平台 Gateway / operator policy，不得交由 LLM 或前端请求自由决定。

### 4.5 时间字段语义不得误读

当前语义：

```text
updated_at：资产记录更新时间
last_seen_at：最近扫描 / 校验 / 看到该资产的时间
source_modified_at / file_modified_at：NAS 文件本体修改时间，当前未稳定暴露
```

Hermes 当前可以说：

```text
按资产记录更新时间排序。
按最近扫描 / 校验时间排序。
```

Hermes 当前不得说：

```text
按文件修改时间排序。
这是最近修改的文件。
```

除非未来 Catalog Tool 明确返回稳定的 `source_modified_at` 或 `file_modified_at`。

### 4.6 状态字段不得误读为语义索引完成

必须区分：

```text
process_status：平台治理 / 处理状态
index_eligibility=catalog_only：当前只支持目录级辅助
component_index_status：BIM 构件索引占位
semantic_index_status：未来语义索引阶段才应引入
```

Hermes 可以说：

```text
该资产目录记录已进入平台治理流程。
```

Hermes 不得说：

```text
该文件已经完成语义索引。
该文件已经向量化。
该文件内容可问答。
```

除非未来工具明确返回正式 `semantic_index_status` 且对应索引已通过验收。

### 4.7 Prompt / tool description 不得过度承诺 DWG / RVT 能力

推荐表达：

```text
资产目录查询
catalog-only metadata lookup
Missing Evidence for content questions
does not read file content
does not parse DWG/RVT internals
does not perform BIM component search
```

避免表达：

```text
read drawings
understand BIM models
semantic search over NAS
answer from file content
component-level retrieval
```

### 4.8 Feedback 不应直接原样写入 long-term memory

Feedback 首选进入平台侧 feedback / audit 模型。

可写入 Hermes memory 的仅限抽象低敏偏好：

1. 用户经常选择某类专业资产。
2. 用户确认 `file_id` / `model_id` 是目标资产。
3. 用户倾向优先查看某项目范围。

不得写入：

1. 完整 `user_query`。
2. 真实路径。
3. 完整 catalog row。
4. 文件正文。
5. 敏感项目名。
6. 客户材料。

## 5. 未来索引隔离原则

如果未来进入 NAS semantic indexing 或 BIM component indexing，必须分层：

```text
Hermes memory collection：用户偏好、会话记忆、确认反馈
NAS semantic collection：NAS 文件语义索引
BIM component index：RVT / BIM 构件索引
catalog index：资产目录
```

原则：

```text
NAS semantic index 不得混入 Hermes long-term memory。
Catalog metadata 不得伪装成正文 evidence。
Read-only Catalog Tool 不等于 SQL Tool。
```

## 6. 只读 Catalog Tool 建议契约

建议工具名：

```text
asset_catalog_search
```

工具语义：

```text
Search catalog-only DB/NAS asset metadata. Does not read file content.
```

输入建议：

```json
{
  "query": "string",
  "project_scope": {},
  "filters": {
    "project_id": "string",
    "file_kind": "string",
    "discipline": "string",
    "model_format": "string",
    "lifecycle_status": "string",
    "index_eligibility": "catalog_only"
  }
}
```

注意：`project_scope` 必须由平台 Gateway 根据用户身份 / API key 生成，不得由模型或前端任意填写。

输出建议：

```json
{
  "query_id": "string",
  "asset_catalog_only": true,
  "source_view": "FileAssetView | ModelAssetView",
  "items": [
    {
      "file_id": "string",
      "model_id": "string",
      "project_id": "string",
      "display_name": "string",
      "display_path": "string",
      "asset_type": "string",
      "permission_decision": "allowed | denied | masked",
      "capabilities": {
        "catalog_search": true,
        "preview_available": false,
        "full_text_search": false,
        "semantic_search": false,
        "component_search": false
      }
    }
  ],
  "missing_evidence": []
}
```

输出必须避免：

```text
raw storage_path
raw storage_uri
raw DB row
file content
DWG/RVT internals
unredacted secret
```

## 7. 用户回答口径

可以说：

```text
我可以基于当前资产目录帮你查找相关文件记录。
目录信息显示该资产属于某项目 / 某专业 / 某类型。
当前只有 catalog-only 证据，无法证明文件正文或模型构件内容。
这个问题需要 DWG/RVT 内容解析或 BIM 构件索引，目前目录阶段没有该证据。
```

不要说：

```text
我已经读取了该 DWG 图纸内容。
这个 RVT 模型包含某某构件。
文件正文中写明……
我会记住这份 NAS 文件的内容。
该文件已经完成语义向量索引。
```

## 8. 后续 Backlog

1. 只读 `asset_catalog_search` tool 产品化。
2. Catalog Tool 结构化输出 `query_id` / `file_id` / `model_id` / `source_view`。
3. Tool output 默认路径脱敏。
4. Missing Evidence response 模板。
5. catalog-only prompt / tool description 审计。
6. feedback endpoint 对接，但不直接写 long-term memory。
7. `related_file_ids` 低敏 memory 规则。
8. 未来 NAS semantic collection 独立设计。

## 9. 红线

后续开发过程中必须避免：

1. 让 Hermes 直接查业务底表。
2. 让模型生成 SQL。
3. 让 Hermes 执行 DB / NAS 写操作。
4. 将 catalog metadata 当正文 evidence。
5. 将 NAS catalog rows 写入 `documents` / `chunks` / Qdrant / OpenSearch。
6. 将真实 `storage_path` 返回给用户或写入 memory。
7. 将 `updated_at` 说成文件 mtime。
8. 将 `process_status` 说成 semantic index status。
9. 承诺理解 DWG / RVT 内容。
10. 将未来 NAS semantic index 混入 Hermes memory collection。

## 10. 最终结论

当前 Hermes 架构适合继续低侵入接入 catalog-only。

短期目标：

```text
Hermes = 资产目录查询助手
```

中期目标：

```text
Hermes + Gateway + Preview / Full-text 能力，但仍保持 evidence boundary
```

后期目标：

```text
Hermes 编排独立 NAS semantic collection / BIM component index
```

无论哪个阶段，都必须坚持：

```text
Hermes memory 不等于 NAS 内容索引；
catalog metadata 不等于正文 evidence；
只读 Catalog Tool 不等于 SQL Tool。
```
