# Hermes Memory 当前待办清单

## 1. Phase 2.1-Qdrant 未确认项

1. Qdrant 是否需要 `QDRANT_API_KEY`、以及 `api-key` header 是否生效尚未确认；当前仅验证了无鉴权的本地容器路径。
2. Dockerfile 依赖 `python:3.11-slim` 拉取在部分网络环境可能超时（docker.io oauth token timeout），导致 `docker compose build api` 失败；若团队主路径依赖容器构建，需准备镜像源/网络策略或提供替代运行方式。

## 2. 暂不推进事项

- 真实 `rerank` 模型接入
- `facts` 联查
- OCR
- 多 agent 协作
- 复杂权限策略
- 大规模 ingestion 改造

说明：上述事项并非长期放弃，而是不进入当前收口阶段。多模态企业资料、会议音频记忆和更完整企业级 Agent 能力应在记忆底座、会话文档作用域和基础检索稳定后分阶段推进。

## 3. Phase 2.2 后续待办

1. 真实 reranker 模型尚未接入。当前仅完成 `NoopReranker` 与 rerank hook 结构，不能视为排序质量增强已完成；需在后续 rerank 实现阶段处理。
2. rerank 质量评测集尚未建立。当前只有最小评测入口，不能衡量真实召回排序收益；需在 evaluation 阶段补充标注样本与指标。
3. rerank 延迟、成本、超时策略尚未验证。当前仅验证 fail-open 行为，真实模型服务接入后需专项压测。
4. 真实 reranker adapter 尚未选型。下一阶段应先在 API 型 reranker 与轻量 cross-encoder 服务之间选择一条主路线，不应并行扩展多个 provider。
5. candidate pool 内部候选扩大策略尚未实现。当前仍沿用 request `top_k` 召回，后续若要提升 rerank 收益，应增加内部 candidate cap，但不能改变公开 `top_k` 语义。

## 4. Phase 2.3 待办

1. 当前黄金 query 已扩到 48 条，但样本仍以脱敏近真实评测语料为主，不是完整真实企业知识库；进入更大范围 rollout 前仍需补更大范围的真实业务 query 集。
2. rerank candidate 扩大策略尚未进入代码。当前只使用 `RERANK_INPUT_CAP` 截断，未实现 dense/sparse 内部 candidate target 扩大。
3. BGE / cross-encoder 只作为备选路线记录，当前不实现。
4. 当前 baseline vs experiment 已覆盖 48 条小规模样本，top-1 有提升且无回归，已足以支持“默认启用策略评估”，但仍不足以直接作为全局默认启用依据。
5. 默认启用实施前仍需补充 rollout policy 落地：按 query 类型灰度、超时阈值、成本观测和回退开关。
6. Phase 2.5 已落地局部默认启用规则，但当前只覆盖招标资料中的高收益 query；扩大范围前仍需更大规模真实 query 复测。
7. 需要补最小运行手册：灰度开关切换、timeout 观察、fail-open 监控与回滚步骤。
8. Phase 2.6 环境阻塞已解除：Docker daemon、Qdrant、OpenSearch 已恢复，灰度验证脚本可正常运行。
9. Phase 2.6 已修正灰度脚本的 request 上下文传递，当前局部默认启用可命中目标 query；后续应继续观察真实灰度下的 fail-open rate、p95/p99 与收益稳定性。
10. Phase 2.8 已完成退出标准与最后观察窗口判定：最后 `3` 次完整观察满足运行基线稳定、回退稳定、延迟可接受和后端异常窗口可控标准，Phase 2.8 已收口。Phase 2.9a 受控环境重跑显示：前一轮长窗口异常未在更干净环境中复现，dense / sparse 失败与 OpenSearch 超时均恢复为 `0`，命中集恢复稳定；当前更可能是 Mac Air 8GB 的本机资源瓶颈与并行负载放大了异常。Phase 2.9b 长窗口压力验证进一步表明：加装散热器后，Air 可稳定承载 `8` 次窗口，也可跑完 `12` 次窗口，但长窗口下会出现明显 `p99` 长尾尖峰；当前更像宿主机内存 / swap 与 Docker 资源竞争带来的长尾抖动，而不是业务链路失稳。该判断已由后续 Windows + WSL2 高可信补证承接，最终见 Phase 2.9c 条目。
11. Phase 2.9 后续默认采用“白天继续主线开发，晚上或空闲窗口跑长窗口验证”的节奏，避免重度验证打断主线。与此同时，可开始小批量、脱敏、低敏企业资料的受控验证，但不得改变当前规则、启用范围或 rollout readiness 主线判断。

## 5. Phase 2.9 真实文件测试后续待办

