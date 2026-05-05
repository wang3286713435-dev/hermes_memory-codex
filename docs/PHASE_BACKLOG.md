# Phase Backlog

## 当前优先级

1. Phase 2.41 MVP Pilot Evidence Review / Go-No-Go planning 已完成，等待 Codex B review。
2. 下一轮建议仅做 Phase 2.41 docs-only baseline；不要直接进入新能力开发、rollout、repair executor、Data Steward 实现或 Pilot 扩大执行。
3. Phase 2.40a PRD Acceptance Matrix / MVP Evidence Pack artifact baseline 已完成，commit `e6f7fc2`，tag `phase-2.40a-prd-acceptance-matrix-artifact-baseline`。
4. Phase 2.40 PRD Acceptance Matrix / MVP Evidence Pack planning baseline 已完成，commit `1383155`，tag `phase-2.40-prd-acceptance-matrix-plan-baseline`。
5. Phase 2.39 Data Steward / BIM 数据管家 docs-only baseline 已完成：Data Steward 明确为后置产品线，不并入当前 MVP Pilot，不新增 DB schema、Neo4j、PostGIS、空间索引代码或生产级 scheduler。
6. Phase 2.38a：Tender P1 Source Availability Audit Git baseline 已完成，commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
7. Phase 2.38b：Tender P1 Concrete Source Recall Diagnostics 已完成最小实现并通过 Codex B review。
8. 只读 live preview 结果：资质与业绩 candidate source 已在 top-k，人员要求 candidate source 可检索但低排名；限价继续 Missing Evidence，项目经理等级继续人工复核。
9. Phase 2.38d 最小实现、review fix、Q1 intent fix、主仓 answer guard、safe fallback contract 与 runtime post-answer guard 已通过 Codex C Q1/Q2/Q3 真实终端复验；已完成 Git baseline，不得直接进入 broad retrieval fix、repair、rollout 或索引重建。

## Day-1 Pilot 已知问题

1. P1 retrieval recall：`@主标书` 最高投标限价 / 招标控制价 / 投标报价上限未召回具体金额。
2. P1 retrieval recall：`@主标书` 投标资质具体等级 / 类别未召回。
3. P1 partial：项目经理、联合体、业绩、人员要求已有相关 evidence，但仍需人工复核。
4. P2 latency：会议纪要决策 / 风险与公司方向分析长输出偏慢。
5. Pilot 期间所有经营建议必须保留人工决策声明，不得当成自动经营决策。

## Phase 2.35 当前状态

1. Phase 2.35 最小实现已完成，目标测试 `22 passed`。
2. Codex C 复验显示安全边界通过：无编造、facts/transcript 均未替代 evidence。
3. Phase 2.35b 已完成 metadata precision 小修：限价需具体金额，资质需具体等级 + 类别。
4. Phase 2.35b 已新增 API trace 顶层 profile 字段：`metadata_guided_query_profile`、`metadata_deep_field_profile`。
5. alias 首次绑定不稳定已在 Codex C 真实 CLI 中复现：bind 成功后正式 Q1/Q2 变为 `alias_missing=true / retrieval_suppressed=true`。
6. Phase 2.35c 已完成主仓库最小修复：`上一轮已锁定的当前文件` 等说法现在会走 current-document bind / current retrieval fallback，不再被误当成标题或历史上下文。
7. Codex C 真实终端复验通过：session `20260429_165301_e3c312` 中正式 Q1/Q2 均为 `alias_resolved`，`alias_missing=false`，`retrieval_suppressed=false`。
8. Phase 2.35c Git baseline 已完成：Hermes_memory commit `ec77c96`，Hermes 主仓库 commit `ead4e899`，tag `phase-2.35c-alias-session-baseline`。
9. Phase 2.35c baseline 只能声明 alias/session 修复收口；deep-field recall 与 trace 透出仍不完全收口。

## Phase 2.36 规划入口

