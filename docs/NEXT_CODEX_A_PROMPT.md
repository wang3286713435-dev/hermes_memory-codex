# NEXT_CODEX_A_PROMPT

## Phase 2.63 Selective Git Baseline Prompt

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.63 Internal MVP Operator Daily Summary Workflow 的 selective Git baseline。

## Codex B Review 结论

Codex B 已完成 review，结论：通过，可以 baseline。

复核结果：

1. `scripts/phase263_mvp_operator_daily_summary.py` 可从 Phase 2.62 summary JSON 生成 daily summary。
2. 直接读取 issue JSON 或 `--input-dir` 时复用 Phase 2.62 `build_summary()`，没有复制验证逻辑。
3. `ready` / `pause` / `no_go` 语义符合 P0/P1/P2/P3 与 invalid input 规则。
4. Markdown 输出脱敏，不包含 raw query、notes、expected / actual behavior、full path、document ids、chunk ids。
5. `--output-json` / `--output-md` 必须显式提供才写文件。
6. fixed safety fields 保持 `dry_run=true`、`read_only=true`、`production_rollout=false`、`repair_attempted=false`、`external_issue_created=false`、`db_or_index_written=false`。
7. 本阶段未读取真实 issue records、未调用 API/CLI、未写 DB/index、未 repair、未 rollout。

Codex B 已复跑：

```bash
uv run python -m py_compile scripts/phase263_mvp_operator_daily_summary.py
uv run pytest tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase263_review_check.json
```

结果：py_compile passed；pytest `28 passed`；diff check passed；latest JSON check passed。

## 本轮目标

只做 Git baseline，不进入 Phase 2.64，不执行 DB Branch Intake，不读取真实 issue records。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
uv run python -m py_compile scripts/phase263_mvp_operator_daily_summary.py
uv run pytest tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase263_baseline_check.json
```

## Baseline 白名单

只允许 stage 以下文件：

1. `scripts/phase263_mvp_operator_daily_summary.py`
2. `tests/test_phase263_mvp_operator_daily_summary.py`
3. `docs/PHASE263_MVP_OPERATOR_DAILY_SUMMARY_PLAN.md`
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
chore: add phase 2.63 operator daily summary
```

Tag：

```text
phase-2.63-operator-daily-summary-baseline
```

推送：

```bash
git push origin main
git push origin phase-2.63-operator-daily-summary-baseline
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

下一阶段建议：Phase 2.64 Data Steward DB Branch Intake / PR Review，用于对接数据库开发团队；不得自动进入，需等待 Codex B / 用户确认。
