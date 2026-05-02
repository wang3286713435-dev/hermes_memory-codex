# Hermes 企业内核型 AI Agent 技术设计文档

## 目录

1. 设计目标
2. 架构原则
3. 总体系统架构
4. 系统分层设计
5. 核心模块设计
6. 数据流设计
7. 记忆系统设计
8. 检索系统设计
9. 文档摄取系统设计
10. 权限与治理设计
11. 引用与可追溯设计
12. 增量更新设计
13. 评测体系设计
14. 可观测性设计
15. API 设计草案
16. 数据库设计草案
17. 推荐技术栈
18. 部署建议

## 1. 设计目标

Hermes 技术架构目标是支撑企业长期记忆、可信检索、可引用问答、结构化事实查询、权限治理、增量更新和评测闭环。

系统必须避免将向量数据库误用为完整记忆系统。向量数据库只承担语义召回职责，不能替代文档治理、结构化事实、权限控制、版本管理、审计和评测。

## 2. 架构原则

1. 文档知识、结构化事实和会话记忆分层管理。
2. 检索采用 hybrid search，不采用纯向量检索作为唯一方案。
3. 权限过滤必须在内容进入 prompt 前完成。
4. 回答必须优先基于可引用来源。
5. 文档更新必须支持增量处理和版本追溯。
6. 核心链路必须可观测、可审计、可评测。
7. 技术栈优先成熟可落地，避免过度理想化。
8. 中文企业场景优先，包括中文分词、OCR、招标文件、公众号文章和企业专有名词。
9. 多模态能力必须先进入可审计的长期记忆，再进入 Agent 推理；不得只依赖临时上下文读取附件。
10. 会议、音频和经营分析类能力必须保留来源、转写、决策依据和人工确认边界。

## 3. 总体系统架构

系统分为七层：

1. 交互层。
2. Agent 编排层。
3. 检索增强层。
4. 长期记忆层。
5. 数据处理层。
6. 数据存储层。
7. 治理与运维层。

### 3.1 交互层

包括 Hermes Chat UI、Web 控制台、企业微信 / 飞书入口和管理后台。

### 3.2 Agent 编排层

负责用户问题理解、意图识别、query rewrite、tool 调用、检索服务调用、结构化事实查询、prompt 构建、回答生成、引用整理和安全检查。

### 3.3 检索增强层

负责 dense retrieval、BM25 retrieval、metadata filter、hybrid fusion、rerank 和 citation builder。

### 3.4 长期记忆层

包括文档知识层、结构化事实层、会话记忆层、检索层和权限治理层。

### 3.5 数据处理层

负责文档接入、文档解析、文档清洗、去重、版本识别、结构化 chunking、embedding、索引写入和增量更新。

### 3.6 数据存储层

包括 PostgreSQL、现有向量数据库、OpenSearch、MinIO、Redis 和日志存储。

### 3.7 治理与运维层

包括权限控制、审计日志、评测系统、监控指标、链路追踪、告警和任务调度。

## 4. 系统分层设计

### 4.1 文档知识层

保存企业非结构化和半结构化知识，包括原始文件、解析文本、文档元数据、chunk、表格块、OCR 文本、文档版本和引用位置。

### 4.2 结构化事实层

保存可精确查询和聚合的事实，包括客户、项目、合同、招标要求、资质、产品、人员、文章、制度、时间、金额、状态字段。

### 4.3 会话记忆层

保存用户交互相关记忆，包括用户偏好、当前任务上下文、历史问题摘要、用户确认事实、待办事项和项目上下文。会话记忆必须绑定用户和权限范围。

### 4.4 检索层

统一提供语义召回、关键词召回、结构化过滤、权限过滤、版本过滤、重排和引用组装。

### 4.5 权限治理层

负责用户身份识别、角色权限、部门权限、项目权限、文档密级、操作权限和审计记录。

## 5. 核心模块设计

### 5.1 Data Connector Service

负责数据源接入，支持本地文件、企业网盘、公众号文章、API 数据源和后续企业系统。

### 5.2 Document Parser Service

负责 PDF、Word、Excel、PowerPoint、HTML、Markdown、TXT 和图片 OCR 等多格式文档解析。

后续阶段扩展音频会议解析能力，负责会议录音转写、时间戳、发言人、议题、决策、行动项和风险点抽取。若底层模型具备音频理解能力，可作为 provider 接入，但系统仍应保存可追溯转写文本和结构化会议记录。

### 5.3 Knowledge Processing Service

负责清洗、去重、元数据提取、版本识别、结构化 chunking 和表格处理。

### 5.4 Embedding Service

负责将 chunk 生成 1024 维向量并写入现有向量数据库。该服务应支持批量 embedding、失败重试、模型替换和 embedding 模型版本记录。

### 5.5 Index Service

