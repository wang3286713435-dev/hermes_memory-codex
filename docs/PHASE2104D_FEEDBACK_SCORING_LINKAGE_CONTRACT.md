# Phase 2.104d Feedback / Scoring Linkage Contract

## 1. Purpose

Phase 2.104d defines how platform feedback may later feed Hermes evaluation inventory, offline scoring review, issue intake, and low-sensitive continuity hints.

This phase is docs and fixtures only. It does not implement feedback ingestion, scoring script changes, issue creation, memory writes, facts writes, DB writes, Gateway integration, repair, or production rollout.

The core rule is:

```text
Feedback is an evaluation signal, not evidence.
Feedback can help triage quality issues and expand eval inventory.
Feedback must not become facts, memory evidence, permission proof, or automatic repair.
```

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`
- `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`
- `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md`
- `eval/phase2_inventory/phase2_eval_inventory_manifest.json`
- `docs/PHASE2102B_METRIC_SCORING_PACK.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`

Shared `DigitalDeliveryProject` sources:

- `integration-contracts/feedback_contract.md`
- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `docs/01_capability_matrix.md`
- `RISK_RED_LINES.md`

Shared docs status: available.

## 3. Contract Scope

Feedback may later connect to:

1. Phase 2 eval inventory candidates;
2. reviewed offline scoring pack inputs;
3. issue intake / triage candidates;
4. low-sensitive continuity hints after review.

Feedback must not:

1. write directly into long-term facts or memory;
2. be treated as document evidence;
3. create or repair DB / NAS / index data;
4. auto-create production issues without review;
5. expose raw path, raw row, raw answer text, secrets, tokens, credentials, or customer-sensitive notes;
6. bypass permission, evidence availability, or citation requirements.

## 4. Feedback Labels

| Label | Meaning | Linkage Class | Review Requirement |
|---|---|---|---|
| `helpful` | User judged the response useful | safe positive signal | Review required before any metric effect |
| `wrong_document` | Retrieved / answered from wrong source | scoring candidate signal | Review required |
| `missing_evidence` | User confirms evidence was missing or answer should have refused | scoring + issue intake candidate | Review required |
| `wrong_boundary` | Answer violated catalog-only / evidence / memory / permission boundary | forbidden-behavior candidate | Human review required |
| `citation_problem` | Citation missing, wrong, incomplete, or not source-aligned | scoring candidate signal | Review required |
| `permission_problem` | Permission denial or access behavior may be wrong | issue intake + fail-closed candidate | Human review required |
| `overclaim` | Answer claimed unsupported capability or uncited content | forbidden-behavior candidate | Human review required |
| `needs_human_review` | User requests review or uncertainty remains | issue intake candidate | Human review required |
| `irrelevant_result` | Result did not match intent | scoring candidate signal | Review required |

Classification:

1. Safe positive signal: `helpful`.
2. Scoring candidate signal: `wrong_document`, `missing_evidence`, `citation_problem`, `wrong_boundary`, `overclaim`, `permission_problem`, `irrelevant_result`.
3. Issue intake candidate: `missing_evidence`, `wrong_boundary`, `permission_problem`, `overclaim`, `needs_human_review`.
4. Must trigger human review before memory / eval change: all labels except discarded unsafe feedback; `helpful` still cannot auto-pass metrics.

## 5. Sanitized Feedback Input Shape

Planning-only input fields:

```json
{
  "feedback_id": "string",
  "query_id": "string",
  "trace_id": "string",
  "case_id": "string",
  "feedback_label": "string",
  "related_file_ids": ["string"],
  "related_model_ids": ["string"],
  "source_view": "string",
  "evidence_mode": "string",
  "permission_decision": "string",
  "missing_evidence_reason": "string",
  "sanitized_note_label": "string",
  "review_required": true
}
```

Forbidden input fields:

1. raw user note text;
2. raw answer text;
3. raw path / storage path / NAS path;
4. raw DB row;
5. raw catalog row;
6. secret / token / credential / `.env`;
7. customer-sensitive material;
8. full permission proof token;
9. file正文 / document text.

If unsafe fields are present, the safe outcome is `discard_unsafe_feedback` or `manual_review_required` with sanitized reason only.

## 6. Linkage Outcomes

| Outcome | Allowed Next Action | Forbidden Action | Safe Wording |
|---|---|---|---|
| `record_feedback_for_eval_review` | Store sanitized feedback candidate for human review in a future authorized system | Affect official metrics directly | Feedback recorded as review signal only. |
| `candidate_eval_case` | Propose a new or updated eval inventory case after review | Auto-add to committed inventory without review | This feedback may become an eval case after review. |
| `candidate_issue_intake` | Propose an issue intake record after review | Auto-create production issue or repair task | This feedback may require triage. |
| `scoring_input_after_review` | Prepare reviewed result row for offline scoring pack | Mark Top5 / citation / forbidden behavior without reviewed row | Metrics require reviewed sanitized result rows. |
| `low_sensitive_memory_hint_after_review` | Propose a low-sensitive preference or related-ID hint after review | Write raw note, fact, answer text, or permission proof to memory | Only low-sensitive continuity hints are eligible after review. |
| `discard_unsafe_feedback` | Reject unsafe raw text/path/secret feedback | Store unsafe payload | Unsafe feedback was discarded or needs sanitization. |
| `manual_review_required` | Route to human review with sanitized reason | Guess, auto-fix, or auto-confirm | Manual review is required before any downstream action. |

## 7. Scoring Linkage Rules

Feedback may later map to scoring pack review like this:

1. `wrong_document` can become a Top-K / source selection review candidate.
2. `citation_problem` can become a citation accuracy review candidate.
3. `missing_evidence` can become a Missing Evidence / unsupported-content review candidate.
4. `wrong_boundary` and `overclaim` can become forbidden-behavior review candidates.
5. `permission_problem` can become a permission-denial / fail-closed review candidate.
6. `helpful` is positive signal only and must not auto-mark a case as passed.
7. `irrelevant_result` can become query intent / result relevance review candidate.

Official scoring effect requires:

1. a reviewed sanitized result row;
2. matching `case_id`;
3. explicit `top5_hit`, `citation_ok`, or `forbidden_behaviors_observed` values;
4. no raw answer text, raw DB row, raw path, secret, or customer-sensitive payload;
5. metric eligibility defined in the committed eval inventory.

## 8. Memory Linkage Rules

Feedback may only propose low-sensitive memory hints after review, such as:

1. `preferred_result_grouping`;
2. `last_safe_project_context_label`;
3. `feedback_label`;
4. `related_file_ids`;
5. `related_model_ids`.

Feedback must not write:

1. facts;
2. file content;
3. answer content;
4. customer note text;
5. raw paths;
6. permission proof;
7. ACL snapshot;
8. raw catalog rows;
9. raw scoring notes.

Any later memory write must still obey Phase 2.104b memory continuity permission rules.

## 9. Fixture File

The Phase 2.104d fixture file is:

`eval/phase2_inventory/feedback_scoring_linkage_examples.json`

Fixture rules:

1. Use fake IDs only, such as `feedback_demo_301`, `query_demo_301`, `trace_demo_301`, `file_demo_301`, `model_demo_301`, `case_demo_301`.
2. Do not include real project names, real file names, raw paths, raw rows, raw answer text, secrets, tokens, or customer-sensitive content.
3. Every case must make these booleans explicit:
   - `should_affect_official_metric_without_review`
   - `should_write_long_term_memory`
   - `should_create_fact`
   - `should_create_repair`
   - `should_expose_raw_text_or_path`
4. The above booleans must remain false in this planning fixture contract.

## 10. Shared Follow-up

No shared folder files were edited in Phase 2.104d.

Recommended shared follow-up after Codex B review:

1. Mirror accepted feedback labels and sanitized input shape into shared `integration-contracts/feedback_contract.md`.
2. Keep scoring linkage as reviewed / sanitized only.
3. Keep issue intake as candidate-only until a later supervised issue workflow exists.

## 11. Phase 2.104d Conclusion

Phase 2.104d provides a docs-only Feedback / Scoring Linkage Contract and sanitized fixtures.

It is ready for Codex B review after validation, but it does not authorize runtime feedback ingestion, metric changes, memory writes, facts writes, issue creation, repair, DB/NAS/Gateway access, or production rollout.
