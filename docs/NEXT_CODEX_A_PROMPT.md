# NEXT_CODEX_A_PROMPT

本轮目标
Phase 2.57 Natural Import MVP Usability / Evidence Planning docs-only selective Git baseline。

Codex B review 结论
1. Phase 2.57 planning 通过 review。
2. 规划文件已覆盖 natural import operator flow、evidence pack、Go / Pause / No-Go、Mac mini operator runbook outline 与非目标。
3. 本轮为 docs-only；不需要 Codex C，不运行 API / CLI，不上传文件。
4. 继续禁止 DB/NAS/Data Steward 实现、repair/backfill/reindex、production rollout。

必须先执行的轻量验证
在 `/Users/Weishengsu/Hermes_memory` 执行：
```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase257_baseline_check.json
git status --short
```

Selective staging 白名单
只允许 stage：
- `/Users/Weishengsu/Hermes_memory/docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`
- `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
- `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
- `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
- `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
- `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_C_PROMPT.md`
- `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
- `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

禁止 stage
- `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
- `/Users/Weishengsu/Hermes_memory/docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
- `/Users/Weishengsu/Hermes_memory/docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
- `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
- 任何未列入白名单的文件。

提交与 tag
- commit message：`docs: plan phase 2.57 natural import mvp usability`
- tag：`phase-2.57-natural-import-mvp-usability-plan-baseline`
- push 当前分支到 `origin`，并推送 tag。

完成后更新 ignored 状态
更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：
- `status=baseline`
- `git.commit=<new commit hash>`
- `git.tag=phase-2.57-natural-import-mvp-usability-plan-baseline`
- `git.pushed=true`
- `needs_codex_b_review=false`
- `needs_codex_c_validation=false`
- 下一步建议：Phase 2.57a natural import evidence template / runbook runner dry-run planning or implementation；仍不上传文件。

硬边界
1. 不上传文件。
2. 不运行 API / CLI smoke。
3. 不写业务代码。
4. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
5. 不 cleanup/delete/repair/backfill/reindex。
6. 不进入 DB/NAS/Data Steward 实现。
7. baseline 后停止，不自动进入 Phase 2.57a。

返回要求
输出：
1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`，明确历史无关 dirty / untracked 是否仍保留。
5. 确认 ignored latest 未提交。