负责写入向量索引、BM25 索引、元数据索引、版本状态和权限标签。

### 5.6 Retrieval Service

负责 query rewrite、dense retrieval、BM25 retrieval、metadata filter、hybrid fusion、permission filter、version filter 和 rerank。

### 5.7 Fact Memory Service

负责结构化事实的存储、查询、更新、来源追溯和人工校验状态管理。

### 5.8 Conversation Memory Service

负责用户会话记忆的摘要、存储、读取、过期和权限隔离。

### 5.9 Permission Service

负责所有资源访问判断。

### 5.10 Citation Service

负责引用生成和来源定位。

### 5.11 Evaluation Service

负责离线评测、线上反馈和回归测试。

### 5.12 Audit & Observability Service

负责日志、指标、链路追踪和告警。

### 5.13 Meeting Memory Service

负责会议音频或转写文本的结构化处理、会议摘要、发言人识别、议题归档、决策点、行动项、风险点和后续跟进事项管理。该服务属于后续阶段能力，必须与权限、审计、引用和结构化事实层协同。

### 5.14 Multimodal Ingestion Service

负责 Excel、PowerPoint、图片、扫描件和会议音频等多模态企业资料的统一摄取编排。该服务应保留源文件结构、页码或单元格位置、解析 provider、置信度和失败降级状态。

### 5.15 BIM Asset Catalog Service

负责 BIM 建模文件资产目录治理，优先记录项目、楼栋、楼层、专业、模型类型、版本、原始路径 / 存储位置、文件大小、文件 hash、创建 / 修改时间、责任人、权限标签和派生元数据来源。该服务初期不搬迁原始 TB 级模型文件，不直接把原始模型内容送入 LLM 上下文，只管理可检索元数据、派生文本 / 清单 / 属性和可追溯链接，并为后续 IFC、RVT、NWD、DWG 等解析 provider 预留接口。

## 6. 数据流设计

### 6.1 文档摄取数据流

1. 数据源发现文件。
2. 创建 document record。
3. 计算 file hash。
4. 判断新增、修改、重复或删除。
5. 保存原始文件到 MinIO。
6. 调用解析器生成结构化文本。
7. 清洗正文、表格和 OCR 内容。
8. 提取元数据。
9. 识别版本。
10. 生成 chunk。
11. 生成 embedding。
12. 写入向量数据库。
13. 写入 OpenSearch。
14. 写入 PostgreSQL。
15. 更新任务状态。
16. 写入审计日志。

BIM 文件资产目录摄取可复用该流程的发现、hash、版本、权限、审计和索引能力，但初期应只生成资产目录记录和派生索引，不要求保存或解析完整原始模型内容。

### 6.2 问答数据流

1. 用户发起问题。
2. 加载用户身份和权限上下文。
3. 判断意图。
4. 执行 query rewrite。
5. 生成 metadata filter。
6. 执行 dense retrieval。
7. 执行 BM25 retrieval。
8. 查询结构化事实。
9. 执行 hybrid fusion。
10. 执行 permission filter。
11. 执行 version filter。
12. 执行 rerank。
13. 构建 prompt。
14. 调用 LLM 生成回答。
15. 生成 citation。
16. 执行安全检查。
17. 返回答案。
18. 记录审计日志和评测样本。

## 7. 记忆系统设计

### 7.1 短期记忆

短期记忆用于当前会话，包含当前对话上下文、任务目标、临时检索结果、用户刚上传的文件和最近澄清信息。

短期记忆实现方式包括会话窗口、最近消息缓存、会话摘要和当前任务 state。

### 7.2 长期知识记忆

长期知识记忆对应文档知识层，要求可检索、可引用、可更新、可回溯、可权限控制和可版本管理。

### 7.3 结构化事实记忆

结构化事实记忆用于保存明确事实，例如客户名称、项目名称、合同金额、招标截止时间、资质有效期和制度生效时间。结构化事实优先存储在 PostgreSQL，后续再扩展图数据库。

## 8. 检索系统设计

### 8.1 Dense Retrieval

Dense retrieval 使用当前 1024 维 embedding 进行语义召回，适用于语义相似查询、历史案例查询、方案经验查询和非精确描述型查询。

Dense retrieval 的局限包括对编号、日期、金额、客户名和项目名不稳定，不解决权限，不解决版本，不保证引用精度。

### 8.2 BM25 / Sparse Retrieval

BM25 用于关键词和精确匹配，适用于文件编号、招标编号、客户名称、人名、产品型号、资质名称、条款原文、日期和金额。

### 8.3 Hybrid Retrieval

Hybrid retrieval 流程：

1. Query rewrite。
2. Dense topK 召回。
3. BM25 topK 召回。
4. 结构化事实召回。
5. 候选合并。
6. 去重。
7. Metadata filter。
8. Permission filter。
9. Version filter。
10. Rerank。
11. 输出最终上下文。

