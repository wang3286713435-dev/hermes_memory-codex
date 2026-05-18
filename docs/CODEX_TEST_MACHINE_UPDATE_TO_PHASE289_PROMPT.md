# Codex Test-Machine Update To Phase 2.89 Baseline Prompt

## Purpose

Update the Mac mini / test-machine Hermes Memory checkout to the reviewed Phase 2.89 handoff baseline before running any runtime preflight smoke.

This prompt is repository-update only.
It does not authorize running the Phase 2.89 preflight prompt.
It does not authorize runtime evidence write, writer invocation, parser, DB write, NAS copy/scan, index/object-store write, Agent answer integration, repair/reindex, or rollout.

## Target Ref

Use exactly:

- commit: `4e0bd62`
- tag: `phase-2.89-test-machine-runtime-preflight-handoff-baseline`

## Candidate Repo Paths

Check these paths in order and use the first existing Git checkout:

1. `/Users/hermes/code/Hermes_memory`
2. `/Volumes/Weishengsu/Hermes_memory`

If neither exists, stop and report `Pause`.

## Allowed Commands

Allowed only after confirming the worktree is clean:

```bash
git status --short
git fetch --tags origin
git checkout --detach phase-2.89-test-machine-runtime-preflight-handoff-baseline
git rev-parse --short HEAD
git tag --points-at HEAD
git status --short
```

Do not run `git pull`.
Do not merge.
Do not commit.
Do not tag.
Do not push.
Do not stash unless the operator explicitly authorizes it in a separate message.

## Hard Stop Conditions

Stop with `Pause` if:

1. the repo path is missing
2. the worktree is dirty before checkout
3. `git fetch --tags origin` fails
4. the target tag is missing after fetch
5. checkout does not land on `4e0bd62`
6. final worktree is dirty
7. required Phase 2.89 docs are missing after checkout

Required docs after checkout:

1. `docs/PHASE289_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PLAN.md`
2. `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`
3. `docs/NEXT_CODEX_A_PROMPT.md`

Do not require this update prompt itself to exist after checkout.
`docs/CODEX_TEST_MACHINE_UPDATE_TO_PHASE289_PROMPT.md` belongs to the later Phase 2.90 handoff and is not part of the Phase 2.89 target tag.
If the only missing file is this update prompt, and the target commit/tag is correct, final worktree is clean, and the three docs above exist, report `Go`.

## Forbidden

Do not:

1. run `scripts/phase288_runtime_evidence_write_preflight.py`
2. run the Phase 2.89 test-machine preflight prompt
3. call `EvidenceOnlyWriter.write()`
4. write real Hermes DB rows
5. write platform DB rows
6. run parser
7. copy scratch files
8. read raw file content
9. scan NAS
10. write OpenSearch / Qdrant / MinIO
11. enable Agent answer integration
12. run repair / cleanup / backfill / reindex / delete / migration
13. enter production rollout
14. print secrets, raw approval JSON, true filenames, true NAS paths, raw DB rows, source payloads, or sensitive business values

## Report Format

Return a sanitized report:

```yaml
status: go | pause | no_go
repo_path: <path used or null>
before_head: <short hash or null>
before_tag: <tag or null>
before_dirty: true | false | null
fetch_tags_result: passed | failed | not_run
after_head: <short hash or null>
after_tag: <tag or null>
after_dirty: true | false | null
required_docs_present: true | false
missing_required_docs: []
ignored_missing_docs:
  - docs/CODEX_TEST_MACHINE_UPDATE_TO_PHASE289_PROMPT.md
preflight_runner_executed: false
writer_invoked: false
db_writes: false
parser_invoked: false
nas_scanned: false
scratch_copy_performed: false
index_or_object_store_writes: false
agent_answer_integration: false
production_rollout: false
secret_printed: false
go_pause_no_go_reason: <short sanitized reason>
```

## Decision

`Go` means only that the test-machine repository is now cleanly updated to Phase 2.89 baseline.

`Go` does not authorize preflight execution.
After `Go`, wait for a separate instruction to run `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`.
