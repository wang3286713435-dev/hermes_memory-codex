# Mac mini 最小 MVP 部署指南

## 1. 这份指南解决什么问题

这份指南面向“把当前开发中的 Hermes 最小可用版复制到一台新的 Mac mini 测试机上，供内部实际试用”。

目标是尽快得到一个可运行、可验证、可热更新的内部受控 MVP 节点，而不是 production rollout。

本指南只覆盖：

1. `Hermes_memory` 后端内核的最小部署。
2. `hermes-agent` 主应用 / CLI 与 `Hermes_memory` 的接线方式。
3. Day-0 到可用 smoke 的最短路径。

本指南不授权：

1. production rollout。
2. 自动审标、自动投标、自动经营决策。
3. repair、cleanup、backfill、reindex、delete、destructive migration。
4. 完整 IAM / SSO / RBAC / ABAC / 运维监控体系。

## 2. 当前项目的能力边界

### 2.1 目前已经具备

1. 文件入库与版本治理：
   - 支持上传并入库 `txt`、`md`、`html`、`pdf`、`docx`、`xlsx`、`pptx`。
   - 同标题 + 同 source_type + 同 document_type 的文件会归并到同一 document 下做 version 管理。
   - 重复文件可识别 duplicate upload。
2. 检索能力：
   - OpenSearch 稀疏检索可用。
   - Qdrant dense 检索可用。
   - 默认走 hybrid 检索，并保留 trace。
   - OpenSearch 异常时可降级到 PostgreSQL fallback。
3. 结构化引用：
   - Excel 可返回 `sheet_name`、`cell_range` 或 row/range 降级信息。
   - PPTX 可返回 `slide_number`、`slide_title`。
   - 普通文档可返回 `document_id`、`version_id`、`chunk_id`、页码、标题路径。
4. Agent / Memory Kernel：
   - `Hermes_memory` 提供 query routing、governance、retrieval orchestration、citation 生成、context 构建、writeback。
   - `hermes-agent` 已能在 session 中做 alias 绑定并复用 `Hermes_memory` 的检索结果。
5. Facts 能力：
   - 已有 evidence-backed facts 的创建、确认、拒绝、查询与审计接口。
   - facts 已与 source chunk / version 关联，可检查 stale source version。

### 2.2 目前明确不应当当成“已经完成”的

1. 最终答案生成层：
   - `Hermes_memory` 的 `/agent/ask` 目前返回的是“可引用上下文 + answer basis”，不是完整业务闭环的最终智能结论。
2. 生产级权限治理：
   - 当前只有 soft policy / latest-version 级别治理，不是完整 RBAC / ABAC。
3. 自动业务决策：
   - 不允许把输出直接当自动审标、自动经营、自动合同或采购决策。
4. facts / transcript 边界：
   - 必须保持 `facts_as_answer=false`。
   - 必须保持 `transcript_as_fact=false`。
5. 运维自动化：
   - 还没有进入 production 级监控、自动恢复、自动迁移、自动修复流程。

### 2.3 当前最适合拿来做什么

1. 内部受控的企业文件问答与证据检索。
2. 标书基础字段提取、风险项定位、Missing Evidence 显式提示。
3. Excel / PPTX / 会议纪要类文件的结构化引用与人工复核辅助。
4. 有人工 reviewer 在场的方向分析、决策辅助和资料核对。

## 3. 一定要先分清楚的架构事实

当前“应用”其实分成两层：

1. `Hermes_memory`
   - 负责入库、解析、chunk、索引、检索、facts、API、memory kernel 内核。
2. `hermes-agent`
   - 负责 CLI / 会话 / alias / 用户交互 / 模型调用。

如果你只部署 `Hermes_memory`，你会得到：

1. API。
2. 上传与检索能力。
3. 健康检查与后端能力。

但你不会得到完整的“会话式使用体验”：

1. 没有 `@主标书`、`@会议纪要` 这类 alias 交互层。
2. 没有 Hermes CLI 的会话能力。

所以测试机上真正“可用”的最小 MVP，建议同时部署：

1. `Hermes_memory`
2. `hermes-agent`

## 4. 推荐的最小部署拓扑

### 4.1 机器目录

推荐：

