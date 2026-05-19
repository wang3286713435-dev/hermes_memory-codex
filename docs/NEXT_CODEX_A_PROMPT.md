# NEXT_CODEX_A_PROMPT

## Phase 2.102a Codex B Review / Selective Docs Baseline Preparation

You are Codex A. Do not start Phase 2.102b scoring from this file unless the user explicitly asks for a new bounded phase.

## Background

Phase 2.102a Eval Inventory Manifest has been created:

1. manifest: `eval/phase2_inventory/phase2_eval_inventory_manifest.json`
2. docs: `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`
3. status: ready for Codex B review
4. baseline: not yet authorized

The manifest contains:

1. accepted cases: 19
2. metric-eligible cases: 15
3. metric-ineligible cases: 4
4. required groups covered: 12

Current conclusion remains:

1. PRD 100+ question target is not satisfied.
2. Roadmap 300+ question target is not satisfied.
3. Top5 scoring was not computed.
4. Citation accuracy scoring was not computed.
5. Structured fact manual spot-check was not computed.

## Codex B Review Checklist

Review `eval/phase2_inventory/phase2_eval_inventory_manifest.json` and `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md` for:

1. JSON parses and has schema `phase2_eval_inventory_manifest.v1`.
2. Every case has `case_id`, `group`, `question`, `source_category`, `expected_evidence_mode`, `expected_document_refs`, `expected_citation_fields`, `forbidden_behaviors`, `metric_eligible`, `metric_exclusion_reason`, `evidence_ref`, and `notes`.
3. Required groups are covered:
   - `core_retrieval`
   - `tender_metadata`
   - `excel_structured_citation`
   - `pptx_structured_citation`
   - `meeting_transcript_boundary`
   - `facts_boundary`
   - `version_governance`
   - `permission_denial`
   - `gateway_catalog_only`
   - `data_steward_catalog_only`
   - `missing_evidence_unsupported_content`
   - `natural_import_usability`
4. Metric-ineligible cases are not counted toward Top5 / citation scoring.
5. Gateway / Data Steward / Missing Evidence / natural import cases remain boundary/planning/smoke evidence unless later converted into executable eval cases.
6. The manifest does not claim PRD 100+ / Roadmap 300+ target satisfaction.
7. The docs artifact states that Top5 and citation scoring were not computed.

## If User Authorizes Baseline

Only if the user explicitly authorizes baseline:

1. Confirm dirty files are limited to Phase 2.102a docs/data/status files.
2. Do not stage unrelated `docs/digital-delivery-standards/` files.
3. Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/phase2_eval_inventory_manifest.json >/dev/null
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

4. Commit message:

```text
docs: add phase 2 eval inventory manifest
```

5. Tag:

```text
phase-2.102a-eval-inventory-manifest-baseline
```

6. Push `origin/main` and the tag only if the user authorizes push.

## Hard Boundaries

1. Do not implement runtime code.
2. Do not modify existing tests.
3. Do not run API / CLI / Gateway / DB / NAS smoke.
4. Do not connect to DB or NAS.
5. Do not execute SQL.
6. Do not read ignored real reports, raw rows, NAS paths, storage paths, or secrets.
7. Do not write DB, OpenSearch, Qdrant, MinIO, platform systems, Gateway, Hermes memory, `documents`, or `chunks`.
8. Do not execute parser, scratch copy, writer smoke, repair, cleanup, backfill, reindex, delete, migration, or rollout.
9. Do not claim PRD 100+ / Roadmap 300+ target satisfaction.
10. Do not compute Top5 or citation accuracy from an unreviewed inventory.
11. Do not enter Phase 2.102b, Phase 2.103, or Phase 3 automatically.

## Next Recommended Phase If Review Passes

After Codex B review and optional baseline, the next planning candidate is:

```text
Phase 2.102b Metric Scoring Pack
```

But Phase 2.102b should score only the reviewed `metric_eligible=true` inventory subset or first expand the inventory if the user wants PRD 100+ / Roadmap 300+ target progress.
