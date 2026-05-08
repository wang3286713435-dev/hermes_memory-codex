# Phase 2.50b Internal MVP Evidence Pack Planning

## Positioning

The internal MVP evidence pack is a human-review artifact for the internal controlled MVP loop.

It collects references to run records, review outputs, operator records, issue intake, and smoke summaries so Codex B / human reviewers can decide whether the internal MVP loop should continue, pause, or stop.

It is not:

1. production rollout approval.
2. customer delivery approval.
3. automatic tender review approval.
4. automatic bid approval.
5. automatic business decision evidence.
6. repair / cleanup / backfill / reindex authorization.

This planning phase does not generate a real evidence pack, scan real reports, run API / CLI smoke, start services, write DB / facts / document_versions / audit_logs / OpenSearch / Qdrant, or enter rollout.

## Minimum Evidence Pack Composition

A future internal MVP evidence pack should be a pointer bundle, not a raw data dump.

Minimum components:

| Component | Source | Required | Notes |
|---|---|---:|---|
| canonical run record JSON | `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json` | yes | Explicit JSON input for Phase 2.49 bridge. |
| Phase 2.49 review payload | `phase249_review_payload.json` | yes | Sanitized dry-run output. |
| Phase 2.49 review report | `phase249_review_report.json` | recommended | Used for Go / Pause / No-Go summary. |
| operator checklist / command sheet sign-off summary | Mac Mini operator notes | recommended | Summary only; no raw local logs in tracked docs. |
| issue intake / triage summary | `reports/pilot_issues/` / triage output | recommended | Link P0/P1/P2/P3 issues without auto-fixing. |
| Codex C smoke / Pilot summary | Codex C report or sanitized summary | optional | Include session id / pass-partial-fail counts when available. |
| deployment record summary | `reports/deployment_records/` | optional | Only when a separately authorized human operator run exists. Empty otherwise. |
| optional human notes | Markdown notes | optional | Human-readable only; not Phase 2.49 bridge input. |

The pack should not include raw model output, raw transcript, customer source text, secrets, `.env` values, tokens, passwords, or local absolute paths.

## Directory And Naming Proposal

Suggested ignored local directory:

```text
reports/internal_mvp_runs/<YYYYMMDD>_<session>_evidence_pack/
```

Candidate files:

```text
manifest.json
summary.md
review_payload.json
review_report.json
issue_summary.json
codex_c_smoke_summary.json
operator_signoff_summary.json
deployment_record_summary.json
human_notes.md
```

Naming rules:

1. `<YYYYMMDD>` should match the internal MVP run date.
2. `<session>` should be sanitized and traceable to the operator record.
3. `manifest.json` should contain paths and hashes to local ignored artifacts.
4. `summary.md` should be human-readable and must not contain raw sensitive content.
5. Real evidence pack JSON / Markdown stays ignored by Git.

Tracked Git may contain only sanitized planning docs, templates, README files, and fake examples after review.

## Manifest Fields

A future `manifest.json` may contain:

```json
{
  "record_type": "internal_mvp_evidence_pack_manifest",
  "dry_run": true,
  "production_rollout": false,
  "repair_authorized": false,
  "date": "YYYY-MM-DD",
  "session_id": "<sanitized-session-id>",
  "operator": "<name-or-role>",
  "reviewer": "<name-or-role>",
  "source_files": {
    "run_record_json": "...",
    "phase249_review_payload": "...",
    "phase249_review_report": "...",
    "issue_summary": "...",
    "codex_c_smoke_summary": "...",
    "deployment_record_summary": ""
  },
  "decision": "go|pause|no_go",
  "decision_reason": "",
  "not_claimable": []
}
```

This is a planning shape only. Phase 2.50b does not create this file.

## Human Review Fields

Every evidence pack should expose these human-review fields:

| Field | Purpose |
|---|---|
| reviewer | Human reviewer / Codex B reviewer. |
| operator | Mac Mini or internal MVP operator. |
| date | Run date. |
| session_id | Sanitized session reference. |
| review_status | `pending_review`, `accepted`, `pause`, `no_go`, or equivalent. |
| P0 / P1 / P2 / P3 summary | Issue severity overview. |
| citation coverage | Whether evidence includes document/version/chunk references. |
| Missing Evidence visibility | Whether Missing Evidence was surfaced and reviewed. |
| facts_as_answer | Must remain `false`. |
| transcript_as_fact | Must remain `false`. |
| snapshot_as_answer | Must remain `false`. |
| third_document_contamination | Must remain `false` for Go. |
| Go / Pause / No-Go decision | Human-reviewed continuation judgment. |
| decision_reason | Short reviewer rationale. |
| not_claimable | Explicit list of capabilities not proven by the evidence pack. |

## PRD Acceptance Matrix Linkage

Evidence packs can be linked from `docs/PRD_ACCEPTANCE_MATRIX.md` through `evidence_ref`.

Recommended linkage:

1. `evidence_ref` should point to a sanitized summary or commit/tag, not raw local report content.
2. A capability can be marked `done` only when supported by committed tests, eval, smoke, or reviewed evidence.
3. A capability with Missing Evidence, partial recall, manual review, or limited coverage should remain `partial`.
4. Planned capabilities should remain `planned`.
5. Data Steward / BIM productization, production rollout, repair executor, automatic facts extraction, and complete automatic tender review remain `deferred` unless separate phases implement and validate them.

## Redaction / Ignore / Storage Policy

The evidence pack storage strategy is local-first and ignored by default.

Do not commit:

1. real run records.
2. raw model output.
3. raw transcript content.
4. customer source text.
5. raw screenshots containing sensitive content.
6. secrets, `.env`, tokens, passwords, or credentials.
7. local absolute paths when they reveal operator or customer context.
8. real evidence pack JSON / Markdown.
9. `latest.*` pointers or local manifests unless explicitly sanitized and reviewed.

Allowed in Git:

1. planning docs.
2. sanitized templates.
3. README / `.gitignore` storage rules.
4. fake examples after Codex B review.

## Go / Pause / No-Go Semantics

### Go

`Go` only means the internal controlled MVP may continue under the same human-review boundaries.

It is not rollout approval, customer delivery approval, automatic tender review approval, automatic bid approval, or automatic business decision evidence.

### Pause

`Pause` means the loop should stop expanding until a bounded review or fix handles the issue.

Typical reasons:

1. P1 blocker.
2. alias/session instability.
3. unreviewed Missing Evidence.
4. unclear citation.
5. operator uncertainty.

### No-Go

`No-Go` means the current internal MVP run must stop.

No-Go triggers include:

1. any P0.
2. facts / transcript / snapshot replacing retrieval evidence.
3. hidden Missing Evidence.
4. third-document contamination.
5. permission leakage.
6. repair / cleanup / backfill / reindex requirement.
7. rollout or customer-delivery claim.

## Future Phase Candidates

1. Phase 2.50c: evidence pack fake artifact / sanitized template.
2. Phase 2.50d: evidence pack generator dry-run.
3. Phase 2.50e: Codex B review checklist for evidence packs.
4. Real Mac Mini operator evidence pack: only after separate human authorization.

## Current Conclusion

Phase 2.50b establishes the evidence pack structure and governance semantics only.

It does not create a real pack, scan real reports, run services, write data, execute repair, or approve rollout.