```text
/Users/hermes/
  code/
    Hermes_memory/
    hermes-agent/
  env/
    hermes_memory.env
    hermes_agent.env
  data/
  logs/
  reports/
  tmp/
```

### 4.2 服务分工

最小建议保留：

1. Postgres
2. Redis
3. OpenSearch
4. MinIO
5. Qdrant
6. Hermes_memory API
7. hermes-agent CLI

### 4.3 最短可跑方式

对新 Mac mini，最省事的方式是：

1. `Hermes_memory` 整套基础服务走 Docker Compose。
2. `hermes-agent` 走本地 Python venv。

这样：

1. 底层依赖稳定。
2. CLI 使用体验保留。
3. 后续更新代码只要 `git pull` + 重启。

## 5. Mac mini 上的实际部署步骤

## 5.1 机器准备

至少确认：

1. macOS 初始化完成。
2. `git`、`uv`、Docker runtime 已安装。
3. 新机器只在内网 / VPN 内访问，不对公网暴露。

## 5.2 创建目录

```bash
mkdir -p /Users/hermes/code
mkdir -p /Users/hermes/env
mkdir -p /Users/hermes/data
mkdir -p /Users/hermes/logs
mkdir -p /Users/hermes/reports
mkdir -p /Users/hermes/tmp
```

## 5.3 拉取两个仓库

```bash
git clone <Hermes_memory_remote> /Users/hermes/code/Hermes_memory
git clone <hermes_agent_remote> /Users/hermes/code/hermes-agent
```

如果你们已经有 baseline tag，测试机必须明确记录：

1. `Hermes_memory` 的 branch / commit / tag。
2. `hermes-agent` 的 branch / commit / tag。

不要在测试机上直接拿“开发中但未确认”的 dirty worktree 启动。

## 5.4 准备 `Hermes_memory` 环境变量

先复制模板：

```bash
cp /Users/hermes/code/Hermes_memory/.env.example /Users/hermes/code/Hermes_memory/.env
cp /Users/hermes/code/Hermes_memory/.env.example /Users/hermes/env/hermes_memory.env
```

建议把 `/Users/hermes/env/hermes_memory.env` 当成源文件，再同步到仓库根目录 `.env`，因为当前 `docker-compose.yml` 默认读取仓库根目录 `.env`。

最关键的变量有：

1. `DATABASE_URL`
2. `OPENSEARCH_URL`
3. `QDRANT_URL`
4. `QDRANT_COLLECTION`
5. `ALIYUN_EMBEDDING_API_KEY`
6. 可选 `ALIYUN_RERANK_API_KEY`
7. `STORAGE_BACKEND`
8. `LOCAL_STORAGE_PATH`

### 5.4.1 如果你直接用仓库自带 Docker Compose

建议保持 `.env.example` 里的容器内主机名：

```text
DATABASE_URL=postgresql+psycopg://hermes:hermes@postgres:5432/hermes_memory
REDIS_URL=redis://redis:6379/0
OPENSEARCH_URL=http://opensearch:9200
MINIO_ENDPOINT=minio:9000
QDRANT_URL=http://qdrant:6333
```

### 5.4.2 重要提醒

1. `ALIYUN_EMBEDDING_API_KEY` 如果不配，系统仍可启动，但 dense embedding / dense retrieval 会退化或 fail-open。
2. `RERANK_ENABLED=false` 也能跑；只是没有 rerank 增益。
3. `QDRANT_COLLECTION` 必须与当前实际索引集合一致，建议先保持 `hermes_chunks`。

## 5.5 启动 `Hermes_memory`

```bash
cd /Users/hermes/code/Hermes_memory
docker compose up -d --build
```

检查状态：

```bash
docker compose ps
curl http://127.0.0.1:8000/health
```

如果健康正常，应该返回类似：

```json
{"status":"ok","app":"Hermes Memory","environment":"local"}
```

可进一步打开：

```text
http://127.0.0.1:8000/docs
```

## 5.6 首次验证 `Hermes_memory`

先做最小 API 验证：

1. `/health` 正常。
2. `/docs` 可打开。
3. 能通过 `/api/v1/documents/upload` 上传一份样例文档。
4. 能通过 `/api/v1/retrieval/search` 查回该文档。

