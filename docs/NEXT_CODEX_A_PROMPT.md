# NEXT_CODEX_A_PROMPT

## Phase 2.112i Test-machine Retrieval Backend Environment Fix

Do not ask Codex A to modify alias parser / alias continuity code for this blocker.

Phase 2.112h test-machine validation proved the alias path now works:

```text
import alias: @建筑类数据样表
follow-up alias_resolution.status: alias_resolved
alias_missing: false
stable_owner_missing: false
```

The remaining blocker is:

```text
retrieval_suppressed=true
retrieval_suppressed_reason=retrieval_backend_failed
root cause: retrieval_backend_failed_postgres_hostname_unresolved
```

This is a test-machine Hermes_memory API / DB hostname environment issue, not an alias bug.

## Test-machine Task

On the Mac mini / test machine:

1. Do not change Hermes agent code.
2. Do not repeat imports in a loop.
3. Inspect how Hermes_memory API is running:
   - Docker compose service, or
   - host process / local script / launchd.
4. Inspect only DB connection key names and hostname category; do not print DB URL values, password, token, or secret.
5. If Hermes_memory API runs inside Docker compose, ensure it shares the Docker network where service hostname `postgres` resolves.
6. If Hermes_memory API runs on the host, `postgres` service hostname likely will not resolve; use the test-machine approved host-accessible DB hostname / port from secure env, commonly a localhost-style endpoint, without printing secret values.
7. Restart Hermes_memory API after fixing env/network.
8. Confirm `/health` passes.
9. Restart 8642 only if needed.
10. First try the follow-up retrieval again in the same logical conversation/session:

```text
围绕 @建筑类数据样表 总结这个文件的表格结构，必须只基于 retrieval evidence，并给出 citation。
```

11. If the restart lost session continuity, run at most one fresh controlled import using the same authorized small `.xlsx` and explicit alias `@建筑类数据样表`, then run the follow-up retrieval once.

## Go Criteria

Return Go only if:

1. Hermes_memory API health passes;
2. 8642 health passes;
3. follow-up alias is resolved;
4. `alias_missing=false`;
5. `retrieval_suppressed=false`;
6. `retrieval_evidence_document_ids` is non-empty;
7. citation is present and manually reviewable;
8. no third-document contamination;
9. no metadata/facts/snapshot/transcript substitution.

## Pause Criteria

Return Pause if:

1. DB hostname remains unresolved;
2. any retrieval backend error remains;
3. alias unexpectedly regresses to missing;
4. evidence IDs remain empty;
5. citation is missing;
6. provider usage limit blocks the answer.

## Hard Prohibitions

Do not:

1. output secrets, DB URLs, passwords, tokens, file content, raw local paths, or env values;
2. scan NAS;
3. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
4. manually write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
5. run uncontrolled repeated imports;
6. claim Phase 2 natural import closeout before retrieval evidence + citation pass.

## Required Report

Return:

1. Hermes_memory run mode category: docker / host / launchd / unknown;
2. DB hostname category before and after fix, sanitized;
3. whether `/health` passes;
4. 8642 health and upload flag visibility;
5. follow-up alias/retrieval/citation table;
6. safety flags;
7. Go / Pause / No-Go;
8. if Pause, the single smallest blocker.
