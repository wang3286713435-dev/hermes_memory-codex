# Phase 2.101 PRD Acceptance Gap Closure Plan

## 1. Summary

Phase 2 remains open.

This plan converts the Phase 2.100a boundary audit into a decision table. It does not close Phase 2, does not implement runtime capabilities, and does not move any original PRD / Roadmap acceptance item to Phase 3 without explicit user approval.

Current position:

1. Hermes Memory is a strong internal controlled MVP candidate.
2. Phase 2 closeout readiness is still `no`.
3. Remaining gaps must now be classified as closeout blockers, evidence-pack requirements, explicit user-decision backlog items, or Phase 3+ candidates.

## 2. Decision Taxonomy

| decision | meaning |
|---|---|
| `phase2_closeout_blocker` | Must be completed or explicitly reclassified before Phase 2 can close. |
| `phase2_evidence_pack_required` | Capability appears implemented or partially implemented, but consolidated acceptance evidence is missing. |
| `phase2_backlog_candidate_user_decision` | Can be deferred only if the user explicitly accepts it as Phase 2 backlog / exception. |
| `phase3_plus_candidate_user_decision` | Fits Phase 3+ scope, but should still be explicitly acknowledged before deferral. |
| `already_satisfied_keep_evidence` | Existing evidence is enough for current controlled MVP; keep the artifact in the closeout evidence pack. |

## 3. Gap Decision Table

