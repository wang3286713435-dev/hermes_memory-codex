# Hermes Memory 当前待办清单

## 0. 当前 MVP Pilot 状态

1. Phase 2.34 compare false-positive baseline 已完成：Hermes_memory commit `789ed22`，Hermes 主仓库 commit `5de49bf5`，tag `phase-2.34-compare-contamination-baseline`。
2. Phase 2.37 planning baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
3. 当前进入 Phase 2.37a：MVP Pilot issue intake local dry-run，优先把 Day-1 / Codex C / 用户真实试用反馈结构化留痕与分级。
4. Phase 2.37a 不做自动审标、不做 rollout、不写 DB、不自动修复 issue；如果 evidence 不足，必须保留 Missing Evidence。
5. 新增 BIM 数据管家 PRD 扩展规划：先做 BIM 文件资产目录治理，作为后置专项规划线，不并入当前 MVP Pilot。

## 0.1 Phase 2.35 当前待办

1. Codex C 真实终端复验已完成：安全边界通过，但整体仍为 partial。
2. Phase 2.35b 已完成最小修复：API trace 顶层暴露 `metadata_guided_query_profile` / `metadata_deep_field_profile`，Q1/Q2 应可直接核对 `pricing_scope` / `qualification_scope`。
3. 最高投标限价 / 招标控制价 / 投标报价上限：metadata anchor 已要求具体金额 / 货币 / 万元 / 元；如真实标书仍无具体金额，必须继续 Missing Evidence。
4. 投标资质：metadata anchor 已要求具体资质等级 + 类别；证照清单不再强标为资质等级命中。
5. 项目经理、联合体、业绩、人员要求：已有相关 evidence，但仍为 partial，需要 Codex C 继续按 Missing Evidence / 人工复核口径验证。
6. 首次 session alias 绑定后丢失：主仓库 direct assertion diagnostics 未复现，暂作为 terminal-only tail，不能盲目大改。
7. 下一步：补全指定测试复跑后交 Codex B review；通过后由 Codex C 重跑 Day-1 Q1/Q2。

## 0.2 Phase 2.34 历史状态

