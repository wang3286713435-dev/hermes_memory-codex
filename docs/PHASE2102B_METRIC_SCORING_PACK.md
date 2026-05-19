# Phase 2.102b Metric Scoring Pack

## Purpose

Phase 2.102b adds an offline scoring pack for the Phase 2.102a evaluation inventory.

The scorer reads:

1. committed manifest: `eval/phase2_inventory/phase2_eval_inventory_manifest.json`
2. explicit reviewed results JSON passed by `--results`

It computes Top5 hit rate, citation correctness rate, missing result IDs, excluded case IDs, and forbidden behavior violations.

## Scope

This phase is scoring machinery only.

It does not:

1. run live retrieval
2. call Hermes API / CLI / Gateway
3. connect to DB / NAS / OpenSearch / Qdrant / MinIO
4. run parser, scratch copy, writer smoke, repair, backfill, reindex, migration, or rollout
5. expand the inventory to PRD 100+ or Roadmap 300+
6. close Phase 2

## CLI

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase2102b_metric_scoring_pack.py \
  --manifest eval/phase2_inventory/phase2_eval_inventory_manifest.json \
  --results /path/to/sanitized_phase2_results.json
```

Optional output:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python scripts/phase2102b_metric_scoring_pack.py \
  --results /path/to/sanitized_phase2_results.json \
  --output /tmp/phase2_metric_summary.json
```

`--output` is only written when explicitly provided. Otherwise the sanitized JSON summary is printed to stdout.

## Results Schema

Reviewed results must use:

```json
{
  "schema_version": "phase2_eval_results.v1",
  "results": [
    {
      "case_id": "phase2_core_001_qa_doc_single_file_scope",
      "top5_hit": true,
      "citation_ok": true,
      "forbidden_behaviors_observed": [],
      "notes": "sanitized optional note"
    }
  ]
}
```

Allowed result fields:

1. `case_id`
2. `top5_hit`
3. `citation_ok`
4. `forbidden_behaviors_observed`
5. `notes`

Raw answer text, raw DB rows, NAS paths, storage paths, local paths, tokens, API keys, and secrets are rejected.

## Scoring Rules

Only manifest cases with `metric_eligible=true` count toward Top5 and citation denominators.

Cases with `metric_eligible=false` are reported in `excluded_case_ids`, but they never improve rates.

Forbidden behavior is evaluated across all known result rows, including metric-ineligible cases. Ineligible cases stay out of the Top5 / citation denominator, but any observed forbidden behavior still blocks review.

If an eligible case has no result, the summary status is `incomplete`.

If any known result contains `forbidden_behaviors_observed`, the summary status is `blocked_for_review`.

If all eligible cases have results and no forbidden behavior is observed, the summary status is `scored`.

`phase2_closeout_readiness` is always `false` in this phase.

## Output Fields

The scorer emits:

1. `schema_version=phase2_metric_scoring_pack.v1`
2. `manifest_case_count`
3. `metric_eligible_case_count`
4. `metric_ineligible_case_count`
5. `results_case_count`
6. `scored_case_count`
7. `missing_result_case_ids`
8. `excluded_case_ids`
9. `top5_hit_count`
10. `top5_hit_rate`
11. `citation_ok_count`
12. `citation_ok_rate`
13. `forbidden_violation_count`
14. `forbidden_violation_case_ids`
15. `status`
16. `phase2_closeout_readiness`
17. `prd_100_target_status`
18. `roadmap_300_target_status`

## Current Baseline Meaning

The current committed inventory has:

1. accepted cases: 19
2. metric-eligible cases: 15
3. metric-ineligible cases: 4

This does not satisfy:

1. PRD 100+ eval question target
2. Roadmap 300+ eval question target
3. PRD/Roadmap Top5 targets
4. PRD/Roadmap citation accuracy targets
5. structured fact manual spot-check target

Phase 2 remains open after Phase 2.102b.

## Validation

Completed local validation:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile scripts/phase2102b_metric_scoring_pack.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_phase2102b_metric_scoring_pack.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

No live runtime smoke is required or allowed for this phase.
