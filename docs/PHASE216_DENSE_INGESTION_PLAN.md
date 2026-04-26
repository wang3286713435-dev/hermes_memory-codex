# Phase 2.16 dense ingestion 与 hybrid 检索闭环补齐规划

## 1. 阶段目标

Phase 2.16 目标是补齐真实上传文件的 dense ingestion，使新上传 chunk 能进入 Qdrant，并让现有 dense/sparse/hybrid 查询链路真正拥有 dense 语料。

本阶段仍不改 retrieval contract，不改 memory kernel 主架构，不推进权限、facts、rerank 策略或 rollout。

## 2. 当前 dense 缺口

### 2.1 上传 ingestion 未写入 Qdrant

当前 `DocumentIngestionService.ingest_uploaded_file()` 已完成：

1. parse
2. chunk
3. PostgreSQL `chunks` 落库
4. citation record 写入
5. OpenSearch sparse 索引

但 `_index_chunks()` 只调用 `OpenSearchChunkIndexer`，未对 chunk 生成 embedding，也未调用 `QdrantDenseRetriever.upsert_chunk()`。

因此真实上传文件目前主要依赖 OpenSearch sparse，dense corpus 不完整。

### 2.2 Qdrant adapter 已具备基础能力

当前 `QdrantDenseRetriever` 已具备：

1. `ensure_collection()`
2. `upsert_chunk(chunk_id, vector, payload)`
3. query-side embedding
4. `/points/search`
5. filter 支持 `source_type`、`document_id`、`document_type`、`is_latest`

当前配置基线：

1. `vector_store_provider=qdrant`
2. `qdrant_collection=hermes_chunks`
3. `qdrant_vector_size=1024`
4. `embedding_provider=aliyun`
5. `aliyun_embedding_model=text-embedding-v3`
6. `aliyun_embedding_dimension=1024`

### 2.3 dense retrieval 查询侧已存在，但语料侧不足

`RetrievalService` 在 dense / hybrid 模式下会调用 `self.dense.search()`。如果 request 没有 `query_vector`，Qdrant retriever 会用 Aliyun embedding 生成 query vector。

但由于上传 ingestion 未写入 Qdrant，真实上传文件的 dense 返回可能为空或不完整，hybrid 上限被 OpenSearch sparse 语料主导。

## 3. 最小实现边界

### 3.1 新上传文件 dense ingestion

在 ingestion 完成 chunk 落库后，增加最小 dense indexing 步骤：

1. 对每个 chunk 生成 1024 维 embedding。
2. 调用 Qdrant upsert 写入 `hermes_chunks`。
3. payload 至少保留：
   - `document_id`
   - `chunk_id`
   - `version_id`
   - `source_type`
   - `document_type`
   - `title` / `source_name`
   - `chunk_index`
   - `is_latest`
   - `text`
   - `heading_path`
   - `section_path`
   - `page_start`
   - `page_end`
   - `metadata_json`

### 3.2 fail-open 原则

dense ingestion 失败不得阻断：

1. PostgreSQL 落库
2. OpenSearch sparse 索引
3. ingestion job 完成 sparse 可检索路径

dense 失败应记录为可诊断状态，而不是把整个文件 ingestion 判定失败。

建议 trace / job metadata 记录：

1. `dense_ingestion_status`
2. `dense_indexed_count`
3. `dense_failed_count`
4. `dense_failure_reason`
5. `embedding_model`
6. `embedding_dimension`
7. `qdrant_collection`

### 3.3 不改变 retrieval contract

检索请求和响应 contract 保持不变。dense ingestion 只补齐索引侧语料，不改变公开 search API、filter 语义、rerank 规则或 Hermes 上层 memory kernel 架构。

## 4. 回填策略

### 4.1 默认先支持新上传文件

Phase 2.16 最小实现先保证新上传文件自动进入 Qdrant。

### 4.2 现有真实文件池用显式小脚本回填

现有真实文件池建议单独提供限定脚本，例如：

`scripts/phase216_backfill_dense_vectors.py`

要求：

1. 只接受显式 `document_id` 列表。
2. 默认覆盖 Phase 2.11d / 2.14 已验证真实文件池。
3. 不默认全库扫描。
4. 每个 document 输出 chunk 总数、dense indexed、failed count。
5. 支持 dry-run。
6. Qdrant / embedding 失败时 fail-open 并汇总失败原因。

### 4.3 首轮建议回填文件池

1. 主标书：`869d4684-0a98-4825-bc72-ada65c15cfc9`
2. 对比标书：`a47a409f-cb8a-4d29-b938-43c10767802d`
3. 答疑文件：`1db84714-d49f-48a2-8fa9-c6f73424dd32`
4. 附件十一交付标准：`46372530-ea3d-4442-bd67-23efeb0b70df`
5. 3-1 数字化交付标准：`60d9601a-e797-47c9-a421-61dba6f88c7c`
6. 会议纪要：`92051cc6-56b5-4930-bdf0-119163c83a75`
7. Excel 样本：`976d7376-6fd1-4285-9e8f-5772210d6558`
8. PPTX 样本：`ecf7583c-0180-46f9-a013-88480bbcdc3e`

## 5. 测试计划

### 5.1 单元测试

1. dense upsert payload 字段完整。
2. vector dimension 不匹配时失败可诊断。
3. ingestion 调用 dense upsert。
4. Qdrant upsert 失败时 OpenSearch ingestion 不被阻断。
5. dense ingestion status / failed count 写入 job 或 trace metadata。

### 5.2 集成测试

