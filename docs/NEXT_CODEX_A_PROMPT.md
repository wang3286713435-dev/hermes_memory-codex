# NEXT_CODEX_A_PROMPT

## Phase 2.65 Mac mini MVP Landing Pack Git Baseline

Codex B review 通过。Phase 2.65 Mac mini MVP Landing Pack 与 reviewed-ref fix 已满足 baseline 条件。

本轮只做 selective Git baseline。不要继续开发新功能，不执行 Mac mini 安装，不启动服务，不运行 API/CLI smoke，不进入 Phase 2.66。

## Codex B Review 结论

通过，可以 baseline。

Review 结果：

1. Release manifest helper 保持只读、离线、无副作用。
2. `hermes-agent` reviewed ref 已 pin 为：
   - `phase-2.56e-natural-import-real-upload-smoke-baseline`
3. Reviewed-ref manifest 结果：
   - `status=ready_for_operator_review`
   - `pause_reasons=[]`
4. Placeholder-ref manifest 结果：
   - `status=pause`
   - `pause_reasons=["missing_reviewed_hermes_agent_ref"]`
5. 文档仍禁止真实 DB smoke、NAS scan、Data Steward feature activation、repair、cleanup、backfill、reindex、delete、migration 和 production rollout。
6. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 是历史无关 dirty，必须继续排除。

Codex B 已复跑：

```bash
uv run python -m py_compile scripts/phase265_mvp_release_manifest.py
uv run pytest tests/test_phase265_mvp_release_manifest.py tests/test_phase260_mvp_local_readiness_pack.py tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
uv run python scripts/phase265_mvp_release_manifest.py --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline --operator codex-b | python3 -m json.tool
uv run python scripts/phase265_mvp_release_manifest.py --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline --hermes-agent-ref NEEDS_REVIEWED_AGENT_REF --operator codex-b | python3 -m json.tool
git diff --check
python3 -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase265_b_review_check.json
```

结果：

- py_compile 通过。
- 目标 pytest `41 passed`。
- reviewed-ref manifest `ready_for_operator_review`，无 pause reasons。
- placeholder-ref manifest `pause/missing_reviewed_hermes_agent_ref`。
- `git diff --check` 通过。
- latest JSON 校验通过。

## 本轮目标

只做 Git baseline。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
uv run python -m py_compile scripts/phase265_mvp_release_manifest.py
uv run pytest tests/test_phase265_mvp_release_manifest.py tests/test_phase260_mvp_local_readiness_pack.py tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
uv run python scripts/phase265_mvp_release_manifest.py --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline --operator codex-a | python3 -m json.tool
uv run python scripts/phase265_mvp_release_manifest.py --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline --hermes-agent-ref NEEDS_REVIEWED_AGENT_REF --operator codex-a | python3 -m json.tool
git diff --check
python3 -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase265_baseline_check.json
```

## Baseline 白名单

只允许 stage 以下文件：

1. `scripts/phase265_mvp_release_manifest.py`
2. `tests/test_phase265_mvp_release_manifest.py`
3. `docs/PHASE265_MAC_MINI_MVP_LANDING_PLAN.md`
4. `docs/MAC_MINI_MVP_INSTALL_UPDATE_QUICKSTART.md`
5. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
6. `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`
7. `docs/ACTIVE_PHASE.md`
8. `docs/PHASE_BACKLOG.md`
9. `docs/HANDOFF_LOG.md`
10. `docs/NIGHTLY_SPRINT_QUEUE.md`
11. `docs/NEXT_CODEX_A_PROMPT.md`
12. `docs/TODO.md`
13. `docs/DEV_LOG.md`

## 必须排除

不得 stage 以下文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`
3. 任何真实 DB / NAS / Mac mini smoke 输出。
4. 任何 secrets / `.env` / raw logs。
5. 任何业务数据、真实上传文件或 report artifacts。

## Commit / Tag

Commit message：

```text
chore: add phase 2.65 mac mini mvp landing pack
```

Tag：

```text
phase-2.65-mac-mini-mvp-landing-baseline
```

Push：

```bash
git push origin HEAD
git push origin phase-2.65-mac-mini-mvp-landing-baseline
```

## 硬边界

1. 不执行真实 Mac mini deployment。
2. 不启动 Docker 服务。
3. 不运行 API / CLI smoke。
4. 不连接真实 DB。
5. 不扫描 NAS。
6. 不上传真实文件。
7. 不写 DB / facts / document_versions / audit_logs。
8. 不写 OpenSearch / Qdrant / MinIO。
9. 不执行 repair / cleanup / backfill / reindex / delete / migration。
10. 不进入 Data Steward DB smoke。
11. 不创建 PR。
12. 不进入 production rollout。
13. 不进入 Phase 2.66。

## 完成后必须停止

baseline 完成后更新 ignored `reports/agent_runs/latest.json`，记录 commit、tag、push result 和 final status，然后停止。

下一步建议：把 Mac mini install prompt / quickstart 交给 Mac mini 侧 Codex/operator 执行实机安装；主线继续围绕 MVP 真实可用性收敛，不进入 production rollout。
