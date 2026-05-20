# Phase 2.108 Standalone Kernel Freeze Contract

## 1. Purpose

Phase 2.108 closes a product-positioning gap that appeared during platform integration:

```text
Platform can expose Hermes conservatively.
Platform must not shrink Hermes into a conservative plugin.
```

The stable platform baseline is intentionally `catalog-only`, read-only, permission-first, and Missing-Evidence-first. That is a safety boundary for platform embedding, not a definition of Hermes's full product identity.

This phase freezes the standalone Hermes kernel contract before Phase 2 can be considered safe to pause for platform integration. It ensures that, even if a test machine stays on a Phase 2 stable tag, later platform work can still unlock Hermes evidence search, low-sensitive memory continuity, workspace state, NAS governance, and orchestration without reinterpreting Hermes as a path-query chatbot.

This is a docs / contract phase only. It does not modify runtime code, DB, NAS, parser, indexes, memory stores, Gateway, platform repo, or production rollout behavior.

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PRD.md`
- `docs/ROADMAP.md`
- `docs/TECHNICAL_DESIGN.md`
- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`
- `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md`
- `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`
- `docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md`
- `docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md`
- `docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md`
- `eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`

Shared `DigitalDeliveryProject` sources:

- `integration-contracts/hermes_kernel_authority_contract.md`
- `integration-contracts/platform_to_hermes_contract.md`
- `integration-contracts/hermes_native_gateway_contract.md`
- `integration-contracts/gateway_response_contract.md`
- `agent-briefings/hermes_capability_handoff.md`
- `docs/01_capability_matrix.md`

## 3. Core Freeze Statement

Phase 2 stable Hermes must be understood as:

```text
Hermes is an enterprise agent kernel with a conservative platform-facing surface.
```

It must not be understood as:

```text
Hermes is only a platform catalog chatbot.
```

The platform-facing surface can remain narrow:

1. `asset_catalog_search`
2. `catalog-only`
3. permission proof
4. path redaction
5. Missing Evidence
6. safe IDs and traces
7. no raw row / raw path / secret exposure

The standalone Hermes kernel must remain broader:

1. workspace and task context
2. session / thread / response continuity
3. evidence-first retrieval and citation policy
4. low-sensitive memory continuity
5. vector / BM25 / rerank retrieval foundation
6. file governance and natural import path
7. NAS scratch-copy / parser / evidence-write future path
8. orchestration and review-task future path

## 4. Standalone Hermes Workspace Boundary

Hermes must be allowed to develop and keep its own workspace concept independent of the platform UI.

The workspace may contain low-sensitive operational state such as:

1. current project context label;
2. session / thread references;
3. current task goal and bounded step status;
4. related `file_id` / `model_id` / `document_id` references;
5. `query_id` / `trace_id` references;
6. user confirmation labels and feedback labels;
7. evidence mode summaries;
8. pending Missing Evidence or human-review tasks.

The workspace must not contain:

1. raw NAS path;
2. raw `storage_path` / `storage_uri`;
3. raw DB row;
4. raw file content;
5. DWG / RVT / BIM extracted content unless a later governed evidence phase explicitly authorizes it;
6. secrets, tokens, passwords, or API keys;
7. permission proof token material;
8. customer-sensitive free text without a later reviewed retention policy.

## 5. Platform Gateway Boundary

The current platform Gateway safety model remains correct and must not be weakened.

Gateway owns:

1. login and project switch;
2. `project_scope`;
3. permission proof;
4. path redaction;
5. forbidden-field scan;
6. platform audit;
7. fail-closed behavior for raw path, raw row, secret, or unsupported evidence claims.

Hermes owns:

1. answer governance;
2. Evidence / Missing Evidence decisions;
3. session and reasoning continuity;
4. tool orchestration semantics;
5. low-sensitive memory candidates;
6. response / query / trace semantics;
7. cross-tool synthesis when future tools are enabled.

Platform may wrap Hermes conservatively. Platform must not become the owner of Hermes reasoning state.

