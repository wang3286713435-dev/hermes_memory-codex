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
| User-level closeout evidence | `missing_live_evidence` | Current committed metric inventory does not yet contain accepted natural-language import usability evidence for full Phase 2 closeout. |
| Employee / non-developer usability | `missing_live_evidence` | No committed accepted operator/employee usability report proves the full one-sentence import flow. |
| Direct API upload | `forbidden_substitute` | Direct API upload is useful ingestion evidence but cannot substitute for natural-language import usability. |

## 4. Required Closeout Interpretation

Current natural-language import is valuable but not enough to announce full Phase 2 closeout.

Historical real upload smoke proves an important technical path:

1. Hermes CLI natural-language import can detect import intent.
2. Runtime can call the real upload adapter path when explicitly enabled.
3. Upload can return `document_id`, `version_id`, `chunk_count`, and `indexed_count`.
4. Alias can persist in the same session.
5. Follow-up retrieval can cite the imported document.

However, full Phase 2 closeout still needs either:

1. a new accepted natural-language import smoke using the Hermes CLI natural-language import path, with committed sanitized evidence fields; or
2. an explicit user exception moving this gap out of Phase 2.

Planning docs, mocked integration, dry-run templates, operator checklists, and direct API upload are not sufficient substitutes.

## 5. Future Accepted Smoke Requirements

A future accepted smoke must use a command like:

```text
请把 <AUTHORIZED_FILE_PATH> 导入 Hermes，归到 <PROJECT_CONTEXT>，并绑定为 <ALIAS>
```

Minimum requirements:

1. User explicitly authorizes a single small non-sensitive file.
2. Hermes CLI natural-language import path is used.
3. Direct API upload is not used as substitute evidence.
4. Runtime returns `document_id`, `version_id`, `chunk_count`, `indexed_count`.
5. Alias persists in the same session.
6. Follow-up retrieval returns only the imported document.
7. Citation is present.
8. Missing Evidence is returned if parser, permission, or evidence is unavailable.
9. No third-document contamination appears.
10. No raw path, secret, raw row, raw answer, file content, or customer-sensitive material is exposed.

## 6. Closeout Decision

Current decision:

```text
natural_import_mvp_closeout = not_ready_until_evidence_or_user_exception
```

Meaning:

1. Stable platform baseline remains valid and separate.
2. Natural-language import has partial technical proof.
3. Full Phase 2 closeout remains blocked by natural-language import usability evidence unless the user explicitly grants an exception.
4. No production rollout, full NAS scan, DB write, parser/index write, or arbitrary file ingestion is authorized by this phase.

## 7. Candidate User Exception

If the user decides not to block full Phase 2 on natural-language import usability, the exception must explicitly say:

```text
Natural-language import usability is accepted as post-Phase-2 backlog.
Direct API upload and prior controlled smoke are sufficient only as technical ingestion evidence, not as user-facing natural-import evidence.
```

Without that explicit exception, this gap continues to block full closeout.

## 8. Next Step

Recommended next step:

1. Codex B reviews this pack and `eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`.
2. If accepted, user may authorize a docs / matrix baseline.
3. A future Codex C smoke may be authorized only with a specific small non-sensitive file path and explicit execution permission.

Do not run the smoke from this phase.
