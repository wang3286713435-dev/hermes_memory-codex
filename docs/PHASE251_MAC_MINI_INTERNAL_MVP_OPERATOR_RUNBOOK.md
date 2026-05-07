# Phase 2.51 Mac Mini Internal MVP Operator / Hot Update Runbook

## Positioning

The Mac Mini is the company internal controlled MVP runtime machine for Hermes. It is not a production rollout node, customer delivery environment, automatic tender review system, automatic bid system, or automatic business decision system.

This runbook defines the operator flow for starting, checking, updating, rolling back, and recording internal MVP usage after a reviewed baseline has been produced on the development machine.

This document is an operator artifact only. It does not execute deployment commands, start services, pull remotes, modify code, write DB / index state, or approve rollout.

## Roles

| Role | Responsibility | Boundary |
|---|---|---|
| Development machine | Develop, test, review, commit, tag, and push reviewed baselines | Does not imply Mac Mini auto-update |
| Mac Mini operator | Pull reviewed refs, start / check services, run internal MVP checks, write ignored run records | Does not make ad-hoc code edits |
| Codex A | Executes bounded tasks from `docs/NEXT_CODEX_A_PROMPT.md` | Does not expand scope or perform destructive repair |
| Codex B | Review, prompt generation, roadmap / scope alignment | Must approve baseline / Yellow Lane transitions |
| Codex C | Real terminal smoke / API / CLI validation | Does not perform primary implementation unless explicitly asked |
| Codex D | Read-only drift audit / observability review | Does not mutate runtime data |

Human business owners remain responsible for tender, contract, procurement, customer communication, company-direction, and Data Steward decisions.

## Day-Start Checks

Before internal MVP use, the operator should verify:

1. Machine identity, power, network, NAS / external SSD mount, and available disk space.
2. `.env` exists only on the Mac Mini / local env path and is not committed to Git.
3. Docker dependencies are available and healthy.
4. Hermes_memory API `/health` is reachable.
5. Hermes CLI help works.
6. `QDRANT_COLLECTION` points to `hermes_chunks`.
7. Both repos are on reviewed commits / tags.
8. Worktrees are clean or any dirty state is explicitly documented and approved.

If any check fails, the operator should stop and write a local ignored deployment / run record. Do not “fix forward” with unreviewed code edits.

## Hot Update Flow

Hot update discipline:

1. Development happens on the development machine.
2. Codex A / B complete phase implementation, review, baseline, tag, and push.
3. Mac Mini operator records current commit / tag before pulling.
4. Mac Mini operator fetches reviewed refs only.
5. Mac Mini operator checks out the approved branch / tag.
6. Operator runs read-only health / smoke checks.
7. Only after checks pass does the internal MVP daily loop resume.
8. If checks fail, roll back to the previous known good tag and record the incident.

Do not use Mac Mini as an ad-hoc development machine. Do not patch runtime code there to bypass failures.

## Command Templates

These are templates only. This phase does not execute them.

### Check Current State

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

### Fetch Reviewed Refs

```bash
cd /Users/hermes/code/Hermes_memory
git fetch origin --tags

cd /Users/hermes/code/hermes-agent
git fetch origin --tags
```

### Update To Reviewed Main

Only run if the worktree is clean and the operator is authorized to move to `origin/main`.

```bash
cd /Users/hermes/code/Hermes_memory
git pull --ff-only origin main

cd /Users/hermes/code/hermes-agent
git pull --ff-only origin main
```

### Checkout Reviewed Tag

Use a reviewed tag from the handoff record.

```bash
cd /Users/hermes/code/Hermes_memory
git checkout <reviewed-hermes-memory-tag>

cd /Users/hermes/code/hermes-agent
git checkout <reviewed-hermes-agent-tag>
```

### Health Checks

```bash
cd /Users/hermes/code/Hermes_memory
docker compose ps
curl http://127.0.0.1:8000/health

cd /Users/hermes/code/hermes-agent
hermes chat --help
```

### Write Daily Run Record

Use `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`.

The canonical run record for the Phase 2.49 review bridge is JSON:

- `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`

Operators should manually assemble the sanitized JSON record from the JSON blocks in the template. Markdown notes are optional and human-readable only:

