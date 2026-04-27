# Phase 2.29d Release Candidate Checklist Plan

## 1. 阶段目标

Phase 2.29d 只规划 MVP freeze candidate 的人工复核与 release candidate checklist。

本阶段回答：

1. MVP freeze candidate 是否具备进入人工复核的证据边界。
2. Codex B 应如何审核 freeze report 与 decision record。
3. Codex C 是否需要抽样复验 Hermes CLI / API 场景。
4. release candidate checklist 应包含哪些只读证据、Go / No-Go 条件与签核字段。

本阶段不回答：

1. 是否可以 production rollout。
2. 是否可以执行 repair executor。
3. 是否可以默认扫描真实 reports / reviews。
4. 是否可以修改业务数据。

## 2. 边界定义

### 2.1 MVP freeze candidate

MVP freeze candidate 表示当前能力链路可以进入人工审阅候选状态。

它只代表：

1. 核心能力已有可复现 dry-run / eval / smoke 证据。
2. Go / No-Go 条件可被人工检查。
3. known risks 已被显式列出。
4. 后续可由 Codex B / Codex C 做人工审阅与抽样复验。

它不代表：

1. production rollout ready。
2. repair executor approved。
3. facts 可以替代 retrieval evidence。
4. 完整 RBAC / ABAC、生产级 runbook、生产 cron 或自动 repair 已完成。

### 2.2 Release candidate checklist

Release candidate checklist 是人工审阅用的证据清单。

它只记录：

1. 输入证据是否齐全。
2. 当前状态是否满足 MVP freeze candidate。
3. warnings / known risks 是否被人工接受或标记为 No-Go。
4. Codex B / Codex C 的审阅和复验结论。

它不生成 production rollout artifact，不写 DB，不执行 repair。

## 3. 输入证据清单

release candidate checklist 应显式引用下列证据，而不是默认扫描真实目录：

1. Phase 2.29a freeze report dry-run JSON。
2. Phase 2.29b decision record dry-run JSON。
3. Phase 2.14 API deterministic eval summary。
4. Phase 2.14b / 2.20a CLI smoke summary。
5. Phase 2.25a readiness audit dry-run summary。
6. Phase 2.26a repair plan dry-run summary。
7. Phase 2.26b archive / trend diff summary。
8. Phase 2.27 review / audit / linkage summary。
9. Codex B manual review note。
10. Codex C sampled terminal validation note，若需要声明真实终端 MVP candidate 验证。

## 4. Codex B 人工审核标准

Codex B 审核应至少检查：

1. freeze report 的 `status`、`destructive_actions`、`production_rollout`、`repair_executed` 字段。
2. decision record 的 `decision_status`、`mvp_freeze_candidate`、`manual_review_required`、`production_rollout`、`repair_approved` 字段。
3. `pass` 是否只被解释为 MVP freeze candidate，不被解释为 production rollout。
4. `warn` 是否进入人工审阅，而不是自动通过。
5. `fail` 是否保持 No-Go。
6. facts 是否保持 `facts_as_answer=false`，不得替代 retrieval evidence。
7. report / review / audit linkage 是否只使用 sanitized summary，不泄露 notes、reason、approved_action、item-level entity details 或本机绝对路径。
8. 是否保留 stale confirmed fact、soft policy、专用 rerank key smoke 等 known risks。
9. 是否未执行 repair、backfill、reindex、cleanup、delete 或 DB mutation。

## 5. Codex C 抽样复验建议

Phase 2.29d planning 本身不需要 Codex C 真实终端验收。

如果后续要声明“真实 Hermes 终端 MVP candidate 已通过”，建议 Codex C 抽样复验：

1. API / CLI health。
2. active document scope 与 file alias。
3. A/B compare 不混入第三份文件。
4. missing alias suppress retrieval。
5. stale alias / stale source warning。
6. Excel sheet / cell citation。
7. PPTX slide citation。
8. meeting transcript 不被标记为 fact。
9. confirmed facts auxiliary context 保持 `facts_as_answer=false`。
10. fact-only query 不触发无关 retrieval。

Codex C 复验仍不代表 production rollout，只作为 MVP candidate 人工验收证据。

## 6. Release Candidate Checklist 草案

### 6.1 Evidence completeness

