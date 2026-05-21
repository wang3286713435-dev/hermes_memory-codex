# NEXT_CODEX_A_PROMPT

## Phase 2.112b Review Hold

Codex A has completed the bounded Phase 2.112b runtime fix. Do not continue implementation unless Codex B review or test-machine validation reports a new blocker.

## Current State

- Phase 2.112b fix implemented in Hermes main repo.
- Targeted validation passed: py_compile passed; natural import / upload client / session scope pytest `99 passed`.
- Runtime test-candidate pushed: commit `1d02a7918`, tag `phase-2.112b-natural-import-alias-runtime-test-candidate` on `backup2` / `hermes_repo`.
- No real import was repeated.
- No DB / facts / document_versions / OpenSearch / Qdrant / MinIO writes were performed.

## Next Required Action

1. Codex B review has passed the Phase 2.112b diff.
2. Test-machine Codex should rerun `docs/CODEX_TEST_MACHINE_PHASE2112_NATURAL_IMPORT_VALIDATION_PROMPT.md`.
3. Codex A should not baseline or enter Phase 2.113 before review and real OpenWebUI / 8642 validation.

## Hard Boundaries

- Do not repeat real import from this development task.
- Do not write DB / facts / document_versions / OpenSearch / Qdrant / MinIO.
- Do not execute repair, cleanup, backfill, reindex, delete, migration, or rollout.
- Do not modify retrieval contract or memory kernel main architecture.
- Do not baseline or push runtime changes before Codex B review and test-machine validation.
