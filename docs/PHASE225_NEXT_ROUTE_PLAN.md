# Phase 2.25 项目状态审计与下一阶段路线裁决

## 1. 本轮目标

Phase 2.25 只做项目状态审计、候选方向评审与下一阶段路线裁决。

本轮不写功能代码，不改 retrieval contract，不改 memory kernel 主架构，不进入生产 rollout。

## 2. 当前项目阶段判断

Hermes_memory 当前已经从“企业文档检索原型”进入“企业长期记忆底座 MVP 后段”。

当前可确认：

1. 文档知识层、hybrid 检索、上下文治理、多格式解析、版本治理、权限审计、facts 基础治理和评测框架均已有最小闭环。
2. 真实企业文件池、Excel/PPTX、会议纪要、dense/rerank smoke、API eval 与 CLI smoke 已形成可重复验证能力。
3. confirmed facts 已可进入 Agent 辅助上下文，但仍不能替代 retrieval evidence，也不能作为 final answer 的独立依据。

当前不能误报：

1. 还不是完整企业长期记忆系统收官。
2. 还不是生产级 rollout 完成。
3. facts 自动抽取、完整 RBAC/ABAC、完整知识管理员后台、OCR/ASR、多系统接入仍未完成。

## 3. 已完成能力清单

1. 文档接入：docx、xlsx、pptx、会议纪要文本已完成真实上传、解析、chunk、索引与检索验证。
2. 检索底座：OpenSearch sparse、Qdrant dense、hybrid smoke、rerank smoke 均已可观测。
3. 上下文治理：session document scope、file alias、A/B compare、history memory 非 evidence、防污染 trace 已完成。
4. 招标增强：tender metadata snapshot 可辅助基础信息定位，且 `snapshot_as_answer=false`。
5. 结构化文件：Excel sheet/cell citation、PPTX slide citation 已通过真实终端验收。
6. 会议纪要：action / decision / risk 可检索，`transcript_as_fact=false`。
7. 权限审计：soft policy、deny 防泄露、audit log、governance eval 已完成。
8. 版本治理：latest / superseded、显式历史版本查询、alias stale version 诊断已完成。
9. facts：evidence-backed facts、权限过滤、人工确认、只读 confirmed facts、Agent 辅助上下文已完成。
10. 评测：Phase 2.14 API deterministic eval、CLI smoke、governance eval、facts eval 已形成基线。

## 4. 未完成 / 半完成能力清单

1. facts 自动抽取尚未实现；当前 facts 仍需显式创建或人工确认。
2. facts 仍不允许替代 retrieval evidence，不进入 final answer 独立作答。
3. 生产级 rollout readiness 尚未系统审计：部署、配置、迁移、备份恢复、健康检查、观测性和运行手册仍需专门检查。
4. 数据维护工具不足：重复文档、旧版本、索引一致性、stale facts 修复仍主要依赖人工排查。
5. 管理后台 / 审计可视化未实现。
6. 完整 RBAC/ABAC、IAM/SSO、项目级权限、密级治理仍未实现。
7. OCR、原始音频 ASR、图片 / 扫描件、多系统连接仍未实现。
8. 评测规模仍未达到 PRD 中 100 / 300 条级别，质量看板和 CI 化仍需后续推进。

## 5. A-F 候选方向评审