1. Phase 2.14 full eval 通过，或失败项有明确 No-Go / manual review 记录。
2. governance / facts eval 通过。
3. CLI smoke 通过，或 skipped 项有明确替代覆盖。
4. readiness audit dry-run 为 pass / warn，且 warning 已人工记录。
5. repair plan dry-run 无 critical；stale facts / missing sources / index inconsistencies 已登记。
6. freeze report dry-run 使用显式输入，不默认扫描真实 reports / reviews。
7. decision record 已生成，并且未把 `warn` 自动升级为 MVP candidate。

### 6.2 Safety invariants

1. `production_rollout=false`。
2. `repair_approved=false`。
3. `repair_executed=false`。
4. `destructive_actions=[]`。
5. `facts_as_answer=false`。
6. 不写业务 DB。
7. 不修改 facts、document_versions、OpenSearch、Qdrant。
8. 不执行 repair / backfill / reindex / cleanup / delete。
9. 不创建 production cron / scheduler。
10. 不默认扫描真实 reports / reviews。

### 6.3 Data governance

1. latest / superseded version filtering 仍稳定。
2. explicit historical version query 仍可诊断 stale version。
3. audit / access policy 仍是 soft placeholder，不等于完整 RBAC / ABAC。
4. confirmed facts 只作为 auxiliary context，不替代 retrieval evidence。
5. stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e` 继续保留为 warning，除非后续单独 review / repair phase 处理。
6. 专用 `ALIYUN_RERANK_API_KEY` smoke 仍为可选尾项，不阻塞 MVP freeze candidate。

### 6.4 Sign-off fields

建议 release candidate checklist 至少包含：

1. `checklist_id`
2. `generated_at`
3. `reviewer`
4. `reviewed_at`
5. `checklist_status`
6. `freeze_report_ref`
7. `decision_record_ref`
8. `codex_b_decision`
9. `codex_c_validation_required`
10. `codex_c_validation_ref`
11. `go_no_go_reasons`
12. `accepted_warnings`
13. `residual_risks`
14. `next_recommendation`
15. `production_rollout=false`
16. `repair_approved=false`
17. `destructive_actions=[]`

## 7. Go / No-Go 规则

### 7.1 Go for MVP freeze candidate manual review

可以进入 MVP freeze candidate manual review 的条件：

1. freeze report 与 decision record 均来自显式输入。
2. 核心 eval / smoke / readiness / repair plan evidence 齐全。
3. `production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`。
4. known risks 已列入 checklist。
5. Codex B 完成人工审核。

### 7.2 Needs manual review

以下情况必须进入 manual review，不得自动通过：

1. freeze report 为 `warn`。
2. readiness audit 存在 warning。
3. repair plan 存在 stale fact / missing source / index inconsistency。
4. CLI smoke 存在 skipped 或替代覆盖。
5. Codex C 验收尚未执行但对外口径需要“真实终端通过”。

### 7.3 No-Go

以下情况必须 No-Go：

1. freeze report 或 decision record 为 fail / no_go。
2. evidence 中出现 `production_rollout=true`。
3. evidence 中出现 `repair_executed=true` 或 `repair_approved=true`。
4. `destructive_actions` 非空。
5. facts 被描述为可替代 retrieval evidence。
6. 需要真实 DB mutation 才能得出结论。
7. 需要 repair / backfill / reindex / cleanup / delete。
8. 需要默认扫描真实 reports / reviews 才能得出结论。

## 8. 推荐下一步

推荐下一步先做 Phase 2.29d planning baseline。

baseline 后可进入 Phase 2.29e，范围建议为：

1. release candidate checklist dry-run runner。
2. 显式读取 freeze report / decision record / evidence summary。
3. 输出 checklist JSON。
4. 保持 `production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`。

不建议直接进入 production rollout、repair executor 或自动 facts 抽取。

## 9. 规划结论

Phase 2.29d 的结论是：可以规划 MVP freeze candidate manual review / release candidate checklist，但不能把该 checklist 解释为 production rollout readiness。

当前建议：

1. 进入 Phase 2.29d planning baseline。
2. baseline 后再由 Codex B 审核是否进入 Phase 2.29e checklist dry-run 最小实现。
3. Codex C 仅在后续需要声明真实终端 MVP candidate 验证时参与抽样复验。