1. 目标：把 Phase 2.35c 剩余 tail item 分清是“真实缺字段 / 章节召回不足 / trace 展示问题 / 需人工复核”。
2. 重点字段：最高投标限价 / 招标控制价 / 投标报价上限、投标资质具体等级 / 类别、项目经理等级 / B 证、联合体、类似业绩、人员数量 / 专业 / 资质。
3. 推荐方向：优先规划 section-targeted retrieval diagnostics 与 trace polish，不直接扩大到完整自动审标。
4. 规划阶段不需要 Codex C；只有进入实现并影响真实终端输出后才需要真实 CLI 复验。

## Phase 2.36a / 2.36b 当前状态

1. Phase 2.36a Hermes_memory retrieval-layer trace diagnostics 已完成并通过 Codex B review，目标测试合计 `30 passed`。
2. Codex C 真实终端抽样显示 Q1/Q2 安全边界正常、无编造，但终端 trace 仍为 `metadata_deep_field_profile=null`、`deep_field_profile=null`、`deep_field_diagnostics=null`。
3. 失败定位转入 Hermes 主仓库 adapter / kernel / context_builder trace 映射与展示层。
4. Codex C 指定 Step 1 一步绑定 prompt 仍失败：`请在企业记忆中锁定“...”，并绑定为 @主标书` 未被 alias bind parser 稳定识别。
5. 下一步 Phase 2.36b 只做主仓库消费层 / 展示层最小修复；不扩大 Hermes_memory retrieval 逻辑，不进入真实业务数据写入。
6. Phase 2.36b 主仓库最小实现已完成：adapter / kernel / context_builder 可提升并渲染 deep-field trace，session scope parser 支持 `绑定为 / 绑定成` 与中文弯引号标题。
7. Phase 2.36b 目标测试通过：主仓库 py_compile 通过，`tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py` 为 `59 passed`。
8. Codex C 终端复验显示 Phase 2.36b 的一步 alias binding 与 terminal-visible trace 已基本通过：Q1/Q2 分别显示 `pricing_scope` / `qualification_scope` 与 diagnostics。
9. Phase 2.36b 暂不 baseline：Q1 diagnostics 出现 concrete found 与答案 Missing Evidence 不一致；Q2 对“一级注册建造师电子证书要求”存在过度表述为项目经理等级的风险。
10. Phase 2.36c 已完成 Hermes_memory 最小修复：final retrieval evidence 会重新校正 concrete evidence，metadata anchor 不足时输出保守 Missing Evidence diagnostics。
11. Phase 2.36c 已补项目经理等级边界：电子证书格式 / 材料条款不能作为 explicit role-level requirement。
12. Phase 2.36c 目标测试 `33 passed`；Codex B review 已通过。
13. Codex C 真实终端复验已通过：session `20260430_123308_6660a8` 中 Step 1 alias binding 成功，Q1 限价 diagnostics 与 Missing Evidence 一致，Q2 未把电子证书 / 材料条款推断为项目经理等级。
14. Phase 2.36c Git baseline 已完成：commit `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。
15. deep-field recall 仍 partial，真实限价金额、具体资质等级 / 类别、业绩、人员数量继续作为后续尾项，不得写成完整自动审标能力收口。

## Phase 2.37 规划入口

1. 目标：把 Day-1 / Codex C / 用户真实试用反馈转成结构化 issue intake records。
2. 推荐先做 issue intake / triage，而不是继续盲修 deep-field recall。
3. issue_type 至少覆盖 retrieval_recall、trace_ux、latency、alias_session、contamination_false_positive、missing_evidence_expected、answer_boundary。
4. priority 规则必须保留 P0/P1/P2/P3，P0 包括编造、facts/transcript 替代 evidence、跨文件污染、权限泄露和自动决策越界。
5. Phase 2.37 规划已完成，新增 `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`。
6. 推荐 Phase 2.37a：local issue intake schema / templates / dry-run validator or summary generator。
7. Phase 2.37a 仍不得自动修复 issue、写 DB / facts / document_versions、修改 OpenSearch / Qdrant、进入 rollout 或做自动审标结论。
8. Phase 2.37 planning Git baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
9. Phase 2.37a 入口已写入 `docs/NEXT_CODEX_A_PROMPT.md`：local issue intake schema / template / dry-run validator + summary generator。
10. Phase 2.37a 最小实现已完成：本地 intake 工具支持 template、单文件 / 目录读取、schema 校验、triage summary 与 strict invalid exit。
11. Phase 2.37a 目标验证通过：py_compile 通过，`tests/test_phase237a_pilot_issue_intake.py` 为 `9 passed`，临时 dry-run smoke 通过。
12. 下一步需 Codex B review；通过后只做 Phase 2.37a Git baseline，不直接进入 deep-field recall 修复、repair 或 rollout。
13. Phase 2.37a Git baseline 已完成：commit `1e1ca45`，tag `phase-2.37a-pilot-issue-intake-baseline`。
14. Phase 2.37b 最小 runbook / storage convention 已完成：新增 `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md` 与 `reports/pilot_issues/` ignore / README 策略。
15. Phase 2.37b 验证通过：`git diff --check` 通过，template / strict dry-run 命令通过，`reports/pilot_issues/example.json` 被 git ignore 命中。
16. 下一步需 Codex B review；通过后只做 Phase 2.37b docs baseline，不直接进入 P1 修复、repair 或 rollout。
17. Phase 2.37b Git baseline 已完成：commit `e8c0631`，tag `phase-2.37b-pilot-issue-intake-runbook-baseline`。
18. Phase 2.37c planning 已完成：新增 `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`，规划 daily / per-round triage summary、P0/P1/P2/P3 分诊、首批 known issue 候选与后续 Phase 2.37d 方向。
19. 下一步需 Codex B review；通过后只做 Phase 2.37c docs baseline，不直接进入 P1 fix、repair、rollout 或外部 issue 创建。
20. Phase 2.37c Git baseline 已完成：commit `4aa6bd4`，tag `phase-2.37c-pilot-issue-triage-summary-plan-baseline`。
21. Phase 2.37d 最小实现已完成：新增本地 triage summary generator，读取 `reports/pilot_issues/*.json` 并输出 ignored 的 JSON / Markdown summary；目标测试 `9 passed`，`git diff --check` 通过。
22. Phase 2.37d Git baseline 已完成：commit `d97a67c`，tag `phase-2.37d-pilot-triage-summary-baseline`。
23. Phase 2.38a 最小实现已完成：新增只读 source availability audit runner，字段覆盖限价、资质等级/类别、项目经理等级、类似业绩、人员要求；目标测试 `10 passed`。
24. Phase 2.38a Git baseline 已完成：commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
25. Codex B localhost 覆写 read-only live audit 显示：`price_ceiling=anchor_only`，`qualification_grade_category=concrete_source_found`，`project_manager_level=ambiguous`，`performance_requirement=concrete_source_found`，`personnel_requirement=concrete_source_found`。
26. Phase 2.38b 最小实现已完成：新增只读 concrete recall diagnostics runner，目标测试 `9 passed`，`git diff --check` 通过。
27. Phase 2.38b localhost read-only preview：`qualification_grade_category=candidate_in_top_k`，`performance_requirement=candidate_in_top_k`，`personnel_requirement=candidate_present_but_low_rank`。
28. `price_ceiling` 保持 `field_should_remain_missing_evidence`；`project_manager_level` 保持 `field_requires_human_review`。
29. Phase 2.38b Codex B review 已通过，下一步只做 Git baseline，不直接进入 2.38c。
30. Phase 2.38b Git baseline 已完成：commit `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`。
31. Phase 2.38c planning 已完成：新增 `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`，结论为人员要求低排名更像 query/profile/candidate-pool tail，不是 source missing。
32. Phase 2.38c 推荐后续 Phase 2.38d：personnel-only aliases / section hints / candidate-pool diagnostics；继续后置限价缺源、项目经理人工复核、broad retrieval tuning、repair 与 rollout。
33. Phase 2.38c Git baseline 已完成：commit `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`。
34. Phase 2.38d 入口已写入 `docs/NEXT_CODEX_A_PROMPT.md`：仅处理 `personnel_requirement` 低排名，禁止顺手处理限价、项目经理等级、broad retrieval tuning、repair、reindex 或 rollout。
35. Phase 2.38d 首轮实现、review-fix 与 Q1 intent fix 已通过 Codex B 复审。
36. Codex C 真实终端复验显示 retrieval / trace 层已修复：Q1/Q2 均为 `personnel_scope`，metadata fields 仅 `personnel_requirement`；Q3 broad query 仍为 `qualification_scope`。
37. Codex C 第二轮复验显示最终回答仍失败：Q1/Q2 会输出项目经理 / 每个项目只能1个 / 类似工程业绩，Q3 人员小节仍有隐式数量过度表述。
38. 主仓第二轮 final answer guard 已完成：`personnel_scope` context block 明确禁止输出项目经理 / 项目负责人 / 注册建造师 / 一级建造师 / B证 / 安全考核证 / 投标资质 / 联合体 / 类似工程业绩，且禁止把角色列表转成隐式数量。
39. 第三轮 structured answer guard 已完成：`personnel_forbidden_answer_terms`、`personnel_count_inference_forbidden=true`、`ignore_non_personnel_content_in_mixed_chunks=true` 已进入 `personnel_scope` context。
40. broad `qualification_scope` 不应误套 personnel-only boundary 的测试已补，主仓目标测试 `12 passed`。
41. 第四轮 safe fallback contract 已完成：若答案草稿含 forbidden terms 或隐式数量推断，context 要求丢弃草稿并输出 Missing Evidence / 人工复核模板。
42. 当前白名单未允许修改 `run_agent.py`；本轮未接入真正 post-answer retry / replacement，仍需 Codex C 真实终端复验。
43. 下一步等待 Codex B review；通过后建议 Codex C 重跑 Q1/Q2/Q3；通过后再由 Codex B 写入 Phase 2.38d Git baseline prompt。

## 后置项

1. 完整 AI 审标 / 自动审标：后置，当前只做 retrieval evidence 与 trace 改善。
2. 长输出 query 延迟优化：需先收集更多 Pilot 样本，不在 Phase 2.35b 中扩大。
3. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
4. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
5. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
6. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
7. rollout readiness：后置，当前仍不进入生产 rollout。
8. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。
9. default real reports / reviews scan：后置，除非用户显式指定输入。
10. production rollout 继续后置；MVP Pilot 不得解释为 production ready。
11. Data Steward 产品化、Building Asset Catalog MVP、建筑本体 / 知识图谱、空间索引、子 Agent 调度与监控面板均后置；当前不新增 DB schema、Neo4j、PostGIS、空间索引代码或生产级 scheduler。

## 永久边界

1. 不擅自修改 retrieval contract。
2. 不擅自修改 memory kernel 主架构。
3. 不执行 destructive repair / delete / cleanup。
4. 不让 facts 自动替代 retrieval evidence。
5. 不创建生产 cron / 定时任务。
6. 每轮开始读取 ACTIVE_PHASE 与 PHASE_BACKLOG。
7. 用户要求执行任务入口时，读取 `docs/NEXT_CODEX_A_PROMPT.md`。
8. 夜间执行时读取 `docs/NIGHTLY_SPRINT_PROTOCOL.md` 与 `docs/NIGHTLY_SPRINT_QUEUE.md`。
9. 每轮结束更新 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json。
10. 夜间 sprint 结束额外写入 ignored 的 `reports/nightly_runs/<timestamp>.json`。
11. planning / implementation / validation / baseline 分阶段推进。
12. baseline 前默认需要 Codex B 审核，除非用户明确授权。
