# Phase 2.15 项目状态审计与下一阶段路线裁决

## 1. 本轮目标

Phase 2.15 只做项目状态审计、PRD 完成度估算与下一阶段路线裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构，不进入 rollout。

## 2. 已完成能力

1. 企业文档检索底座：已完成真实 docx / xlsx / pptx / 会议纪要文本接入、解析、chunk、OpenSearch sparse 索引与检索验证。
2. 多文件与上下文治理：已完成 session document scope、context governance、file alias、A/B compare、防第三文件污染、history memory 非 evidence 规则。
3. 招标资料增强：已完成 tender metadata snapshot，基础信息 query 可锚定工程地点、建设单位、代建单位等来源 chunk，且 `snapshot_as_answer=false`。
4. 结构化文件 MVP：Excel 可保留 sheet / cell range citation，PPTX 可保留 slide number / slide title citation。
5. 会议纪要文本 MVP：docx/txt/md 会议资料可提取 action / decision / risk，且 `transcript_as_fact=false`。
6. 评测体系首轮：已完成 API deterministic eval runner 与 Hermes CLI smoke eval；当前 API eval `10/10` 通过，CLI smoke `4/4` 通过。

## 3. 部分完成能力

1. Hybrid search：dense/sparse/hybrid 主结构存在，但真实上传 ingestion 仍主要依赖 OpenSearch sparse；dense ingestion 尚未形成闭环。
2. Rerank：阿里云 rerank adapter 与局部默认启用灰度已验证，但未进入更大范围 rollout。
3. 文档版本治理：已有 document / version / chunk 基础结构，但版本对比、失效策略、增量更新闭环仍不足。
4. 多模态资料：Excel/PPTX MVP 已完成，但 PDF OCR、图片 OCR、扫描件、原始音频 ASR 未做。
5. 会话记忆：已完成文档作用域与历史记忆非 evidence 规则，但完整长期会话记忆、任务状态、人工确认事实沉淀未完成。
6. 评测体系：已有 API eval + CLI smoke，但还未达到 PRD 要求的 100/300 条评测集、质量看板与 CI 化。

## 4. 未完成能力

1. dense ingestion：上传 ingestion 尚未将 chunk 稳定 upsert 到 Qdrant。
2. 结构化事实层：客户、项目、合同、资质、人员、金额、日期等事实库尚未落地。
3. 权限治理：尚未完成部门 / 项目 / 密级 / 用户级权限过滤与越权评测。
4. 审计日志闭环：尚未形成用户查询、检索 evidence、回答引用、权限判断的系统级审计闭环。
5. 增量更新闭环：文件更新、版本失效、索引重建、旧 chunk 下线仍未完整闭环。
6. 知识管理员后台与人工校验机制：尚未实现。
7. 完整 OCR / 原始音频 ASR / 图片理解：尚未实现。
8. 生产级 rollout：尚未进入。

## 5. PRD 完成度估算

| 模块 | 完成度估算 | 判断 |
| --- | --- | --- |
| 企业文档检索底座 | 约 70% | Word / Excel / PPTX / 会议纪要文本已形成真实闭环，但 dense ingestion、权限、增量仍缺。 |
| 企业上下文治理 | 约 75% | session scope、alias、compare、防污染已通过；project/task 持久化与完整会话记忆仍缺。 |
| 多模态 / 结构化文件 | 约 45% | Excel/PPTX MVP 可用；PDF OCR、图片、扫描件、音频仍未覆盖。 |
| 会议记忆 | 约 40% | 转写文本 / 会议纪要可检索并抽取行动项；原始音频 ASR、人工确认、事实写入未完成。 |
| 评测体系 | 约 35% | API deterministic eval 与 CLI smoke 起步完成；评测规模、CI、看板、反馈闭环未完成。 |
| 权限 / 审计 / facts / dense ingestion | 约 15% | 多数仍是 PRD 核心缺口，不能误报完成。 |

## 6. 最大风险

当前最大风险不是文档能否接入，而是“可用能力增长快于治理能力”。

具体表现：

1. dense ingestion 缺失会限制语义召回与 hybrid 质量上限。
2. 权限 / 审计未闭环会阻止企业级真实 rollout。
3. facts 未落地会限制从“检索助手”升级为“企业长期记忆系统”。
4. 评测集规模仍小，难以覆盖未来权限、版本、增量和多模态组合回归。

## 7. 下一阶段候选评审

### A. Phase 2.15a 继续评测体系完善

优点：风险低，可直接巩固当前所有已完成能力，适合进入 CI / nightly / 报告化。

不足：不直接补 dense / 权限 / facts 等核心能力缺口。

### B. Phase 2.16 dense ingestion

优点：补齐 PRD 检索底座核心短板，让上传文件真正进入 dense + sparse + hybrid 闭环。

不足：会触及 embedding 批处理、Qdrant 写入、重试、版本、失败回滚和成本监控，需要较严谨实现。

### C. Phase 2.17 权限 / 审计

优点：是企业 rollout 前硬门槛。

不足：需要用户、组织、项目、文档密级与审计模型，若在 dense ingestion 前做，检索底座仍不完整。

### D. Phase 2.18 原始音频 ASR

优点：扩展会议记忆输入源。

不足：不是当前最高风险；没有权限、审计、facts 前，不宜提前扩大敏感音频入口。

### E. Phase 2.19 企业事实层 facts

优点：是从检索助手走向长期记忆系统的关键。

不足：需要事实 schema、人工确认、来源追溯、更新策略；应在检索底座更完整后推进。

## 8. 推荐路线

推荐下一阶段进入：

**Phase 2.16：dense ingestion 与 hybrid 检索闭环补齐。**

理由：

1. dense ingestion 是 PRD 文档检索底座的核心缺口。
2. 当前真实文件验证主要依赖 OpenSearch sparse，长期会限制语义召回与复杂问法稳定性。
3. dense ingestion 完成后，API eval / CLI smoke 可继续复用，用于防止回归。
4. 权限 / 审计 / facts 都应建立在更完整的检索与索引闭环之上。

建议 Phase 2.16 严格限定为：

1. 上传 ingestion 将 chunk upsert 到 Qdrant。
2. 记录 embedding model / dimension / vector status。
3. dense 写入失败可诊断、可重试、可 fail-open。
4. 复用 Phase 2.14 eval 验证 dense/sparse/hybrid 返回一致性。
5. 不做权限大改、不做 facts、不做 rollout。

## 9. 当前阶段结论

Phase 2.10-2.14b 已经把 Hermes 从“能检索文档”推进到“可处理多文件、多格式、会话作用域与基础评测”的阶段。

但当前仍不能宣称：

1. 完整企业长期记忆系统已完成。
2. 生产级 rollout 已具备条件。
3. 权限 / 审计 / facts / dense ingestion 已闭环。

当前建议结束状态审计，进入 Phase 2.16 的最小实现规划与实施。