1. Phase 2.33 Day-1 run sheet baseline 已完成：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`。
2. Codex C Day-1 真实终端验收：`7 pass / 3 partial / 0 fail`，P0 为 `0`，四个 alias 后续解析稳定，无 facts 替代 evidence，无 transcript_as_fact，无实际第三文件污染。
3. 当前建议继续内部受控 Day-1 Pilot，但不得进入 production rollout 或自动经营决策。
4. 当前 Phase 2.34 优先处理 P1：`@会议纪要 vs @主标书` compare 输出层误报 `third_document_mixed=true`。实际 evidence 仅来自两份目标文档，属于 contamination / UX false-positive。
5. 主标书最高投标限价、资质等级、业绩、人员数量等深层字段召回仍为 P1 retrieval recall backlog；本轮不顺手扩大实现。
6. 会议纪要决策 / 公司方向分析长输出延迟为 P2 backlog；本轮不顺手优化。

## 1. Phase 2.1-Qdrant 未确认项

1. Qdrant 是否需要 `QDRANT_API_KEY`、以及 `api-key` header 是否生效尚未确认；当前仅验证了无鉴权的本地容器路径。
2. Dockerfile 依赖 `python:3.11-slim` 拉取在部分网络环境可能超时（docker.io oauth token timeout），导致 `docker compose build api` 失败；若团队主路径依赖容器构建，需准备镜像源/网络策略或提供替代运行方式。

## 2. 暂不推进事项

- production rollout
- repair executor / destructive repair / cleanup / delete
- facts 自动抽取
- facts 替代 retrieval evidence 或 final answer
- 完整 RBAC / ABAC / SSO / 管理后台
- OCR / ASR 全量化
- 全局 rerank rollout / 排序收益大规模优化
- 默认扫描真实 reports / reviews
- TB 级 BIM 原始模型内容全量解析、在线查看器、碰撞检测、自动算量、自动设计审查

说明：上述事项并非长期放弃，而是不进入当前 MVP Pilot / issue intake 阶段。当前已具备 rerank smoke、dense ingestion、facts governance、audit、version governance 与多模态 MVP 的阶段闭环；下一步重点是把真实试用反馈结构化分流，不扩大到 rollout 或自动修复。

## 0.3 BIM 数据管家后置规划

1. PRD 已新增 BIM 数据管家方向：Hermes 初期只管理 BIM 模型文件资产目录、版本、权限、项目归属、检索、引用和后续解析入口。
2. BIM 文件资产目录最小元数据包括项目、楼栋、楼层、专业、模型类型、版本、路径 / 存储位置、文件大小、hash、创建 / 修改时间、责任人和权限标签。
3. 原始模型文件不直接进入 LLM 上下文；Hermes 只保存元数据、派生文本、结构化属性和可追溯链接。
4. 后续可单独规划 `BIM asset catalog planning`，先用少量项目目录试点，不全量处理几个 TB 的模型资产。

## 3. Phase 2.2 后续待办

1. 本节为历史状态归档。Phase 2.2 当时仅完成 `NoopReranker` 与 rerank hook，真实 provider、灰度与质量评测尚未完成。
2. 后续 Phase 2.3-2.8 已完成 rerank 局部默认启用、灰度观察、fail-open 与长期窗口验证。
3. Phase 2.9d 已完成 Aliyun embedding / rerank provider 首轮真调用，其中 rerank 使用 embedding key fallback 调用 `gte-rerank-v2`。
4. Phase 2.17 已完成 Rerank Smoke Audit 与 dense / hybrid eval 扩展，确认真实调用、合理 skipped、latency / fail-open 可观测。
5. 当前保留尾项不是“真实 reranker 未接入”，而是专用 `ALIYUN_RERANK_API_KEY` smoke 与排序收益专项评测；全局 rerank rollout 与排序策略优化继续后置。

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
3. dense ingestion 未接通是 Phase 2.9 时的历史问题；已在 Phase 2.16 修复。当前新上传 dense ingestion、显式 backfill 与 6 文件真实池回填已完成；后续尾项是 eval 覆盖、回填策略治理和环境配置一致性。
4. 高可信度灰度测试已完成阶段补证。Windows + WSL2 高可信验证中，长窗口 `20/20` 成功，OpenSearch timeout / dense_failed_count / sparse_failed_count / 命中漂移 / 后端异常窗口均为 `0`；连续真实工作流 `30` 次 retrieval + `30` 次 agent ask 共 `60/60` 成功，document_id / 标题收敛失败与错误文档命中均为 `0`。该结论支撑 Phase 2.9c 稳定性收口，但仍不等同于生产级全面 rollout。
5. 下一步主线不再继续拆 Phase 2.9c 小轮，建议进入非阻塞尾项收敛：继续扩样验证“投标人须知前附表 / 资格审查 / 合同专用条款 / 工程量清单 / 限价明细”相关真实问法，并补 Aliyun embedding / rerank provider smoke。
6. Phase 2.9c 第一轮与第二轮结构化章节增强已证明方向有效：资质等级门槛、项目经理执业门槛、不平衡报价类查询已能更稳定收敛到“资格后审 / 资格审查文件 / 工程量清单”；付款节点、结算方式、缺陷责任期、质保金、误期赔偿已开始稳定打到“第三章 招标人对招标文件及合同范本的补充/修改”，但仍未证明能稳定命中最理想的合同专用条款 chunk。
7. 总工期 / 关键节点方向已从“明显打不进去”提升到“有提升但仍不稳定”。当前代表性查询能将目标 `工期要求` chunk 拉到 top1，但仍需更多真实问法扩样确认，不应直接宣称稳定够用。
8. 多文件连续切换稳定性已补证。Windows 连续真实工作流中 document_id / 标题收敛失败为 `0`、错误文档命中为 `0`，当前可作为 Phase 2.9c 收口证据。
9. 高可信度灰度证据已补齐到 Phase 2.9c 阶段可接受。Windows 长窗口 wall `p95/p99 = 2397.266 ms / 2596.483 ms`；连续真实工作流 `p95/p99 = 34.935 ms / 40.929 ms`。Aliyun embedding / rerank 当时因缺 secret 未真实调用，该历史尾项已由 Phase 2.9d 首轮真调用承接；当前仅保留专用 `ALIYUN_RERANK_API_KEY` smoke 为可选后置项。
10. 当前仍需继续作为质量尾项扩样的是“前附表 / 工期节点”。合同专用条款方向已开始逼近并出现真实命中提升；“总工期 / 关键节点 / 计划开工日期 / 计划竣工日期”已出现 top 结果改善，但仍未证明所有真实问法都稳定够用。
11. Phase 2.9c 最终收口判断：建议收口。`总工期 / 关键节点` 已从“明显打不进去”提升到“有提升但仍不稳定”，可作为质量尾项继续扩样；高可信机器长窗口与连续真实工作流补证已完成，稳定性阻塞已解除。
12. Phase 2.9c 后续不再继续拆小轮推进。下一阶段建议限定为非阻塞尾项收敛：继续扩样验证 `总工期 / 关键节点` 真实问法，并补 Aliyun embedding / rerank provider smoke；不得误判为生产级全面 rollout。
13. Phase 2.9c 新增兼容性回归修复项已完成：`RetrievalService.search()` 引入 `_infer_document_scope()` 后曾打断 `db=None` 路径，导致 `phase26_rerank_gray_validation.py` 报 `NoneType.query`。当前已在 service 层恢复无 DB 安全返回，并补上 `_database_fallback_search()` 的无 DB 保护；后续仍需持续把无 DB 评估脚本纳入最小回归保护，避免再次误判成环境问题。
14. 总工期 / 关键节点 不再作为 Phase 2.9c 稳定性收口阻塞。本轮增加 schedule 参数短语精确加权后，真实大标书查询已能把 `工期要求` 目标 chunk 提升到 top1，`施工工期 / 合同工期` 定义 chunk 提升到 top2，技术要求进度段落被压到更后；当前判定为“有提升但仍不稳定”，转入后续质量尾项。
15. Windows 高可信灰度补证已完成：长窗口 `20/20` 成功，连续真实工作流 `60/60` 成功；`OpenSearch timeout = 0`、`dense_failed_count = 0`、`sparse_failed_count = 0`、命中集漂移 `0`、后端异常窗口 `0`、document_id / 标题收敛失败 `0`、错误文档命中 `0`。Aliyun embedding / rerank 缺 secret 是当时历史状态，已由 Phase 2.9d provider smoke 首轮真调用补齐；专用 rerank key smoke 仍可选后置。
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
14. Phase 2.11c 已完成规划：优先用轻量 tender metadata snapshot 辅助基础信息召回，再配合 query profile / section boost；snapshot 不替代 evidence。
15. Phase 2.11c 最小实现已完成：Hermes_memory 新增轻量 `tender_metadata_snapshot` 导航，基础信息 query 可锚定工程地点、建设单位、代建单位等来源 chunk；真实大标书复测中三类 query 均返回目标 `document_id`，top1 不再落到第八章工程量清单。
16. Phase 2.11c 真实终端验收已通过：`@主标书` 绑定到 `869d4684-0a98-4825-bc72-ada65c15cfc9`，工程地点 / 建设单位 / 代建单位均由 metadata snapshot 导航到目标 evidence chunk。
17. Phase 2.11c trace 语义已验收：`metadata_snapshot_used=true`、`evidence_required=true`、`snapshot_as_answer=false`，最终答案由 retrieval evidence 支撑，`contamination_flags=[]`。
18. Phase 2.11d 已进入规划：需要用 15 条综合回归 prompt 验证 active document、alias、compare、metadata snapshot、history memory 非 evidence 与 missing alias suppress retrieval 的组合稳定性。
19. Phase 2.11d 新数据需求：第二份大型标书、一份企业制度 / 合同类文件；Hermes_memory 侧需配合确认入库、索引与文件级检索可用。
20. Phase 2.11d 新增文件已完成入库：香港中文大学医学院智能化工程标书 `613` chunks、3-1 数字化交付标准 `20` chunks、会议纪要汇编 `17` chunks，均完成 OpenSearch 索引。
21. Phase 2.11d 综合回归已执行 15/15 通过；当前未发现大标书、交付标准、会议纪要之间的 document scope 污染。
22. Phase 2.11d 非阻塞尾项：multi-document compare 顶层 trace 暂不聚合每份文档的 metadata snapshot 字段；当前不影响 retrieval evidence 与防污染结论。
23. Phase 2.11e 已完成边界规划：PRD / Roadmap / Technical Design 建议单独纳入文档基线，Linear 协作文档单独纳入协作基线，`scripts/run_local_api.sh` 单独纳入 DX 工具，`.run/` 建议删除或忽略，`uv.lock` 保留到依赖治理阶段。
24. Phase 2.11e hygiene 收口：`.run/` 已确认为本地 API 日志与 pid 运行产物并加入 `.gitignore`；`uv.lock` 当前为未跟踪依赖解析产物，暂不纳入提交，后续应单独做依赖治理与 lockfile 策略确认。
25. Phase 2.12 已完成立项评审草案：Excel / PPTX ingestion MVP 应先完成依赖治理与样本确认；实现前需准备 2-3 个真实 Excel 与 2-3 个真实 PPTX，并以 sheet/cell range、slide citation 为最小验收边界。
26. Phase 2.12 前置依赖治理已裁决：`uv lock --check` 通过，`uv.lock` 未发现敏感信息或本地绝对路径，适合作为项目依赖锁定文件纳入基线；后续新增解析依赖必须同步更新 `pyproject.toml` 与 `uv.lock`。
27. Phase 2.12 Excel/PPTX ingestion MVP 已完成首轮最小闭环：3 个 Excel 与 3 个 PPTX 均完成上传、解析、chunk、OpenSearch 索引与带 document_id 的 sparse 检索验证。后续尾项：真实 Hermes 终端验收、图表深层数据还原、图片 OCR、dense ingestion 仍需单独推进。
28. Phase 2.12a Hermes 主仓库 structured citation 消费层已完成最小修复：Excel/PPTX retrieval 结果在 CLI 层可稳定展示结构化 citation；Hermes_memory 本轮无 parser/contract 变更，仅记录阶段联调状态。
29. Phase 2.12 真实终端验收已收口：Excel 文件锁定、Excel 单项检索、PPTX 文件锁定、PPTX 单页信息、跨类型防污染 `5/5` 通过；当前可进入 Git baseline，不再阻塞 Phase 2.12 收口。
30. Phase 2.12 后置 Git 核对完成：Hermes 主仓库 `origin` 是上游 HTTPS 远端，推送失败原因是 GitHub HTTPS 凭证不可读；`backup2` 是当前可写备份远端，Phase 2.12 branch/tag 已在 `backup2` 固化，不需要把 primary remote 对齐混入功能阶段。
31. Phase 2.13 建议优先规划会议纪要 / 转写文本 ingestion MVP：先支持 `.docx` / `.txt` / `.md` 会议资料的 speaker、timestamp、action item、decision、risk 抽取与 citation，不直接进入原始音频 ASR。
32. Phase 2.13 首轮最小实现已完成：复用现有 docx/txt/md parser，新增会议文本 metadata 提取与 retrieval-time 动态补齐；真实样本 `会议纪要汇编 (2)` 未重复上传，行动项 / 决策 / 风险 query 均可命中会议 evidence，主标书查询未被会议 metadata 污染。
33. Phase 2.13 trace 语义已修正：会议纪要可作为 retrieval evidence，但 `transcript_as_fact` 必须恒为 `false`；行动项 / 决策 / 风险不会被误标为已确认 facts。
34. Phase 2.13 真实终端验收已通过：`@主标书` 与 `@会议纪要` 均可绑定，行动项 / 决策 / 风险提取命中会议 evidence；会议纪要与主标书对比无 evidence 混用，会议内容不会被当作招标文件条款引用。
35. Phase 2.14 已完成边界规划：先建设 API-level deterministic regression eval，再补少量 Hermes CLI smoke；覆盖 document scope、alias、compare、metadata snapshot、Excel/PPTX citation、meeting transcript 与 evidence policy。
36. Phase 2.14 最小 API eval runner 已完成：内置 11 条 case，真实本地运行 `10 passed / 0 failed / 1 skipped`；missing alias suppress 保持 CLI-only skipped，后续应补少量 Hermes CLI smoke。
37. Phase 2.14b CLI smoke 已在 Hermes 主仓库收口；Hermes_memory 本轮不改 retrieval contract 或业务代码。真实 runner `4/4` 通过，覆盖 missing alias、session alias bind/use、A/B compare 与 meeting transcript 非 fact 语义。

## 8. Phase 2.15 状态审计与下一阶段路线

1. Phase 2.15 已完成项目状态审计：企业文档检索底座、企业上下文治理、Excel/PPTX、会议纪要文本、API eval、CLI smoke 均已形成阶段闭环。
2. 当前 PRD 核心缺口仍包括：dense ingestion、结构化事实层、权限治理、审计日志、增量更新、知识管理员后台、人工校验机制、完整 OCR / ASR 与生产级 rollout。
3. 推荐下一阶段进入 `Phase 2.16 dense ingestion 与 hybrid 检索闭环补齐`，先让真实上传文件进入 Qdrant dense 索引，再评估权限 / 审计 / facts。

## 9. Phase 2.16 dense ingestion 与 hybrid 闭环待办

1. 已完成新上传文件 dense ingestion 最小实现：chunk 落库后生成 Aliyun `text-embedding-v3` 1024 维向量，并 upsert 到 Qdrant `hermes_chunks`。
2. 已完成 dense fail-open：Qdrant 或 embedding 失败不阻断 PostgreSQL / OpenSearch sparse ingestion，并在 `DocumentVersion.metadata_json.dense_ingestion` 记录状态、成功数、失败数和原因。
3. 已新增显式 backfill 脚本 `scripts/phase216_dense_backfill.py`；脚本必须传入 `--document-id`，不允许默认全库扫描。
4. 已完成 smoke：新上传小文件 sparse + dense 均完成；答疑文件 `1db84714-d49f-48a2-8fa9-c6f73424dd32` dense backfill `12/12` 成功，dense-only retrieval 可返回真实候选。
5. 后续待办：按显式 document_id 分批回填 6 文件真实池 / Excel / PPTX 样本，并复跑 Phase 2.14 API eval 与关键 hybrid smoke。
6. Rerank Smoke Audit 作为非阻塞尾项单独登记：后续需验证 rerank provider 是否启用、真实模型调用是否发生、触发条件、fail-open / latency / error trace 可观测性，以及是否纳入 Phase 2.14 eval 或后续 Phase 2.17 质量评测；本轮 dense ingestion 不混入 rerank 策略修改。
7. Phase 2.16 真实文件池 dense backfill 已完成：6 文件共 `1360` chunks，attempted `1360`、succeeded `1360`、failed `0`；两份大标书分别耗时约 `287.230s` 与 `243.877s`。
8. Phase 2.16 hybrid smoke 已完成：6 文件均 `dense_status=executed`、`sparse_status=executed`，结果 document_id 均收敛到目标文件；Phase 2.14 API eval 复跑 `10 passed / 0 failed / 1 skipped`，`p50/p95=38.416ms/271.507ms`。
9. Phase 2.16 可进入收口判断；后续如继续推进，应优先将 dense/hybrid smoke 结构化纳入评测集，并单独处理 Rerank Smoke Audit。

## 10. Phase 2.17 Rerank Smoke Audit 与 dense/hybrid eval 扩展

1. 当前 rerank 默认仍是关闭状态：`rerank_enabled=false`、`rerank_provider=noop`、`rerank_default_enablement_enabled=false`；真实调用需显式启用 Aliyun provider 与局部默认启用。
2. Rerank 触发条件应保持现有策略：候选数达标、query 命中关键词、request 侧 source_type 或 route_type 命中目标范围；本阶段不改策略。
3. Phase 2.17 已新增 Rerank Smoke Audit runner，覆盖主标书基础信息、主标书工期 / 关键节点、答疑文件、Excel structured query、会议纪要 action/decision/risk；本地 live smoke `5 passed / 0 failed`，其中 3 条 tender query 真实调用 `aliyun_text_rerank`，Excel 与会议纪要按当前策略合理 skipped。
4. Phase 2.17 已扩展 Phase 2.14 eval，增加 `dense_status`、`dense_returned`、`sparse_status`、`candidate_pool` 检查；本地 live eval `11 passed / 0 failed / 1 skipped`，dense/hybrid 链路执行且 returned document_ids 未污染。
5. Phase 2.17 非目标：不调 rerank 策略、不改排序权重、不做 query rewrite、不进入 rollout。
6. 后续尾项：若要判断 rerank 排序收益，需要另起排序质量评测阶段；本阶段只确认真实调用、合理跳过、fail-open 与 dense/hybrid 可观测。

## 11. Phase 2.18 权限与审计路线待办

1. Phase 2.18 已完成路线评审：权限 / 审计的企业落地价值最高，且当前检索、上下文、多模态、dense、rerank、eval 底座已足以支撑最小治理闭环。
2. Phase 2.18a 最小实现已完成：支持 requester / tenant / role placeholder、document ACL metadata placeholder、allow / deny / not_configured_allow policy decision、retrieval trace 与 audit log。
3. 当前 policy 默认行为：无 ACL 本地默认 allow，并标记 `not_configured_allow`；显式 tenant mismatch 或 ACL 不匹配时 deny，且 denied document 不进入 results / evidence。
4. Audit 存储复用现有 `audit_logs` 表；audit 写入失败 fail-open，不阻断 retrieval。
5. Phase 2.18a live smoke 已通过：无 ACL 默认 allow、requester allow、tenant mismatch deny 与三条 audit log 写入均验证通过，测试文档 metadata 已恢复。
6. Phase 2.18a 非目标：不做完整 RBAC/ABAC、不接企业 IAM/SSO、不做管理后台、不做 facts、不做原始音频 ASR、不进入 rollout。
7. 下一步建议做 Git baseline；facts、增量更新 / 版本治理、原始音频 ASR、rerank 质量评测均保留为后续阶段。

## 12. Phase 2.19 增量更新 / 版本治理路线待办

1. Phase 2.19 已完成路线评审：当前应优先做增量更新 / 文档版本治理，而不是直接进入 facts、完整 RBAC/ABAC 或原始音频 ASR。
2. Phase 2.19a 最小实现已完成：同名同类型文件上传复用同一 document，新增 version，旧 version 标记 superseded，新 version 标记 latest/active。
3. Retrieval 默认保持 `is_latest=true`；显式 `version_id` filter 可查询历史版本，并在 trace 输出 `stale_version` 与 `latest_version_id`。
4. Audit log 已记录 evidence `version_ids`；OpenSearch / Qdrant 已补 `version_id` filter 支持。
5. 已修复 live smoke 暴露的 OpenSearch 旧版本泄露风险：supersede 旧版本时按 `document_id + old_version_id` 限定更新 OpenSearch 旧 chunks 的 `is_latest=false`、`status=superseded`、`superseded_by_version_id`。
6. Phase 2.19a live smoke 已复验：默认 sparse / dense-only / hybrid 只返回 latest v2，显式旧 `version_id` 只返回 v1，audit 默认 latest 只记录 v2。
7. 当前非目标：不做复杂 diff、不做完整文档生命周期后台、不做全库重建、不物理删除旧 chunk、不做 facts 主线。
8. 尾项：Hermes 主仓库 alias store 若要绑定 version_id，需要后续联调 stale_version 诊断；审计 eval 纳入 Phase 2.14 可作为配套小任务。
9. Phase 2.19b 已进入 Hermes 主仓库边界规划：alias stale version 联调优先于审计 eval 扩展；Hermes_memory 继续保持现有 retrieval trace，不改 contract。
10. Phase 2.19b 主仓库最小实现已完成并完成 live smoke；Hermes_memory 继续只提供 `version_scope` / `latest_version_id` trace，不新增 contract。

## 13. Phase 2.20 治理类 Eval 扩展

1. Phase 2.20 已完成边界规划：将 access policy、audit log、version latest/default filtering、explicit historical version query、deny evidence 防泄露与 audit `evidence_version_ids` 纳入 API deterministic eval。
2. Alias stale version 属于 Hermes session layer，不纳入 Hermes_memory stateless API eval；后续应通过 Hermes CLI smoke 覆盖 `alias_stale_version`、`latest_version_id` 与 compare 一侧 stale 的用户侧诊断。
3. Phase 2.20a 最小实现建议：扩展 `scripts/phase214_regression_eval.py` 增加 governance case group，并在 Hermes 主仓库补少量 alias stale CLI smoke。
4. Phase 2.20 非目标：不做完整 RBAC/ABAC、不做复杂 diff、不做 facts、不进入 rollout、不改 retrieval contract、不改 memory kernel 主架构。
5. Phase 2.20a 最小实现已完成：Hermes_memory API eval 新增 `governance` group，5 条治理 case live 运行 `5 passed / 0 failed / 0 skipped`；主仓库 CLI smoke 新增 stale alias case，live runner `5 passed / 0 failed / 0 skipped`。
6. Phase 2.20a full eval 已复跑通过：`16 passed / 0 failed / 1 skipped`，`p50/p95=11.146ms/539.376ms`。
7. 环境注意事项：dense / hybrid eval 必须使用 `QDRANT_COLLECTION=hermes_chunks`；若本机 ignored `.env` 指向旧 `hermes_gate_chunks`，会造成 core dense `dense_returned=0` 假失败。
8. 本轮未回填、未放宽 eval 断言、未改治理功能；`missing_alias_suppress_cli_only` 继续由 CLI smoke 覆盖。

## 14. Phase 2.21 facts 路线裁决

1. Phase 2.21 已完成候选路线评审：增量治理、facts、原始音频 ASR、完整 RBAC/ABAC、生产级 rollout 均仍有价值，但下一阶段建议优先进入结构化 facts 最小闭环。
2. 推荐 Phase 2.21a 的原因：当前 retrieval evidence、version_id、access/audit 与 eval 已具备 facts 的可信来源基础，适合从文档检索助手推进到企业长期记忆系统。
3. Phase 2.21a 最小 facts 必须包含 `fact_type`、`subject`、`predicate`、`value`、`source_document_id`、`source_version_id`、`source_chunk_id`、`confidence`、`verification_status`、`created_by`、`confirmed_by`、`audit_event_id`。
4. facts 必须来源于 retrieval evidence + version_id + audit；未经人工确认或显式确认的 facts 必须标记 `unverified`，不得当作已确认企业事实使用。
5. Phase 2.21a 非目标：不自动把所有文档转 facts、不做复杂知识图谱、不做自动决策、不进入 rollout、不改 retrieval contract、不改 memory kernel 主架构。
6. Phase 2.21a 最小实现已完成：新增 evidence-backed facts service/API，创建 fact 必须绑定 source chunk，并保留 source document/version/chunk、confidence、verification_status、created_by、confirmed_by、audit_event_id。
7. Phase 2.21a live smoke 已通过：会议纪要 action item 与主标书建设单位各创建 1 条 `unverified` fact，by document / by subject 查询均能返回来源字段。
8. 后续尾项：facts 暂不参与 answer generation；如要进入真实业务，应先补 facts eval、权限过滤查询、人工确认工作流和 stale source 处理策略。

## 15. Phase 2.21b facts governance 待办

1. Phase 2.21b 已完成边界规划：优先推进 facts eval、facts 查询权限过滤与人工确认工作流的最小闭环。
2. facts eval 应纳入 Phase 2.14 deterministic eval，覆盖 source document/version/chunk、默认 unverified、confirm/reject 状态流转与 stale source version 诊断。
3. facts 查询权限过滤应继承 source document ACL / tenant soft policy；deny 后不得返回 fact，也不得泄露 source evidence。
4. facts query audit 应记录 requester、tenant、returned_fact_ids、denied_fact_ids、source_document_ids 与 policy_decision。
5. 人工确认工作流先限定为 `unverified -> confirmed/rejected`，不做 UI 管理后台。
6. 当前明确不做 facts 参与回答生成，不做自动全量 facts 抽取，不做知识图谱或 rollout。
7. Phase 2.21b 第一阶段已完成 facts eval：Phase 2.14 runner 新增 `facts` group，5 条 facts case 覆盖来源字段、默认 unverified、confirmed/rejected 与 stale source version。
8. 当前 live eval 结果：facts group `5 passed / 0 failed / 0 skipped`，full Phase 2.14 eval `21 passed / 0 failed / 1 skipped`。
9. 后续仍需实现 facts 查询权限过滤、fact query audit 与人工确认工作流字段增强。
10. Phase 2.21b 第二阶段已完成 facts 查询权限过滤与 fact query audit：facts 查询继承 source document 的 tenant / requester / role soft policy，deny 后不返回 fact。
11. facts query audit 已记录 requester、tenant、role、filter、returned_fact_ids、denied_fact_ids、source_document_ids 与 policy_decision；audit 写入失败 fail-open。
12. 当前仍未完成：facts 权限 eval 纳入 deterministic eval、facts 是否参与回答生成的独立设计。
13. Phase 2.21b 第三阶段已完成人工确认工作流字段增强：新增 confirmed_at、rejected_by、rejected_at、rejection_reason，confirm/reject 均写入 audit。
14. `confirm_fact` 不允许缺失确认人；`reject_fact` 不允许缺失拒绝人，缺失 rejection_reason 时默认写入 `not_specified`。
15. Phase 2.21b 三项最小目标已完成，建议在 Git baseline 后收口；facts 参与回答生成、自动抽取、复杂知识图谱仍后置。

## 16. Phase 2.22 facts 使用路线裁决

1. Phase 2.22 已完成路线评审：不建议立即让 confirmed facts 参与回答生成，也不建议自动 facts 抽取。
2. 推荐下一阶段进入 `Phase 2.22a facts 管理 / 确认工作流增强`。
3. 最小边界：按 verification_status / pending / document / project / subject 查询 facts，并返回 confirm / reject audit history。
4. facts 查询仍需继承 source document soft policy，不得绕过权限过滤。
5. 非目标：不做 Agent 回答引用 facts、不做自动抽取、不做知识图谱、不做 UI 管理后台、不进入 rollout。
6. Phase 2.22a 最小实现已完成：新增 facts 管理列表、pending 列表、confirm/reject review history 查询。
7. 管理列表支持按 verification_status、source_document_id、source_version_id、subject、fact_type、created_by、confirmed_by 过滤。
8. 管理查询继续继承 source document soft policy，deny 后不返回 fact；`fact.query` audit 写入失败仍 fail-open。
9. 当前仍未做：facts 参与回答生成、自动 facts 抽取、复杂知识图谱、UI 管理后台与 rollout。

## 17. Phase 2.23 confirmed facts 使用路线裁决

1. Phase 2.23 已完成路线评审：不建议直接让 confirmed facts 参与 Agent 回答生成，也不建议自动 facts 抽取。
2. 推荐下一阶段进入 `Phase 2.23a confirmed facts 只读检索 / 引用展示`。
3. 最小边界：list / search confirmed facts，并回链 source_document_id、source_version_id、source_chunk_id。
4. confirmed facts 查询必须继承 source document soft policy，并记录 fact.read / fact.query audit。
5. `stale_source_version` 必须可见；confirmed fact 不替代 retrieval evidence，不进入 Agent final answer。
6. 非目标：不做自动抽取、不做复杂知识图谱、不做 UI 管理后台、不进入 rollout。
7. Phase 2.23a 最小实现已完成：新增 `GET /api/v1/facts/confirmed` 与 service 层 `search_confirmed_facts`。
8. confirmed facts 查询支持 subject、predicate、fact_type、source_document_id、source_version_id 过滤，并返回 source_excerpt / source_location。
9. confirmed facts 查询写入 `fact.search` audit；source document soft policy deny 后仍不返回 fact。
10. 当前仍未做：facts 进入 Agent final answer、自动抽取、知识图谱、UI 管理后台与 rollout。

## 18. Phase 2.24 facts 进入 Agent 上下文路线裁决

1. Phase 2.24 已完成路线评审：建议 confirmed facts 先作为 Agent 辅助上下文，而不是直接进入 final answer。
2. 推荐下一阶段进入 `Phase 2.24a confirmed facts 辅助上下文`。
3. 最小边界：仅 confirmed facts 可进入 context，trace 必须包含 `facts_context_used=true` 与 `facts_as_answer=false`。
4. 每条 fact 必须显示 source_document_id、source_version_id、source_chunk_id；stale_source_version 必须明确提示。
5. facts 查询继续继承 source document soft policy，audit 记录 `facts_context_fact_ids`。
6. 非目标：不自动抽取 facts、不让 facts 替代 retrieval evidence、不做知识图谱、不做 UI、不进入 rollout。
7. Phase 2.24a 最小实现已完成在 Hermes 主仓库消费层；Hermes_memory 继续提供 confirmed facts 查询、权限过滤、source citation 与 stale source 诊断。
8. live smoke 已验证 confirmed facts 辅助上下文、stale source warning、无 retrieval evidence 时 suppress；`facts_as_answer=false` 保持不变。
9. 终端验收修复已完成：facts context 独立分区，meeting transcript 不再被标记为 facts，`stale fact source` query 可输出 `stale_fact_source_count` 与 `latest_version_id`。
10. 二次修复已完成：无作用域 stale / fact-answer policy query 抑制普通 retrieval，避免无关文档污染 facts 诊断。
11. alias 绑定 / retrieval-only 场景已稳定输出 facts false / [] / false 诊断，避免模型把 retrieval chunks 写成 fact ids。
12. Codex C 真实终端复验已通过：`@会议纪要` 绑定稳定，5 条正式验收全过，stale fact 检出，`facts_as_answer` 全场景为 false。
13. 复验未出现 E/C chunks 写入 `facts_context_fact_ids`、fact-only query 检索无关文档或 facts 替代 retrieval evidence。
14. 复验注意：`@会议纪要` 必须在同一会话内先绑定，避免新会话 alias_missing。
15. 当前仍未做：facts 进入 Agent final answer、自动抽取、知识图谱、UI 管理后台与 rollout。

## 19. Phase 2.25 项目状态审计与下一阶段路线裁决

1. Phase 2.25 已完成路线评审：当前 Hermes_memory 处于企业长期记忆底座 MVP 后段，核心检索、上下文、治理、facts 与评测均已有最小闭环。
2. 当前不建议直接进入生产 rollout、facts 自动抽取、facts 更深层 Agent reasoning、管理后台或 OCR / 原始音频 ASR。
3. 推荐下一阶段进入 `Phase 2.25a Enterprise Readiness Audit + 数据维护诊断小工具`。
4. Phase 2.25a 最小边界：环境配置、migration、索引健康、API 健康、eval 入口、备份恢复清单的 readiness audit / smoke。
5. 数据维护诊断建议只做 dry-run：重复 / 近似同名 document、latest/superseded 状态、OpenSearch/Qdrant count、一致性和 stale facts 检查。
6. 非目标：不自动修复、不默认全库重写、不做物理删除、不自动确认 facts、不改 retrieval contract 或 memory kernel 主架构。

## 20. Phase 2.25a readiness audit / 数据维护诊断

1. 已新增 `scripts/phase225_readiness_audit.py`，默认 dry-run，只输出诊断 JSON，不修改任何业务数据。
2. 已覆盖服务健康、版本治理、OpenSearch 一致性、Qdrant dense 一致性、facts 治理、audit logs 与 eval readiness。
3. `destructive_actions` 固定为空；light eval 默认不执行，避免 Phase 2.14 fixture 写入破坏只读语义。
4. 单元测试已覆盖 summary 聚合、warning/fail 判定、Qdrant collection 错误诊断与 stale facts 格式。
5. 本机默认 `.env` 指向容器主机名时会清晰失败；本机直跑需覆写 `DATABASE_URL` / `OPENSEARCH_URL` / `QDRANT_URL` / `QDRANT_COLLECTION`。
6. 使用 127.0.0.1 覆写后 live dry-run 结果为 `status=warn`，`22 passed / 1 warning / 0 failed`；warning 为已知 stale confirmed fact。
7. 后续可考虑 Git baseline，并将该 runner 纳入定期 smoke；当前仍不进入生产 rollout。

## 21. Phase 2.26 stale facts / 数据一致性 repair plan dry-run

1. Phase 2.26 已完成边界规划：下一步优先做 repair plan dry-run，而不是直接修复数据。
2. Phase 2.26a 建议新增只读脚本 `scripts/phase226_repair_plan_dry_run.py`，输出结构化 repair plan。
3. 覆盖项：stale confirmed facts、source missing facts、version index inconsistency、duplicate / near-duplicate documents 初步诊断、audit gap 说明。
4. 所有 plan item 必须 `executable=false`；全局 `dry_run=true` 且 `destructive_actions=[]`。
5. 默认 recommended_action 必须保守：`keep_with_warning`、`revalidate_against_latest`、`mark_needs_review`、`reject_if_source_missing`、`reindex_version_payload`、`rerun_dense_backfill`。
6. 硬边界：不修改 facts、document_versions、OpenSearch、Qdrant，不删除数据，不自动确认 facts，不执行 repair。
7. Phase 2.26b 或后续再考虑 readiness audit 定期 smoke / 报告归档；自动 repair 必须等 dry-run 稳定并经过人工确认。
8. Phase 2.26a 最小实现已完成：新增 repair plan dry-run runner 与 6 条单元测试，输出只读 JSON plan。
9. live dry-run 已检出已知 stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`，无 critical failure。
10. 当前仍不执行 repair / reindex / backfill；下一步可做 Git baseline 后规划人工审核或定期报告。

