# Phase 2.52 Post-Runbook Route Plan

## Goal

Phase 2.52 reviews the next bounded step after the Phase 2.51 Mac Mini operator / hot update runbook baseline.

This phase is planning-only. It does not execute Mac Mini deployment, start services, run API / CLI smoke, read real run records, write DB / facts / document_versions / audit_logs / OpenSearch / Qdrant, or enter production rollout.

## Current Baseline

- Phase 2.50a baseline: `232acf36d563e8f18e3b55ff5981a7ed3c39d766`, tag `phase-2.50a-internal-mvp-runbook-smoke-baseline`.
- Phase 2.51 baseline: `60b081acfa4771eaa5134be3cda2632885853663`, tag `phase-2.51-mac-mini-operator-runbook-baseline`.
- Phase 2.51 runbook established that the canonical Phase 2.49 bridge input is `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`; Markdown notes are optional human notes only.

## Candidate A: Phase 2.51a Fake Deployment Record Dry-run Smoke

Goal:

- Use fake / temporary deployment and hot update records to validate that the runbook record flow, ignored report strategy, and Phase 2.49 bridge expectations are understandable.

Value:

- Exercises the runbook with a synthetic record before any real Mac Mini operator run.
- Can catch record-shape problems early.

Risks:

- Could be mistaken as real deployment evidence if wording is loose.
- Adds another dry-run artifact before the operator has a simpler command surface.

Boundary:

- fake / temp data only.
- no real Mac Mini reports.
- no deployment, DB, index, repair, or rollout.

Fit:

- Useful, but should follow a minimal command sheet so the operator-facing flow is easier to run consistently.

## Candidate B: Phase 2.51b Minimal Operator Command Sheet

Goal:

- Extract the Phase 2.51 runbook into a concise operator command sheet with ordered commands, input placeholders, stop conditions, and record paths.

Value:

- Highest immediate operator usability.
- Reduces the chance of manual copy/paste mistakes on Mac Mini.
- Stays docs-only and does not require running services or touching data.

Risks:

- Must not become a deployment script.
- Must keep placeholders obvious and preserve stop conditions from the full runbook.

Boundary:

- docs-only.
- no shell script.
- no cron / scheduler.
- no command execution.
- no real Mac Mini deployment.

Fit:

- Best next step.

## Candidate C: Phase 2.50b Evidence Pack Planning

Goal:

- Plan the internal MVP daily review evidence pack directory, naming, human review fields, and Go / Pause / No-Go evidence linking.

Value:

- Useful once operator flow produces records.
- Connects Day-start, run record, Phase 2.49 bridge, and review artifacts.

Risks:

- Premature before the operator has a simple day-to-day command sheet.
- May expand artifact taxonomy before real operator feedback.

Boundary:

- planning-only.
- no report scan.
- no evidence upload.
- no rollout.

Fit:

- Good follow-up after Phase 2.51b.

## Recommendation

Recommend Phase 2.51b as the next bounded step: create a minimal operator command sheet.

Rationale:

1. Phase 2.51 already created the full runbook; the immediate gap is operator ergonomics.
2. A command sheet is docs-only and low-risk.
3. It reduces the chance that a real Mac Mini operator misses stop conditions or records the wrong file shape.
4. Fake deployment record smoke is still useful, but should use the command sheet as the operator-facing source.

## Phase 2.51b Minimum Boundary

Create one docs-only artifact, suggested:

- `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`

The command sheet should include:

1. Preconditions and required reviewed Git refs.
2. Day-start read-only checks.
3. Hot update command placeholders.
4. Health check command placeholders.
5. Canonical JSON run record path.
6. Optional Markdown notes path.
7. Phase 2.49 review command.
8. Rollback command placeholders.
9. Stop conditions.
10. Explicit no-rollout / no-repair / no-DB-write boundary.

## Non-goals

Phase 2.51b must not:

1. Create deployment scripts.
2. Create cron / scheduler.
3. Run real commands.
4. Start or stop services.
5. Pull remote or checkout tags.
6. Read real reports / run records.
7. Write DB / facts / document_versions / audit_logs / OpenSearch / Qdrant.
8. Execute repair / backfill / reindex / cleanup / delete / migration.
9. Enter production rollout.
10. Enter Data Steward / BIM implementation.

## Risks

1. Command sheet could be copied as a script if formatting is too shell-like; use clear placeholder warnings.
2. Operator may still need human training; command sheet is not a substitute for review discipline.
3. Out-of-scope dirty files remain in the repo and must stay excluded from any future baseline.

## Current Decision

Proceed to Phase 2.51b planning / docs-only artifact prompt after Codex B review.
