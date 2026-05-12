# Phase 2.66 Mac mini Controlled Install Planning

## 1. Goal

Prepare the Mac mini side Codex / operator to execute a controlled internal MVP installation using the Phase 2.65 landing pack.

This phase is planning only. It does not install Hermes on the Mac mini from the development machine.

## 2. Reviewed Inputs

| repo | reviewed ref | source |
|---|---|---|
| Hermes_memory | `phase-2.65-mac-mini-mvp-landing-baseline` | Phase 2.65 baseline |
| Hermes_memory install target | `phase-2.64b-data-steward-selective-integration-baseline` | current MVP runtime ref in landing manifest |
| hermes-agent install target | `phase-2.56e-natural-import-real-upload-smoke-baseline` | reviewed agent ref |

The Mac mini operator must not guess refs. If a ref is unavailable on the target machine, stop.

## 3. Operator Handoff Files

Mac mini side should read these files in order:

1. `docs/MAC_MINI_MVP_INSTALL_UPDATE_QUICKSTART.md`
2. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
3. `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`
4. `docs/PHASE265_MAC_MINI_MVP_LANDING_PLAN.md`

Optional manifest command:

```bash
cd /Users/hermes/code/Hermes_memory
uv run python scripts/phase265_mvp_release_manifest.py \
  --hermes-memory-ref phase-2.64b-data-steward-selective-integration-baseline \
  --hermes-agent-ref phase-2.56e-natural-import-real-upload-smoke-baseline \
  --operator mac-mini
```

Expected manifest status:

```text
ready_for_operator_review
```

## 4. Mac mini Execution Order

Phase 2.66a should be the first real Mac mini side execution task.

Recommended order:

1. Preflight only:
   - macOS version
   - user
   - git
   - uv
   - Docker
   - disk
   - target directories
   - network access to Git remote
2. Repo checkout:
   - `Hermes_memory`
   - `hermes-agent`
   - exact reviewed refs only
   - clean worktree check
3. Env readiness:
   - check required key names only
   - never print values
   - stop if missing
4. Runtime startup:
   - Docker compose only after preflight and repo checks pass
   - `/health`
   - `hermes chat --help`
5. Minimal internal MVP smoke:
   - only after runtime health passes
   - no real enterprise file upload unless separately authorized
6. Local run record:
   - save sanitized result under ignored local reports
   - do not commit local runtime outputs

## 5. Go / Pause / No-Go

### Go

All are true:

1. Both repos are checked out at reviewed refs.
2. Worktrees are clean.
3. Required tools are available.
4. Required env key names are present.
5. `/health` passes.
6. `hermes chat --help` passes.
7. No secret values are printed.
8. No repair / migration / backfill / reindex is needed.

### Pause

Any are true:

1. Missing secret key.
2. Git ref unavailable.
3. Worktree dirty.
4. Docker unavailable.
5. `/health` fails.
6. CLI help fails.
7. Migration need is unclear.
8. Operator lacks authorization for the current step.

### No-Go

Any are true:

1. Production rollout requested.
2. Repair / cleanup / delete / backfill / reindex requested.
3. Real DB smoke / NAS scan / Data Steward feature activation requested without explicit phase authorization.
4. Secret values are exposed.
5. Business code edits on Mac mini are proposed as a workaround.

## 6. Hard Boundaries

1. Do not perform production rollout.
2. Do not run repair / cleanup / backfill / reindex / delete / migration.
3. Do not scan NAS.
4. Do not enable Data Steward features.
5. Do not upload real business files unless a separate phase explicitly authorizes the exact file.
6. Do not print secrets or `.env` values.
7. Do not patch business code on Mac mini.
8. Do not commit local Mac mini runtime outputs.

## 7. Next Suggested Prompt

Suggested next task:

```text
Phase 2.66a Mac mini preflight only.

Run on the Mac mini side. Only check machine dependencies, target directories, Git remote access, reviewed refs availability, and env key presence by name. Do not start Docker, do not run API / CLI smoke, do not upload files, do not write DB/index, and do not modify business code. Return Go / Pause / No-Go.
```

## 8. Current Decision

Recommendation: start with Phase 2.66a preflight-only on the Mac mini side.

Do not jump directly to full install until preflight evidence is returned.
