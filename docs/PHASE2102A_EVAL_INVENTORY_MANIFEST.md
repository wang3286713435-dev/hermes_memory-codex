# Phase 2.102a Eval Inventory Manifest

## 1. Summary

Phase 2.102a creates a committed starter inventory for future Phase 2 metric scoring.

Manifest path:

```text
eval/phase2_inventory/phase2_eval_inventory_manifest.json
```

Schema:

```text
phase2_eval_inventory_manifest.v1
```

Current conclusion:

1. Inventory created: yes.
2. PRD 100+ question target satisfied: no.
3. Roadmap 300+ question target satisfied: no.
4. Top5 scoring computed: no.
5. Citation accuracy scoring computed: no.
6. Structured fact manual spot-check computed: no.

This phase only establishes a denominator seed. It does not run runtime eval, does not connect to DB / NAS / Gateway, and does not convert smoke evidence into percentage metrics.

## 2. Count Summary

| count | value |
|---|---:|
| accepted_case_count | 19 |
| metric_eligible_case_count | 15 |
| metric_ineligible_case_count | 4 |
| required group count | 12 |
| groups covered | 12 |
| PRD 100+ target status | `not_satisfied_19_of_100` |
| Roadmap 300+ target status | `not_satisfied_19_of_300` |

The inventory intentionally remains small. It is based on committed eval runner cases, committed phase docs, and committed boundary artifacts only.

## 3. Group Coverage

| group | representative case count | metric eligibility | evidence basis |
|---|---:|---|---|
| `core_retrieval` | 2 | eligible | `scripts/phase214_regression_eval.py` core cases |
| `tender_metadata` | 3 | eligible | Phase 2.14 / 2.20 eval cases |
| `excel_structured_citation` | 1 | eligible | Excel sheet/cell eval case |
| `pptx_structured_citation` | 1 | eligible | PPTX slide citation eval case |
| `meeting_transcript_boundary` | 3 | eligible | action / decision / risk eval cases |
| `facts_boundary` | 2 | eligible for facts fixture eval only | facts eval cases; not manual 90% spot-check |
| `version_governance` | 2 | eligible | governance eval cases |
| `permission_denial` | 1 | eligible | tenant mismatch deny governance eval |
| `gateway_catalog_only` | 1 | ineligible | controlled smoke / runbook docs only |
| `data_steward_catalog_only` | 1 | ineligible | catalog-only boundary docs only |
| `missing_evidence_unsupported_content` | 1 | ineligible | standard boundary artifact, not executable metric case |
| `natural_import_usability` | 1 | ineligible | planning/mock evidence, no live usability metric |

## 4. Metric Eligibility Rules

A case is `metric_eligible=true` only when it has:

1. Stable `case_id`.
2. Concrete question.
3. Explicit expected document or fixture reference.
4. Citation / trace expectations.
5. Forbidden behavior assertions.
6. Committed evidence reference that can be reviewed.

A case remains `metric_eligible=false` when:

1. It is a docs-only boundary or runbook item.
2. It lacks executable deterministic eval or accepted terminal validation.
3. It would require ignored private reports, raw DB rows, NAS paths, storage paths, or secrets.
4. It is a user-experience or source-category placeholder without committed denominator evidence.

## 5. Known Gaps Before Phase 2.102b Scoring

| gap | impact | next action |
|---|---|---|
| Starter inventory has 19 cases, not PRD 100+ | PRD metric target not satisfied | Expand reviewed inventory before scoring |
| Starter inventory has 19 cases, not Roadmap 300+ | Roadmap Phase 2 target not satisfied | User decision or expanded inventory required |
| Top5 not computed | Top5 80/85 cannot be claimed | Phase 2.102b only after inventory review |
| Citation accuracy not computed | Citation 85/90 cannot be claimed | Phase 2.102b only after inventory review |
| Structured fact manual spot-check missing | Roadmap 90% fact spot-check cannot be claimed | Separate manual review artifact required |
| Official account / PDF / HTML parser evidence incomplete | PRD source/parser coverage not fully evidenced | Parser/source evidence pack or explicit deferral |
| Gateway / Data Steward cases are catalog-only | Not production or content-evidence metrics | Keep boundary wording strict |
| Natural-language import lacks live usability evidence | User-facing import metric not evidenced | Controlled usability smoke or user-approved deferral |

## 6. Exact Next Step

Recommended next phase:

```text
Phase 2.102b Metric Scoring Pack
```

But only after Codex B reviews this manifest and the user accepts the starter inventory boundary.

Phase 2.102b must not score Top5 or citation accuracy against an unreviewed inventory. The safer sequence is:

1. Codex B review Phase 2.102a.
2. User authorizes selective docs/data baseline if accepted.
3. Phase 2.102b computes metrics only for accepted eligible cases or expands the inventory first.

## 7. Non-goals

This phase did not:

1. Implement runtime code.
2. Modify tests.
3. Run API / CLI / Gateway / DB / NAS smoke.
4. Connect to DB or NAS.
5. Execute SQL.
6. Read ignored real reports, raw rows, NAS paths, storage paths, or secrets.
7. Write DB, OpenSearch, Qdrant, MinIO, platform systems, Gateway, Hermes memory, `documents`, or `chunks`.
8. Execute parser, scratch copy, writer smoke, repair, cleanup, backfill, reindex, delete, migration, or rollout.
9. Claim PRD 100+ / Roadmap 300+ satisfaction.
10. Compute Top5 or citation accuracy.