## 22. Phase 2.26b readiness audit 报告归档规划

1. Phase 2.26b 已完成路线规划：下一步建议做 readiness audit / repair plan dry-run 报告归档，而不是 repair executor。
2. 最小边界：保存 readiness JSON、repair plan JSON，生成 manifest，并支持只读 trend diff。
3. 报告文件名应包含 timestamp、status、git commit，便于人工追踪。
4. 真实 `reports/**/*.json` 与 `latest.json` 默认不提交 Git；如需目录结构，只提交 README / `.gitkeep` / `.gitignore` 策略。
5. 默认不使用 symlink；最新报告指针优先规划为 ignored 的 `latest.json`。
6. 不创建系统 cron，不接生产 scheduler，不默认跑昂贵 full eval，不触发写 fixture 的 eval。
7. 硬边界：不修改 facts、document_versions、OpenSearch、Qdrant，不执行 repair/backfill/reindex，不进入 rollout。
8. 后续实现前需优先明确 reports 目录 ignore 策略与 fake report 单元测试。
9. Phase 2.26b 最小实现已完成：新增报告归档脚本、trend diff、reports ignore 策略与 6 条单元测试。
10. live smoke 已在临时目录归档 fake readiness / repair plan JSON，并生成 manifest/latest；未生成真实仓库 reports JSON。
11. 下一步建议先做 Git baseline，再规划定期 smoke runbook 或报告人工审阅流程；仍不进入 repair executor。