| 方向 | PRD 贡献 | 依赖满足 | 风险可控 | 新样本需求 | contract / 架构影响 | 适合 2.25a | 是否后置 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. facts 自动抽取 MVP | 高，可扩大结构化事实覆盖。 | 部分满足：facts 存储、权限、确认、eval 已有。 | 中高，误抽取、重复事实、旧版本污染和审核压力明显。 | 需要稳定标注样本和抽检集。 | 可不改 contract，但会扩大事实治理压力。 | 暂不推荐首选。 | 应后置到 readiness / 维护工具之后。 |
| B. confirmed facts 更深层 Agent 使用 | 中高，可提升 Agent reasoning。 | 部分满足：辅助上下文已完成。 | 中高，模型仍可能把 facts 当最终答案。 | 不一定需要新样本，但需更强 prompt/eval。 | 主要在主仓库消费层，不应改 contract。 | 不推荐。 | 后置，先稳定运行治理。 |
| C. 企业 rollout readiness | 很高，是真实使用前硬门槛。 | 基础满足：核心能力已有 baseline。 | 可控，只做 audit / smoke / runbook，不发布生产。 | 不需要新业务样本。 | 不应改 contract 或主架构。 | 推荐。 | 不后置。 |
| D. 管理后台 / 审计可视化 | 高，提升知识管理员可操作性。 | 部分满足：API 与 audit 已有。 | 中，容易拉长产品线和前端范围。 | 不需要新样本。 | 不应改 contract，但会引入 UI 面。 | 不推荐首选。 | 后置到 readiness 后。 |
| E. 数据维护工具 | 高，降低长期污染和运维成本。 | 基础满足：version、dense、audit、facts 已有。 | 可控，若只做诊断 / dry-run / 显式 document_id。 | 不需要新样本。 | 不改 contract。 | 推荐作为 2.25a 子项。 | 不后置。 |
| F. 原始音频 ASR / OCR / 更多多模态 | 高，但属于能力扩展。 | 不足：治理、样本、provider、评测都需新增。 | 高，会引入敏感音频、扫描件误识别和权限压力。 | 需要新音频 / 扫描件样本。 | 可能影响 parser / ingestion 架构。 | 不推荐。 | 明确后置。 |

## 6. 推荐下一阶段路线

推荐进入：

**Phase 2.25a：Enterprise Readiness Audit + 数据维护诊断小工具。**

推荐理由：

1. 当前能力已经足够多，下一步最需要确认“能否被稳定运行、诊断、恢复”，而不是继续扩新功能。
2. 生产 rollout 不能直接开始，但 readiness audit 可以提前暴露部署、迁移、配置、备份、健康检查和观测性缺口。
3. 数据维护诊断工具能降低后续 facts 自动抽取与更深 Agent 使用的污染风险。
4. 该方向不需要修改 retrieval contract，也不需要动 memory kernel 主架构。

不推荐下一阶段直接做：

1. facts 自动抽取：容易扩大 unverified facts 数量和人工确认压力。
2. confirmed facts 更深层 Agent 使用：当前 `facts_as_answer=false` 边界刚稳定，不宜马上加深。
3. 管理后台 / 审计可视化：价值高，但适合 readiness 后再做产品化。
4. OCR / 原始音频 ASR：会扩大输入风险，治理成本高。
5. 生产 rollout：当前只适合 readiness planning / audit / smoke，不适合真实发布。

## 7. Phase 2.25a 最小边界

Phase 2.25a 建议只做两类最小工作。

### 7.1 Readiness audit / smoke

1. 环境配置检查：Postgres、OpenSearch、Qdrant、Aliyun embedding / rerank key、QDRANT_COLLECTION、DATABASE_URL。
2. migration 检查：alembic head、facts / audit / version 表结构是否完整。
3. 索引健康检查：OpenSearch index、Qdrant collection、dense/sparse count 粗对齐。
4. API 健康检查：`/health`、retrieval search、facts API、audit 写入 smoke。
5. 评测入口检查：Phase 2.14 eval、governance eval、CLI smoke 是否可执行。
6. 备份恢复清单：Postgres、OpenSearch、Qdrant、原始文件存储当前如何备份；本阶段只写清单和检查，不做生产备份系统。

### 7.2 数据维护诊断小工具

1. 重复 / 近似同名 document 诊断，默认只报告，不自动合并。
2. latest / superseded 状态诊断，检查 DB、OpenSearch、Qdrant 是否一致。
3. Qdrant / OpenSearch chunk count 对齐诊断。
4. stale facts 诊断，输出 fact_id、source_version_id、latest_version_id。
5. dry-run 输出 JSON summary；任何修复必须显式参数触发。
6. 不默认全库重写，不做物理删除，不自动确认 facts。

