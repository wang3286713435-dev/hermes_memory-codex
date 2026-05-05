# PRD Acceptance Matrix / MVP Evidence Pack

## 1. MVP 定位

当前 Hermes Memory MVP 是本地 / 内部受控的企业文件与标书管理 MVP。

它可以用于：

1. 企业文档、标书、Excel、PPTX、会议纪要的受控检索与引用。
2. 多文件会话、alias、compare、防污染与 Missing Evidence 边界验证。
3. confirmed facts 的治理、查询和辅助上下文。
4. readiness / repair / review 的 dry-run 与人工审阅链路。
5. 内部 MVP Pilot / Day-1 试用与问题 intake。

它不是：

1. production rollout ready 系统。
2. 自动审标 / 自动投标 / 自动经营决策系统。
3. repair executor。
4. facts 自动抽取或 facts 替代 retrieval evidence 的系统。
5. Data Steward / BIM 数据管家已实现产品。

## 2. Status 口径

| status | meaning |
|---|---|
| `done` | 已有目标测试、eval、live smoke 或 Git baseline 支撑，且边界清楚 |
| `partial` | 主链路可用，但仍有人工复核、召回、覆盖率、性能或展示缺口 |
| `planned` | 已有规划文档，但未实现 |
| `deferred` | 明确后置，不属于当前 MVP Pilot |

## 3. Evidence Type 口径

| evidence_type | meaning |
|---|---|
| `test` | 单元 / 集成 / direct assertion 测试 |
| `eval` | deterministic eval / CLI smoke / governance eval |
| `live_smoke` | Codex C 或本地真实 API / CLI 复验 |
| `phase_doc` | Phase 文档 / runbook / plan |
| `commit_tag` | Git commit / tag baseline |
| `manual_review_required` | 需要人工复核，不能只靠自动证据 |

## 4. Acceptance Matrix