## 23. Phase 2.27 report review workflow 规划

1. Phase 2.27 已完成路线规划：下一步建议做 report-level 与 repair item-level 人工审阅流。
2. Phase 2.27a 最小边界：review record schema、item decision schema、本地 JSON / Markdown 记录、report path/hash 绑定。
3. report 状态建议包含 `pending_review`、`approved_for_manual_action`、`rejected`、`acknowledged`。
4. item decision 建议包含 `needs_review`、`approved`、`rejected`、`deferred`。
5. `approved` / `approved_for_manual_action` 不等于 executed；所有 review record 与 item decision 均必须 `executable=false`。
6. 真实 `reports/reviews/**/*.json` 与 review markdown 默认不入 Git；只提交模板、README 或 ignore 策略。
7. audit_logs 集成后置到 Phase 2.27b；repair executor 继续后置。
8. 硬边界：不写业务 DB，不修改 facts / versions / indexes，不执行 repair，不进入 rollout。
9. Phase 2.27a 最小实现已完成：新增本地 review record 脚本、item decision skeleton、reviews ignore 策略与 7 条单元测试。
10. live smoke 已在临时目录完成 dry-run-preview 与 tmp review JSON 写入；真实仓库未生成 review record。
11. 下一步建议先做 Git baseline，再评估 Phase 2.27b 是否规划 audit_logs 集成；repair executor 继续后置。

