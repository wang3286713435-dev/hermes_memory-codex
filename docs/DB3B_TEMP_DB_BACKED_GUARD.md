# DB-3B Temporary DB Backed Guard

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-3B 最小实现；SQLite memory temporary DB only；未接真实 MySQL / NAS / OpenSearch / Qdrant

## 1. 本阶段目标

DB-3B 把 DB-3A 的 catalog retrieval guard 从 fake preview object 推进到 temporary DB proof rows。

它只读取 DB-2 temporary mirror proof 表：

```text
external_asset_catalog_contract
```

它不连接真实 MySQL，不创建 migration，不扫描 NAS，不读取真实文件正文，不写 `documents` / `chunks` / OpenSearch / Qdrant。

## 2. 已实现

新增只读方法：

```python
AssetCatalogTemporaryMirrorStore.load_retrieval_preview()
```

该方法：

1. 复用 existing temporary DB safety check。
2. 只接受 SQLite memory DB。
3. 从 `external_asset_catalog_contract` 读取 catalog rows。
4. 将 rows 还原为 `AssetCatalogMirrorPreview`。
5. 交给 `AssetCatalogRetrievalGuard` 继续执行 DB-3A 权限与 Missing Evidence 规则。

## 3. 行为合同

允许：

1. `AssetCatalogMirrorPreviewer(...).preview()` 写入 SQLite memory temp DB。
2. `AssetCatalogTemporaryMirrorStore.load_retrieval_preview()` 只读加载 temp DB rows。
3. `AssetCatalogRetrievalGuard.evaluate(...)` 对加载结果执行 catalog lookup / content answer guard。

禁止：

1. file-backed SQLite。
2. attached file DB。
3. 真实 MySQL。
4. migration。
5. NAS scan。
6. REST action。
7. documents / chunks 写入。
8. OpenSearch / Qdrant 写入。
9. embedding / semantic index。

## 4. 验收

测试覆盖：

1. temp DB backed catalog lookup 只返回授权 metadata。
2. `prompt_items` 仍为空。
3. write flags 仍为 false。
4. temp DB backed content answer 返回 `asset_catalog_only`。
5. file-backed SQLite 仍被拒绝。

## 5. 下一步

DB-3C 候选：

1. Missing Evidence response DTO。
2. permission scope / project scope 组合策略。
3. DB-3B QA probe 后再决定是否做 temp DB checkpoint-read guard。

真实 MySQL 接入仍需要单独授权，不由 DB-3B 自动触发。
