# Phase 2.64 Data Steward DB Branch Intake / PR Review

## Goal

Phase 2.64 records the intake state for the Data Steward DB branch and prepares it for Codex B / user review.

This phase does not merge the branch into `main`, does not connect to a real database, does not scan NAS, and does not continue DB feature development.

## DB Branch State

- Worktree: `/Users/Weishengsu/Hermes_memory_db0`
- Branch: `codex/data-steward-db0-contract`
- Local HEAD: `a272081`
- Remote branch after push: `a272081f1ddd5c71086c488c3f9142eb39e3efa6`
- Closeout tag: `phase-db-branch-closeout-merge-readiness-baseline`
- Remote tag after push: `a272081f1ddd5c71086c488c3f9142eb39e3efa6`
- Previous DB-4D baseline: `39cda74` / `phase-db4d-readonly-local-live-smoke-interface-baseline`

## Verification

Executed in `/Users/Weishengsu/Hermes_memory_db0`:

```bash
git branch --show-current
git status --short
git rev-parse --short HEAD
git describe --tags --abbrev=0
npm test
npm run lint
git diff --check
git log --oneline -1
```

Results:

- Branch: `codex/data-steward-db0-contract`
- HEAD: `a272081`
- Tag: `phase-db-branch-closeout-merge-readiness-baseline`
- `npm test`: `71 passed`
- `npm run lint`: `All checks passed!`
- `git diff --check`: passed
- Last commit: `a272081 DB branch closeout merge readiness`

## DB Branch Push Result

The branch and closeout tag were pushed:

```text
codex/data-steward-db0-contract -> origin/codex/data-steward-db0-contract
phase-db-branch-closeout-merge-readiness-baseline -> origin/phase-db-branch-closeout-merge-readiness-baseline
```

## Untracked QA Probe Files

The DB worktree still contains only expected untracked QA probe files. They were not staged, deleted, or pushed:

- `tests/test_db1_contract_probe.py`
- `tests/test_db1_contract_probe_round2.py`
- `tests/test_db1_contract_probe_round3.py`
- `tests/test_db2_mirror_probe.py`
- `tests/test_db2_temp_db_probe.py`
- `tests/test_db3a_retrieval_guard_probe.py`
- `tests/test_db3b_temp_db_guard_probe.py`
- `tests/test_db3c_missing_evidence_response_probe.py`
- `tests/test_db3d_temp_db_missing_evidence_response_probe.py`
- `tests/test_db4a_readonly_preflight_probe.py`
- `tests/test_db4c_readonly_live_smoke_probe.py`
- `tests/test_db4d_readonly_local_live_smoke_probe.py`

## Merge Readiness Gates

Before any PR or merge decision, the following gates must remain true:

1. Feature flags default off.
2. Catalog-only assets do not enter `documents` or `chunks`.
3. Catalog-only assets do not write OpenSearch or Qdrant.
4. `asset_catalog_only` Missing Evidence remains available for content questions without text evidence.
5. Missing `permission_tags` / `project_scope` defaults to deny.
6. No real DB secrets enter the repository.
7. No real NAS scan output enters the repository.
8. QA probe files are not merged.
9. Mainline retrieval / ingestion / memory kernel behavior is not broken.
10. DB branch remains a catalog / readiness layer until separately authorized.

## Test-machine Real DB Smoke Preconditions

Real DB smoke remains postponed. It requires:

1. Hermes Memory deployed on the test machine.
2. User authorization for the exact smoke.
3. Database team confirmation that the four View contracts remain compatible.
4. Safe credential transfer for `hermes_agent_ro`.
5. Either structure-only smoke or explicitly authorized `LIMIT 30` smoke.
6. Sanitized output only.

The smoke must not output real project names, file names, NAS paths, raw rows, `asset_uid`, `source_id`, stderr, or passwords.

## Non-goals

This phase does not:

- connect to real MySQL / PostgreSQL / platform DB
- scan NAS
- read `/Volumes/zyzn/卓羽智能项目`
- write migration
- write `documents` / `chunks`
- write OpenSearch / Qdrant / MinIO
- perform retrieval / indexing
- implement DB-5 selective indexing
- implement DB-6 operation plan / approval
- merge the DB branch into `main`
- create a PR automatically
- enter production rollout

## Current Conclusion

DB branch intake is documented and the closeout branch/tag are now pushed. The next step is Codex B review, then a separate user decision on whether to create a PR, draft a merge plan, or wait for test-machine DB smoke.