## 24. Phase 2.27b review audit 路线规划

1. Phase 2.27b 已完成路线规划：建议先做 report-level audit summary preview，而不是直接写 `audit_logs`。
2. 推荐最小边界：读取 review record，输出 sanitized audit payload，保持 dry-run，不写业务 DB。
3. 建议 event_type：`report.review.created`，后续可扩展到 acknowledged / approved_for_manual_action / rejected。
4. audit payload 可包含 report_hash、report_type、review_status、reviewer、reviewed_at、summary counts、`executable=false`。
5. 必须排除 notes、reason、approved_action、完整 item_decisions、report 原文和本机绝对路径。
6. item-level audit summary 后置，完整 review record 入 audit 不推荐。
7. 真实写 `audit_logs` 在 Phase 2.27b 时仍后置；该项已由 Phase 2.27d 独立阶段承接为显式 `--write-audit` opt-in 最小实现。
8. repair executor 继续后置，`approved_for_manual_action` 仍不等于 executed。
9. Phase 2.27b 最小实现已完成：新增 sanitized audit payload preview runner，读取本地 review record，只输出 report-level audit summary。
10. preview payload 固定 `dry_run=true`、`executable=false`、`would_write_audit_logs=false`，不写 DB、不写 audit_logs。
11. 已通过单元测试与临时目录 live smoke，确认 notes、reason、approved_action、完整 item_decisions、本机绝对路径和 item-level entity details 不进入 payload。
12. Phase 2.27b preview 不等于已写审计；后续 Phase 2.27d 已实现 report-level sanitized audit 的显式 `--write-audit` opt-in，仍不包含 item-level audit、完整 review record 入库或 repair 执行。
13. 本轮按 `NEXT_CODEX_A_PROMPT.md` 完成实现；未启用 Nightly Sprint，未提交 Git。

## 25. Phase 2.28 Agent Operating Protocol / 文件化交接机制