融合策略采用 Reciprocal Rank Fusion 作为 MVP 默认方案。

### 8.4 Metadata Filter

支持 document_type、source_type、department_id、project_id、customer_id、created_at、updated_at、effective_at、version、is_latest、status、confidentiality_level、permission_tags、author、source_uri、file_name 和 title_path 等字段。

### 8.5 Rerank

MVP 使用 bge-reranker 中文能力模型或兼容 rerank 服务。Rerank 输入 query 和候选 chunk，输出 relevance score，支持 topN 和失败降级，不承担权限控制职责。

### 8.6 Query Rewrite

Query rewrite 用于中文口语标准化、简称扩展、项目名补全、多轮上下文补全、关键词查询生成和过滤条件识别。

## 9. 文档摄取系统设计

### 9.1 文档接入

支持手动上传、批量目录同步、公众号文章抓取、API 接入和定时任务。

### 9.2 文档解析

推荐实现：

1. PDF：PyMuPDF + pdfplumber。
2. OCR：PaddleOCR。
3. Word：python-docx + LibreOffice。
4. Excel：openpyxl。
5. PowerPoint：python-pptx。
6. HTML：BeautifulSoup + Readability。
7. Markdown/TXT：原生文本解析。
8. Audio：优先接入稳定转写 provider；若 Hermes 当前模型具备音频理解能力，可作为会议转写或摘要 provider 之一，但必须落地可审计转写文本。
9. BIM：初期只接入资产目录和派生元数据；后续解析 provider 可逐步评估 IFC、RVT、NWD、DWG 等格式，但不得把原始模型二进制直接作为 LLM 上下文。

Excel 解析应保留 workbook、sheet、行列坐标、表头、合并单元格、公式、金额和单位。PowerPoint 解析应保留 slide index、标题、正文、备注、图表说明和图片 OCR。音频解析应保留 audio_id、segment_id、timestamp、speaker、transcript、decision、action_item 和 confidence。

BIM 资产目录应保留 model_asset_id、project_id、building、floor、discipline、model_type、version、source_path、storage_location、file_size、content_hash、created_at、modified_at、owner、permission_tags 和 derived_metadata_source。模型构件级解析、几何解析、碰撞检查、自动算量和在线查看器属于后续专项，不纳入当前技术设计落地范围。

### 9.3 文档清洗

清洗对象包括页眉页脚、水印、空白段落、页码、目录噪声、HTML 导航、广告推荐和 OCR 乱码。

### 9.4 去重

去重层级包括文件级 hash、文本级 hash、chunk 级 hash 和相似 chunk 去重。

### 9.5 版本识别

版本依据包括文件名、文档标题、文档编号、发布时间、生效时间、修改时间、内容 hash 和文档内部版本声明。

### 9.6 结构化 Chunking

分块策略包括标题层级优先、条款完整性优先、表格完整性优先、语义完整性优先、公众号按小标题切分、招标文件按章节切分、制度文件按条款切分。

建议大小：普通文本 500-1200 中文字，招标条款按条款独立切分，表格按完整表格或逻辑行组切分，overlap 100-200 中文字。

多模态 chunking 后续应支持表格块、PPT 页面块、会议议题块和会议行动项块。表格 chunk 必须保留 sheet 与单元格位置；PPT chunk 必须保留页码和页面标题；会议 chunk 必须保留时间戳、发言人和议题上下文。

## 10. 权限与治理设计

权限模型采用 RBAC + ABAC。

RBAC 用于管理管理员、知识管理员、普通员工、部门负责人、项目成员和审计人员。

ABAC 基于用户部门、用户项目、用户角色、文档密级、文档类型、项目归属、客户归属和操作类型判断。

权限执行原则包括默认拒绝、最小权限、先过滤后生成、无权限内容不得进入 prompt、引用展示必须校验权限、所有权限拒绝写入审计日志。

## 11. 引用与可追溯设计

每个回答记录 answer_id、query_id、document_id、version_id、chunk_id、source_name、source_uri、page、section_path、quote_text、retrieval_score、rerank_score 和 generated_at。

引用展示包含文件名、版本、页码、章节、更新时间、原文摘录和原文链接。

## 12. 增量更新设计

增量更新包括数据源扫描增量、内容 hash 增量、chunk 增量、embedding 增量、BM25 索引增量、权限元数据增量和版本状态增量。

更新策略：

1. Hash 未变则跳过解析。
2. 内容变化则重新生成受影响 chunk。
3. 新版本标记为 latest。
4. 旧版本标记为 historical 或 deprecated。
5. 删除文件不物理删除知识，先标记 archived。
6. 查询默认只检索 latest + active 文档。

## 13. 评测体系设计

### 13.1 离线评测