- `reports/internal_mvp_runs/<YYYYMMDD>_<session>_notes.md`

Do not pass Markdown notes to `scripts/phase249_internal_mvp_run_record_review.py --input-run-record`.

```bash
cd /Users/hermes/code/Hermes_memory
mkdir -p reports/internal_mvp_runs
$EDITOR reports/internal_mvp_runs/<YYYYMMDD>_<session>.json

# Optional human notes only; not valid as --input-run-record.
$EDITOR reports/internal_mvp_runs/<YYYYMMDD>_<session>_notes.md
```

Real run records and optional Markdown notes remain ignored and must not be committed. If the operator only wrote Markdown notes, convert them into a sanitized JSON run record before running the Phase 2.49 bridge.

### Review Daily Run Record

```bash
cd /Users/hermes/code/Hermes_memory
uv run python scripts/phase249_internal_mvp_run_record_review.py \
  --input-run-record reports/internal_mvp_runs/<YYYYMMDD>_<session>.json \
  --review-report \
  --output-dir reports/internal_mvp_runs/<YYYYMMDD>_review
```

### Rollback To Known Good Tag

Only use reviewed known-good tags recorded before the update.

```bash
cd /Users/hermes/code/Hermes_memory
git checkout <previous-known-good-hermes-memory-tag>

cd /Users/hermes/code/hermes-agent
git checkout <previous-known-good-hermes-agent-tag>
```

After rollback, rerun health checks and write an ignored incident record.

## Records And Evidence

Each operator action should leave an ignored local record:

1. Current refs before update.
2. Target refs after update.
3. Health / smoke result.
4. Stop condition, if any.
5. Rollback ref and reason, if rollback occurs.
6. Daily MVP run record.
7. Review report generated from the run record.

Storage policy:

- Real run records: `reports/internal_mvp_runs/`, ignored.
- Real deployment records: `reports/deployment_records/`, ignored.
- Real smoke / evidence files: local ignored report paths only.
- Tracked Git may contain sanitized templates, README files, and planning docs only.

## Stop Conditions

Stop immediately if any condition appears:

1. Hermes_memory API `/health` unavailable.
2. Hermes CLI unavailable.
3. Docker dependency unhealthy.
4. DB / OpenSearch / Qdrant points to an unexpected host or collection.
5. `QDRANT_COLLECTION` is not `hermes_chunks` unless a reviewed phase explicitly changed it.
6. Worktree dirty before pull / checkout.
7. Unknown commit, unreviewed commit, or missing baseline tag.
8. Alias/session blocker appears in internal MVP daily checks.
9. Facts / transcript / metadata snapshot replaces retrieval evidence.
10. Third-document contamination appears.
11. Missing Evidence is hidden or softened.
12. Any repair / cleanup / backfill / reindex / migration is needed.
13. Any business owner decision is required but not confirmed.

Stop means pause the internal MVP loop and write an ignored local record. It does not mean auto-repair.

## Strict Prohibitions

The Mac Mini operator must not:

1. Develop mainline features directly on the Mac Mini.
2. Patch code ad hoc to pass local smoke.
3. Commit Mac Mini local edits as feature work.
4. Run destructive repair / cleanup / backfill / reindex / delete.
5. Run unplanned migrations.
6. Create production cron / scheduler jobs.
7. Treat Hermes output as final tender, contract, procurement, customer, Data Steward, or business decision.
8. Merge Data Steward / BIM TB-scale management into the current internal MVP.
9. Expose `.env`, secrets, tokens, raw customer data, or raw run records in tracked Git.

## Go / Pause / No-Go

| Result | Meaning | Action |
|---|---|---|
| Go | Internal controlled MVP may continue for the approved scope | Continue with daily run record and review loop |
| Pause | Human review or Codex B issue intake is required | Stop expansion; resolve or record workaround |
| No-Go | P0 / unsafe boundary detected | Stop current loop and escalate |

`Go` never means production rollout, customer delivery, automatic tender review, automatic bid, automatic business decision, or repair authorization.

## Next Phase Candidates

1. Phase 2.51a: fake / local-only deployment record dry-run smoke.
2. Phase 2.51b: minimal operator command sheet.
3. Phase 2.50b: internal MVP evidence pack.

Do not start those phases without a new bounded prompt.