1. Phase 2.28 已新增 Codex A/B/C 文件化协作协议：`docs/AGENT_OPERATING_PROTOCOL.md`。
2. Codex A 每轮开始必须读取 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG、ACTIVE_PHASE、PHASE_BACKLOG。
3. Codex A 每轮结束必须更新 ACTIVE_PHASE、HANDOFF_LOG、`reports/agent_runs/latest.json`。
4. Codex B 负责读取交接文件、监督是否偏离 PRD / Roadmap / Phase 文档，并给下一轮 prompt。
5. Codex C 负责真实终端验收和 live smoke，不默认承担主实现。
6. `reports/agent_runs/latest.json` 是本地状态文件，默认 ignored，不入 Git。
7. `AGENT_OPERATING_PROTOCOL.md`、`ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、`PHASE_BACKLOG.md` 可作为协作基线提交。
8. 硬停止条件已文档化：真实数据 mutation、repair/delete/cleanup、rollout、contract rewrite、主架构改动、facts 替代 evidence、生产 cron 等均需停止。
9. 下一步建议先做 Phase 2.28 协作协议 baseline，再进入 Phase 2.27b audit preview 实现。
10. Phase 2.28b 已新增 `docs/NEXT_CODEX_A_PROMPT.md` 作为 Codex A 固定任务入口，后续用户可只要求执行该文件。
11. `NEXT_CODEX_A_PROMPT.md` 当前写入 Phase 2.27b sanitized audit payload preview / dry-run 完整任务；本轮不创建脚本、不写测试、不进入实现。
12. `reports/agent_runs/latest.json` 继续作为 ignored 本地状态文件，不入 Git。
13. Phase 2.28c 已新增 Nightly Sprint Protocol 与 Queue，允许夜间仅执行 bounded Green Lane 任务。
14. Nightly Sprint 初始队列：Phase 2.27b audit preview / dry-run、Phase 2.27b baseline、Phase 2.27c route planning。
15. Yellow Lane 完成后必须停止等待 Codex B；Red Lane 夜间禁止，包括 repair executor、migration、rollout、facts 自动抽取、contract / 主架构修改与生产 cron。
16. `reports/nightly_runs/*.json` 是 ignored 本地状态文件，不入 Git；只提交 README / `.gitignore` 策略。

## 26. Phase 2.27c review audit write 路线规划

1. Phase 2.27c 已通过 Nightly Sprint Green Lane 完成路线规划：评审是否将 report review 事件真实写入 `audit_logs`。
2. 当前建议：可以进入后续最小实现，但仅限 report-level sanitized audit 写入；默认仍保持 preview-only。
3. 后续实现必须显式 opt-in，例如 `--write-audit`；不得在夜间自动执行真实 DB 写入。
4. audit payload 只能包含 review_id、report_hash、report_type、review_status、reviewer、reviewed_at、summary counts 与 `executable=false`。
5. 必须继续排除 notes、reason、approved_action、完整 item_decisions、本机绝对路径和 fact_id / document_id 等 item-level entity details。
6. `approved_for_manual_action` 仍不等于 executed；repair executor、item-level audit summary、完整 review record 入库继续后置。
7. 下一阶段候选：`Phase 2.27d report-level review audit write MVP`，但属于 Yellow Lane，必须等待 Codex B 审核与用户显式授权。

## 27. Phase 2.27d report-level review audit write MVP

1. Phase 2.27d 已完成最小实现：review audit preview 默认不写 DB，仅在显式 `--write-audit` 时写入 report-level sanitized `audit_logs`。
2. 写入事件限定为 `report.review.created`，并继续保留 `executable=false` 与 `approved_for_manual_action` 不等于 executed 的语义。
3. `notes`、`reason`、`approved_action`、完整 `item_decisions`、本机绝对路径、item-level entity details 与 `executed` 字段继续硬排除。
4. audit 写入失败 fail-open 并返回 warning；本阶段不扩大 schema，不写 item-level audit，不写完整 review record。
5. 测试结果：py_compile 通过，`tests/test_phase227b_review_audit_preview.py` 共 `15 passed`。
6. live smoke 使用临时 SQLite DB 写入 `1` 条 sanitized audit event；未写生产 / 真实业务 DB。
7. 下一步建议进入 Phase 2.27d Git baseline；baseline 后再评审是否需要把 report review audit 纳入 readiness / eval。
8. repair executor、repair 执行、rollout、真实数据修改继续后置并禁止自动推进。

## 28. Phase 2.27e review audit eval / readiness 规划

1. Phase 2.27e 已完成路线规划：建议优先把 report review audit 安全断言纳入 deterministic eval / unit test。
2. readiness audit 可增加只读检查：近期是否存在 `report.review.created` event，以及是否只统计 report-level sanitized audit。
3. `--write-audit` 的验证应使用临时 SQLite / fixture DB，不触碰真实企业 DB。
4. archive / review / audit 三者关联诊断可作为第二优先级，只使用 hash / id，不写本机路径或 item-level entity details。
5. item-level audit summary、完整 review record 入库、repair executor 与 rollout 继续后置。
6. 后续最小实现不得修改 facts、document_versions、OpenSearch、Qdrant，不得执行 repair/backfill/reindex/cleanup/delete。
7. Phase 2.27e 最小实现已完成：readiness audit 新增只读 `report.review.created` sanitized summary 检查，缺失事件为 warning，unsafe payload 为 fail；相关单测与只读 smoke 已通过。

## 29. Phase 2.27f archive / review / audit 关联诊断规划

1. Phase 2.27f 已完成路线规划：建议下一步只做 archive / review / audit 三者只读关联诊断。
2. 最小边界：用 `report_hash` / `report_type` 关联 archived report 与 review record，用 `review_id` / `trace_id=report_review:<review_id>` 关联 review record 与 audit event。
3. 输出只读 summary，缺少 archive / review / audit 任一环节时为 warning，不自动 fail。
4. 诊断输出不得包含 report 原文、本机绝对路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。
5. 第一轮实现不建议直接纳入 readiness audit 默认扫描；可后续显式参数化接入。
6. item-level / repair-level linkage、repair executor、真实 DB 写入与 rollout 继续后置。
7. Phase 2.27f planning 已进入 baseline，下一步只建议在 Codex B 审核后实现只读 linkage summary。
8. Phase 2.27f 最小实现已完成：新增只读 linkage summary runner 与 9 条单元测试，临时目录 smoke 覆盖 pass / missing audit warn / unsafe audit fail；未写 DB、未写 `audit_logs`、未执行 repair。
9. Phase 2.27f 安全补丁已完成：audit event 顶层 unsafe 字段与绝对路径现在会 fail；目标测试 12 passed，临时 smoke 覆盖 unsafe top-level fail。

## 30. Phase 2.27g linkage readiness route planning

1. Phase 2.27g 已完成路线规划：评审 linkage summary 是否显式参数化接入 readiness audit。
2. 推荐路线为 B + D：后续如需要代码衔接，仅做显式参数读取 linkage summary；同时在 Phase 2.29 MVP readiness freeze 中列为人工验收项。
3. 不推荐默认扫描 `reports/` / `reviews/` / audit records，避免读取本机路径、notes、reason、完整 item_decisions 或 item-level entity details。
4. 不推荐继续追加新的 Phase 2.27x 实现；优先在 Phase 2.27g baseline 后进入 Phase 2.29 readiness freeze planning。
5. repair executor、rollout、真实 DB 写入、item-level linkage 与默认目录扫描继续后置。
6. Phase 2.27g planning baseline 已准备收口：本阶段只提交规划与交接文件，不写代码、不写 DB、不改 readiness runner。

## 31. Phase 2.29 MVP readiness freeze planning

1. Phase 2.29 已完成路线规划：当前进入 MVP readiness freeze，而不是继续补新功能或进入 rollout。
2. 已梳理候选 MVP 能力清单、必须复跑验证项、人工验收项与 Go/No-Go 判定标准。
3. 推荐下一步仅进入 Phase 2.29a：freeze checklist / freeze report dry-run，不进入 repair executor、production rollout 或新一轮能力扩展。
4. facts 继续保持 auxiliary context / read-only 边界，`facts_as_answer=false` 不可放松。
5. linkage summary、review audit、readiness audit 继续作为 freeze 证据链的一部分，但不默认扫描真实 reports / reviews。
6. Phase 2.29 planning baseline 收口后，下一轮入口切换为 Phase 2.29a freeze checklist / freeze report dry-run。

## 32. Phase 2.29a freeze report dry-run

1. Phase 2.29a 已新增只读 freeze report dry-run runner。
2. runner 仅读取显式传入的 JSON 证据，不默认扫描真实 reports / reviews，不默认运行 full eval。
3. 输出固定保留 `dry_run=true`、`destructive_actions=[]`、`rollout_ready=false`、`production_rollout=false`、`repair_executed=false`。
4. 目标测试 `8 passed`，临时目录 smoke 通过。
5. 下一步建议 Codex B review 后执行 Phase 2.29a Git baseline。
6. Phase 2.29a baseline 收口后，下一步进入 Phase 2.29b readiness freeze baseline decision planning。

## 33. Phase 2.29b readiness freeze baseline decision planning

1. Phase 2.29b 已完成路线规划：只生成 readiness freeze decision record，不执行 rollout、repair 或 DB mutation。
2. `pass` 可进入 MVP freeze candidate 评审，但仍不等于 production ready。
3. `warn` 不自动进入 MVP candidate，必须人工确认或补充证据。
4. `fail` 必须 No-Go。
5. No-Go 条件包括 production rollout、repair executor、facts 替代 retrieval evidence、默认扫描真实 reports/reviews、真实 DB mutation。
6. 下一步建议进入 Phase 2.29b 最小实现：读取显式 freeze report JSON，输出 decision record / no-go reasons。
7. Phase 2.29b planning baseline 后，下一轮入口切换为 decision record dry-run 最小实现。

## 34. Phase 2.29b decision record dry-run

1. Phase 2.29b 最小实现已完成：新增 `scripts/phase229b_freeze_decision_dry_run.py` 与目标测试。
2. runner 只读取显式 freeze report JSON，不默认扫描真实 reports / reviews，不写 DB。
3. `pass` 映射为 `approved_for_mvp_freeze_candidate`；`warn` 映射为 `needs_manual_review`；`fail` 映射为 `no_go`。
4. `production_rollout=true`、`repair_executed=true` 或非空 `destructive_actions` 会强制 No-Go。
5. 输出恒定保留 `dry_run=true`、`production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`。
6. 验证结果：py_compile 通过，目标 pytest `8 passed`，临时目录 pass / warn / fail dry-run smoke 通过。
7. 下一步建议 Codex B review 后进入 Phase 2.29b Git baseline；production rollout 与 repair executor 继续后置。
8. Phase 2.29b Git baseline 已准备收口：提交范围限定为 decision dry-run runner、测试与阶段文档；不提交 ignored `latest.json` 或真实 reports / reviews 产物。

## 35. Phase 2.29d release candidate checklist planning

1. Phase 2.29d 已完成路线规划：只规划 MVP freeze candidate 人工复核与 release candidate checklist，不进入 production rollout。
2. MVP freeze candidate 被限定为“可人工审阅的候选状态”，不等于 production ready、repair approved 或 facts 可替代 retrieval evidence。
3. release candidate checklist 草案已覆盖 evidence completeness、safety invariants、data governance、sign-off fields 与 Go / No-Go 条件。
4. Codex B 审核重点：freeze report / decision record 状态、warnings、`production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`、`facts_as_answer=false` 与 sanitized linkage。
5. Codex C 仅在后续需要声明“真实 Hermes 终端 MVP candidate 已通过”时做抽样复验；Phase 2.29d planning 本身不需要 live terminal 验收。
6. 当前 known risks 必须继续保留：stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`、soft policy 非完整 RBAC/ABAC、专用 `ALIYUN_RERANK_API_KEY` smoke 可选尾项、facts 不得作为 final answer。
7. 下一步建议先做 Phase 2.29d planning Git baseline；baseline 后再由 Codex B 决定是否进入 Phase 2.29e checklist dry-run 最小实现。

## 36. Phase 2.30a practical MVP pilot pack

1. Phase 2.30a 已整理内部受控 MVP Pilot Pack，目标是支持标书审查、企业文件内容提取、公司未来发展方向辅助分析三类真实使用。
2. MVP 被限定为人工监督的内部试运行版本，不等于 production rollout、自动审标、自动经营决策或 repair executor。
3. 新增 playbook 要求所有结论必须带 retrieval evidence / citation；无 evidence 时必须明确缺失，不得凭 facts 或历史记忆作答。
4. 标书审查模板覆盖项目基础信息、投标资格、商务 / 合同风险、缺失信息识别，并要求输出风险等级与待人工确认项。
5. 文件提取模板覆盖标书 / Word / PDF、Excel sheet/cell、PPTX slide、会议纪要 action / decision / risk、A/B compare 防污染。
6. 发展方向分析模板强制 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分离，并标明“辅助建议，需人工决策”。
7. Pilot 验收清单包含 12 条真实终端 query，建议 Codex C 做抽样验收；本轮未写代码、脚本或测试。
8. Phase 2.30b 已完成 alias/session 最小修复：标题类 alias bind resolver 未命中时允许同轮 retrieval fallback，再由唯一检索文档完成绑定。
9. Phase 2.30b 已通过 Codex C 真实终端复验：12 条 Pilot query 为 `10/12 pass, 2/12 partial, 0 failed`，alias/session 修复有效。
10. Phase 2.30b follow-up 已补齐 runbook 原文 alias 绑定：`把会议纪要文件设为 @会议纪要`、`把硬件清单设为 @硬件清单`、`把C塔方案设为 @C塔方案`、`把当前主标书设为 @主标书`、`把当前标书设为 @主标书`。
11. 下一步建议先做 Phase 2.30a / 2.30b Git baseline，再进入 Phase 2.31 内部受控 MVP Pilot 试用操作规划。
12. 已知试用风险：深层字段召回仍需人工复核，经营建议必须人工决策，当前不进入 production rollout。

## 37. Phase 2.31 internal controlled MVP Pilot operations

1. Phase 2.31 已完成 docs-only planning，新增内部受控 MVP Pilot 操作规划、使用者指南、反馈模板与 known risk checklist。
2. Pilot 范围限定为标书审查 / 风险提取、企业文件内容提取与 citation 定位、公司未来发展方向辅助分析。
3. Pilot 明确不覆盖 production rollout、自动审标定论、自动经营决策、repair executor、facts 自动抽取或 facts 替代 retrieval evidence。
4. 每次试用必须检查 `/health`、建立 Hermes CLI session、绑定 `@主标书` / `@会议纪要` / `@硬件清单` / `@C塔方案`，并保存输出。
5. 人工复核必须检查 document_id / version_id、citation、`facts_as_answer=false`、`transcript_as_fact=false`、contamination_flags 与 Missing Evidence。
6. 最高投标限价、业绩要求、付款节点、工期节点、质保 / 违约等深层字段仍需人工复核。
7. 经营建议只能作为辅助建议，必须人工决策；无 evidence 的内容必须进入 Missing Evidence 或 Assumption。
8. 下一步建议 Codex B review Phase 2.31 文档；通过后再做文档 baseline，不自动进入 production rollout。
9. Codex B review 已确认 Phase 2.31 文档方向可进入 docs baseline。
10. 已补充 `docs/NIGHTLY_CODEX_A_PROMPT.md`，明确 Nightly Sprint 需要 Codex A 会话被启动，Markdown 本身不会自动运行。
11. `NIGHTLY_SPRINT_QUEUE.md` 已从“等待 B review 无可执行项”调整为：Item 1 docs-only baseline，Item 2 Phase 2.32 feedback intake planning。

## 38. Phase 2.32 MVP Pilot feedback intake

1. Phase 2.32 已完成 docs-only planning，新增 MVP Pilot feedback intake / triage loop。
2. 反馈来源限定为 feedback template、真实 Hermes 输出、人工复核结论、Codex C 复验记录与业务影响说明。
3. triage 字段覆盖场景、query、期望 / 实际、pass / partial / fail、document_id / version_id、citation、问题类型、业务影响、优先级、是否需要 Codex C、是否需要新 phase。
4. 已定义问题类型：alias/session、retrieval recall、citation、contamination、facts boundary、transcript boundary、UX / prompt、latency / runtime、environment、other。
5. 已定义 P0/P1/P2/P3：P0 包括 facts 替代 evidence、transcript 误作 fact、compare 第三文件污染、无 citation 确定结论、alias/session 大面积失效。
6. 已定义 Go / No-Go：P0 为 0 且 P1 可人工规避时可继续试用；任一 P0 或连续未解释 fail 应暂停或降级。
7. 当前不自动修复、不自动写 DB、不自动创建 Linear / GitHub issue、不进入 rollout。
8. 下一步建议 Codex B review Phase 2.32 文档；通过后再做 docs-only baseline。
9. Phase 2.32 docs-only baseline 已完成：commit `160ce62`，tag `phase-2.32-feedback-intake-plan-baseline`。
10. 下一步建议 Phase 2.33：整理 Day-1 run sheet 与最小 query set，让内部试用可以直接执行。

## 39. Phase 2.33 MVP Pilot Day-1 execution packet

1. Phase 2.33 已完成 docs-only planning，新增 `docs/MVP_PILOT_DAY1_RUN_SHEET.md`。
2. Day-1 run sheet 覆盖目标 / 非目标、角色、时间表、环境检查、alias 绑定、最小 query set、输出保存规则、人工复核、问题分级与 Go / Pause。
3. 最小 query set 覆盖 `@主标书` 基础信息与风险、缺失风险检查、`@硬件清单` Excel sheet/cell、`@C塔方案` PPTX slide、`@会议纪要` action / decision / risk、A/B 防污染、facts 边界与公司方向辅助分析。
4. 每条输出必须保存 query、原始输出、document_id/version_id、citation、`facts_as_answer`、`transcript_as_fact`、contamination_flags、pass/partial/fail、issue_type 与 priority。
5. Go 条件：P0 为 0、alias/session 不成为主要阻塞、partial / Missing Evidence 可人工记录、使用者理解输出只是辅助建议。
6. Pause 条件：facts 替代 evidence、无 citation 给确定结论、compare 混入第三文件、alias/session 大面积失效、使用者要求自动决策 / repair / rollout。
7. 当前不写代码、不运行 pytest、不进入 production rollout、不自动创建 issue。
8. 下一步建议 Codex B review Phase 2.33 run sheet；通过后再做 docs-only baseline。
9. Codex B 已审核 Day-1 run sheet，可执行 Phase 2.33 docs-only Git baseline；baseline 后停止等待检查。

## 40. Phase 2.34 Day-1 compare false-positive fix

1. Codex C Day-1 Pilot 结果：10 条 query 为 `7 pass / 3 partial / 0 fail`，P0 为 `0`；四个 alias 均稳定。
2. 当前 P1/P2 分流：Q1/Q2 主标书深层字段召回进入 P1 backlog；Q7/Q10 长输出延迟进入 P2 backlog；本轮只修 Q8 compare false-positive。
3. 已完成最小修复：最终 `retrieval_evidence_document_ids` 均属于 `compare_document_ids` 时，trace/context 稳定输出 `third_document_mixed=false`。
4. 已保留真实污染检测：最终 evidence 出现 compare 外 document_id 时仍输出 `third_document_mixed=true` 与 `unexpected_document_id`。
5. 候选过滤诊断改为 `out_of_scope_document_ids_filtered`，不再在最终 `contamination_flags` 中误导为第三文件混入。
6. Codex C 真实终端复验已通过：Q8 compare 输出 `third_document_mixed=false`、`third_document_mixed_document_ids=[]`、`contaminationflags=none`，无实际第三文件 evidence。
7. Facts / transcript 抽样通过：`facts_context_used=false`、`facts_context_fact_ids=[]`、`facts_as_answer=false`、`transcript_as_fact=false`。
8. Phase 2.34 已完成 baseline，Q8 compare false-positive 收口；后续转入 Phase 2.35 主标书深层字段召回专项。

## 41. Phase 2.35 tender deep-field retrieval

1. 已完成 diagnostic-first 最小实现，限定在 Hermes_memory retrieval 层。
2. 新增 / 增强 metadata snapshot fields：
   - `price_ceiling`
   - `qualification_requirement`
   - `project_manager_requirement`
   - `consortium_requirement`
   - `performance_requirement`
   - `personnel_requirement`
3. 已扩展最高投标限价 / 招标控制价 / 投标报价上限的触发词、section hints 与 phrase boosts。
4. 已扩展资质 / 项目经理 / 联合体 / 业绩 / 人员要求的触发词、section hints 与 phrase boosts。
5. 已新增 additive trace：`deep_field_profile`、`deep_field_section_hints`、`deep_field_query_aliases`、`metadata_deep_field_profile`。
6. `snapshot_as_answer=false` 与 `evidence_required=true` 保持不变，snapshot 只做导航，不替代 retrieval evidence。
7. 测试结果：py_compile 通过，目标 pytest `22 passed`。
8. 未做真实 Hermes CLI 复验；下一步需 Codex B review，必要时交 Codex C 复验 Day-1 Q1/Q2。
9. 当前仍不进入 production rollout，不做自动审标，不写 DB，不改索引。
10. Codex C 复验结果：Q1 基础字段通过，但最高投标限价 / 招标控制价 / 投标报价上限仍 Missing Evidence；Q2 投标资质 fail，项目经理 / 联合体 / 业绩 / 人员要求 partial。
11. 安全边界通过：未编造金额、资质、业绩或人员数量；`snapshot_as_answer=false`、`facts_as_answer=false`、`transcript_as_fact=false`。
12. 当前暂不 baseline，进入 Phase 2.35b bounded follow-up。
13. Phase 2.35b 代码层 review 通过，但 Codex C 真实 CLI 复验显示正式 Q1/Q2 被 alias/session 阻断：`alias_missing=true / retrieval_suppressed=true`。
14. Phase 2.35c 下一步只修 Hermes 主仓库 alias/session 首次绑定后丢失；修复后再由 Codex C 重跑 Q1/Q2。
15. Phase 2.35c 已完成主仓库最小修复：`上一轮已锁定的当前文件` 等说法会进入 current-document bind / current retrieval fallback，并持久化 alias 供后续同 session query 使用。
16. Codex C 真实终端复验通过：正式 Q1/Q2 不再丢 alias，不再 suppressed，可进入 Phase 2.35c baseline。
17. deep-field recall 仍 partial：限价具体金额、资质具体等级 / 类别、类似业绩、人员要求仍为后续尾项；`metadata_deep_field_profile=null` 与 `deep_field_profile=single_pass` 属 trace / 展示尾项。

## 42. Phase 2.36 tender deep-field recall tail planning

1. Phase 2.36 已完成路线规划：只做文档规划，不写代码、不运行真实 API / CLI smoke、不提交 Git。
2. 已按字段分类剩余缺口：
   - 最高投标限价 / 招标控制价 / 投标报价上限。
   - 投标资质等级 / 类别。
   - 项目经理等级 / B 证。
   - 联合体。
   - 类似业绩。
   - 人员数量 / 专业 / 证书。
   - trace display / profile fields。
3. 缺口分类使用 A/B/C/D：真实缺字段、章节召回不足、trace 展示问题、需人工确认。
4. 推荐 Phase 2.36a 最小实现：trace polish + section-targeted retrieval diagnostics + fixture-based concrete field tests。
5. 继续保留 Missing Evidence 口径；不得编造限价金额、资质等级、业绩或人员数量。
6. 不进入自动审标、production rollout、repair、DB / OpenSearch / Qdrant 变更。
7. Phase 2.36a 已完成 retrieval-layer 最小实现：顶层 trace 稳定输出 deep-field profile / section hints / query aliases / Missing Evidence reason / diagnostics。
8. 新增 fixture tests 覆盖具体限价、占位限价、具体资质等级+类别、证照清单；目标 pytest `17 passed`。
9. 下一步需 Codex B review；如终端仍显示 `metadata_deep_field_profile=null` 或 `deep_field_profile=single_pass`，需单独授权检查 Hermes 主仓库 adapter/context 展示层。
10. Phase 2.36b 已完成主仓库消费层最小实现：adapter / kernel / context_builder 提升并渲染 deep-field trace；alias parser 支持 `锁定“标题”，并绑定为 @alias`。
11. Phase 2.36b 主仓库目标测试：py_compile 通过，`59 passed`。
12. 下一步需 Codex B review 与 Codex C 真实终端复验；不能把本轮写成 deep-field recall 完全收口。
13. Codex C 复验确认 Phase 2.36b 的 alias binding 与 terminal-visible trace 已基本通过，但发现 diagnostics 与答案边界语义不一致：Q1 限价 diagnostics 可能显示 concrete found，而最终答案仍 Missing Evidence。
14. Phase 2.36c 已完成 Hermes_memory 最小修复：concrete evidence 需经最终 retrieval evidence 校正；metadata anchor 命中但最终 evidence 无具体金额时，trace 保守输出 `missing_concrete_price_amount` 与 `concrete_evidence_present=false`。
15. Phase 2.36c 已约束项目经理等级表述：仅电子证书 / 证照材料 / 格式条款不得推断为“项目经理=一级注册建造师”；需明确“项目经理须具备 X级注册建造师”才算 explicit level evidence。
16. Phase 2.36c 目标测试 `33 passed`；Codex B review 已通过，Codex C 真实终端复验已通过。
17. Phase 2.36c 当前可执行 Git baseline：限价 diagnostics 与 Missing Evidence 语义一致，电子证书 / 材料条款不再推断为项目经理等级；deep-field recall 仍 partial，真实限价金额、具体资质等级 / 类别、业绩、人员数量继续后置，不能宣称完整自动审标收口。

## 43. Phase 2.37 MVP Pilot issue intake / triage planning

1. Phase 2.36c baseline 已完成：commit `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。
2. 下一阶段建议先做 Pilot issue intake / triage，而不是继续盲修单个 deep-field recall 问题。
3. issue intake 应记录 query、expected / actual、document_id、citation、issue_type、priority、source_phase 与 human_review_required。
4. P0 必须覆盖编造、facts/transcript 替代 evidence、跨文件污染、权限泄露、自动决策越界。
5. Phase 2.37 规划已完成，新增 `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`。
6. 推荐 Phase 2.37a 做 local issue intake schema / templates / dry-run validator or summary generator。
7. Phase 2.37a 非目标：不自动修复 issue，不写 DB / facts / document_versions，不修改 OpenSearch / Qdrant，不进入 rollout，不做自动审标结论。
8. Phase 2.37 planning baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
9. Phase 2.37a 最小实现已完成：新增 local intake dry-run 工具与测试，支持 template、single / directory input、schema 校验、summary、strict invalid exit。
10. Phase 2.37a 验证通过：py_compile 通过，`tests/test_phase237a_pilot_issue_intake.py` 为 `9 passed`，临时 dry-run smoke 通过；下一步需 Codex B review 后再 baseline。
11. Phase 2.37a Git baseline 已完成：commit `1e1ca45`，tag `phase-2.37a-pilot-issue-intake-baseline`。
12. Phase 2.37b 最小 runbook / storage convention 已完成：新增 MVP Pilot issue intake runbook，规定 `reports/pilot_issues/*.json` 为本地敏感试用记录且默认 ignored。
13. Phase 2.37b 验证通过：template / strict dry-run 命令通过，`reports/pilot_issues/example.json` ignore 策略通过；下一步需 Codex B review 后再 baseline。
14. Phase 2.37b Git baseline 已完成：commit `e8c0631`，tag `phase-2.37b-pilot-issue-intake-runbook-baseline`。
15. Phase 2.37c planning 已完成：新增 daily / per-round Pilot issue triage summary 规划，明确 P0 pause、P1 bounded fix planning 候选、P2 backlog / UX / latency、P3 polish。
16. Phase 2.37c 非目标：不创建真实 issue records，不写 DB / facts / versions / index，不自动创建外部 issue，不 repair，不 rollout，不自动审标。
