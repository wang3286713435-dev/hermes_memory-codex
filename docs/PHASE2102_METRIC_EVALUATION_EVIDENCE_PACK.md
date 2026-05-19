# Phase 2.102 Metric / Evaluation Evidence Pack

## 1. Summary

Phase 2 metric closeout decision: `not_ready`.

This evidence pack maps PRD / Roadmap acceptance metrics to committed evidence. It does not run new smoke, does not read ignored local reports, and does not convert targeted pass/fail smoke into percentage metrics.

Current evidence is enough to show that Hermes Memory has a repeatable internal evaluation pipeline and multiple controlled MVP capabilities. It is not enough to claim the PRD / Roadmap numeric closeout targets for eval count, Top5 hit rate, citation accuracy, or structured fact manual spot-check accuracy.

## 2. Evidence Taxonomy

| status | meaning |
|---|---|
| `measured_pass` | A committed artifact contains the target, denominator, numerator, and pass result. |
| `measured_fail` | A committed artifact contains the target, denominator, numerator, and fail result. |
| `partial_evidence` | Related tests, evals, smoke, or docs exist, but they do not satisfy the full acceptance metric. |
| `smoke_only_not_metric` | Live smoke or runner pass/fail exists, but it is not a statistical metric. |
| `missing_metric` | The target exists in PRD / Roadmap, but no committed numerator/denominator metric is available. |
| `requires_user_decision` | The evidence boundary is intentionally smaller than the original requirement and needs explicit user acceptance. |

## 3. Metric Evidence Table

