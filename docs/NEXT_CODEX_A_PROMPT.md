# NEXT_CODEX_A_PROMPT

## Phase 2.114 Final User-flow Acceptance Gate

You are Codex A, the Hermes runtime development agent.

Do not write new runtime code unless the Phase 2.114 test-machine smoke returns a concrete blocker.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PLAN.md`
5. `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`
6. `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`
7. `docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`
8. `eval/phase2_inventory/phase2_final_freeze_checklist.json`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

## Current State

Phase 2.113a live validation returned Go.

Phase 2.114 now tests the full user-facing flow:

```text
self-awareness -> natural-language import -> alias -> follow-up retrieval -> citation -> evidence boundary
```

This is a validation gate, not a new feature build.

## Required Next Step

Test-machine Codex should execute:

```text
docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md
```

Required operator inputs:

```text
AUTHORIZED_FILE_PATH=<one small non-sensitive local file path>
ALIAS=<safe alias>
PROJECT_CONTEXT=<safe project context>
```

## Go Criteria

Go requires:

1. 8642 backend health passes.
2. Hermes Memory health passes.
3. Self-awareness answer passes.
4. Natural-language import succeeds for exactly one authorized small sample.
5. Hermes reports safe alias, document_id, version_id, chunk_count, indexed_count, and follow-up suggestions.
6. Same-session `@alias` retrieval returns `alias_missing=false`, `retrieval_suppressed=false`, non-empty evidence document IDs, and citation.
7. Hermes states that alias / import diagnostics / workspace refs / memory metadata are not content evidence.
8. No raw path, secret, file content, NAS scan, repair/reindex/migration/rollout, or manual DB/index write.

## If Test-machine Returns Go

Codex B should:

1. update `eval/phase2_inventory/phase2_final_freeze_checklist.json`;
2. mark final user-flow acceptance as passed with scope;
3. decide whether to tag Phase 2 stable MVP baseline;
4. create Phase 3 entry with inherited known gaps.

Codex A should not automatically implement new runtime features.

## If Test-machine Returns Pause / No-Go

Only then should Codex A receive a new bounded fix prompt with:

1. exact failing case;
2. sanitized diagnostics;
3. smallest allowed write scope;
4. target tests;
5. forbidden actions.

## Do Not

1. Do not run production rollout.
2. Do not scan NAS.
3. Do not import more than one file.
4. Do not write DB / facts / document_versions / OpenSearch / Qdrant outside the configured authorized import pipeline.
5. Do not repair / cleanup / backfill / reindex / delete / migrate.
6. Do not modify retrieval contract.
7. Do not modify memory kernel main architecture.
8. Do not treat diagnostics, aliases, workspace refs, or memory metadata as retrieval evidence.
9. Do not claim DWG/RVT/BIM content understanding.
10. Do not stage unrelated `uv.lock`, adapter reload, repo-hygiene, shared-doc import, or runtime artifact files.
