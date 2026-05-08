# Internal MVP Evidence Pack Template

This is a sanitized fillable template for an internal controlled MVP evidence pack.

It is not production rollout approval, customer delivery approval, automatic tender review approval, automatic bid approval, automatic business decision evidence, or repair authorization.

Real evidence packs must be stored in ignored local paths and must not be committed to Git.

## 1. Metadata

| Field | Value |
|---|---|
| date | `YYYY-MM-DD` |
| session_id | `placeholder_sanitized_session_id` |
| operator | `placeholder_operator` |
| reviewer | `placeholder_reviewer` |
| review_status | `pending_review` / `go` / `pause` / `no_go` |
| human_owner | `placeholder_human_owner` |

## 2. Source Artifact Checklist

| Artifact | Required | Present | Sanitized reference |
|---|---:|---|---|
| canonical run record JSON | yes | yes / no | `placeholder_ignored_run_record_json_ref` |
| Phase 2.49 review payload | yes | yes / no | `placeholder_phase249_review_payload_ref` |
| Phase 2.49 review report | recommended | yes / no | `placeholder_phase249_review_report_ref` |
| issue summary | recommended | yes / no | `placeholder_issue_summary_ref` |
| Codex C smoke summary | optional | yes / no | `placeholder_codex_c_smoke_summary_ref` |
| operator sign-off summary | recommended | yes / no | `placeholder_operator_signoff_summary_ref` |
| deployment record summary | optional | yes / no / not_applicable | `placeholder_optional_deployment_record_summary_ref` |
| human notes | optional | yes / no | `placeholder_optional_human_notes_ref` |

Do not include raw model output, raw transcripts, raw customer source text, secrets, tokens, passwords, `.env` values, or local absolute paths.

## 3. Severity Summary

| Severity | Count | Notes |
|---|---:|---|
| P0 | 0 | `placeholder_p0_notes` |
| P1 | 0 | `placeholder_p1_notes` |
| P2 | 0 | `placeholder_p2_notes` |
| P3 | 0 | `placeholder_p3_notes` |

P0 requires `no_go`.

P1 requires bounded follow-up or explicit human acceptance before any continuation.

## 4. Citation / Missing Evidence / Evidence Policy Checklist

| Check | Required value | Observed | Notes |
|---|---|---|---|
| document_id visible where relevant | true | yes / no | `placeholder` |
| version_id visible where relevant | true | yes / no | `placeholder` |
| chunk_id or structured citation visible | true | yes / no | `placeholder` |
| Excel sheet / cell range visible where relevant | true / not_applicable | yes / no / not_applicable | `placeholder` |
| PPTX slide number / title visible where relevant | true / not_applicable | yes / no / not_applicable | `placeholder` |
| Missing Evidence visible | true | yes / no | `placeholder` |
| Missing Evidence not rewritten as certainty | true | yes / no | `placeholder` |
| `facts_as_answer` | false | false | `placeholder` |
| `transcript_as_fact` | false | false | `placeholder` |
| `snapshot_as_answer` | false | false | `placeholder` |
| third-document contamination | false | false | `placeholder` |

## 5. PRD Acceptance Matrix Linkage

| capability_area | status | evidence_ref | reviewer note |
|---|---|---|---|
| `placeholder_capability_area` | `done` / `partial` / `planned` / `deferred` | `placeholder_sanitized_evidence_ref` | `placeholder` |

Use `docs/PRD_ACCEPTANCE_MATRIX.md` status meanings.

Do not mark a capability `done` unless it is supported by committed tests, eval, smoke, reviewed evidence, or a baseline reference.

## 6. Go / Pause / No-Go Decision

| Field | Value |
|---|---|
| decision | `pending_review` / `go` / `pause` / `no_go` |
| reason | `placeholder_human_review_reason` |
| human_owner | `placeholder_human_owner` |
| required_follow_up | `placeholder_follow_up` |

`go` only means the internal controlled MVP loop may continue under human review.

`go` is not production rollout approval, customer delivery approval, automatic tender review approval, automatic bid approval, automatic business decision evidence, or repair authorization.

## 7. Not-Claimable

Confirm the evidence pack does not claim:

- production ready.
- customer delivery ready.
- automatic tender review.
- automatic bid.
- automatic business decision.
- repair executor ready.
- facts automatic extraction complete.
- facts can replace retrieval evidence.
- Data Steward implemented.
- TB-scale BIM full parsing.
- complete knowledge graph, complete RBAC, or complete multi-agent system.

## 8. Redaction / Ignored Storage Checklist

| Redaction item | Confirmed |
|---|---|
| no secrets / tokens / passwords / `.env` values | yes / no |
| no raw model output | yes / no |
| no raw transcript | yes / no |
| no raw customer source text | yes / no |
| no real document_id / fact_id / session_id in tracked artifact | yes / no |
| no local absolute paths | yes / no |
| real evidence pack stored under ignored local path | yes / no |
| no real evidence pack JSON / Markdown staged for Git | yes / no |

## 9. Reviewer Sign-off

| Field | Value |
|---|---|
| reviewer | `placeholder_reviewer` |
| reviewed_at | `YYYY-MM-DD HH:MM` |
| decision | `pending_review` / `go` / `pause` / `no_go` |
| notes | `placeholder_sanitized_notes` |

