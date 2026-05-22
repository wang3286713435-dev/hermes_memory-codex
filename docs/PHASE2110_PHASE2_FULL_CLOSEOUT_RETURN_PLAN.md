# Phase 2.110 Phase 2 Full Closeout Return Plan

## 1. Purpose

Phase 2.110 answers the user's direct review question:

```text
What is the real natural-language usage flow today, and did the current Phase 2 closeout meet the previously agreed delivery requirements?
```

Decision:

```text
Stable platform integration baseline: keep.
Standalone Hermes kernel preservation baseline: keep.
Full Phase 2 PRD / Roadmap closeout: return / reopen.
```

This phase does not revoke the Phase 2.109 stable freeze checklist. It prevents the project from announcing full Phase 2 completion before the original PRD acceptance requirements have evidence.

This phase is docs / review only. It does not modify runtime code, parsers, indexes, platform code, DB, NAS, Gateway, Hermes memory, documents/chunks, facts, Qdrant, OpenSearch, MinIO, or rollout behavior.

## 2. Current Real Natural-language Usage Flow

The current usable flow is a controlled operator / API / CLI flow, not yet a fully smooth conversational "say one sentence and Hermes imports everything" product flow.

### 2.1 Standalone Hermes File / Tender Governance Flow

Current practical flow:

1. **Operator selects intent and file scope.** The user or operator identifies a file, folder, sample, or existing document alias and states the target task.
2. **Hermes classifies the request boundary.** The system separates catalog lookup, governed file import, retrieval question, Missing Evidence, and unsafe / unsupported actions.
3. **Controlled upload or import path is used.** Real file ingestion still goes through explicit API / CLI / checklist paths, not unbounded free-form NAS scanning or implicit file system takeover.
4. **Parser and indexing run only when authorized.** Supported files can enter parsing, chunking, metadata extraction, embedding / vector search, BM25 / hybrid retrieval, and citation-bearing answer paths when the configured runtime path allows it.
5. **Answers require evidence.** Hermes should answer from retrieval evidence with citations; if evidence is missing, stale, unauthorized, catalog-only, or unsupported, it must say Missing Evidence rather than inventing content.
6. **Feedback and issues are recorded separately.** User feedback and issue intake can become review signals, not automatic facts, not automatic repair, and not production changes.

### 2.2 Platform / Data Steward Flow

Current platform integration flow is narrower:

1. Platform authenticates user and project scope.
2. Platform Gateway generates permission proof and redacts unsafe path fields.
3. Hermes receives a catalog-only / read-only question surface.
4. Hermes can answer asset-directory questions with safe IDs and trace fields.
5. Hermes must return Missing Evidence for DWG/RVT/BIM/PDF/Office content questions unless future governed evidence search is enabled.

This means platform use is currently safe and useful for asset catalog assistance, but it is not the full standalone Hermes memory / evidence / file-governance experience.

## 3. What Is Actually Ready

### 3.1 Ready Enough to Keep

The following Phase 2 baselines remain valid:

1. Platform catalog-only Gateway integration with permission, redaction, Missing Evidence, and safe IDs.
2. Standalone Hermes kernel preservation contract: Hermes remains an enterprise Agent kernel, not a platform plugin.
3. Natural-language import for the authorized small `.xlsx` test-machine path: real upload flag visible, explicit alias resolved, same-session follow-up retrieval returned evidence IDs and citation, and no third-document contamination appeared.
4. Tender / meeting / Excel / PPTX controlled MVP workflows with citation and Missing Evidence boundaries.
5. DB / NAS / Data Steward catalog-only contract and controlled structure / redacted smoke evidence.
6. NAS scratch copy and parser dry-run planning / controlled smoke boundaries for small samples.

### 3.2 Not Ready Enough for Full Phase 2 Closeout

The following remain blockers or require explicit user backlog exception before declaring full Phase 2 complete:

