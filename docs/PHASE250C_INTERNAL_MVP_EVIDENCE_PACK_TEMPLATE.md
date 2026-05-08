# Phase 2.50c Internal MVP Evidence Pack Template

## Goal

Phase 2.50c turns the Phase 2.50b evidence pack plan into sanitized template artifacts that a Mac Mini operator, Codex B, or a human reviewer can use as a fillable shape.

This phase does not create a real internal MVP evidence pack.

## Boundaries

This phase is docs / template only.

It does not:

1. generate a real evidence pack.
2. read real reports, run records, deployment records, reviews, or customer artifacts.
3. run API / CLI smoke.
4. start or stop services.
5. write DB, facts, document_versions, audit_logs, OpenSearch, or Qdrant.
6. execute repair, backfill, reindex, cleanup, delete, migration, or rollout.
7. authorize Data Steward implementation.

The templates are not:

1. production rollout approval.
2. customer delivery.
3. automatic tender review.
4. automatic bid.
5. automatic business decision.
6. repair authorization.

## Template Artifacts

Phase 2.50c adds:

1. `docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json`
   - machine-readable placeholder shape.
   - valid JSON.
   - `template_only=true`.
   - fixed safety flags: `production_rollout=false`, `repair_authorized=false`, `data_mutation=false`, `destructive_actions=[]`.
   - no real document IDs, fact IDs, session IDs, customer text, secrets, raw output, or local paths.

2. `docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md`
   - human-fillable Markdown template.
   - covers source artifact checklist, P0/P1/P2/P3 summary, citation and Missing Evidence checks, PRD matrix linkage, Go/Pause/No-Go, not-claimable items, and redaction / ignored storage checks.

3. `docs/PHASE250C_INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md`
   - phase record and boundary statement.

## Required JSON Fields

The JSON template contains:

1. `record_type="internal_mvp_evidence_pack_template"`.
2. `template_only=true`.
3. safety flags for no rollout, no repair, no mutation.
4. metadata placeholders for date, session, operator, reviewer.
5. `source_files` references for:
   - run record JSON.
   - Phase 2.49 review payload.
   - Phase 2.49 review report.
   - issue summary.
   - Codex C smoke summary.
   - operator sign-off summary.
   - deployment record summary.
   - human notes.
6. `summary` fields for severity counts, citation coverage, Missing Evidence, evidence policy flags, and third-document contamination.
7. `decision` with `go|pause|no_go|pending_review`.
8. `prd_acceptance_links`.
9. `not_claimable`.
10. `redaction_confirmed`.
11. `destructive_actions=[]`.

## Future Real Pack Requirements

A future real evidence pack requires a separate phase, explicit authorization, and ignored local storage.

Real evidence packs must not be committed to Git by default.

Any future generator must keep the same boundaries:

1. do not include raw model output.
2. do not include raw transcripts.
3. do not include raw customer source text.
4. do not include secrets, `.env`, tokens, passwords, or credentials.
5. do not include local absolute paths.
6. do not claim rollout, customer delivery, automatic tender review, automatic bid, automatic business decision, or repair authorization.

## Validation Results

Target validation for this phase:

1. `python3 -m json.tool docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json >/tmp/internal_mvp_evidence_pack_template_check.json`
2. `git diff --check`
3. `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`
4. ignored-path checks for `reports/agent_runs/latest.json`, `reports/internal_mvp_runs/*.json`, `reports/internal_mvp_runs/*.md`, `reports/internal_mvp_runs/latest.json`, and `reports/deployment_records/*`.

## Current Conclusion

Phase 2.50c creates sanitized evidence pack templates only.

It is ready for Codex B review after the target validation commands pass.

The next phase should not generate a real evidence pack unless Codex B and the user explicitly authorize a separate bounded phase.
