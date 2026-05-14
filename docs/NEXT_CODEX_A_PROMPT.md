# NEXT_CODEX_A_PROMPT

## Phase 2.81 Docs Baseline Task

Phase 2.80a Mac mini / test-machine controlled scratch parser dry-run returned `go`.

Validated smoke summary:

```json
{
  "decision": "go",
  "sample_count": 3,
  "copied_count": 3,
  "parsed_preview_count": 3,
  "cleanup_status": "all_deleted",
  "parser_invoked": true,
  "parser_dry_run_only": true,
  "documents_written": false,
  "chunks_written": false,
  "db_writes": false,
  "opensearch_writes": false,
  "qdrant_writes": false,
  "minio_writes": false,
  "agent_answer_integration": false,
  "raw_text_output": false,
  "secret_printed": false,
  "raw_row_output": false,
  "true_filename_output": false,
  "true_nas_path_output": false,
  "true_business_data_output": false,
  "production_rollout": false
}
```

Codex B review 已通过。Phase 2.81 planning 已完成：

- `docs/PHASE281_SANITIZED_EVIDENCE_MANIFEST_PLAN.md`

当前下一步只做 selective docs Git baseline，不实现 manifest runner，不进入 Phase 2.81a。

## 允许 stage 的文件

只允许 stage 以下文件：

1. `docs/PHASE280A_CONTROLLED_SCRATCH_PARSER_DRY_RUN_RESULT.md`
2. `docs/PHASE281_SANITIZED_EVIDENCE_MANIFEST_PLAN.md`
3. `docs/NEXT_CODEX_A_PROMPT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

## 当前结论

Phase 2.81 只完成 planning：

1. Evidence manifest 只能从 sanitized parser preview 派生。
2. Manifest 不包含 raw text、真实文件名、真实 NAS 路径、raw DB row、secret 或敏感业务数据。
3. Manifest 可包含 asset provenance、parser status、file type bucket、text length bucket、structure count buckets、hash presence、cleanup status、安全 flags。
4. Manifest 仍是 local ignored artifact，不入 Git。
5. 不写 `documents`、`chunks`、OpenSearch、Qdrant、MinIO、platform DB 或 Hermes DB。
6. 不把 manifest 接入 Agent final answer。
7. 失败路径必须 cleanup，并输出 `pause` / `no_go`。
8. Phase 2.81 只是 planning，未实现 manifest runner。

## 硬边界

禁止：

1. 实现 manifest runner。
2. 生成真实 manifest artifact。
3. 执行 parser。
4. 复制真实文件。
5. 读取真实文件正文。
6. 写平台 DB / Hermes DB / `documents` / `chunks`。
7. 写 OpenSearch / Qdrant / MinIO。
8. 扫描 NAS。
9. Agent DB / NAS CRUD。
10. Agent final answer integration。
11. repair / cleanup source data / backfill / reindex / delete。
12. production rollout。

## Baseline Steps

1. 复核 `git status --short`，dirty 只能是上述允许文件；`reports/agent_runs/latest.json` 是 ignored local state，不得 stage。
2. 运行：
   - `git diff --check`
   - `uv run python -m json.tool reports/agent_runs/latest.json >/dev/null`
   - `git check-ignore reports/agent_runs/latest.json`
3. Selective stage 上述 8 个 docs 文件。
4. Commit message:
   - `docs: baseline phase 2.81 sanitized evidence manifest plan`
5. Tag:
   - `phase-2.81-sanitized-evidence-manifest-plan-baseline`
6. Push `origin/main` 与 tag。
7. Baseline 后停止，不得进入 Phase 2.81a。

## Acceptance Criteria

1. Final `git status --short` clean。
2. Commit 只包含允许的 8 个 docs 文件。
3. `reports/agent_runs/latest.json` 未被 staged / committed。
4. 未生成 manifest artifact。
5. 未运行 parser、未复制真实文件、未连接 DB / NAS、未写 DB / index / object store。
6. 未接入 Agent final answer，未 rollout。

## 后续建议

Codex B review 通过后，可以二选一：

1. 先做 Phase 2.81 docs baseline。
2. 或在用户显式授权后，另开 Phase 2.81a sanitized evidence manifest dry-run implementation。

Phase 2.81a 必须是单独授权任务，不得由本文件自动触发。