1. Hermes Memory self-awareness / kernel activation is incomplete: user-facing Hermes must reliably present and use its own memory / workspace / retrieval / evidence kernel.
2. PRD target of at least 100 high-quality evaluation questions is not met by the committed accepted inventory.
3. Roadmap target of 300+ questions is not met.
4. Top5 hit-rate target is not measured at required accepted-inventory scale.
5. Citation accuracy target is not measured at required accepted-inventory scale.
6. Structured fact manual spot-check target is missing.
7. Natural-language import beyond the accepted authorized small `.xlsx` scope is not productized as unrestricted production import.
8. Full source coverage for official-account / PDF / HTML / full Office parsing is not consolidated into accepted metric evidence.
9. Tender deep-field reliability remains partial or requires explicit Missing Evidence / manual-review acceptance.
10. Version diff and full incremental delete / invalidation lifecycle remain partial.
11. Department / project / confidentiality policy remains basic / contract-level, not full RBAC / ABAC.
12. Knowledge-admin backend and human validation workflow remain partial / service-level.
13. Platform native session, memory continuity runtime, and governed document evidence search remain contract / future unlock paths, not current runtime claims.

## 4. Return Decision

Phase 2.110 return decision:

```text
phase2_stable_platform_baseline = keep
phase2_standalone_kernel_preservation = keep
phase2_full_closeout = returned
phase3_planning = allowed only if inherited gaps are explicit
phase2_completion_announcement = blocked
```

The project must not say:

```text
Phase 2 is fully complete.
```

The project may say:

```text
Phase 2 has a stable platform integration baseline and a preserved standalone Hermes kernel baseline, but full PRD / Roadmap closeout is returned until acceptance gaps are closed or explicitly reclassified.
```

## 5. Minimum Work Before Announcing Full Phase 2 Completion

At minimum, one of the following must happen before full Phase 2 can be announced complete.

### Option A: Close the Gaps with Evidence

1. Expand accepted eval inventory toward PRD / Roadmap targets.
2. Run and record Top5 / citation metrics against accepted results.
3. Add structured fact manual spot-check evidence.
4. Preserve the accepted Phase 2.112i natural-language import evidence as `passed_with_scope`, and only expand it through separately authorized sample matrices.
5. Consolidate parser/source coverage evidence.
6. Decide and verify tender deep-field behavior.
7. Record permission/version/admin/human-validation acceptance evidence.

### Option B: User Explicitly Reclassifies Gaps

The user may explicitly decide that some original Phase 2 requirements move to backlog / Phase 3+. If so, the project must record the exception and must not present those deferred requirements as completed.

## 6. Natural-language Import Acceptance Result

Phase 2.112i accepted the following scoped real flow:

```text
User: import an authorized small .xlsx sample through natural language, bind @建筑类数据样表, then ask a same-session follow-up retrieval question.
```

Accepted evidence:

1. Hermes_memory `/health` passed and the 8642 backend was available.
2. `real_upload_flag_visible=true`.
3. `alias_resolution.status=alias_resolved`, `alias_missing=false`, and `retrieval_suppressed=false`.
4. `retrieval_evidence_document_ids_non_empty=true`.
5. `citation_present=true`.
6. `third_document_contamination=false`.

Closeout interpretation:

```text
natural_language_import_usability = passed_with_scope
scope = authorized_small_xlsx_test_machine_path
```

This does not authorize production rollout, NAS full scan, DWG/RVT/BIM content understanding, large-file parser/indexing claims, automatic long-term memory writes for file content, repair/reindex/cleanup automation, or unrestricted natural-language ingestion.

## 7. Next Recommended Phase

Recommended next phase:

```text
Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack
```

Scope:

1. Build a compact closeout matrix for natural-language import usability, parser/source coverage, and accepted eval metrics.
2. Decide which gaps are mandatory before Phase 2 completion and which require explicit user backlog exception.
3. Create a test-machine / Mac mini prompt for a real natural-language import acceptance smoke only if user authorizes it.
4. Keep platform catalog-only stable baseline separate and usable.

Hard boundary:

Do not use this return plan to expand into production rollout, full NAS scan, Agent DB CRUD, arbitrary SQL, raw NAS path exposure, repair executor, or DWG/RVT/BIM content understanding.
