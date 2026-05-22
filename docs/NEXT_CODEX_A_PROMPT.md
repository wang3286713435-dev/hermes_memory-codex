# NEXT_CODEX_A_PROMPT

## Phase 2.113 Closeout Gate

You are Codex A, the Hermes runtime development agent.

Do not write new runtime code unless Codex B returns a concrete new blocker.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`
5. `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Current State

Phase 2.113a live validation returned Go on the test machine.

Runtime candidate:

```text
hermes-agent tag = phase-2.113a-self-awareness-runtime-test-candidate
```

Validated:

1. 8642 backend health passed.
2. Hermes Memory health passed.
3. Self-awareness answer passed.
4. Ordinary retrieval guard passed.
5. Fuzzy file discovery safety passed.
6. No secret / raw path / file content / NAS scan / repair / reindex / rollout / manual DB-index write.

Skipped by design:

```text
natural_import_feedback = skipped_by_no_import_authorization
```

This is acceptable for the Phase 2.113a live gate because the test-machine prompt only required that case if a small non-sensitive import was explicitly authorized.

## Required Next Step

This is now a Codex B closeout / freeze-checklist task, not a Codex A implementation task.

Codex B should:

1. update Phase 2.113 closeout status;
2. update Phase 2 final freeze checklist;
3. decide whether a separate authorized natural import UX smoke is still needed before Phase 2 stable freeze;
4. prepare the next bounded phase only if an explicit remaining blocker exists.

## If User Says "Continue"

Do not write runtime code.

Report that Phase 2.113a live validation is Go and that Codex B should update closeout / freeze checklist first.

## Do Not

1. Do not run production rollout.
2. Do not scan NAS.
3. Do not write DB / facts / document_versions / OpenSearch / Qdrant.
4. Do not repair / cleanup / backfill / reindex / delete / migrate.
5. Do not modify retrieval contract.
6. Do not modify memory kernel main architecture.
7. Do not treat diagnostics, aliases, workspace refs, or memory metadata as retrieval evidence.
8. Do not claim DWG/RVT/BIM content understanding.
9. Do not stage unrelated `uv.lock`, adapter reload, repo-hygiene, shared-doc import, or runtime artifact files.