| metric_id | source_requirement | target | current_evidence_status | evidence_refs | measured_value_or_known_result | missing_denominator_or_gap | closeout_impact | next_action | codex_c_needed |
|---|---|---|---|---|---|---|---|---|---|
| M01 | `PRD.md` §13.12 | At least 100 high-quality evaluation questions | `missing_metric` | Phase 2.14 / 2.20a eval runner; `scripts/phase214_regression_eval.py`; `docs/PHASE214_REGRESSION_EVAL_PLAN.md` | Committed runner contains core/governance/facts case groups; documented full eval examples reached 21 passed / 0 failed / 1 skipped. | No committed 100+ question inventory with stable IDs, grouping, expected docs, and owner review. | Blocks metric closeout. | Create eval inventory manifest and count accepted high-quality questions. | no, unless validating new inventory live. |
| M02 | `ROADMAP.md` Phase 2 acceptance | Evaluation set expands to 300+ | `missing_metric` | Same as M01; Phase 2.100a audit. | No committed 300+ count. | No 300+ accepted question inventory or coverage matrix. | Blocks Roadmap Phase 2 closeout. | Decide whether 300+ remains Phase 2 blocker or user-approved backlog. | no |
| M03 | `PRD.md` §13.13 | Core Top5 hit rate 80%+ | `missing_metric` | Phase 2.14 / 2.17 / 2.20a eval docs. | Pass/fail eval exists; no Top5 numerator/denominator. | Runner does not document Top5 hit-rate computation over 100+ query set. | Blocks PRD metric closeout. | Add Top5 measurement report on accepted eval set. | yes, if using live retrieval evidence. |
| M04 | `ROADMAP.md` Phase 2 acceptance | Core Top5 hit rate 85%+ | `missing_metric` | Phase 2.100a audit; Phase 2.14 / 2.20a eval docs. | No committed Top5 85% result. | No 300+ denominator and no Top5 hit-rate report. | Blocks Roadmap Phase 2 closeout. | Same as M03, with Roadmap threshold. | yes, if measured live. |
| M05 | `PRD.md` §13.14 | Citation accuracy 85%+ | `missing_metric` | Structured citation phases; `docs/PRD_ACCEPTANCE_MATRIX.md`; Phase 2.12 / 2.13 / 2.14 docs. | Targeted citation behavior exists for Excel/PPTX/meeting/tender cases. | No aggregate citation accuracy numerator/denominator. | Blocks PRD citation metric closeout. | Produce citation accuracy review set and manual/automated scoring method. | yes, for terminal citation review. |
| M06 | `ROADMAP.md` Phase 2 acceptance | Citation accuracy 90%+ | `missing_metric` | Same as M05. | No committed 90% aggregate result. | No Roadmap-scale citation scoring report. | Blocks Roadmap Phase 2 closeout. | Same as M05, with 90% threshold. | yes |
| M07 | `ROADMAP.md` Phase 2 acceptance | Structured fact key-field manual spot-check accuracy 90%+ | `missing_metric` | Phase 2.21a/b facts governance docs and tests. | Facts creation/governance/eval exist, but no manual accuracy score. | No sampled fact set, reviewer sheet, numerator, denominator, or failure taxonomy. | Blocks structured facts closeout. | Run manual spot-check on accepted facts sample; document 90%+ or gap. | yes, if Codex C performs independent review. |
| M08 | `PRD.md` §13.15 | Permission tests show no unauthorized recall | `partial_evidence` | `docs/PHASE218_ACCESS_AUDIT_PLAN.md`; `docs/PHASE220_GOVERNANCE_EVAL_PLAN.md`; `tests/test_phase218_access_audit.py`; `scripts/phase214_regression_eval.py` governance group. | Soft-policy no ACL / allow / tenant deny cases documented; governance group 5 passed / 0 failed / 0 skipped in Phase 2.20a. | Scope is soft policy fixture, not full department/project/confidentiality RBAC/ABAC. | Supports MVP permission evidence but not full Roadmap permission closeout. | Keep as MVP evidence; decide full RBAC/ABAC deferral separately. | no for fixture; yes for enterprise terminal policy smoke. |
| M09 | `PRD.md` §13.1 | Internal documents, tender documents, official account articles connected | `partial_evidence` | `docs/PRD_ACCEPTANCE_MATRIX.md`; structured ingestion / tender phases. | Internal/tender/structured sample ingestion is evidenced. | Official account article ingestion evidence is not clearly packaged. | Blocks PRD source-category closeout unless user accepts deferral. | Add source-category evidence matrix or explicitly defer official account evidence. | maybe |
| M10 | `PRD.md` §13.2 | PDF, Word, Excel, PowerPoint, HTML basic parsing | `partial_evidence` | Phase 2.12 Excel/PPTX; Phase 2.13 meeting DOCX; Phase 2.98/2.99 standard boundary tests for PDF/Office Missing Evidence. | Word/Excel/PPTX evidence exists; PDF/HTML parser evidence not consolidated. | No committed PDF/HTML parsing proof pack. | Blocks full parser-format claim. | Create parser/source evidence pack or mark unsupported formats as Missing Evidence scope. | maybe |
| M11 | Gateway catalog-only controlled smoke evidence | Read-only catalog-only Gateway behavior evidenced | `smoke_only_not_metric` | Phase 2.92-2.97 Gateway docs, controlled smoke result review, frontend read-only trial runbook. | Gateway controlled smoke accepted as read-only/catalog-only evidence. | Not a production rollout metric and not raw DB/NAS content evidence. | Keep in closeout pack; does not close runtime content integration. | Preserve safe-field / forbidden-field evidence refs. | no |
| M12 | Data Steward / DB / NAS catalog-only boundary evidence | Catalog-only boundary evidenced | `partial_evidence` | Data Steward risk boundary, Phase 2.39 plan, shared contract alignment, Phase 2.72-2.79 sanitized/catalog-only docs. | Catalog-only planning and red-line evidence exists. | Productized asset catalog, graph/spatial, and content understanding are not implemented. | Supports Phase 2 boundary evidence only. | Keep as catalog-only evidence; require user approval for Phase 3+ deferral. | no |
| M13 | Mac mini internal MVP deployment / employee trial evidence | Internal controlled trial evidence consolidated | `partial_evidence` | Phase 2.31 pilot ops nightly launcher; Phase 2.33 Day-1 run sheet; PRD acceptance matrix. | Runbooks and Day-1 materials exist. | No consolidated employee trial metric report with users, query set, pass/partial/fail, and issues. | Blocks internal MVP evidence-pack closeout. | Create controlled trial summary from committed docs and approved Codex C reports. | yes |
| M14 | Natural-language import usability evidence | User can import files naturally | `partial_evidence` | Phase 2.53 natural file import planning/integration notes in `DEV_LOG.md`; PRD acceptance matrix. | Mocked natural import integration and intent tests are documented. | No live user-facing natural import usability evidence; real upload remains separately controlled. | Blocks natural import usability claim. | Produce usability smoke or explicitly scope natural import as backlog. | yes |
| M15 | Missing Evidence behavior for unsupported content evidence | Unsupported / unavailable evidence returns Missing Evidence | `smoke_only_not_metric` | Phase 2.98 / 2.99 standard boundary docs/tests; PRD acceptance matrix; tender deep-field live notes. | Missing Evidence boundary is tested for standard/Office/PDF content questions and used for hard tender fields. | Not an aggregate metric; hard tender fields still partial. | Supports safety boundary, not field-completion closeout. | Keep as evidence and pair with tender deep-field decision. | no |
| M16 | Facts boundary | Facts do not replace retrieval evidence | `smoke_only_not_metric` | Phase 2.21-2.24 docs; `docs/PHASE224_FACTS_AGENT_CONTEXT_PLAN.md`; PRD acceptance matrix. | `facts_as_answer=false` validated in facts auxiliary context; stale fact warning exists. | Not a structured fact extraction accuracy metric. | Supports evidence policy, not automatic facts closeout. | Keep in closeout pack; do not claim auto extraction. | no |
| M17 | Meeting transcript boundary | Transcript is retrieval evidence, not confirmed fact | `smoke_only_not_metric` | `docs/PHASE213_MEETING_TRANSCRIPT_INGESTION_PLAN.md`; Phase 2.14 meeting eval cases. | `transcript_as_fact=false` documented; action/decision/risk cases exist. | Raw audio ASR remains deferred; no aggregate transcript accuracy metric. | Supports meeting transcript MVP boundary. | Keep as evidence; ASR remains future. | no |
| M18 | Version governance evidence | Latest/default filtering and stale diagnostics | `partial_evidence` | `docs/PHASE219_VERSION_GOVERNANCE_PLAN.md`; Phase 2.20 governance eval; PRD acceptance matrix. | Default latest, explicit old version, stale trace, audit evidence_version_ids documented. | Version diff view and delete/invalidation lifecycle remain separate gaps. | Supports version-governance MVP; not full version-diff closeout. | Keep governance evidence and decide version diff / lifecycle backlog. | no |