| PRD item | capability area | status | evidence | known gap | next phase candidate | not claimable |
|---|---|---|---|---|---|---|
| 企业文档接入与解析 | document ingestion / parsing | `done` | `commit_tag`: `phase-2.12-structured-file-ingestion-baseline`; `phase-2.13-meeting-transcript-ingestion-baseline` | OCR / 原始音频 ASR / 扫描件解析仍未覆盖 | 后续 OCR / ASR 专项规划 | 完整多模态解析、原始音频 ASR |
| 结构化 chunk 与 metadata | structured chunking / metadata | `done` | `test` + `commit_tag`: Excel/PPTX / meeting transcript / tender metadata phases | 图表深层还原、图片 OCR 后置 | structured file quality follow-up | 完整图表语义还原、OCR |
| BM25 / OpenSearch 检索 | sparse retrieval | `done` | `eval`: Phase 2.14 / 2.20a full eval; `commit_tag`: `phase-2.14-regression-eval-baseline` | tender 深层字段仍有 partial | PRD evidence pack 继续记录 pass / partial | 所有标书字段 100% 命中 |
| Dense ingestion / Qdrant | dense retrieval | `done` | `commit_tag`: `phase-2.16-dense-ingestion-baseline`; `eval`: dense/hybrid smoke | 大文件回填耗时明显；自动 eval 覆盖仍需维护 | dense / hybrid eval maintenance | production-scale dense SLA |
| Hybrid retrieval | sparse / dense / hybrid retrieval | `done` | `eval`: Phase 2.17 dense/hybrid eval extension | 不宣称 dense 一定优于 sparse | eval trend tracking | 排序收益已系统证明 |
| Rerank smoke | rerank smoke / evaluation boundary | `partial` | `commit_tag`: `phase-2.17-rerank-hybrid-eval-baseline`; smoke 真实调用 / skipped 合理 | 只验证链路可观测，不验证排序收益 | rerank quality eval | rerank 策略收益已完成 |
| Citation / trace | citation / trace / evidence policy | `done` | `eval`, `live_smoke`, `commit_tag`: 2.11-2.20 series | 部分长输出展示仍需人工观察 | evidence pack maintenance | citation 永远完美 |
| Missing Evidence 边界 | Missing Evidence / 人工复核 | `partial` | `live_smoke`: Day-1 / Phase 2.35-2.38; `manual_review_required` | 主标书限价、资质等级 / 类别、项目经理等级、业绩、人员数量仍需人工复核 | tender deep-field recall issue backlog | 自动审标结论、无人工复核 |
| 同会话文件作用域 | alias / session scope | `done` | `commit_tag`: `phase-2.10-session-document-scope-baseline`; `phase-2.11b-file-alias-baseline`; `phase-2.30b` 真实复验 | 需持续 Pilot issue intake 观察 | session regression smoke | 所有企业会话场景零风险 |
| Compare 防污染 | compare scope / contamination guard | `done` | `commit_tag`: `phase-2.34-compare-contamination-baseline`; Codex C live smoke | 复杂多文件 compare 仍需持续样本 | compare regression cases | 任意多文档复杂分析完全自动可靠 |
| Excel structured citation | Excel sheet / cell citation | `done` | `commit_tag`: `phase-2.12-structured-file-ingestion-baseline`; live terminal 5/5 | 图表 / 合并单元格深语义后置 | Excel quality tail | 完整 Excel BI 解析 |
| PPTX structured citation | PPTX slide citation | `done` | `commit_tag`: `phase-2.12-structured-file-ingestion-baseline`; live terminal 5/5 | 图片 OCR / 图表 OCR 后置 | PPTX OCR / chart follow-up | 完整 PPT 图片理解 |
| 会议纪要检索 | meeting transcript / transcript_as_fact=false | `done` | `commit_tag`: `phase-2.13-meeting-transcript-ingestion-baseline`; `live_smoke` | 原始音频 ASR 后置 | ASR planning if needed | 原始音频会议记忆已完成 |
| Facts 创建与治理 | facts governance | `done` | `commit_tag`: `phase-2.21a-evidence-backed-facts-baseline`; `phase-2.21b-facts-governance-baseline` | 自动抽取后置；人工确认 UI 后置 | facts management polish | facts 自动抽取 |
| Confirmed facts 只读查询 | facts read / citation | `done` | `commit_tag`: `phase-2.23a-confirmed-facts-read-baseline` | 不进入 final answer 替代 evidence | evidence pack examples | facts 可替代文档证据 |
| Facts 辅助上下文 | facts_as_answer=false | `done` | `commit_tag`: `phase-2.24a-facts-agent-context-baseline`; Codex C 真实复验 | 只能 auxiliary，不能单独作答 | regression smoke maintenance | facts 单独作为最终答案来源 |
| Access soft policy | access / audit / soft policy | `done` | `commit_tag`: `phase-2.18a-access-audit-baseline`; governance eval | 完整 RBAC / ABAC 后置 | RBAC planning | 完整企业权限系统 |
| Audit logs | retrieval / fact / review audit | `partial` | `commit_tag`: `phase-2.18a-access-audit-baseline`; 2.27d report-level sanitized audit | report review audit 仅 report-level；item-level 后置 | audit coverage matrix | 完整合规审计系统 |
| Version governance | active/latest / stale diagnostics | `done` | `commit_tag`: `phase-2.19a-version-governance-baseline`; `phase-2.19b-alias-stale-version-baseline` | 删除治理 / 自动合并同名文档后置 | delete / invalidation planning | 完整文档生命周期后台 |
| Regression eval | API deterministic eval / CLI smoke | `done` | `commit_tag`: `phase-2.14-regression-eval-baseline`; `phase-2.14b-cli-smoke-eval-baseline`; `phase-2.20a-governance-eval-baseline` | missing alias suppress 属 CLI smoke；full eval 需维护环境变量 | eval report pack | 全量生产级评测系统 |
| Readiness audit | readiness audit dry-run | `done` | `commit_tag`: `phase-2.25a-readiness-audit-baseline` | 只诊断，不修复；stale fact warning 仍存在 | scheduled smoke planning | production readiness 已完成 |
| Repair plan | repair plan dry-run | `done` | `commit_tag`: `phase-2.26a-repair-plan-dry-run-baseline` | 不执行 repair；只生成不可执行 plan | manual review / executor planning | repair executor ready |
| Report archive / trend | reports archival / trend diff | `done` | `commit_tag`: `phase-2.26b-audit-report-archival-baseline` | 真实 reports JSON ignored；非生产归档 | report review adoption | 自动运维报告系统 |
| Report review workflow | local review / sanitized audit | `done` | `commit_tag`: `phase-2.27a-report-review-dry-run-baseline`; 2.27b/2.27d/2.27f chain | approved_for_manual_action 不等于 executed | review governance pack | approved 即已执行 |
| Pilot issue intake | Pilot issue intake / triage | `done` | `commit_tag`: `phase-2.37a-pilot-issue-intake-baseline`; `phase-2.37d-pilot-triage-summary-baseline` | 持续趋势和外部 issue 系统未接入 | Pilot evidence pack | 自动创建 / 自动修复 issue |
| Internal MVP Pilot Pack | Pilot ops / Day-1 run sheet | `done` | `commit_tag`: `phase-2.31-pilot-ops-nightly-launcher-baseline`; `phase-2.33-pilot-day1-run-sheet-baseline` | 当前仍是内部受控试用，不是 rollout | MVP release candidate checklist | production rollout ready |
| Tender deep-field retrieval | tender recall / personnel guard | `partial` | `commit_tag`: `phase-2.38d-personnel-runtime-guard-baseline`; Codex C Q1/Q2/Q3 live pass | 限价、资质等级 / 类别、项目经理等级、业绩、人员数量仍需人工复核 / Missing Evidence | issue-intake driven P1 backlog | 完整自动审标 |
| Data Steward 产品线 | Data Steward deferred product line | `planned` / `deferred` | `commit_tag`: `phase-2.39-data-steward-product-plan-baseline`; `phase_doc`: `docs/PHASE239_DATA_STEWARD_PRODUCT_PLAN.md` | 只完成规划；未实现 asset catalog / graph / spatial / scheduler | separate Data Steward phase planning | Data Steward 已实现、TB BIM 全量解析 |

