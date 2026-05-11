# Phase 2.65 Mac mini MVP Landing Acceleration Pack

## 1. Goal

Package the current reviewed Hermes internal MVP baseline into a Mac mini install / update / rollback handoff pack.

This phase prepares operator-facing instructions and a read-only release manifest. It does not deploy to the Mac mini.

## 2. Current Reviewed Baseline

| repo | reviewed ref | status |
|---|---|---|
| Hermes_memory | `phase-2.64b-data-steward-selective-integration-baseline` | ready for Mac mini install planning |
| hermes-agent | `phase-2.56e-natural-import-real-upload-smoke-baseline` | ready for Mac mini install planning |

Phase 2.64b commit: `da84197`.

## 3. Scope

In scope:

1. Mac mini install / update / rollback quickstart.
2. Codex Mac mini install and update prompt refresh.
3. Operator command sheet refresh.
4. Read-only release manifest helper.
5. Targeted tests for the manifest helper.
6. Handoff state updates for Codex B review.

Out of scope:

1. Real Mac mini deployment.
2. Docker service startup.
3. API / CLI smoke.
4. Real DB connection.
5. NAS scan.
6. File upload.
7. DB / facts / document_versions / audit_logs writes.
8. OpenSearch / Qdrant / MinIO writes.
9. Repair / cleanup / backfill / reindex / delete / migration.
10. Data Steward feature activation or real DB smoke.
11. Production rollout.

## 4. Release Manifest Helper

Script:

```bash
uv run python scripts/phase265_mvp_release_manifest.py \
  --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline \
  --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline \
  --operator codex-a
```

The helper is read-only and offline. It prints JSON to stdout. It writes a file only when `--output-json` is explicitly provided.

Required fixed safety fields:

1. `dry_run=true`
2. `read_only=true`
3. `production_rollout=false`
4. `repair_attempted=false`
5. `db_or_index_written=false`
6. `real_db_connected=false`
7. `nas_scanned=false`
8. `destructive_actions=[]`
9. `secrets_read=false`
10. `secrets_printed=false`

Expected current status is `ready_for_operator_review` when both reviewed refs above are used.

If a future operator changes the agent ref back to `NEEDS_REVIEWED_AGENT_REF` or leaves it empty, the manifest must remain `pause`.

## 5. Recommended Mac mini Paths

```text
/Users/hermes/code/Hermes_memory
/Users/hermes/code/hermes-agent
/Users/hermes/env
/Users/hermes/reports
```

## 6. Mac mini Install Gate

The Mac mini operator may proceed only when:

1. Hermes_memory reviewed ref is explicit.
2. hermes-agent reviewed ref is explicit.
3. Worktrees are clean.
4. Required `.env` keys are present without exposing values.
5. Docker / git / uv are available.
6. The operator accepts this is internal controlled MVP, not production rollout.

Missing hermes-agent reviewed ref remains a hard pause.

## 7. Review Status

Phase 2.65 implementation should stop after local tests and manifest sample output. Codex B must review before baseline or Mac mini execution.
