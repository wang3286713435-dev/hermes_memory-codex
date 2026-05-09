# NEXT_CODEX_A_PROMPT

本轮目标
Phase 2.58 Natural Import Operator Pack selective Git baseline。

Codex B review 结论
1. Phase 2.58 已通过 review。
2. 已复跑验证：
   - `uv run python -m py_compile scripts/phase257a_natural_import_evidence_template.py` 通过。
   - `uv run pytest tests/test_phase257a_natural_import_evidence_template.py -q` 为 `14 passed`。
   - `git diff --check` 通过。
   - `reports/agent_runs/latest.json` JSON 校验通过。
3. review helper 已阻断：
   - `real_upload_called=true` -> `pause`
   - `plain_upload_bypass_used=true` -> `pause`
   - `real_file_uploaded=true` -> `pause`
4. 本轮无真实 upload、无 API/CLI smoke、无 DB/index 写入。

必须先执行的轻量验证
在 `/Users/Weishengsu/Hermes_memory` 执行：
```bash
uv run python -m py_compile scripts/phase257a_natural_import_evidence_template.py
uv run pytest tests/test_phase257a_natural_import_evidence_template.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase258_baseline_check.json
git status --short
```

Selective staging 白名单
只允许 stage：
- `/Users/Weishengsu/Hermes_memory/scripts/phase257a_natural_import_evidence_template.py`
- `/Users/Weishengsu/Hermes_memory/tests/test_phase257a_natural_import_evidence_template.py`
- `/Users/Weishengsu/Hermes_memory/docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
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
- commit message：`feat: add natural import operator pack dry-run`
- tag：`phase-2.58-natural-import-operator-pack-baseline`
- push 当前分支到 `origin`，并推送 tag。

完成后更新 ignored 状态
更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：
- `status=baseline`
- `git.commit=<new commit hash>`
- `git.tag=phase-2.58-natural-import-operator-pack-baseline`
- `git.pushed=true`
- `needs_codex_b_review=false`
- `needs_codex_c_validation=false`
- 下一步建议：Phase 2.59 可规划第二个用户授权文件真实 natural import smoke，或继续 Mac mini MVP operator runbook；不得自动上传。

硬边界
1. 不上传文件。
2. 不运行 API / CLI smoke。
3. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
4. 不 cleanup/delete/repair/backfill/reindex。
5. 不进入 DB/NAS/Data Steward 实现。
6. baseline 后停止，不自动进入 Phase 2.59。

返回要求
输出：
1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`，明确历史无关 dirty / untracked 是否仍保留。
5. 确认 ignored latest 未提交。