| gap_id | source_requirement | audit_status | proposed_decision | why | minimum_next_action | required_evidence_or_artifact | recommended_phase | user_decision_needed | risk_if_deferred |
|---|---|---|---|---|---|---|---|---|---|
| G01 | Roadmap Phase 2: core entities can be queried structurally; PRD structured facts entity/relationship layer | partial | `phase2_closeout_blocker` | Evidence-backed facts exist, but full entity/relationship querying for core business objects is not complete. | Define minimum Phase 2 entity set and query examples. | Entity query acceptance cases and pass/fail eval summary. | Phase 2.102 / 2.103 | yes, if reduced scope is accepted | Phase 2 may claim structured querying without actual relationship coverage. |
| G02 | Roadmap Phase 2: structured fact extraction | partial | `phase2_backlog_candidate_user_decision` | Current facts are evidence-backed, manual/API-created, governed, and confirmed; automatic broad extraction is intentionally not enabled. | Decide whether manual/evidence-backed facts satisfy Phase 2 or whether candidate extraction remains required. | User decision record plus facts eval / governance evidence. | Phase 2.101 decision, then Phase 2.102 evidence | yes | Auto-extraction expectations may be silently deferred without owner approval. |
| G03 | Roadmap Phase 2: tender requirements extracted into structured fields: price ceiling | partial | `phase2_closeout_blocker` | Price ceiling / highest bid limit still reaches Missing Evidence in hard main-tender cases. | Either implement targeted extraction/recall or explicitly backlog with manual review wording. | Codex C live proof or accepted backlog decision. | Phase 2.103 | yes, if deferred | Tender automation may overclaim financial field reliability. |
| G04 | Tender structured fields: qualification level/category | partial | `phase2_closeout_blocker` | Qualification level/category remains unstable or Missing Evidence in real tender queries. | Add focused acceptance cases and decide implementation vs manual review. | Retrieval/citation evidence for qualification level/category or backlog decision. | Phase 2.103 | yes, if deferred | Bid qualification answers may be incomplete or misleading. |
| G05 | Tender structured fields: project manager level | partial | `phase2_closeout_blocker` | Project manager level still requires cautious Missing Evidence handling. | Keep conservative answer boundary and decide whether to implement deep-field extraction. | Live query evidence or manual-review exception. | Phase 2.103 | yes, if deferred | System may imply unsupported staffing compliance conclusions. |
| G06 | Tender structured fields: performance requirements | partial | `phase2_closeout_blocker` | Similar-performance amount/scale/year limits are not reliably extracted. | Add field-specific examples and acceptance threshold. | Citation-backed performance requirement evidence or backlog decision. | Phase 2.103 | yes, if deferred | Tender review may miss material eligibility conditions. |
| G07 | Tender structured fields: personnel count/qualification | partial | `phase2_closeout_blocker` | Personnel-only guard improved answer boundaries, but personnel count/qualification still often remains Missing Evidence. | Decide if Missing Evidence + manual review is acceptable for Phase 2. | Codex C evidence pack and accepted limitation note. | Phase 2.103 | yes, if deferred | Personnel compliance may be overstated or under-evidenced. |
| G08 | Roadmap Phase 2: project/customer/qualification/case relationship querying | partial | `phase2_closeout_blocker` | Facts exist, but project/customer/qualification/case relationship model and relationship eval are incomplete. | Define relationship schema subset and 10-20 acceptance queries or request deferral. | Relationship query eval with source citations. | Phase 2.103 | yes, if reduced | Management queries may be claimed before relationship facts are reliable. |
| G09 | Roadmap Phase 2: version differences can be viewed | partial | `phase2_backlog_candidate_user_decision` | Active/latest and stale diagnostics exist; explicit version diff view is not implemented. | Decide whether stale/latest governance satisfies Phase 2 MVP or diff view remains required. | User decision plus version governance evidence. | Phase 2.101 / 2.102 | yes | Users may expect visual or structured diff that does not exist. |
| G10 | PRD / Technical Design: incremental update, delete, invalidation, old chunk lifecycle | partial | `phase2_backlog_candidate_user_decision` | Supersede/latest works; delete, archive, repair executor, and cleanup remain dry-run or forbidden. | Define Phase 2 lifecycle minimum: supersede-only vs delete/invalidate closure. | Version lifecycle evidence and explicit exception for repair/delete. | Phase 2.101 / 2.102 | yes | Old chunks or stale facts may persist longer than expected. |
| G11 | Roadmap / Technical Design: department/project/confidentiality permission strategy | partial | `phase2_closeout_blocker` | Soft access policy is implemented; full RBAC/ABAC department/project/confidentiality model is not. | Decide minimum permission acceptance boundary for Phase 2. | Permission matrix, denial tests, and explicit soft-policy limitation. | Phase 2.102 | yes, if full model deferred | Enterprise users may overtrust access isolation. |
| G12 | Roadmap Phase 2: user feedback enters evaluation loop | partial | `phase2_closeout_blocker` | Pilot issue intake exists, but product feedback is not yet wired into eval dataset/dashboard loop. | Define feedback intake -> triage -> eval case update workflow. | Feedback-loop runbook and sample issue-to-eval trace. | Phase 2.102 / 2.104 | yes, if deferred | Real pilot issues may not improve regression coverage. |
| G13 | PRD: 100+ questions; Roadmap: 300+ questions | partial | `phase2_evidence_pack_required` | Eval runner exists, but question inventory count evidence is not consolidated. | Build acceptance evidence pack with query inventory and grouping. | Eval set manifest showing PRD 100+ and Roadmap 300+ status. | Phase 2.102 | no, unless lower count accepted | Closeout metrics may be unsubstantiated. |
| G14 | PRD Top5 80%+, Roadmap Top5 85%+, PRD citation 85%+, Roadmap citation 90%+ | partial | `phase2_evidence_pack_required` | Current eval reports are pass/fail and smoke-oriented; aggregate metric pack is missing. | Compute or document measured Top5 and citation accuracy on accepted eval set. | Metric report with denominator, numerator, methodology, and failures. | Phase 2.102 | no, unless exception accepted | Quality claims become unverifiable. |
| G15 | Roadmap: structured fact key-field manual spot-check accuracy 90%+ | not_started | `phase2_evidence_pack_required` | Facts mechanics exist, but manual spot-check accuracy report is missing. | Sample confirmed/unverified facts and produce manual accuracy record. | Spot-check worksheet/report with 90%+ or documented gap. | Phase 2.102 | no, unless metric deferred | Facts layer may be treated as reliable without measured accuracy. |
| G16 | Roadmap / PRD: knowledge administrator backend / human validation workflow | partial | `phase2_backlog_candidate_user_decision` | Service/API confirmation and local report review exist; no full admin backend/UI or operational validation workflow. | Decide whether API/service workflow is enough for Phase 2. | Human validation workflow evidence or explicit admin-backend deferral. | Phase 2.101 / 2.102 | yes | Human validation may exist only as developer workflow, not user workflow. |
| G17 | PRD source/parser evidence: official account articles, PDF, HTML, Word/Excel/PowerPoint | partial | `phase2_evidence_pack_required` | Word/Excel/PPTX are evidenced; official account/PDF/HTML evidence is not clearly summarized. | Create parser/source evidence pack and mark unsupported categories explicitly. | Source-category matrix with samples, parser status, citations, and known gaps. | Phase 2.102 | no, unless categories deferred | MVP data-source claims may exceed tested formats. |
| G18 | PRD / PRD_ACCEPTANCE_MATRIX: Mac mini internal MVP deployment / employee trial evidence | partial | `phase2_evidence_pack_required` | Multiple runbooks/pilot docs exist, but consolidated internal employee trial proof is missing. | Consolidate Mac mini/internal trial status and Day-1 results. | Controlled trial summary with environment, users, pass/partial/fail, and issues. | Phase 2.104 | no | Stakeholders may confuse planning/runbooks with trial evidence. |
| G19 | Roadmap MVP: natural-language import / file ingestion usability | partial | `phase2_evidence_pack_required` | Upload/ingestion works, but natural-language import usability evidence is not packaged. | Define and test user-facing import scenarios or explicitly scope out. | Usability smoke notes and accepted user-facing limitations. | Phase 2.104 | yes, if deferred | Users may expect conversational import that was not validated. |
| G20 | Gateway catalog-only controlled smoke evidence | done | `already_satisfied_keep_evidence` | Gateway controlled smoke, runbook, and result review are documented as read-only catalog-only evidence. | Keep evidence in closeout pack; do not expand scope automatically. | Phase 2.92-2.97 Gateway docs and smoke review refs. | Phase 2.102 evidence pack | no | If wording drifts, Gateway Go may be mistaken for production rollout. |
| G21 | Data Steward / BIM catalog-only Phase 2 boundary | done | `already_satisfied_keep_evidence` | Phase 2 contains catalog-only planning/boundary evidence, not product implementation. | Keep explicit catalog-only evidence and red lines. | Data Steward risk boundary, shared contract, catalog-only docs. | Phase 2.102 evidence pack | no | Catalog metadata may be mistaken for BIM content understanding. |
| G22 | Data Steward productization / graph / spatial / DWG/RVT/BIM content understanding | reclassified_candidate | `phase3_plus_candidate_user_decision` | This is beyond current MVP and explicitly belongs to future Data Steward product line. | Record explicit user approval to keep in Phase 3+. | Phase 3+ deferral note in closeout decision record. | Phase 3+ | yes | Customers may expect productized BIM/Data Steward capabilities in Phase 2. |

