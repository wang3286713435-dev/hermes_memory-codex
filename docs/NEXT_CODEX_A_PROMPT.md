# NEXT_CODEX_A_PROMPT

## Phase 2.102 Codex B Review / Selective Docs Baseline Preparation

You are Codex A. Do not start new implementation from this file unless the user explicitly asks for Codex B review support or Git baseline preparation.

## Background

Phase 2.102 Metric / Evaluation Evidence Pack has been created:

1. artifact: `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`
2. status: ready for Codex B review
3. current decision: Phase 2 metric closeout decision=`not_ready`
4. baseline: not yet authorized

The evidence pack uses committed docs/tests only. It does not read ignored real reports, raw DB rows, NAS paths, secrets, or local private run records.

## Codex B Review Checklist

Review `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md` for:

1. Evidence taxonomy includes `measured_pass`, `measured_fail`, `partial_evidence`, `smoke_only_not_metric`, `missing_metric`, and `requires_user_decision`.
2. Metric table covers PRD 100+ / Roadmap 300+ eval inventory, Top5 80/85, citation 85/90, structured fact manual spot-check 90, permission denial, parser/source categories, Gateway/Data Steward, Mac mini / employee trial, natural import, Missing Evidence, facts/transcript/version boundaries.
3. Numeric metric claims are not invented; missing numerator/denominator items remain `missing_metric`.
4. Gateway / Data Steward evidence remains catalog-only and read-only, not production rollout or content-evidence.
5. Facts and transcript boundaries remain evidence-policy claims, not automatic fact extraction or final answer replacement.
6. Final closeout decision remains `not_ready` unless Codex B and the user explicitly accept exceptions.

## If User Authorizes Baseline

Only if the user explicitly authorizes baseline:

1. Confirm dirty files are limited to Phase 2.102 docs/status files.
2. Do not stage unrelated `docs/digital-delivery-standards/` files.
3. Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

4. Commit message:

```text
docs: add phase 2 metric evidence pack
```

5. Tag:

```text
phase-2.102-metric-evaluation-evidence-pack-baseline
```

6. Push `origin/main` and the tag if the user authorizes push.

## Hard Boundaries

1. Do not implement runtime code.
2. Do not modify tests.
3. Do not run API / CLI / Gateway / DB / NAS smoke.
4. Do not connect to DB or NAS.
5. Do not read ignored real reports, raw rows, NAS paths, storage paths, or secrets.
6. Do not write DB, OpenSearch, Qdrant, MinIO, platform systems, Gateway, Hermes memory, `documents`, or `chunks`.
7. Do not execute parser, scratch copy, writer smoke, repair, cleanup, backfill, reindex, delete, migration, or rollout.
8. Do not enter Phase 2.103 or Phase 3 automatically.

## Next Recommended Phase If Review Passes

After Codex B review and optional baseline, the next planning candidate is:

```text
Phase 2.102a Eval Inventory Manifest
```

Goal: create a committed eval inventory with stable question IDs, groups, expected documents, expected citations, and source requirements before any Top5 / citation metric scoring.
