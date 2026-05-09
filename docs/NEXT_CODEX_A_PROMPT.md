# NEXT_CODEX_A_PROMPT

## Phase 2.61a Git Baseline Prompt

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.61a Internal MVP Issue Intake Runner 的 selective Git baseline。

Codex B 已审核通过：

1. `scripts/phase261a_mvp_issue_intake.py` 是只读本地 issue intake helper。
2. 目标测试通过：`15 passed`。
3. `--new-template` dry-run 输出正常。
4. 未执行真实上传、API/CLI smoke、DB/index 写入、外部 issue 创建、repair/backfill/reindex 或 rollout。

本轮不要进入 Phase 2.61b，不要执行真实 smoke，不要上传文件。

## 本轮目标

Phase 2.61a Internal MVP Issue Intake Runner 收口与 Git baseline。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/PHASE261_INTERNAL_MVP_OPERATOR_FLOW_PLAN.md`
7. `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
8. `scripts/phase261a_mvp_issue_intake.py`
9. `tests/test_phase261a_mvp_issue_intake.py`
10. `reports/agent_runs/latest.json`

## 允许提交的白名单文件

只允许 stage / commit 下列 Phase 2.61 / 2.61a 文件：

1. `scripts/phase261a_mvp_issue_intake.py`
2. `tests/test_phase261a_mvp_issue_intake.py`
3. `docs/PHASE261_INTERNAL_MVP_OPERATOR_FLOW_PLAN.md`
4. `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/NIGHTLY_SPRINT_QUEUE.md`
9. `docs/NEXT_CODEX_A_PROMPT.md`
10. `docs/TODO.md`
11. `docs/DEV_LOG.md`

## 必须排除的文件

不要 stage / commit 下列文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. 任何 `reports/**/*.json`
6. 任何真实 issue record、真实源文件、上传文件、smoke evidence JSON
7. 任何 DB/NAS/Data Steward 分支文件

## 复核命令

baseline 前运行：

```bash
uv run python -m py_compile scripts/phase261a_mvp_issue_intake.py
uv run pytest tests/test_phase261a_mvp_issue_intake.py tests/test_phase260_mvp_local_readiness_pack.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase261a_baseline_check.json
uv run python scripts/phase261a_mvp_issue_intake.py --new-template
```

期望：

1. pytest 为 `15 passed`。
2. template 输出包含 `dry_run=true`、`read_only=true`、`destructive_actions=[]`。
3. `db_or_index_written=false`、`external_issue_created=false`、`repair_attempted=false`、`production_rollout=false`。

## Git baseline 步骤

1. 确认 dirty 中除白名单外只有历史无关 dirty / DB 草稿，且不得 stage。
2. selective stage 白名单文件，注意包含 untracked 脚本、测试和新规划文档。
3. 运行：

```bash
git diff --cached --check
git diff --cached --name-only
```

4. commit：

```bash
git commit -m "chore: add phase 2.61a mvp issue intake runner"
```

5. tag：

```bash
git tag phase-2.61a-mvp-issue-intake-baseline
```

6. push 当前分支与 tag：

```bash
git push origin HEAD
git push origin phase-2.61a-mvp-issue-intake-baseline
```

7. 更新 ignored `reports/agent_runs/latest.json`：
   - `phase`: `Phase 2.61a Internal MVP Issue Intake Runner`
   - `status`: `baseline`
   - `git.commit`: 当前 commit hash
   - `git.tag`: `phase-2.61a-mvp-issue-intake-baseline`
   - `git.pushed`: `true`
   - `needs_codex_b_review`: `false`
   - `needs_codex_c_validation`: `false`
   - `next_recommendation`: 进入 Phase 2.61b / 2.62 主线规划；优先 internal MVP issue storage policy / operator usability polish，不进入 production rollout。

8. 最终确认：

```bash
git status --short
git check-ignore -q reports/agent_runs/latest.json && echo ignored
```

## 硬边界

本轮禁止：

1. 不上传文件。
2. 不执行 API / CLI smoke。
3. 不写 DB / facts / document_versions / audit_logs。
4. 不写 OpenSearch / Qdrant / MinIO。
5. 不 cleanup / delete / repair / backfill / reindex / migration。
6. 不创建外部 issue / Linear / GitHub issue。
7. 不进入 DB / NAS / Data Steward / BIM / TB 文件池。
8. 不进入 production rollout。
9. 不修改 retrieval contract、facts contract、version governance、memory kernel 主架构。
10. 不 stage 历史无关 dirty 或 DB 草稿。

## 完成后停止

完成 baseline 后立即停止，输出：

1. commit hash
2. tag
3. push 结果
4. final `git status --short`
5. 是否确认未上传文件 / 未写 DB / 未执行 API/CLI smoke / 未创建外部 issue
6. 下一步建议