## 5. MVP 落地判断

### 5.1 当前可以做

当前可以进入内部受控 MVP Pilot / Day-1 试用。

理由：

1. 文档 / 表格 / PPT / 会议纪要 ingestion 与 citation 已有 baseline。
2. alias / session / compare / contamination guard 已有真实终端复验。
3. dense / sparse / hybrid / rerank smoke 已纳入 eval 或 smoke。
4. access / audit / version governance / facts governance 已有最小闭环。
5. `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false` 的边界已有多轮验收。
6. Pilot issue intake 与 triage 能把真实试用问题结构化沉淀。

### 5.2 当前必须人工复核

以下内容必须继续人工复核：

1. 主标书最高投标限价 / 招标控制价 / 投标报价上限。
2. 投标资质具体等级 / 类别。
3. 项目经理等级 / B 证。
4. 类似业绩金额 / 规模 / 年限。
5. 人员数量 / 专业 / 职称 / 资质。
6. 公司经营方向、客户建议、投标策略等经营性判断。
7. 任何 Missing Evidence 输出。

### 5.3 当前不应声明

当前不应声明：

1. production ready。
2. 自动审标可替代人工。
3. 自动经营决策可替代管理层。
4. repair executor 可用。
5. facts 自动抽取已完成。
6. facts 可替代 retrieval evidence。
7. Data Steward 已实现。
8. TB BIM 全量解析已完成。
9. Neo4j / PostGIS / 空间索引 / 子 agent scheduler 已落地。
10. 完整知识图谱 / 多 agent / 完整 RBAC 已完成。

## 6. Evidence Pack 后续维护优先级

下一阶段如果继续推进，应优先维护：

1. 每个 matrix row 的 commit / tag / eval / Codex C session 引用。
2. Pilot issue intake 中 P0 / P1 的趋势。
3. Day-1 / 内部试用 query pass / partial / fail 变化。
4. `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false` 的回归证据。
5. permission deny 后无 evidence 泄露的 governance evidence。
6. tender deep-field Missing Evidence 与人工复核记录。

## 7. Data Steward 边界

Data Steward / 数据管家是后置产品线。

当前只完成：

1. PRD / Roadmap / Technical Design 规划。
2. Phase 2.39 Data Steward product line plan。

当前没有完成：

1. Building Asset Catalog MVP。
2. BIM / IoT / 运维系统真实接入。
3. TB BIM 全量解析。
4. Neo4j / PostGIS / 空间索引代码。
5. 子 agent 调度与监控面板。
6. Data Steward production rollout。

## 8. 下一步建议

建议 Codex B 审核本 matrix 后，再决定是否进入 Phase 2.40a docs-only baseline。

如果继续推进，只建议做 evidence pack 的只读维护策略或人工 review 流程，不建议直接进入新功能开发。
