# Mac Mini Operator Command Sheet

This sheet is for Hermes internal controlled MVP operation on the Mac Mini.

It is not a production rollout, customer delivery, automatic tender review, automatic bid, or automatic business decision process. Commands below are templates. Phase 2.51b does not execute them.

## Phase 2.65 Current Reviewed Refs

| repo | reviewed ref | action |
|---|---|---|
| Hermes_memory | `phase-2.64b-data-steward-selective-integration-baseline` | usable for install planning |
| hermes-agent | `phase-2.56e-natural-import-real-upload-smoke-baseline` | usable for install planning |

Optional read-only manifest:

```bash
cd /Users/hermes/code/Hermes_memory
uv run python scripts/phase265_mvp_release_manifest.py \
  --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline \
  --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline \
  --operator mac-mini
```

The manifest does not read `.env`, does not print secrets, does not start services, and does not mutate Git / DB / index state.

## 0. Preconditions

Before touching Git or services, confirm:

1. You are operating on the Mac Mini internal MVP machine.
2. `.env` exists locally and is not tracked by Git.
3. NAS / external disk / network are available.
4. The target commit / tag was reviewed and handed off from the development machine.
5. You have operator authorization for this specific update window.

If any item is unclear, stop.

## 1. Repo State

Check both worktrees before update. Dirty worktree means pause.

```bash
cd /Users/hermes/code/Hermes_memory
git status --short
git branch --show-current
git rev-parse HEAD
git tag --points-at HEAD

cd /Users/hermes/code/hermes-agent
git status --short
git branch --show-current
git rev-parse HEAD
git tag --points-at HEAD
```

Record current refs before changing anything.

## 2. Hot Update

Only run when both worktrees are clean and the target ref is reviewed.

```bash
cd /Users/hermes/code/Hermes_memory
git fetch origin --tags
git pull --ff-only origin main
# or: git checkout <reviewed-hermes-memory-tag>

cd /Users/hermes/code/hermes-agent
git fetch origin --tags
git pull --ff-only <reviewed-agent-remote> <reviewed-agent-branch>
# or: git checkout <reviewed-hermes-agent-tag>
```

Do not patch code on the Mac Mini to make a smoke pass.

## 3. Health Checks

```bash
cd /Users/hermes/code/Hermes_memory
docker compose ps
curl http://127.0.0.1:8000/health

cd /Users/hermes/code/hermes-agent
hermes chat --help
```

Env sanity:

1. `QDRANT_COLLECTION` should be `hermes_chunks`.
2. DB / OpenSearch / Qdrant should point to expected local or reviewed internal endpoints.
3. Never print secrets, tokens, or `.env` values into chat or tracked files.

## 4. Daily Run Record

Canonical JSON record:

```text
reports/internal_mvp_runs/<YYYYMMDD>_<session>.json
```

Optional human notes:

```text
reports/internal_mvp_runs/<YYYYMMDD>_<session>_notes.md
```

Markdown notes are not valid Phase 2.49 bridge input. If only Markdown notes exist, convert them into sanitized JSON first.

## 5. Review Command

Use the canonical JSON path only.

```bash
cd /Users/hermes/code/Hermes_memory
uv run python scripts/phase249_internal_mvp_run_record_review.py \
  --input-run-record reports/internal_mvp_runs/<YYYYMMDD>_<session>.json \
  --review-report \
  --output-dir reports/internal_mvp_runs/<YYYYMMDD>_review
```

Real run records and review outputs remain ignored and must not be committed.

## 6. Rollback

Rollback only to a previous reviewed known-good tag recorded before update.

```bash
cd /Users/hermes/code/Hermes_memory
git checkout <previous-known-good-hermes-memory-tag>

cd /Users/hermes/code/hermes-agent
git checkout <previous-known-good-hermes-agent-tag>
```

After rollback, rerun health checks and write an ignored incident / deployment record.

## 7. Stop Conditions

Stop immediately if any condition appears:

1. API `/health` unavailable.
2. Hermes CLI unavailable.
3. Docker / DB / OpenSearch / Qdrant unhealthy or unexpected.
4. Worktree dirty before update.
5. Unknown or unreviewed commit / tag.
6. Alias / session blocker in internal MVP checks.
7. `facts_as_answer=true`, `transcript_as_fact=true`, or `snapshot_as_answer=true`.
8. Third-document contamination.
9. Missing Evidence hidden or softened.
10. Any repair / backfill / reindex / migration / cleanup / delete is needed.

Stop means pause and record; it does not mean fix forward.

## 8. Never Do

1. No ad-hoc development on Mac Mini.
2. No unreviewed edits.
3. No repair / backfill / reindex / migration / cleanup / delete.
4. No production cron or scheduler.
5. No Data Steward / BIM TB-scale implementation in this MVP loop.
6. No secrets, `.env` values, raw customer data, raw reports, or raw run records in Git.
