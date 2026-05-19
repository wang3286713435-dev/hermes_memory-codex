# Active Phase

- 当前 phase：Phase 2.99a Codex B Review Fix: Office Extension Missing Evidence Coverage。
- 背景：Phase 2.98 baseline 已完成：commit `40f71b9`，tag `phase-2.98-standard-agent-boundary-review-baseline`，pushed=true。
- 本轮目标：修复 Codex B review 发现的 `docx` / `xlsx` 正文类问题误落入 `current_lineage` 覆盖缺口；不扩大 runtime 能力。
- 修改文件：`app/services/asset_catalog/standard_answer_boundary.py`、`app/services/asset_catalog/__init__.py`、`tests/test_data_steward_standard_answer_boundary.py`、`docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：已用 TDD 补充 `docx` / `xlsx` 回归测试，并将 Office 扩展名正文类问题统一归入 `missing_evidence` + `full_text_evidence`。
- 测试结果：Phase 2.99a RED 已观察；目标测试 `11 passed`；py_compile 通过；相邻 Data Steward 回归 `12 passed`；explicit probe 显示 `docx/xlsx/pptx/pdf` 均返回 `missing_evidence ('full_text_evidence',)`；`git diff --check`、latest JSON parse、latest ignore check 与 `git status --short` 已复核。
- live smoke 结果：未执行；Phase 2.99 不运行 Gateway smoke、DB/NAS live smoke 或 parser/writer smoke。
- 当前结论：Phase 2.99a 小修已完成，尚未 baseline；需要 Codex B 复核。
- 阻塞点 / 风险点：该模块仍只是本地边界 artifact，不是 runtime prompt deployment；future 能力仍不得进入当前回答承诺。
- 是否建议 baseline：否；先等待 Codex B review。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.100 或 rollout。
- 下一轮建议：Codex B 复核 Phase 2.99a；通过后再执行 selective baseline。
- 是否需要 Codex B 审核：是。
- 是否需要 Codex C 真实终端验收：否；本阶段只需本地目标测试，不需要真实 Gateway / DB / NAS smoke。
- 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、真实 DB writer smoke、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Hermes memory 写 NAS 内容、Agent answer integration、repair、reindex、delete、migration、production rollout。