1. 上传小文档后 Qdrant collection 中可查到对应 points。
2. payload filter 可按 `document_id` / `source_type` / `document_type` 命中。
3. dense retrieval 返回真实 candidate。
4. hybrid retrieval 同时包含 dense 与 sparse candidate。
5. OpenSearch 正常、Qdrant 失败时上传仍完成，dense 状态可诊断。

### 5.3 回归评测

Phase 2.16 完成后应复跑：

1. `scripts/phase214_regression_eval.py`
2. 关键真实 query 的 dense-only smoke
3. hybrid smoke
4. 不污染现有 sparse-only 成功 case

## 6. 风险点

1. Aliyun embedding 调用成本与延迟会随 chunk 数增长。
2. 大标书 600+ chunks 的同步 embedding 可能拖慢上传。
3. Qdrant upsert 失败若处理不当，会误伤 sparse ingestion。
4. payload schema 与 retrieval filter 不一致会导致 dense 精确过滤失效。
5. 现有 Qdrant collection 若有历史脏数据，回填前需先做限定 document 级验证。

## 7. 非目标

1. 不改 rerank 策略。
2. 不改 query rewrite。
3. 不做权限大改。
4. 不做 rollout。
5. 不重建全库 index。
6. 不默认全库 backfill。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。

## 8. 当前建议

建议开始 Phase 2.16 最小实现，但第一步应只做新上传文件 dense ingestion 与限定文件池 backfill 脚本，不直接扩大到全库重建或生产 rollout。

## 9. 首轮最小实现结果

已完成：

1. 新上传文件 ingestion 后追加 dense indexing。
2. dense payload 保留 `document_id`、`version_id`、`chunk_id`、`source_type`、`document_type`、`source_name`、`chunk_index` 等字段。
3. Qdrant / embedding 失败时 fail-open，不阻断 PostgreSQL 与 OpenSearch sparse 路径。
4. `DocumentVersion.metadata_json.dense_ingestion` 记录 dense 状态、成功数、失败数、embedding model、dimension 与 Qdrant collection。
5. 新增显式 document_id backfill 脚本：`scripts/phase216_dense_backfill.py`。

验证结果：

1. 目标测试 `19 passed`。
2. 新上传 smoke 在 `OPENSEARCH_URL=localhost`、`QDRANT_URL=localhost` 下完成 sparse + dense：`indexed_count=1`、`dense_ingestion.status=executed`、`dense_indexed_count=1`。
3. 已知答疑文件 `1db84714-d49f-48a2-8fa9-c6f73424dd32` 完成 dense backfill：`12/12` 成功。
4. dense-only retrieval 已能从 Qdrant 返回真实候选，且 document_id 精确收敛。

降级项：

1. 本机直接运行时，如果环境变量仍指向容器内 host `postgres` / `qdrant` / `opensearch`，需要覆写为 `localhost`。
2. 全量真实文件池 backfill 尚未执行，建议下一轮按显式 document_id 分批扩大。

## 10. Rerank Smoke Audit 尾项

本阶段 dense ingestion 不混入 rerank 策略修改。Rerank Smoke Audit 作为后续独立验证项登记。

后续需单独确认：

1. rerank provider 当前是否启用。
2. rerank 真实模型调用是否实际发生。
3. rerank 触发条件是什么。
4. fail-open、latency、error trace 是否可观测。
5. 是否应纳入 Phase 2.14 eval，或进入后续 Phase 2.17 质量评测。

## 11. 真实文件池 dense backfill 与 hybrid smoke

### 11.1 回填结果

| 文件 | document_id | chunks | attempted | succeeded | failed | duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 主标书 | `869d4684-0a98-4825-bc72-ada65c15cfc9` | 683 | 683 | 683 | 0 | 287.230s |
| 对比标书 | `a47a409f-cb8a-4d29-b938-43c10767802d` | 613 | 613 | 613 | 0 | 243.877s |
| 答疑文件 | `1db84714-d49f-48a2-8fa9-c6f73424dd32` | 12 | 12 | 12 | 0 | 5.706s |
| 交付标准旧版 | `46372530-ea3d-4442-bd67-23efeb0b70df` | 15 | 15 | 15 | 0 | 5.611s |
| 交付标准新版 | `60d9601a-e797-47c9-a421-61dba6f88c7c` | 20 | 20 | 20 | 0 | 7.689s |
| 会议纪要 | `92051cc6-56b5-4930-bdf0-119163c83a75` | 17 | 17 | 17 | 0 | 6.982s |

### 11.2 Qdrant payload 抽样

已抽样主标书 3 条 Qdrant payload，均包含：

1. `document_id`
2. `chunk_id`
3. `version_id`
4. `chunk_index`
5. `source_name`

### 11.3 dense / hybrid smoke

6 个目标文件均完成 hybrid smoke：

1. `dense_status=executed`
2. `sparse_status=executed`
3. `dense_returned > 0`
4. `sparse_returned > 0`
5. result document_id 均收敛到目标文件
6. candidate_pool 均显示 dense / sparse source count

### 11.4 Phase 2.14 回归评测

复跑 `scripts/phase214_regression_eval.py`：

1. `10 passed`
2. `0 failed`
3. `1 skipped`
4. `latency p50=38.416 ms`
5. `latency p95=271.507 ms`

### 11.5 当前判断

Phase 2.16 dense ingestion 与真实文件池回填已达到阶段收口条件。

仍保留的非阻塞尾项：

1. Rerank Smoke Audit。
2. 是否将 dense/hybrid smoke 纳入更完整的自动评测集。