指标包括 Recall@K、Precision@K、MRR、NDCG、Citation Accuracy、Answer Faithfulness、Version Accuracy、Permission Safety 和 Latency。

### 13.2 在线评测

采集点赞、点踩、用户追问、引用错误反馈、没有找到反馈、人工复核结果、查询无结果率和低置信度率。

### 13.3 回归评测

Embedding 模型、chunking 策略、hybrid 权重、reranker、query rewrite prompt、权限策略和版本策略变更后必须触发回归评测。

## 14. 可观测性设计

核心指标包括查询量、检索成功率、无结果率、平均召回数量、rerank 延迟、LLM 延迟、回答失败率、引用缺失率、权限拒绝次数、文档摄取成功率、解析失败率、索引写入失败率和增量任务积压量。

日志字段包括 trace_id、user_id、query、rewritten_query、filters、dense_results、bm25_results、reranked_results、final_context、answer、citations 和 permission_decisions。

## 15. API 设计草案

### 15.1 文档上传

`POST /api/documents/upload`

### 15.2 摄取任务创建

`POST /api/ingestion/jobs`

### 15.3 摄取任务查询

`GET /api/ingestion/jobs/{job_id}`

### 15.4 检索

`POST /api/retrieval/search`

请求字段包括 query、user_id、top_k、filters、search_mode 和 include_citations。

### 15.5 问答

`POST /api/agent/ask`

请求字段包括 user_id、session_id、query、mode、filters 和 citation_required。

### 15.6 事实查询

`POST /api/facts/query`

### 15.7 事实更新

`POST /api/facts/upsert`

### 15.8 权限检查

`POST /api/permissions/check`

### 15.9 评测运行

`POST /api/evaluation/run`

## 16. 数据库设计草案

### 16.1 documents

字段包括 id、title、source_type、source_uri、document_type、owner_id、department_id、project_id、confidentiality_level、status、created_at 和 updated_at。

### 16.2 document_versions

字段包括 id、document_id、version_name、version_number、file_hash、content_hash、is_latest、effective_at、expired_at 和 created_at。

### 16.3 chunks

字段包括 id、document_id、version_id、text、title_path、section_path、page_start、page_end、content_hash、token_count、embedding_id、sparse_id、permission_tags 和 created_at。

### 16.4 permissions

字段包括 id、resource_type、resource_id、subject_type、subject_id、action、effect 和 condition_json。

### 16.5 facts

字段包括 id、entity_type、entity_id、predicate、value、value_type、source_document_id、source_chunk_id、confidence、verified_status、created_at 和 updated_at。

### 16.6 conversation_memories

字段包括 id、user_id、conversation_id、memory_type、content、source、permission_scope、expires_at 和 created_at。

### 16.7 audit_logs

字段包括 id、trace_id、user_id、action、resource_type、resource_id、request_json、result_json 和 created_at。

## 17. 推荐技术栈

### 17.1 后端框架

最终推荐 Python FastAPI。理由是 AI 和文档处理生态成熟，与 embedding、OCR、解析库集成成本低，FastAPI 适合构建轻量服务和内部 API。

### 17.2 异步任务

最终推荐 Celery + Redis。理由是适合文档摄取、解析、embedding、索引写入等异步任务，支持失败重试和任务状态管理。

### 17.3 元数据与事实库

最终推荐 PostgreSQL。理由是稳定可靠，适合文档元数据、版本、权限、事实和审计索引，并支持 JSONB 和结构化查询。

### 17.4 向量数据库

最终推荐沿用现有向量数据库。理由是当前系统已配置，向量维度为 1024，MVP 阶段避免引入额外迁移风险。

### 17.5 全文检索

最终推荐 OpenSearch。理由是支持 BM25、中文分词配置、元数据过滤，部署和授权成本相对可控。

### 17.6 对象存储

最终推荐 MinIO。理由是 S3 兼容、私有化部署成熟，适合保存原始文件和解析中间产物。

### 17.7 OCR

最终推荐 PaddleOCR。理由是中文识别能力较强，可私有化部署，适合扫描件和图片资料。

### 17.8 文档解析

最终推荐 PyMuPDF、pdfplumber、python-docx、openpyxl、python-pptx、BeautifulSoup 和 LibreOffice headless。

### 17.9 Rerank

最终推荐 bge-reranker 中文模型私有化部署。理由是中文相关性表现较好，可本地部署，成本和合规性可控。

### 17.10 可观测性

最终推荐 OpenTelemetry、Prometheus、Grafana 和 Loki。

## 18. 部署建议

MVP 阶段采用模块化单体 + 独立基础组件部署。

建议服务包括 Hermes API 服务、Worker 服务、Retrieval 服务、PostgreSQL、Redis、OpenSearch、MinIO、向量数据库、Reranker 服务和 Observability 服务。

后续规模扩大后，再拆分为独立微服务。
