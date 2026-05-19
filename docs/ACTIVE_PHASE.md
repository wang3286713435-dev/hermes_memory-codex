# Active Phase

- 当前 phase：Phase 2.102a Eval Inventory Manifest。
- 背景：Phase 2.102 baseline 已完成：commit `a5c1490`，tag `phase-2.102-metric-evaluation-evidence-pack-baseline`，pushed=true。
- 本轮目标：创建 committed eval inventory manifest，定义稳定 question IDs、groups、source categories、evidence/citation expectations 与 metric eligibility，为后续 Top5 / citation scoring 建立 denominator seed。
- 修改文件：`eval/phase2_inventory/phase2_eval_inventory_manifest.json`、`docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已新增 starter inventory，共 19 个 accepted cases、15 个 metric-eligible cases、4 个 metric-ineligible cases，覆盖 12 个 required groups；Gateway / Data Steward / Missing Evidence / natural import 保持 ineligible 边界。
- 测试结果：manifest JSON parse 通过；`git diff --check` 通过；latest JSON parse 通过；latest ignore check 通过；`git status --short --untracked-files=all` 已复核。
- live smoke 结果：不适用；本阶段 docs/data-manifest only，未运行 API / CLI / Gateway / DB / NAS smoke。
- 当前结论：Phase 2 closeout readiness 仍为否；Phase 2.102a 只建立 inventory，不计算 Top5 / citation accuracy，不声称 PRD 100+ / Roadmap 300+ 已满足。
- 阻塞点 / 风险点：PRD 100+ / Roadmap 300+ 仍未达标；Top5、citation accuracy、structured fact manual spot-check 仍未计算；official account / PDF / HTML parser evidence 仍不完整；无关 untracked `docs/digital-delivery-standards/` 未纳入本轮。
- 是否建议 baseline：暂不建议；先交 Codex B review。
- 是否建议进入下一阶段：否；下一步只做 review / selective baseline 决策。
- 下一轮建议：Codex B review `eval/phase2_inventory/phase2_eval_inventory_manifest.json` 与 `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`；通过后由用户明确授权 docs/data baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：当前不需要；后续 metric scoring / live validation 阶段可能需要。
- 当前仍禁止：runtime code、测试修改、Agent DB CRUD、Agent 生成 SQL、真实 DB / NAS / API / Gateway smoke、前端直连 Hermes raw/internal endpoints、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
