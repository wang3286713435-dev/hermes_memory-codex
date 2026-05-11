# NEXT_CODEX_A_PROMPT

## Phase 2.61c Git Baseline Prompt

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.61c Local Issue Storage Artifact 的 selective Git baseline。

Codex B 已审核通过：

1. `reports/internal_mvp_issues/.gitignore` 默认忽略真实 issue JSON / Markdown / 截图 / 日志 / 表格 / 文档。
2. `reports/internal_mvp_issues/README.md` 明确真实 issue records 默认不入 Git，外部 issue 创建、repair、cleanup、delete、backfill、reindex、rollout 均未授权。
3. 当前目录下只有 `.gitignore` 与 `README.md`，没有真实 issue records。
4. 静态验证通过：`git diff --check`、`latest.json` JSON 校验、sample ignore checks。

本轮不要进入 Phase 2.62，不要生成真实 issue records，不要创建外部 issue。

## 本轮目标

Phase 2.61c Local Issue Storage Artifact 收口与 Git baseline。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `reports/internal_mvp_issues/.gitignore`
7. `reports/internal_mvp_issues/README.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`
10. `reports/agent_runs/latest.json`

## 允许提交的白名单文件

只允许 stage / commit 下列 Phase 2.61c 文件：

1. `reports/internal_mvp_issues/.gitignore`
2. `reports/internal_mvp_issues/README.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

## 必须排除的文件

不要 stage / commit 下列文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. 任何真实 issue JSON / Markdown / 截图 / 日志 / 表格 / 文档
6. 任何真实 upload / smoke / business evidence records
7. 任何 DB/NAS/Data Steward 分支文件

## 复核命令

baseline 前运行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase261c_baseline_check.json
git check-ignore -q reports/internal_mvp_issues/sample.json && echo sample_json_ignored
git check-ignore -q reports/internal_mvp_issues/sample.md && echo sample_md_ignored
git check-ignore -q reports/internal_mvp_issues/screenshot.png && echo sample_png_ignored
git check-ignore -q reports/internal_mvp_issues/README.md || echo readme_not_ignored
git check-ignore -q reports/internal_mvp_issues/.gitignore || echo gitignore_not_ignored
```

stage 后运行：

```bash
git diff --cached --check
git diff --cached --name-only
```

期望 staged 文件只包含白名单 9 个文件。

## Git baseline 步骤

1. 确认 dirty 中除白名单外只有历史无关 dirty / DB 草稿，且不得 stage。
2. selective stage 白名单文件。
3. commit：

```bash
git commit -m "docs: add internal MVP issue storage policy"
```

4. tag：

```bash
git tag phase-2.61c-internal-mvp-issue-storage-baseline
```

5. push 当前分支与 tag：

```bash
git push origin HEAD
git push origin phase-2.61c-internal-mvp-issue-storage-baseline
```

6. 更新 ignored `reports/agent_runs/latest.json`：
   - `phase`: `Phase 2.61c Local Issue Storage Artifact`
   - `status`: `baseline`
   - `git.commit`: 当前 commit hash
   - `git.tag`: `phase-2.61c-internal-mvp-issue-storage-baseline`
   - `git.pushed`: `true`
   - `needs_codex_b_review`: `false`
   - `needs_codex_c_validation`: `false`
   - `next_recommendation`: 继续 Mac mini internal MVP operator polish / issue triage；不得进入 rollout。

7. 最终确认：

```bash
git status --short
git check-ignore -q reports/agent_runs/latest.json && echo latest_ignored
```

## 硬边界

本轮禁止：

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
12. 不 stage 历史无关 dirty 或 DB 草稿。

## 完成后停止

完成 baseline 后立即停止，输出：

1. commit hash
2. tag
3. push 结果
4. final `git status --short`
5. 是否确认未生成真实 issue records / 未上传文件 / 未写 DB / 未执行 API/CLI smoke / 未创建外部 issue
6. 下一步建议
