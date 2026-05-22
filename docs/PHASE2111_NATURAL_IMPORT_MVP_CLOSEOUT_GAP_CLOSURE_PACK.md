# Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack

## 1. Purpose

Phase 2.111 converts the natural-language import gap into a closeout evidence matrix.

It answers:

```text
Which natural-language import capabilities are proven?
Which are partial / planning / mocked evidence?
Which require a future user-authorized real smoke?
Which can leave Phase 2 only by explicit user exception?
```

This phase is docs / matrix / handoff only. It does not run a real import smoke, upload files, connect to runtime services, write business data, modify parsers, or enter rollout.

## 2. Sources Reviewed

- `docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md`
- `eval/phase2_inventory/phase2_full_closeout_return_checklist.json`
- `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`
- `eval/phase2_inventory/phase2_eval_inventory_manifest.json`
- `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
- `docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md`
- `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`
- `docs/PHASE256_NATURAL_IMPORT_REAL_ADAPTER_PLAN.md`
- `docs/PHASE256B_NATURAL_IMPORT_REAL_SMOKE_PLAN.md`
- `docs/PHASE256D_NATURAL_IMPORT_RUNTIME_WIRING_PLAN.md`
- `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`
- `docs/PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md`
- `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
- `scripts/phase257a_natural_import_evidence_template.py`
- `tests/test_phase257a_natural_import_evidence_template.py`
- `docs/PRD.md`
- `docs/ROADMAP.md`

## 3. Current Evidence Summary

| Area | Current Status | Closeout Meaning |
|---|---|---|
| Intent detection | `proven` | Explicit import utterances can be detected and fail-closed for unsafe patterns. |
| Runtime pre-retrieval hook | `proven` | Natural import can intercept before ordinary retrieval / answer flow. |
| Real upload client path | `proven` | Existing controlled smoke proved natural import can call the Hermes_memory upload path. |
| Same-session alias and retrieval | `proven` | Existing smoke returned document/version/chunk/index metadata, bound alias, and retrieved same-session evidence. |
| Operator checklist and evidence template | `proven` | Dry-run template and checklist exist for controlled future smoke authorization. |
| User-level closeout evidence | `passed_with_scope` | Phase 2.112i accepted the authorized small `.xlsx` test-machine flow: real upload flag visible, alias resolved, same-session retrieval evidence non-empty, citation present, no third-document contamination. |
| Employee / non-developer usability | `out_of_scope_for_current_acceptance` | Broader employee / non-developer usability matrix remains future work and is not claimed by the scoped acceptance. |
| Direct API upload | `forbidden_substitute` | Direct API upload is useful ingestion evidence but cannot substitute for natural-language import usability. |

## 4. Required Closeout Interpretation

Current natural-language import is valuable but not enough to announce full Phase 2 closeout.

Historical real upload smoke proves an important technical path:

1. Hermes / OpenWebUI-compatible natural-language import path can detect import intent.
2. Runtime can call the real upload adapter path when explicitly enabled.
3. Upload can return `document_id`, `version_id`, `chunk_count`, and `indexed_count`.
4. Alias can persist in the same session.
5. Follow-up retrieval can cite the imported document.

Phase 2.112i has now supplied the missing scoped smoke evidence:

1. authorized small `.xlsx` sample;
2. natural-language import through the 8642 / OpenWebUI-compatible backend;
3. explicit alias `@建筑类数据样表`;
4. same-session follow-up retrieval;
5. non-empty retrieval evidence IDs;
6. citation present;
7. no third-document contamination.

This closes the natural import closeout blocker only for the accepted scope. Planning docs, mocked integration, dry-run templates, operator checklists, and direct API upload remain insufficient substitutes for any future broader acceptance claim.

## 5. Scope-limited Acceptance Boundaries

The accepted evidence is intentionally narrow:

1. Authorized small `.xlsx` only.
2. No production rollout.
3. No NAS full scan.
4. No DWG/RVT/BIM content understanding.
5. No large-file parser/indexing claim.
6. No automatic long-term memory writes for file content.
7. No repair/reindex/cleanup automation.
8. No unrestricted file ingestion.

## 6. Closeout Decision

Current decision:

```text
natural_import_mvp_closeout = passed_with_scope
```

Meaning:

1. Stable platform baseline remains valid and separate.
2. Natural-language import now has accepted scoped live evidence for the authorized small `.xlsx` path.
3. Full Phase 2 completion still cannot be announced while other PRD-critical P0/P1 blockers remain unverified.
4. No production rollout, full NAS scan, DB write, parser/index write outside the accepted import path, or arbitrary file ingestion is authorized by this phase.

## 7. Remaining User Exception Area

If the user later wants broader import claims without executing a broader sample matrix, that exception must explicitly say:

```text
Natural-language import is accepted beyond the authorized small .xlsx scope by business exception.
Unverified file types, large files, NAS scans, production rollout, and automatic memory writes remain excluded unless separately authorized.
```

Without that explicit exception, the current claim remains `passed_with_scope`.

## 8. Next Step

Recommended next step:

1. Codex B reviews this updated pack and `eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`.
2. If accepted, user may authorize a docs / matrix baseline.
3. Future sample expansion requires a separate phase and explicit file authorization.

Do not run more smoke from this phase.