如果这一步都没过，不要继续接 `hermes-agent`。

## 5.7 安装 `hermes-agent`

在 `hermes-agent` 仓库中按其 README 做本地安装。最短路径通常是：

```bash
cd /Users/hermes/code/hermes-agent
./setup-hermes.sh
```

如果你们团队不用安装脚本，也可以保留你们现有的 venv 方案，但要保证：

1. `hermes` 命令可用。
2. `hermes chat --help` 可用。

## 5.8 把 `hermes-agent` 指向 `Hermes_memory`

当前 `hermes-agent` 的 memory kernel 不是只靠 HTTP 调 API，它还会直接加载本地 `Hermes_memory` 仓库路径。

最关键的两个环境变量：

```bash
export HERMES_MEMORY_KERNEL_ENABLED=1
export HERMES_MEMORY_PATH=/Users/hermes/code/Hermes_memory
```

建议先在当前 shell 中设置，再启动 Hermes CLI：

```bash
cd /Users/hermes/code/hermes-agent
export HERMES_MEMORY_KERNEL_ENABLED=1
export HERMES_MEMORY_PATH=/Users/hermes/code/Hermes_memory
hermes chat --help
```

如果你们是长期运行，建议把这两个变量写入测试机的受控启动脚本或 operator 管理的 env 文件，不要靠手工每次输入。

## 5.9 首次验证 CLI / 应用层

最小 smoke 顺序建议：

1. `curl http://127.0.0.1:8000/health`
2. `hermes chat --help`
3. 启动一个新会话
4. 在同一 session 中绑定：
   - `@主标书`
   - `@会议纪要`
   - `@硬件清单`
   - `@C塔方案`
5. 跑最小 query：
   - 主标书基础字段 + Missing Evidence
   - Excel `sheet_name` / `cell_range`
   - PPTX `slide_number` / `slide_title`
   - 会议纪要 action items / risks

验收时必须确认：

1. `facts_as_answer=false`
2. `transcript_as_fact=false`
3. 没有第三文件污染
4. citation 可人工复核

## 6. 推荐你采用的“最小复制策略”

如果你现在的目标不是“再开发”，而是“尽快把能跑的 MVP 复制到测试机使用”，我建议你这么做：

1. 先冻结一个双仓 baseline：
   - `Hermes_memory` 一个 commit / tag
   - `hermes-agent` 一个 commit / tag
2. 开发机上先把这两个版本跑通。
3. 测试机只做：
   - clone / pull 到对应 tag
   - 配 env
   - `docker compose up -d --build`
   - 安装 / 启动 `hermes-agent`
   - 跑 smoke
4. 不要在测试机临时改代码。
5. 后续热更新只允许：
   - 开发机验证
   - Git commit / tag
   - 测试机 pull
   - 重启服务
   - 复跑 smoke

## 7. 目前最容易踩坑的点

1. 只部署了 `Hermes_memory`，但没有部署 `hermes-agent`
   - 结果 API 在，但实际使用者没有完整 alias / session 体验。
2. `HERMES_MEMORY_PATH` 没指向测试机上的真实仓库路径
   - 结果 CLI 启动了，但 enterprise retrieval / alias 能力不工作。
3. `ALIYUN_EMBEDDING_API_KEY` 没配置
   - 结果 dense 检索和 dense ingestion 退化，效果和开发机不一致。
4. `QDRANT_COLLECTION` 配错
   - 结果检索“像是能跑”，但其实打到了错误 collection。
5. 测试机上直接使用开发中的 dirty worktree
   - 结果无法复盘，也无法稳定 hot update。
6. 把“内部受控 MVP 通过”误当成“可以上线生产”
   - 这是当前阶段最需要避免的误判。

## 8. 一句话结论

如果你要把“现在这个项目”复制到一台新的 Mac mini 上实际试用，最小可行方案不是只搬一个仓库，而是：

1. 用 Docker Compose 部署 `Hermes_memory` 整套后端。
2. 同时部署 `hermes-agent`。
3. 通过 `HERMES_MEMORY_KERNEL_ENABLED=1` 和 `HERMES_MEMORY_PATH=...` 把两者接起来。
4. 用 `API /health + hermes chat --help + 四个 alias + 四类 smoke query` 作为上线前最小验收。