## 8. 明确非目标

Phase 2.25a 不做：

1. 生产级 rollout。
2. 自动 facts 抽取。
3. facts 替代 retrieval evidence。
4. 完整管理后台 / 审计 UI。
5. 完整 RBAC/ABAC / IAM / SSO。
6. OCR / 原始音频 ASR / 更多多模态解析。
7. retrieval contract 重构。
8. memory kernel 主架构重构。

## 9. 风险与阻塞点

1. readiness audit 会暴露部署与数据一致性尾项，但这正是进入真实使用前必须面对的风险。
2. 数据维护工具如果越界为自动修复，可能误删或误改真实企业资料；必须先 dry-run。
3. facts 自动抽取若过早推进，会放大重复事实、旧版本事实和人工确认压力。
4. confirmed facts 更深层进入 Agent reasoning 前，还需要更强 eval 保护。
5. 当前仍缺完整备份恢复演练、长期运行观测和正式生产部署方案。

## 10. 当前结论

建议进入 Phase 2.25a 实现，但边界必须限定为：

**readiness audit / smoke + 数据维护诊断 dry-run。**

不建议直接进入生产 rollout、facts 自动抽取、facts 深层 Agent 使用、管理后台或 OCR / ASR 扩展。

## 11. Phase 2.25a 最小实现结果

本轮已新增只读 readiness audit runner：

1. `scripts/phase225_readiness_audit.py`。
2. 默认 dry-run，只诊断，不修复、不删除、不迁移。
3. 输出 JSON summary，固定包含 `destructive_actions=[]` 与 `dry_run=true`。
4. 支持 `--document-id` 限定抽样真实文件池，避免默认对全库做重操作。
5. 支持 `--skip-service-check`、`--run-light-eval`、`--fail-on-warn`。

当前覆盖项：

1. 服务健康：Postgres、OpenSearch、Qdrant、核心 endpoint 与 `QDRANT_COLLECTION`。
2. 版本治理：多 latest、零 latest、superseded active/latest、`current_version_id` 指针。
3. OpenSearch 一致性：抽样 chunk count、旧版本 `is_latest=true` 泄露。
4. Qdrant 一致性：dense points、payload 中 document/version/chunk/is_latest 字段。
5. facts 治理：confirmed facts 来源字段、stale source version、状态计数、受限来源文档统计。
6. audit logs：retrieval / fact query / fact search / fact confirm / fact reject 统计。
7. eval readiness：Phase 2.14 runner 可导入；light eval 因保持只读语义默认不执行。

验证结果：

1. `uv run python -m py_compile scripts/phase225_readiness_audit.py` 通过。
2. `uv run pytest tests/test_phase225_readiness_audit.py -q` 通过，`6 passed`。
3. 使用默认 `.env` 直接 dry-run 失败，根因是本机直跑解析不到 `postgres/opensearch/qdrant` 容器主机名；该失败可诊断，不会修复环境。
4. 使用 `127.0.0.1` 覆写后 dry-run 通过为 `status=warn`：`23` checks，`22` passed，`1` warning，`0` failed。
5. 唯一 warning 为已知 stale confirmed fact：`9f98384b-5053-4a8f-9b83-35983b28b38e` 指向旧版本 `896a19d7-2b01-4492-9672-bb4fdfbc7921`，latest 为 `76ca95a1-393f-4278-b254-ab66295bb14f`。

本阶段结论：

1. Phase 2.25a 的 readiness audit / 数据维护诊断 dry-run 最小闭环已形成。
2. 当前不是生产 rollout 通过结论，只是具备进入 Git baseline 或继续扩展诊断项的条件。
3. 后续若继续推进，应优先补 baseline，再考虑将 runner 纳入定期 smoke 或 CI。
