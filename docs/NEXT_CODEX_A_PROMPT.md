# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已 review Phase 2.53 Natural Language File Import MVP Boundary Planning，结论：通过。下一轮只允许做 docs-only Git baseline。

## 本轮目标

Phase 2.53 Natural Language File Import MVP Boundary Planning Git Baseline。

只做 selective staging / commit / tag / push；不进入 Phase 2.53a 实现，不上传真实文件，不运行 API / CLI smoke，不改 Hermes 主仓。

## Codex B Review 结论

通过，理由：

1. `docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md` 明确自然语言导入只支持单个显式本地文件路径。
2. 规划复用 Hermes_memory 现有 `POST /api/v1/documents/upload` 与 `DocumentIngestionService.ingest_uploaded_file()`，不改 ingestion / retrieval contract。
3. 规划明确普通“查看路径 / 总结文件”不得自动导入，必须有“导入 / 上传 / 收录”等显式 intent。
4. 规划明确文件不存在、目录路径、unsupported extension、过大文件、API 不可用、upload / ingestion 失败都必须 fail closed。
5. 规划明确 alias 只能在 upload 成功并返回 `document_id` / `version_id` 后绑定。
6. 规划明确目录递归、NAS / TB BIM 文件池、Data Steward、repair、backfill、reindex、rollout 均后置。
7. 规划足以作为 Phase 2.53a mocked implementation / tests 的边界输入。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## 允许 stage 的文件

只允许 stage 以下文件：

1. `docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

## 必须排除 / 不得 stage

以下文件不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`
5. 任何真实 reports / reviews / run records

## Baseline 操作

只在 staged 文件完全等于白名单时继续。

```bash
cd /Users/Weishengsu/Hermes_memory
git add docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git diff --cached --name-only
```

确认 staged 仅上述 8 个文件后：

```bash
git commit -m "docs: baseline phase 2.53 natural language file import plan"
git tag phase-2.53-natural-language-file-import-plan-baseline
git push origin main
git push origin phase-2.53-natural-language-file-import-plan-baseline
```

## Baseline 后复核

```bash
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
```

允许最终仍显示 out-of-scope dirty / untracked only if 它们是：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`

如果出现其他 dirty，停止并写交接。

## 硬禁止

1. 不写功能代码。
2. 不新增 scripts / tests。
3. 不上传真实文件。
4. 不运行 API / CLI smoke。
5. 不修改 Hermes 主仓。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete / migration。
8. 不进入 production rollout。
9. 不进入 Data Steward / BIM TB 级管理实现。
10. 不修改 retrieval contract。
11. 不修改 memory kernel 主架构。
12. baseline 后不得自动进入 Phase 2.53a。

## 完成后状态

更新 `reports/agent_runs/latest.json`（ignored）：

1. `phase=Phase 2.53 Natural Language File Import MVP Boundary Planning Git Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push 结果。
4. `needs_codex_b_review=false`
5. `needs_codex_c_validation=false`
6. 下一步建议：进入 Phase 2.53a mocked implementation / tests；仍不做真实 upload smoke，除非另行授权。

完成后停止，等待 Codex B / 用户检查。
