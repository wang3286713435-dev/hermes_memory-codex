# Nightly Sprint Queue

## Current Queue State

- Current phase: Phase 2.64b Selective Data Steward DB Integration.
- Current state: implementation completed, waiting for Codex B review.
- Current allowed work: review documentation, selective baseline prompt preparation after review, and merge readiness checklist review.
- Current forbidden work: real DB connection, NAS scan, migration, DB-5 / DB-6, real retrieval / indexing, PR creation, merge to `main`, production rollout.

## Green Lane

1. Codex B review of Phase 2.64b selective integration.
2. Documentation-only clarification if Codex B finds wording gaps in integration scope or merge gates.

## Yellow Lane

1. Phase 2.64b selective Git baseline: only after Codex B review.
2. PR creation for `codex/data-steward-db0-contract`: only after user approval.
3. Merge planning for DB branch: only after Codex B review and user approval.
4. Test-machine real DB smoke planning: only after test-machine deployment and user approval.

## Red Lane

1. Connect to real database.
2. Scan NAS or `/Volumes/zyzn/卓羽智能项目`.
3. Write migration / `documents` / `chunks` / OpenSearch / Qdrant.
4. DB-5 selective indexing or DB-6 operation plan / approval.
5. Merge DB branch into `main`.
6. Production rollout.