1. 增强大型标书深层结构化章节召回能力。当前在 800+ 页真实标书中，资质等级门槛、项目经理执业资格、总工期、里程碑节点、付款节点 / 支付比例、结算方式、缺陷责任期 / 质保金 / 保留金、延期误期赔偿、不平衡报价处置标准等核心参数仍无法稳定召回；下一步应优先增强“投标人须知前附表 / 资格审查 / 资信标 / 合同专用条款 / 工程量清单 / 限价明细”的章节定向检索能力。
2. 明确当前检索能力仍偏“初筛”，尚未达到完整审标。当前可稳定覆盖约 60%～70% 的高价值审标条款，但仍缺约 30%～40% 的核心商务 / 合同 / 资审参数；在补齐结构化召回前，暂不应宣称已具备“完整 AI 审标自动化能力”。
3. dense ingestion 仍未接通。当前上传 ingestion 尚未将 chunk upsert 到 Qdrant，dense 当前仍为 `0`；本轮真实文件验证主要依赖 sparse / OpenSearch，该项应单独立项，不与当前真实文件测试收口混在一起。
4. 高可信度灰度测试已完成阶段补证。Windows + WSL2 高可信验证中，长窗口 `20/20` 成功，OpenSearch timeout / dense_failed_count / sparse_failed_count / 命中漂移 / 后端异常窗口均为 `0`；连续真实工作流 `30` 次 retrieval + `30` 次 agent ask 共 `60/60` 成功，document_id / 标题收敛失败与错误文档命中均为 `0`。该结论支撑 Phase 2.9c 稳定性收口，但仍不等同于生产级全面 rollout。
5. 下一步主线不再继续拆 Phase 2.9c 小轮，建议进入非阻塞尾项收敛：继续扩样验证“投标人须知前附表 / 资格审查 / 合同专用条款 / 工程量清单 / 限价明细”相关真实问法，并补 Aliyun embedding / rerank provider smoke。
6. Phase 2.9c 第一轮与第二轮结构化章节增强已证明方向有效：资质等级门槛、项目经理执业门槛、不平衡报价类查询已能更稳定收敛到“资格后审 / 资格审查文件 / 工程量清单”；付款节点、结算方式、缺陷责任期、质保金、误期赔偿已开始稳定打到“第三章 招标人对招标文件及合同范本的补充/修改”，但仍未证明能稳定命中最理想的合同专用条款 chunk。
7. 总工期 / 关键节点方向已从“明显打不进去”提升到“有提升但仍不稳定”。当前代表性查询能将目标 `工期要求` chunk 拉到 top1，但仍需更多真实问法扩样确认，不应直接宣称稳定够用。
8. 多文件连续切换稳定性已补证。Windows 连续真实工作流中 document_id / 标题收敛失败为 `0`、错误文档命中为 `0`，当前可作为 Phase 2.9c 收口证据。
9. 高可信度灰度证据已补齐到 Phase 2.9c 阶段可接受。Windows 长窗口 wall `p95/p99 = 2397.266 ms / 2596.483 ms`；连续真实工作流 `p95/p99 = 34.935 ms / 40.929 ms`。Aliyun embedding / rerank 因缺 secret 未真实调用，作为非阻塞 provider smoke 尾项保留。
10. 当前仍需继续作为质量尾项扩样的是“前附表 / 工期节点”。合同专用条款方向已开始逼近并出现真实命中提升；“总工期 / 关键节点 / 计划开工日期 / 计划竣工日期”已出现 top 结果改善，但仍未证明所有真实问法都稳定够用。
11. Phase 2.9c 最终收口判断：建议收口。`总工期 / 关键节点` 已从“明显打不进去”提升到“有提升但仍不稳定”，可作为质量尾项继续扩样；高可信机器长窗口与连续真实工作流补证已完成，稳定性阻塞已解除。
12. Phase 2.9c 后续不再继续拆小轮推进。下一阶段建议限定为非阻塞尾项收敛：继续扩样验证 `总工期 / 关键节点` 真实问法，并补 Aliyun embedding / rerank provider smoke；不得误判为生产级全面 rollout。
13. Phase 2.9c 新增兼容性回归修复项已完成：`RetrievalService.search()` 引入 `_infer_document_scope()` 后曾打断 `db=None` 路径，导致 `phase26_rerank_gray_validation.py` 报 `NoneType.query`。当前已在 service 层恢复无 DB 安全返回，并补上 `_database_fallback_search()` 的无 DB 保护；后续仍需持续把无 DB 评估脚本纳入最小回归保护，避免再次误判成环境问题。
14. 总工期 / 关键节点 不再作为 Phase 2.9c 稳定性收口阻塞。本轮增加 schedule 参数短语精确加权后，真实大标书查询已能把 `工期要求` 目标 chunk 提升到 top1，`施工工期 / 合同工期` 定义 chunk 提升到 top2，技术要求进度段落被压到更后；当前判定为“有提升但仍不稳定”，转入后续质量尾项。
15. Windows 高可信灰度补证已完成：长窗口 `20/20` 成功，连续真实工作流 `60/60` 成功；`OpenSearch timeout = 0`、`dense_failed_count = 0`、`sparse_failed_count = 0`、命中集漂移 `0`、后端异常窗口 `0`、document_id / 标题收敛失败 `0`、错误文档命中 `0`。Aliyun embedding / rerank 因缺 secret 未真实调用，继续作为非阻塞尾项。
16. Phase 2.9d 非阻塞尾项已完成首轮收敛：Aliyun embedding 真调用返回 `executed` 与 `1024` 维向量；Aliyun rerank 使用 `ALIYUN_EMBEDDING_API_KEY` fallback 真调用 `gte-rerank-v2` 返回 `executed`，top chunk 正确；大型标书 `总工期 / 关键节点` 10 条真实问法扩样全部命中 `工期要求` 目标 chunk。后续若要求专用 rerank key，需单独补 `ALIYUN_RERANK_API_KEY` 专用 key smoke。
17. Phase 2.9d 文档基线已固化：Phase 2.9c 已收口，Phase 2.9d 首轮尾项已完成；当前仍不进入生产级 rollout。PRD 核心缺口继续保留为未完成：dense ingestion、结构化事实层、会话记忆层、权限治理层、增量更新闭环、审计日志闭环、完整评测系统、版本治理增强、知识管理员后台、人工校验机制。

