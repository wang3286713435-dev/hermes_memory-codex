# Phase 2.49 Internal MVP Run Record Review Bridge

## Goal

Phase 2.49 adds a local-only bridge from an explicit internal MVP run record JSON to a sanitized Phase 2.42a review dry-run payload.

The purpose is to reduce manual table copying after Day-0 / Day-1 internal MVP runs. This phase is not production rollout, customer delivery, automatic tender review, automatic business decision, Data Steward implementation, or repair authorization.

## Implemented Scope

The new runner is:

- `scripts/phase249_internal_mvp_run_record_review.py`

It requires:

- `--input-run-record <path>`

It never scans `reports/` by default. It only reads the explicitly supplied JSON file.

The runner outputs:

- `review_payload`
- optional `review_report` when `--review-report` is passed

The `review_payload` is compatible with `scripts/phase242a_mvp_pilot_review_dry_run.py::build_review_report()`.

## Sanitized Payload Fields

The bridge produces:

- `pilot_round`
- `reviewer`
- `source_sessions`
- `p0_items`
- `p1_items`
- `p2_items`
- `p3_items`
- `evidence_policy`
- `citation_summary`
- `missing_evidence`
- `known_risks`
- `next_phase_candidates`
- `not_claimable_confirmed`

The fixed safety flags are:

- `dry_run=true`
- `production_rollout=false`
- `repair_authorized=false`
- `destructive_actions=[]`
- `data_mutation=false`

## Decision Mapping

The bridge maps run record observations into review tendency:

- P0 / unsafe evidence policy / third-document contamination => `no_go`
- unreviewed alias missing, retrieval suppressed, hidden Missing Evidence, or blocking P1 => `pause`
- visible and human-reviewed Missing Evidence may continue as internal controlled MVP review
- clean records => `go`

The bridge does not claim production readiness. `go` only means the record is compatible with continued internal controlled MVP review.

## Unsafe Signals

The following signals are promoted to P0 / unsafe or pause:

- `facts_as_answer=true`
- `transcript_as_fact=true`
- `snapshot_as_answer=true`
- `third_document_contamination=true`
- persistent `alias_missing=true`
- `retrieval_suppressed=true`
- P0 issue summary entry
- hidden or unreviewed Missing Evidence

## Output Policy

By default the runner prints JSON to stdout only.

If `--output-dir` is provided, it writes sanitized JSON / Markdown only to that explicit directory. Tests use temporary directories only. The runner must not write real reports into tracked repo paths by default.

## Prohibited Inputs / Outputs

Run records must not contain or propagate:

- raw model output
- secrets
- `.env` values
- tokens / passwords
- customer-sensitive source text
- raw transcript content

The runner does not read:

- DB
- API
- Hermes CLI
- OpenSearch
- Qdrant
- facts
- document versions

## Validation

Implemented tests:

- safe fake run record builds `go` compatible payload
- `facts_as_answer=true` produces unsafe / `no_go`
- `transcript_as_fact=true` produces unsafe / `no_go`
- third-document contamination becomes P0 / `no_go`
- alias missing / retrieval suppressed pauses unless reviewed workaround exists
- hidden Missing Evidence pauses
- script requires explicit `--input-run-record`
- optional output writes only to explicit temporary output directory
- optional `--review-report` integrates with Phase 2.42a report builder

## Current Conclusion

Phase 2.49 is implemented and the Codex B review-fix has been applied.

Review-fix coverage:

- `issue_summary.p0_count > 0` now creates a P0 placeholder item when detailed `issues` are absent.
- `issue_summary.p1_count > 0` now creates a blocking P1 placeholder item when detailed `issues` are absent.
- `issue_summary.p2_count / p3_count > 0` now creates non-blocking placeholder items when detailed `issues` are absent.
- `not_repair_cleanup_backfill_reindex_delete=false` now sets `evidence_policy.repair_authorized=true`, creates a P0 boundary item, and makes `decision_hint=no_go`.
- `no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation=false` now sets `evidence_policy.data_mutation=true`, creates a P0 boundary item, and makes `decision_hint=no_go`.
- `decide_hint()` now treats production rollout, repair, data mutation, facts-as-answer, transcript-as-fact, snapshot-as-answer, and third-document contamination as unsafe.

No baseline has been created. No real internal MVP run records were read. No API / CLI smoke was run. No business data, DB, facts, document versions, audit logs, OpenSearch, or Qdrant writes occurred.

## Next Step

Codex B should review the runner and tests. If accepted, the next action is a Phase 2.49 Git baseline prompt. Phase 2.50 should not start before that review / baseline decision.
