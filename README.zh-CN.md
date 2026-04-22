# Hermes Memory

Hermes Memory 是企业级 Hermes AI Agent 的内建 memory kernel。它为文档摄取、解析、切分（chunking）、混合检索（hybrid retrieval）、“引用优先”的回答、版本感知元数据、治理（governance）钩子以及记忆回写（memory writeback）提供第一阶段的工程基础。

## 1. 范围

本仓库实现了以下文档中定义的 Phase 1 工程骨架：

- `docs/PRD.md`
- `docs/TECHNICAL_DESIGN.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE_DECISION_RECORD.md`

当前 Phase 1 的闭环重点包括：

1. FastAPI 后端服务。
2. 配置管理。
3. PostgreSQL 元数据模型与摄取状态。
4. 文档上传与存储。
5. 支持 `txt`、`md`、`html`、`pdf`、`docx` 的文档解析。
6. 按标题与段落的结构化 chunking，并在超长时降级为长度切分。
7. OpenSearch 的 BM25 chunk 索引。
8. 支持元数据过滤的检索 API。
9. 为下游 agent 回答提供 citation（引用）归一化。
10. 内建 memory kernel，用于 agent 查询路由、检索编排、上下文构建、citation 生成、治理与回写。
11. 健康检查 API。
12. Docker Compose：PostgreSQL、Redis、OpenSearch、MinIO。

## 2. 技术栈

最终 MVP 技术栈：

1. 后端：Python FastAPI。
2. 异步任务：Celery + Redis。
3. 元数据与结构化事实：PostgreSQL。
4. 向量存储：现有的 1024 维向量数据库。
5. 全文检索：OpenSearch。
6. 对象存储：MinIO。
7. OCR：PaddleOCR 集成点。
8. Rerank：兼容 bge-reranker 的服务集成点。
9. 可观测性：结构化日志；OpenTelemetry/Prometheus/Grafana/Loki 预留为后续工作。

## 3. 本地启动

创建环境变量文件：

```bash
cp .env.example .env
```

启动依赖与服务：

```bash
docker compose up --build
```

健康检查：

```bash
curl http://localhost:8000/health
```

API 文档：

```text
http://localhost:8000/docs
```

## 4. Phase 1 验证

创建一个示例文档：

```bash
cat > /tmp/hermes-sample.md <<'EOF'
# 招标资料

## 项目背景

智慧园区项目需要支持统一身份认证、知识检索和权限治理。

## 资质要求

投标方应具备软件开发能力、项目实施经验和信息安全管理能力。
EOF
```

上传并摄取文档：

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/tmp/hermes-sample.md" \
  -F "title=智慧园区招标资料" \
  -F "source_type=tender" \
  -F "document_type=md"
```

检索已索引的 chunks：

```bash
curl -X POST "http://localhost:8000/api/v1/retrieval/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "资质要求",
    "top_k": 5,
    "filters": {
      "source_type": "tender"
    },
    "include_citations": true
  }'
```

期望响应包含 `results[*].chunk_id`、`document_id`、`version_id`、`source_name`、`heading_path`、`page_start`、`page_end` 以及 chunk 文本内容。

通过内建 Hermes memory kernel 发起提问：

```bash
curl -X POST "http://localhost:8000/api/v1/agent/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "智慧园区项目有哪些资质要求？",
    "user_id": "u-demo",
    "session_id": "s-demo",
    "filters": {
      "source_type": "tender"
    },
    "citation_required": true
  }'
```

agent 路径会经过 `app/memory_kernel`。该模块负责查询路由、治理过滤、检索编排、上下文构建、citation 生成与记忆回写。检索与引用服务仍然作为模块化依赖存在，但不再以外置 add-on 的形式挂到 agent 上。

如果 OpenSearch 不可用，检索会降级为 PostgreSQL 的 `ILIKE` 搜索，并返回 `backend=database_fallback`。在接入现有 1024 维向量数据库适配器之前，dense 向量检索会被刻意标记为 TODO。

## 5. 开发

本地安装：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

运行 API：

```bash
uvicorn app.main:app --reload
```

语法检查：

```bash
python -m compileall app
```

当未使用 `DB_AUTO_CREATE_TABLES=true` 时，显式执行迁移：

```bash
alembic upgrade head
```

## 6. 目录结构

```text
app/
  api/          HTTP API 路由。
  core/         Settings、日志、应用生命周期。
  db/           数据库引擎、会话、模型基类。
  memory_kernel/内建 Hermes memory kernel 编排层。
  models/       SQLAlchemy 持久化模型。
  schemas/      Pydantic 请求/响应 schema。
  services/     摄取、解析、chunking、检索、agent、citation 等领域服务。
  worker/       Celery 应用与后台任务入口。
```

## 7. 当前边界

这是一个可运行的 Phase 1 最小知识闭环。目前尚未实现 dense 向量检索、OCR、生产级权限过滤或 LLM 回答生成。这些都被明确列为后续工作项。