## 4. Recommended Fastest Safe Route To MVP Landing

The fastest safe route is not to keep adding broad features. It is to turn current evidence into a closeout decision pack and get explicit user decisions on high-risk gaps.

Recommended route:

1. **Phase 2.102 Metric / Evidence Pack**
   Consolidate PRD 100+ / Roadmap 300+ eval inventory, Top5 metrics, citation accuracy, permission-denial evidence, parser/source coverage, Gateway catalog-only evidence, Data Steward catalog-only boundary, and controlled employee trial status.
2. **Phase 2.103 Tender Deep-field Closure / Backlog Decision**
   Decide and verify price ceiling, qualification level/category, project manager level, performance requirements, and personnel count/qualification. If not implemented, record explicit manual-review/backlog acceptance.
3. **Phase 2.104 Feedback / Admin / Human Validation Scope Decision**
   Define the minimum acceptable Phase 2 feedback loop, knowledge-admin workflow, and human-validation mechanism. Keep full UI/admin backend as backlog only if the user approves.
4. **Phase 2.105 Permission / Incremental Lifecycle Decision**
   Decide whether soft policy and supersede/latest lifecycle are acceptable for Phase 2, or whether stronger department/project/confidentiality and delete/invalidation behavior must close first.
5. **Phase 2.106 Final Phase 2 Closeout Review**
   Run only after blockers are closed or explicitly reclassified by the user.

## 5. Phase 2 Closeout Gate Checklist

Before any Phase 2 closeout claim:

1. Every `phase2_closeout_blocker` is either completed with evidence or explicitly reclassified by the user.
2. Every `phase2_evidence_pack_required` item has an evidence artifact with source refs, tested scope, and known limitations.
3. Every `phase2_backlog_candidate_user_decision` has an explicit user decision and risk note.
4. Every `phase3_plus_candidate_user_decision` has an explicit user decision and no Phase 2 overclaim wording.
5. Tender deep fields have either retrieval/citation evidence or accepted Missing Evidence/manual-review scope.
6. Eval count, Top5, citation accuracy, and structured fact manual spot-check metrics are documented with denominators.
7. Permission evidence states clearly whether it is soft policy or full RBAC/ABAC.
8. Gateway and Data Steward evidence remains catalog-only/read-only and does not imply production rollout or raw content understanding.
9. No repair executor, parser expansion, DB/NAS write, reindex, migration, or rollout is introduced as part of closeout.
10. Codex B review signs off before any baseline; Codex C validation is requested only for runtime evidence phases.

## 6. Items That Must Not Move To Phase 3 Without Explicit User Approval

1. Structured entity and relationship querying.
2. Tender deep fields: price ceiling, qualification level/category, project manager level, performance requirements, personnel count/qualification.
3. Project/customer/qualification/case relationship querying.
4. Department/project/confidentiality permission strategy.
5. User feedback entering the evaluation loop.
6. PRD/Roadmap eval count, Top5, citation accuracy, and structured fact manual spot-check metrics.
7. Knowledge administrator backend / human validation workflow.
8. Version difference view.
9. Incremental delete / invalidation / old chunk lifecycle.
10. Official account / PDF / HTML parser/source evidence if PRD §13 source/parser coverage remains unchanged.

## 7. Items Safe To Defer To Phase 3+ If User Approves

1. Data Steward productization.
2. Graph / spatial index / Neo4j / PostGIS product implementation.
3. DWG / RVT / BIM raw content understanding and TB-scale model parsing.
4. Complete knowledge graph beyond the Phase 2 structured fact layer.
5. Full production rollout.
6. Repair executor or destructive cleanup tools.
7. Automatic broad facts extraction if Phase 2 accepts manual/evidence-backed facts.
8. Full admin UI if Phase 2 accepts service/API-level human validation as temporary scope.

## 8. Current Conclusion

Phase 2 closeout readiness: no.

Phase 2.101 produces a decision map. It does not close any gap by itself. The next required action is Codex B review, followed by a user decision on which gaps must be closed in Phase 2 and which may be explicitly deferred.
