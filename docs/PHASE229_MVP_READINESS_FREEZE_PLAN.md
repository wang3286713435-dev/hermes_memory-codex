# Phase 2.29 MVP Readiness Freeze Plan

## 1. 当前总体状态判断

当前项目已从“能力拼装期”进入“候选 MVP 冻结前审计期”。

已经可以确认：

1. 企业长期记忆底座主链路已形成可复现闭环。
2. 文档检索、上下文治理、版本治理、facts 治理、评测体系、只读治理工具链均已有基线。
3. 多类型资料摄取已覆盖大标书、Excel、PPTX、会议纪要 / transcript。
4. 评测与治理证据已能通过 deterministic eval、CLI smoke、readiness audit、repair plan dry-run、report review / audit / linkage summary 留痕。

仍不能确认：

1. 已达到 production rollout readiness。
2. 已具备自动 repair 能力。
3. facts 可以直接替代 retrieval evidence。
4. 已具备完整 RBAC/ABAC、原始音频 ASR、自动 facts 抽取或生产化 cron 调度。

因此，Phase 2.29 的正确目标不是继续加新能力，而是冻结一个“可验收 MVP 候选版本”。

## 2. MVP 候选能力清单

### 2.1 文档检索与上下文治理

1. active document scope。
2. file alias。
3. A/B compare。
4. missing alias suppress。
5. stale alias version warning。

### 2.2 多类型文件能力

1. 大标书 / 大文档检索。
2. Excel sheet / cell citation。
3. PPTX slide citation。
4. 会议纪要 / transcript 的 action / decision / risk 检索。

### 2.3 检索质量与混合检索

1. sparse retrieval。
2. dense ingestion + Qdrant backfill。
3. hybrid eval。
4. rerank smoke。

### 2.4 权限 / 审计 / 版本治理

1. soft ACL。
2. retrieval / facts / review audit。
3. latest / superseded version filtering。
4. explicit historical version query。
5. stale source / stale version diagnostics。

### 2.5 facts 能力

1. evidence-backed facts。
2. facts query ACL。
3. confirm / reject workflow。
4. confirmed facts read-only search。
5. confirmed facts auxiliary context，且 `facts_as_answer=false`。

### 2.6 评测与治理工具链

1. Phase 2.14 deterministic eval。
2. CLI smoke。
3. governance eval。
4. facts eval。
5. readiness audit dry-run。
6. repair plan dry-run。
7. report archival / trend diff。
8. report review record。
9. sanitized review audit preview / write。
10. archive / review / audit linkage summary。

## 3. MVP Freeze Checklist

建议冻结清单至少包含：

1. 文档问答主链路：单文件、A/B compare、alias、missing alias suppress、stale alias warning。
2. 多类型文件：Excel citation、PPTX citation、meeting transcript 检索。
3. hybrid 检索：sparse / dense / hybrid / rerank smoke。
4. 版本治理：latest 默认过滤、explicit old version、stale source diagnostics。
5. facts 治理：unverified / confirmed / rejected、ACL、audit、auxiliary context 但 `facts_as_answer=false`。
6. 权限与审计：soft ACL、audit_logs、report review audit。
7. 评测闭环：Phase 2.14 eval、CLI smoke、governance eval、facts eval。
8. 治理 dry-run：readiness audit、repair plan、report archival、report review、linkage summary。

## 4. 必须复跑的验证项

建议在 Phase 2.29a 中至少复跑：

1. Phase 2.14 deterministic eval 全量。
2. CLI smoke 关键会话态场景。
3. governance eval。
4. facts eval。
5. readiness audit dry-run。
6. repair plan dry-run。
7. rerank smoke。
8. dense / hybrid smoke。

不建议在 Phase 2.29a 默认复跑：

1. 真实 reports / reviews 默认目录扫描。
2. repair executor。
3. 原始音频 ASR。
4. 全量生产数据 mutation。

## 5. 人工验收项

建议纳入人工 freeze checklist：

1. linkage summary 结果是否可读、可追溯、无敏感字段泄露。
2. report review audit 是否只保留 report-level sanitized 摘要。
3. facts auxiliary context 是否稳定保持 `facts_as_answer=false`。
4. stale alias / stale source warning 是否可被终端用户理解。
5. 大标书、Excel、PPTX、会议纪要四类资料的引用展示是否清晰。
6. 默认 latest / historical version 行为是否符合预期。