## 6. Phase 2.10+ 企业级 Agent 长期能力候选

1. Phase 2.10 优先处理 Enterprise Session Document Scope：同一 Hermes 会话内维护 active document scope，支持文件切换、上下文防污染和多文件对比，不再依赖新开会话作为产品方案。
2. Phase 2.11 进入规划阶段：企业会话上下文治理继续增强，并规划 Excel、PowerPoint、图片、扫描件和会议音频的企业级摄取策略；当前只明确数据模型、解析 provider、引用格式、权限、审计和评测方式，不直接实现完整 multimodal ingestion。
3. 后续候选 Phase 2.12：Excel / PowerPoint ingestion MVP。Excel 应保留 sheet、行列坐标、表头、公式、金额和单位；PowerPoint 应保留页码、标题、正文、备注、图表说明和图片 OCR。
4. 后续候选 Phase 2.13：Meeting Audio Memory MVP。支持会议录音转写、发言人、议题、决策点、行动项、风险和后续跟进事项沉淀，并与项目、客户、合同和结构化事实关联。
5. 长期目标是将 Hermes 从文档检索器升级为企业级 Agent 中枢，但所有高风险动作仍需人工确认；会议、经营、投标、财务和法务相关结论必须保留来源、引用、权限与审计。

## 7. Phase 2.11 当前待办

1. 企业上下文治理详细设计已补齐：明确 active document、project scope、compare scope、history memory 的优先级和防污染规则。
2. Excel / PPTX 摄取验收样本已补齐：覆盖 sheet/cell、slide/page、备注、图表说明、引用位置和权限标签。
3. 会议音频记忆验收样本已补齐：覆盖转写、说话人、时间戳、议题、决策、行动项、风险和人工确认边界。
4. Phase 2.11a 最小切口已评审：建议优先选择企业上下文治理增强，而不是 Excel/PPTX ingestion MVP。
5. Phase 2.11a 最小实现边界：project scope / task scope / active document / compare scope / history memory 优先级、evidence source trace、history memory 不得替代本轮 retrieval evidence、上下文污染诊断规则。
6. Phase 2.11a 最小实现已在 Hermes 主仓库完成；Hermes_memory 保持 stateless，未改 retrieval contract。
7. Phase 2.11a 已修复 `history_memory_as_evidence` 语义错误：历史记忆可作为提示，但不得替代本轮 retrieval evidence。
8. Phase 2.11a 真实终端验收已通过：A 锁定、刚才文件延续、A/B 对比均无历史记忆伪 evidence 或第三文件污染。
9. Phase 2.11a 非目标：不实现 Excel/PPTX parser，不实现 OCR/ASR，不推进 facts、权限大改或 rollout。
10. 保留 dirty 声明：Hermes 主仓库 `uv.lock` 不处理；`tests/agent/test_memory_kernel_adapter_reload.py` 作为后续候选回归测试确认。
11. Phase 2.11b 已在 Hermes 主仓库完成 session-level 企业文件别名最小实现：alias 绑定 `document_id`，支持使用与对比；Hermes_memory 继续保持 stateless，不改 retrieval contract。
12. Phase 2.11b 已修复真实终端 alias 绑定路径：绑定在 Hermes 会话层完成，不依赖模型工具；Hermes_memory 侧无需变更。
13. Phase 2.11b 真实终端验收已通过：`@主标书` / `@交付标准` 绑定、使用、对比与 missing alias 抑制均通过；基础信息召回质量尾项不属于 alias 功能失败。