## 6. Memory And Vector Foundation Are Not Wasted

The existing memory and retrieval foundation remains part of Hermes's product value.

Current platform integration only exposes the first layer:

```text
Catalog Layer
```

The following layers remain reserved and must not be erased from the product roadmap:

1. Evidence Layer: governed document evidence search over authorized, parsed, citation-bearing content.
2. Memory Layer: low-sensitive continuity with related IDs, query / trace refs, feedback labels, and preferences.
3. Retrieval Layer: hybrid retrieval with vector search, BM25, metadata filters, rerank, citation, and evaluation.
4. Workspace Layer: task state, session continuity, and bounded project context.
5. Governance Layer: natural import, file governance, NAS scratch-copy, parser dry-run, evidence-write gates, human review.

Phase 2 stable platform baseline must therefore say:

```text
The platform currently exposes only catalog-only access.
Hermes retains the broader memory / retrieval / evidence kernel for later controlled unlock.
```

It must not say:

```text
Hermes has no use for memory or vector retrieval because the platform only exposes catalog search.
```

## 7. Phase 2 Acceptance Addendum

Phase 2 can pause on a stable platform baseline only if all of the following remain true:

1. Hermes identity is frozen as enterprise agent kernel, not platform plugin.
2. Platform catalog-only mode is described as a current safety surface, not a product ceiling.
3. Standalone Hermes workspace / memory / evidence / retrieval / NAS governance paths are preserved in docs and shared contracts.
4. Test-machine stable tags remain usable for platform integration even if Phase 3 implementation continues elsewhere.
5. Platform future work can unlock Hermes native session, evidence search, memory continuity, and feedback without changing the meaning of Phase 2.
6. Phase 2 stable tag is not production rollout.
7. Phase 2 stable tag is not DWG/RVT/BIM content understanding.
8. Phase 2 stable tag is not Agent DB CRUD, Agent SQL, or unrestricted NAS scanning.

## 8. Phase 3 Unlock Map

Phase 3 should not start by replacing the platform Gateway. It should unlock Hermes capabilities through controlled contracts.

Recommended unlock order:

1. Native session / thread / response lifecycle.
2. Evidence Availability from catalog assets to governed evidence states.
3. `document_evidence_search` for authorized parsed content.
4. Low-sensitive memory continuity runtime.
5. Feedback to evaluation / triage linkage.
6. Natural import and file governance usability.
7. NAS scratch-copy to parser to evidence write under explicit authorization.
8. Orchestration and human-review task routing.

Data Steward remains one module in this map. It should not consume the entire Hermes roadmap.

## 9. Go / Pause / No-Go

### Go

1. Phase 2 stable baseline keeps platform read-only / catalog-only.
2. Hermes standalone kernel authority is documented and shared.
3. Workspace / memory / evidence / retrieval / NAS governance are preserved as future unlock paths.
4. Platform contract says current Gateway mode is conservative and `architecture_authority_health=orange`.
5. Shared docs and local docs use consistent wording.

### Pause

1. Platform or docs imply Hermes is only a catalog chatbot.
2. Shared docs omit standalone workspace / memory / evidence future unlocks.
3. Test-machine stable tag is described as full Phase 2 closeout.
4. Data Steward is described as Hermes's full product identity.

### No-Go

1. Hermes is asked to bypass Gateway permission proof.
2. Hermes is asked to naked-connect DB or generate SQL.
3. Hermes is asked to expose raw NAS paths or raw DB rows.
4. Catalog metadata is used as content evidence.
5. Platform becomes the reasoning/session owner and Hermes becomes stateless text generation only.

## 10. Conclusion

Phase 2.108 keeps the conservative platform baseline while protecting the original Hermes goal:

```text
Hermes must remain a company-level enterprise agent kernel.
The platform may expose it safely in stages.
```

This contract allows the platform to keep using the Phase 2 stable tag while Phase 3 later expands Hermes into governed evidence search, memory continuity, workspace operation, NAS governance, and orchestration without breaking the Phase 2 integration promise.
