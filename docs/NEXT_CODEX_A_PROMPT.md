# NEXT_CODEX_A_PROMPT

## Phase 2.61b Git Baseline Prompt

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.61b Local Issue Storage Policy docs-only baseline。

Codex B 已审核通过：

1. `docs/PHASE261B_ISSUE_STORAGE_POLICY_PLAN.md` 只做本地 issue records ignored storage policy 规划。
2. 规划明确真实 issue JSON / Markdown 默认不入 Git。
3. 规划明确后续 Phase 2.61c 最小候选只提交 `reports/internal_mvp_issues/.gitignore` 与 `README.md`。
4. 未写代码、未写 DB/index、未创建外部 issue、未执行 repair/backfill/reindex、未进入 rollout 或 Data Steward。

本轮不要进入 Phase 2.61c，不要创建 `reports/internal_mvp_issues/`，不要生成真实 issue records。

## 本轮目标

Phase 2.61b Local Issue Storage Policy Planning 收口与 Git baseline。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/PHASE261B_ISSUE_STORAGE_POLICY_PLAN.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. `reports/agent_runs/latest.json`

## 允许提交的白名单文件

只允许 stage / commit 下列 Phase 2.61b 文件：

1. `docs/PHASE261B_ISSUE_STORAGE_POLICY_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

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
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase261b_baseline_check.json
```

stage 后运行：

```bash
git diff --cached --check
git diff --cached --name-only
```

期望 staged 文件只包含白名单 8 个 tracked docs 文件。

## Git baseline 步骤

1. 确认 dirty 中除白名单外只有历史无关 dirty / DB 草稿，且不得 stage。
2. selective stage 白名单文件。
3. commit：

```bash
git commit -m "docs: baseline phase 2.61b issue storage policy"
```

4. tag：

```bash
git tag phase-2.61b-issue-storage-policy-baseline
```

5. push 当前分支与 tag：

```bash
git push origin HEAD
git push origin phase-2.61b-issue-storage-policy-baseline
```

6. 更新 ignored `reports/agent_runs/latest.json`：
   - `phase`: `Phase 2.61b Local Issue Storage Policy Planning`
   - `status`: `baseline`
   - `git.commit`: 当前 commit hash
   - `git.tag`: `phase-2.61b-issue-storage-policy-baseline`
   - `git.pushed`: `true`
   - `needs_codex_b_review`: `false`
   - `needs_codex_c_validation`: `false`
   - `next_recommendation`: 进入 Phase 2.61c local issue storage artifact，或继续 Mac mini internal MVP operator polish；不得进入 rollout。

7. 最终确认：

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
7. 不创建真实 issue records。
8. 不创建 `reports/internal_mvp_issues/`；该目录留到 Phase 2.61c。
9. 不进入 DB / NAS / Data Steward / BIM / TB 文件池。
10. 不进入 production rollout。
11. 不修改 retrieval contract、facts contract、version governance、memory kernel 主架构。
12. 不 stage 历史无关 dirty 或 DB 草稿。

## 完成后停止

完成 baseline 后立即停止，输出：

1. commit hash
2. tag
3. push 结果
4. final `git status --short`
5. 是否确认未上传文件 / 未写 DB / 未执行 API/CLI smoke / 未创建外部 issue / 未创建真实 issue records
6. 下一步建议