## 4. Source / Parser Evidence Table

| source_or_format | current_evidence_status | evidence_refs | known_gap | closeout_action |
|---|---|---|---|---|
| Internal documents | `partial_evidence` | Word/DOCX ingestion and meeting transcript phases; internal MVP pilot docs. | Needs consolidated inventory of internal docs used in eval/pilot. | Add to source-category evidence matrix. |
| Tender documents | `partial_evidence` | Tender metadata, 6-file regression pool, Phase 2.38d tender personnel guard, PRD acceptance matrix. | Deep-field extraction remains partial. | Pair source evidence with tender deep-field decision. |
| Official account articles | `missing_metric` | PRD/Roadmap requirement only found in current evidence pack. | No committed parser/source proof summary. | Add sample evidence or user-approved deferral. |
| PDF | `partial_evidence` | Standard boundary Missing Evidence tests / docs. | Parsing proof is not consolidated as basic parser evidence. | Add PDF parser smoke/evidence pack or mark as unsupported scope. |
| Word / DOCX | `partial_evidence` | Meeting transcript DOCX and document ingestion references. | General Word parsing evidence should be linked to sample matrix. | Add sample doc ID / parser evidence ref. |
| Excel | `partial_evidence` | Phase 2.12 structured ingestion, sheet/cell citation, live terminal 5/5. | Chart/OCR/deep spreadsheet semantics deferred. | Keep as MVP parser evidence. |
| PowerPoint | `partial_evidence` | Phase 2.12 slide citation, live terminal 5/5. | Image/chart OCR deferred. | Keep as MVP parser evidence. |
| HTML | `missing_metric` | PRD/Roadmap requirement only found in current evidence pack. | No committed HTML parser proof summary. | Add HTML parser smoke/evidence pack or user-approved deferral. |

## 5. Permission / Denial Evidence Table

| evidence_area | current_evidence_status | evidence_refs | known_result | gap | next_action |
|---|---|---|---|---|---|
| No ACL local default | `partial_evidence` | Phase 2.18a; Phase 2.20a governance eval. | `not_configured_allow` behavior documented. | Not full enterprise permission model. | Keep as local-dev boundary evidence. |
| Requester allow | `partial_evidence` | Phase 2.18a live smoke; governance eval fixture. | `policy_decision=allow` and audit requester recorded. | Fixture scope only. | Keep and add enterprise policy smoke if needed. |
| Tenant mismatch deny | `partial_evidence` | Phase 2.18a live smoke; `gov_access_tenant_mismatch_deny`. | Denied document not returned; denied IDs audited. | Does not prove department/project/confidentiality RBAC/ABAC. | User decision on full permission scope. |
| Evidence version audit | `partial_evidence` | Phase 2.19a / 2.20a. | `evidence_version_ids` recorded for latest and explicit old version cases. | Production audit coverage is not complete. | Include in governance evidence pack. |
| Full department/project/confidentiality policy | `missing_metric` | Roadmap / Technical Design requirement. | No full RBAC/ABAC matrix evidence. | Blocks Roadmap permission closeout unless deferred. | Phase 2.105 decision or implementation plan. |

## 6. Gateway / Data Steward Catalog-only Evidence Table