## 6. 当前不进入 MVP 的后置能力

当前明确后置：

1. production rollout。
2. repair executor。
3. 自动 facts 抽取。
4. facts 替代 retrieval evidence。
5. 完整 RBAC/ABAC。
6. 原始音频 ASR。
7. 默认扫描真实 reports / reviews。
8. item-level review audit summary 扩张。
9. production cron / scheduler。

## 7. 当前不能 rollout 的原因

当前不建议 rollout，原因包括：

1. 当前冻结证据仍以 MVP 候选为目标，不是生产运行手册。
2. repair executor 未建立人工确认与回滚闭环。
3. readiness / governance 工具链虽可诊断，但尚未冻结为稳定 runbook。
4. 仍未进入完整权限模型、生产级审计可视化、生产级多租户治理。
5. 部分治理链路仍刻意保持 dry-run / preview / explicit opt-in。

## 8. Go / No-Go 判定标准

### Go for MVP freeze candidate

满足以下条件可进入 MVP freeze candidate：

1. 核心 eval / smoke 可稳定复跑。
2. 多类型文件引用与上下文治理无明显回归。
3. facts 保持 evidence-backed 且不替代 retrieval evidence。
4. version / ACL / audit / readiness / repair plan 链路均有可追溯 dry-run 证据。
5. linkage summary、review audit、report archival 均保持非破坏性、可审阅。

### No-Go for production rollout

以下任一存在时不得进入 rollout：

1. repair executor 未冻结。
2. 仍依赖大量人工判断但无正式 runbook。
3. facts 可能被误用为最终答案来源。
4. readiness / governance 只读工具链尚未形成稳定冻结报告。

## 9. Phase 2.29a 推荐最小动作

推荐 Phase 2.29a 只做以下之一：

1. MVP freeze checklist runner / runbook 规划或最小 dry-run。
2. freeze report dry-run，汇总 eval、readiness audit、repair plan、governance 证据。

不建议 Phase 2.29a 做：

1. 新能力开发。
2. production rollout。
3. repair executor。
4. 默认读取真实 reports / reviews。

## 10. Phase 2.29 与 Production Rollout 的边界

Phase 2.29 是“冻结一个可验收 MVP 候选版本”。

它意味着：

1. 我们开始用 freeze checklist 管理能力边界。
2. 我们开始判断哪些能力可进入 demo / pilot 候选。
3. 我们开始沉淀 go / no-go 标准。

它不意味着：

1. 进入 production rollout。
2. 启用自动 repair。
3. 允许 facts 替代 retrieval evidence。
4. 允许默认扫描真实审阅与报告目录。
5. 完整权限模型已完成。

## 11. 规划结论

Phase 2.29 应作为“readiness freeze 阶段”，而不是“继续补工具阶段”。

推荐结论：

1. 进入 Phase 2.29a，但只做 freeze checklist / freeze report dry-run。
2. 不再继续无限扩展 2.27x 治理子阶段。
3. 不进入 production rollout。
4. 不进入 repair executor。

## 12. Phase 2.29a 最小实现状态

Phase 2.29a 已完成 freeze report dry-run 最小实现。

新增能力：

1. `scripts/phase229a_freeze_report_dry_run.py` 生成只读 freeze report JSON。
2. 支持显式传入 eval summary、readiness report、repair plan 与 optional linkage summary。
3. 默认不扫描真实 `reports/` / `reviews/` 目录。
4. 默认不运行 full eval 或昂贵 smoke。
5. 输出恒定保持 `dry_run=true`、`destructive_actions=[]`、`rollout_ready=false`、`production_rollout=false`、`repair_executed=false`。
6. Go / No-Go 只判断 MVP freeze candidate，不允许把结果解释为 production rollout。

验证结果：

1. `uv run python -m py_compile scripts/phase229a_freeze_report_dry_run.py` 通过。
2. `uv run pytest tests/test_phase229a_freeze_report_dry_run.py -q`：8 passed。
3. 临时目录 fake report JSON dry-run 通过；未读取真实 reports / reviews，未写 DB，未生成真实 rollout 或 repair 产物。

当前结论：

1. Phase 2.29a 实现可进入 review / baseline。
2. baseline 前不建议进入 Phase 2.29b。
3. 生产 rollout、repair executor、facts 自动抽取继续后置。
