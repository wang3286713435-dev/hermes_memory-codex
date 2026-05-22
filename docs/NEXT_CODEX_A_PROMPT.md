# NEXT_CODEX_A_PROMPT

## Phase 2.112h Test-machine Validation Handoff

Do not ask Codex A to implement more code for Phase 2.112h unless the test machine returns Pause / No-Go.

Current runtime candidate:

```text
repo: /Users/hermes/code/hermes-agent
tag: phase-2.112h-explicit-import-alias-runtime-test-candidate
commit: e1d38e1ec
```

## Test-machine Task

On the Mac mini / test machine:

1. Ensure Hermes Memory is running and healthy.
2. Checkout `hermes-agent` to `phase-2.112h-explicit-import-alias-runtime-test-candidate`.
3. Restart the OpenWebUI-compatible Hermes backend on port `8642`.
4. Confirm `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible to the backend.
5. Run one authorized small `.xlsx` natural import through the real 8642 / OpenWebUI-compatible path, not direct upload API.
6. The import prompt must explicitly request:

```text
@建筑类数据样表
```

Use a natural-language phrase that previously failed, for example:

```text
请帮我导入这个文件，别名设为 @建筑类数据样表，后续我会用这个别名查询它。
```

7. In the same logical conversation/session, ask:

```text
围绕 @建筑类数据样表 总结这个文件的表格结构，必须只基于 retrieval evidence，并给出 citation。
```

## Go Criteria

Return Go only if all are true:

1. `natural_import_detected=true`
2. `real_upload_enabled=true`
3. `upload_adapter_status=executed`
4. `ingestion_status=upload_succeeded`
5. `chunk_count > 0`
6. `indexed_count > 0`
7. import alias is exactly `建筑类数据样表`
8. import alias status is `alias_bound` or equivalent success
9. follow-up `alias_resolution.status=alias_resolved`
10. `alias_missing=false`
11. `retrieval_suppressed=false`
12. `retrieval_evidence_document_ids` is non-empty
13. citation is present and manually reviewable
14. no third-document contamination
15. `metadata_as_answer=false`
16. `facts_as_answer=false`
17. `snapshot_as_answer=false`
18. `transcript_as_fact=false`

## Pause Criteria

Return Pause if:

1. import succeeds but requested alias is not exactly preserved;
2. follow-up still returns `alias_missing=true`;
3. retrieval is suppressed;
4. evidence IDs are empty;
5. citation is missing;
6. provider usage limit blocks the retrieval answer;
7. diagnostics are internally contradictory.

## Hard Prohibitions

Do not:

1. repeat imports in a loop;
2. scan NAS;
3. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
4. write DB / facts / document_versions directly;
5. manually write OpenSearch / Qdrant / MinIO;
6. output secret, token, file content, or raw local path;
7. claim Phase 2 natural import closeout before the follow-up retrieval + citation passes.

## Required Report

Return:

1. checkout commit / tag / worktree clean status;
2. 8642 health and upload flag visibility;
3. import result table;
4. follow-up alias/retrieval/citation table;
5. safety flags;
6. Go / Pause / No-Go;
7. if Pause, the single smallest blocker.