| area | current_evidence_status | evidence_refs | accepted_boundary | not_claimable |
|---|---|---|---|---|
| Gateway controlled smoke | `smoke_only_not_metric` | Phase 2.92-2.97 docs and smoke result review. | Read-only, catalog-only, safe fields, forbidden-field scan, no side effects. | Production rollout, raw DB/NAS content integration, Agent SQL/CRUD. |
| Frontend Gateway trial runbook | `partial_evidence` | Phase 2.97 runbook. | Operator checklist for limited internal trial. | Completed production trial or production Gateway rollout. |
| Data Steward catalog-only boundary | `partial_evidence` | Data Steward risk boundary; Phase 2.39 plan; shared contract alignment. | Catalog metadata, redacted identifiers, no raw content evidence. | Productized Data Steward, BIM content understanding, graph/spatial implementation. |
| DB / NAS sanitized catalog evidence | `partial_evidence` | Phase 2.72-2.79 docs in `DEV_LOG.md`; PRD acceptance matrix. | Sanitized stats, catalog-only, scratch/parser previews under explicit phases. | Real NAS semantic search, raw NAS path/content exposure, DB writer authorization. |

## 7. Mac mini / Employee Trial / Natural Import Evidence Table

| area | current_evidence_status | evidence_refs | known_result | gap | next_action |
|---|---|---|---|---|---|
| Mac mini runtime readiness | `partial_evidence` | Phase 2.60-2.67 references in `DEV_LOG.md`; PRD acceptance matrix. | Health / CLI / minimal smoke reported in earlier phase notes. | No single closeout-ready report tying environment, refs, smoke, and trial outcome together. | Create controlled trial evidence pack. |
| Employee Day-1 / pilot trial | `partial_evidence` | Phase 2.31 pilot ops; Phase 2.33 Day-1 run sheet; Phase 2.37 issue intake/triage. | Runbooks and issue intake exist. | No consolidated employee pass/partial/fail metric pack. | Codex B/C review of pilot evidence and issue trends. |
| Natural-language import usability | `partial_evidence` | Phase 2.53 natural import planning/integration notes. | Mocked intent/flow exists. | No live usability result for natural-language import into production-like flow. | Run controlled usability smoke or explicitly defer. |
| Missing Evidence user behavior | `partial_evidence` | Standard boundary phases and tender deep-field notes. | System can avoid unsupported answers. | Need user acceptance that Missing Evidence + manual review is acceptable for hard fields. | Include in Phase 2.103 / 2.104 decision. |

## 8. Phase 2 Metric Closeout Decision

Decision: `not_ready`.

Reasons:

1. PRD 100+ and Roadmap 300+ eval inventories are not committed as accepted question manifests.
2. Top5 80% / 85% metrics are missing numerator and denominator.
3. Citation accuracy 85% / 90% metrics are missing numerator and denominator.
4. Structured fact manual spot-check accuracy 90% is missing.
5. Parser/source coverage for official account articles, PDF, and HTML is not consolidated.
6. Permission evidence is sufficient for current soft-policy MVP scope but not the full Roadmap department/project/confidentiality model.
7. Mac mini / employee trial / natural import evidence needs consolidation.

## 9. Follow-up Phases Needed

1. **Phase 2.102a Eval Inventory Manifest**
   Create a committed list of accepted evaluation questions with IDs, groups, expected documents, expected citations, and source requirements.
2. **Phase 2.102b Metric Scoring Pack**
   Compute Top5 and citation accuracy only after the accepted inventory exists.
3. **Phase 2.102c Parser / Source Category Evidence Pack**
   Consolidate internal/tender/official account and PDF/Word/Excel/PowerPoint/HTML evidence.
4. **Phase 2.102d Structured Fact Manual Spot-check**
   Produce the 90% manual accuracy report or document the gap.
5. **Phase 2.103 Tender Deep-field Closure / Backlog Decision**
   Handle price ceiling, qualification level/category, project manager level, performance, and personnel count/qualification.
6. **Phase 2.104 Controlled Employee Trial / Natural Import Review**
   Consolidate Mac mini, employee trial, natural import, and feedback loop evidence.
7. **Phase 2.105 Permission Scope Decision**
   Decide whether soft-policy evidence is accepted for Phase 2 or full RBAC/ABAC remains a closeout blocker.

## 10. Current Conclusion

Phase 2 closeout metrics are not ready.

The strongest current evidence is repeatable deterministic eval infrastructure, targeted live smoke, governance/facts/version tests, structured citation cases, and safe catalog-only boundaries. The missing piece is the formal acceptance metric layer: inventory counts, denominators, numerator calculations, and manual spot-check artifacts.
