# Active Phase

- 当前 phase：Phase 2.102 Metric / Evaluation Evidence Pack。
- 背景：Phase 2.101 baseline 已完成：commit `5f15852`，tag `phase-2.101-prd-acceptance-gap-closure-plan-baseline`，pushed=true。
- 本轮目标：把 PRD / Roadmap 的 Phase 2 指标和验收项整理成 evidence pack，明确哪些已有 committed evidence，哪些只是 smoke / partial，哪些缺 numerator / denominator 或 Codex C 复验。
- 修改文件：`docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 Phase 2.102 metric / evidence pack，覆盖 PRD 100+、Roadmap 300+、Top5 80/85、citation 85/90、structured fact manual spot-check 90、permission denial、parser/source categories、Gateway/Data Steward catalog-only、Mac mini / employee trial、natural import、Missing Evidence、facts/transcript/version boundaries。
- 测试结果：`git diff --check` 通过；latest JSON parse 通过；latest ignore check 通过；`git status --short --untracked-files=all` 已复核。
- live smoke 结果：不适用；本阶段 docs-only，未运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2 metric closeout decision=`not_ready`；现有 eval/smoke 证明链路可重复，但没有 PRD/Roadmap 指标所需 numerator / denominator。
- 阻塞点 / 风险点：PRD 100+ / Roadmap 300+ eval inventory、Top5、citation accuracy、structured fact manual spot-check、official account/PDF/HTML parser evidence、employee trial / natural import evidence仍缺 committed metric pack；`docs/digital-delivery-standards/` 当前存在无关 untracked 文件，未纳入本轮。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；下一步只做 review / selective baseline 决策。
- 下一轮建议：Codex B review `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`；通过后由用户明确授权 docs baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：当前不需要；后续 metric scoring / employee trial / parser-source evidence 阶段可能需要。
- 当前仍禁止：runtime code、测试修改、Agent DB CRUD、Agent 生成 SQL、真实 DB / NAS / API / Gateway smoke、前端直连 Hermes raw/internal endpoints、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
