# NEXT_CODEX_A_PROMPT

## Phase 2.62 Selective Git Baseline Prompt

你是 Codex A。本轮只执行 Phase 2.62 Internal MVP Issue Triage Summary Runner 的 selective Git baseline。

## Codex B Review 结论

Codex B 已完成 review，结论：通过，可以 baseline。

复核结果：

1. `scripts/phase262_mvp_issue_triage_summary.py` 复用 Phase 2.61a issue validator 语义。
2. `--input-json` 支持重复输入。
3. `--input-dir` 只读取一层 `*.json`，不读取 Markdown / 图片 / 日志 / docx / xlsx 正文。
4. 默认只写 stdout；`--output-json` 必须显式提供。
5. summary 固定包含 dry-run / read-only / no mutation safety fields。
6. P0 / dangerous flags 输出 `no_go`。
7. P1 / ordinary validation error / invalid JSON 输出 `pause`。
8. P2 / P3 clean issues 输出 `ready`。
9. `issue_refs` 不包含 raw query、notes、expected_behavior、actual_behavior、本地完整路径、returned_document_ids、evidence_chunk_ids。
10. 本阶段未读取真实 issue records、未创建外部 issue、未写 DB/index、未 repair、未 rollout。

Codex B 已复跑：

```bash
uv run python -m py_compile scripts/phase262_mvp_issue_triage_summary.py
uv run pytest tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase262_review_check.json
```

结果：py_compile passed；pytest `19 passed`；diff check passed；latest JSON check passed。

## 本轮目标

只做 Git baseline，不进入 Phase 2.63，不实现 operator daily workflow，不读取真实 issue records。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
uv run python -m py_compile scripts/phase262_mvp_issue_triage_summary.py
uv run pytest tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase262_baseline_check.json
```

## Baseline 白名单

只允许 stage 以下文件：

1. `scripts/phase262_mvp_issue_triage_summary.py`
2. `tests/test_phase262_mvp_issue_triage_summary.py`
3. `docs/PHASE262_MVP_ISSUE_TRIAGE_SUMMARY_PLAN.md`
4. `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/NIGHTLY_SPRINT_QUEUE.md`
9. `docs/NEXT_CODEX_A_PROMPT.md`
10. `docs/TODO.md`
11. `docs/DEV_LOG.md`

## 必须排除

不得 stage 以下文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. `reports/internal_mvp_issues/**/*.json`
6. `reports/internal_mvp_issues/**/*.md`
7. `reports/internal_mvp_issues/**/*.png`
8. `reports/internal_mvp_issues/**/*.log`
9. 任何真实 issue record、真实 upload / smoke / business evidence record。

## Commit / Tag

Commit message：

```text
chore: add phase 2.62 issue triage summary runner
```

Tag：

```text
phase-2.62-issue-triage-summary-baseline
```

推送：

```bash
git push origin main
git push origin phase-2.62-issue-triage-summary-baseline
```

## 硬边界

1. 不生成真实 issue records。
2. 不读取真实 reports / run records。
3. 不上传文件。
4. 不执行 API / CLI smoke。
5. 不写 DB / facts / document_versions / audit_logs。
6. 不写 OpenSearch / Qdrant / MinIO。
7. 不 cleanup / delete / repair / backfill / reindex / migration。
8. 不创建外部 issue / Linear / GitHub issue。
9. 不进入 DB / NAS / Data Steward / BIM / TB 文件池。
10. 不进入 production rollout。
11. 不修改 retrieval contract、facts contract、version governance、memory kernel 主架构。

## 完成后必须停止

baseline 完成后更新 `reports/agent_runs/latest.json` 为 ignored 本地状态，记录 commit、tag、push result 与 final status，然后停止。

下一阶段候选：Phase 2.63 operator daily summary workflow，或 Data Steward DB Branch Intake / PR Review。不得自动进入。
