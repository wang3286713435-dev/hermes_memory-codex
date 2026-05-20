# Phase 2.104b Low-sensitive Memory Continuity + Permission Boundary Contract

## 1. Purpose

Phase 2.104b defines the boundary between platform permission, catalog permission decisions, and Hermes low-sensitive memory continuity.

The core rule is:

```text
Platform permission proof is the authority.
Catalog permission decision applies only to the current catalog / asset response.
Hermes memory continuity is only a low-sensitive UX hint.
Hermes memory must never grant access, bypass denial, or become content evidence.
```

This phase is docs and fixtures only. It does not implement memory runtime read/write behavior, `document_evidence_search`, tools, DB access, Gateway access, or production rollout.

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`
- `eval/phase2_inventory/evidence_availability_contract_examples.json`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`
- `docs/PHASE2102B_METRIC_SCORING_PACK.md`

Shared `DigitalDeliveryProject` sources:

- `agent-briefings/hermes_capability_handoff.md`
- `docs/01_capability_matrix.md`
- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `integration-contracts/feedback_contract.md`
- `RISK_RED_LINES.md`

Shared docs status: available.

## 3. Three Permission Layers

| Layer | Source | Role | Must Not Do |
|---|---|---|---|
| `platform_permission` | Platform / Gateway / API key / project switch / tenant context | Final authorization authority for the current request or session boundary | Must not be replaced by catalog response, memory, feedback, or prior session state |
| `catalog_permission_decision` | Gateway / catalog response | Indicates whether safe catalog metadata may be shown for the current request | Must not grant content evidence access by itself |
| `memory_continuity_reference` | Hermes low-sensitive memory, session context, or feedback | UX continuity hint for likely related files/models/queries/preferences | Must never grant access, bypass denial, or become content evidence |

Platform permission must be refreshed or revalidated when the user changes project, tenant, role, session, token, or requester identity.

Catalog permission is scoped to one catalog response. It does not prove that document evidence, vector evidence, or model internals are accessible.

Memory references may suggest context candidates, but every answer still needs current platform permission and, for content-level questions, governed evidence.

## 4. Allowed Low-sensitive Memory Fields

Allowed fields are low-sensitive metadata or references only:

| Field | Meaning | Evidence Status |
|---|---|---|
| `related_file_ids` | File IDs referenced in a governed interaction | Not content evidence |
| `related_model_ids` | Model IDs referenced in a governed interaction | Not content evidence |
| `query_id` | Query trace reference | Not content evidence |
| `trace_id` | Observability / debugging reference | Not content evidence |
| `feedback_label` | Low-sensitive user feedback label | Not content evidence |
| `last_safe_project_context_label` | Safe project context label, not raw path or ACL | Not permission proof |
| `preferred_result_grouping` | Display preference, such as group by file type or discipline | Not evidence |
| `last_evidence_mode` | Last known evidence mode label, such as `catalog_only` | Not current evidence proof |
| `last_permission_decision_summary` | Safe summary label, such as `allowed_catalog_only` or `permission_denied` | Not reusable authorization |

Allowed fields help Hermes continue a workflow. They do not prove access, do not prove content, and do not preserve permission across changed contexts.

## 5. Forbidden Memory Fields

Hermes memory must not store:

1. raw `storage_path`;
2. raw NAS path;
3. raw DB row;
4. raw catalog row;
5. file正文 / document text;
6. DWG / RVT / BIM content;
7. customer-sensitive note text;
8. secret / token / password / credential / `.env`;
9. full permission proof token;
10. project member list / ACL snapshot unless separately authorized.

If any forbidden field is detected in a proposed memory write, the safe action is to reject the memory write or sanitize it into an allowed low-sensitive label.

## 6. Access Revalidation Rules

1. Memory related IDs may propose candidate context only.
2. Every new answer must re-check current Platform permission proof.
3. Absent, stale, mismatched, or denied permission means Hermes cannot use memory refs to answer.
4. For "continue from last file" requests, Hermes can say it needs current permission proof before using that reference.
5. Memory cannot preserve access after project switch, role change, logout, token expiry, tenant change, or requester identity change.
6. Catalog permission decision can show catalog metadata only for the current response; it does not authorize content evidence retrieval.
7. Content-level answers still require governed evidence and citations or Missing Evidence.

## 7. Permission Conflict Outcomes

### 7.1 `allowed_current_scope`

When it applies:

- Current `platform_permission` is valid and allows the requester.
- Catalog permission allows safe metadata for the current response.
- Memory reference, if present, only proposes a candidate file/model/query.

Safe behavior:

- Use memory reference as a candidate context hint.
- Re-run catalog or future evidence availability checks under current permission.
- Keep answer within current evidence mode.

Safe user wording:

> I can continue from the referenced file/model after checking current permission. The memory reference is only a context hint; it is not content evidence.

Forbidden behavior:

- Treat prior memory as access proof.
- Treat related file/model IDs as content evidence.
- Skip current permission check.

### 7.2 `denied_current_scope`

When it applies:

- Current platform permission denies the requester.
- Tenant, role, project, or token no longer allows access.

Safe behavior:

- Do not use memory refs to answer.
- Do not expose content, raw path, or sensitive metadata.
- Return a safe denial message.

Safe user wording:

> I cannot use the prior file/model reference because the current permission context does not allow access. Please refresh access through the platform workflow.

Forbidden behavior:

- Answer from prior context.
- Use feedback or related IDs to bypass denial.
- Reveal denied source details.

### 7.3 `requires_permission_refresh`

When it applies:

- Current platform permission proof is absent, stale, expired, or mismatched.

Safe behavior:

- Ask for permission refresh.
- Keep memory reference inactive until permission is revalidated.
- Return Missing Evidence / permission refresh required for content-level questions.

Safe user wording:

> I remember a low-sensitive reference to the prior file/model, but I need current platform permission proof before using it.

Forbidden behavior:

- Assume permission is still valid.
- Continue from last file after logout, project switch, role change, token expiry, or tenant change.

### 7.4 `memory_reference_only`

When it applies:

- Memory reference exists and is allowed as low-sensitive metadata.
- Current evidence availability is still catalog-only or otherwise not enough for content-level answer.

Safe behavior:

- Use the reference to identify a candidate.
- Return Missing Evidence for content-level questions.
- State that related IDs are not content evidence.

Safe user wording:

> I can use the remembered file/model ID as a candidate reference, but it does not prove the file content. Current evidence is still catalog-only, so this content question requires Missing Evidence or manual review.

Forbidden behavior:

- Claim Hermes has read the remembered file.
- Query vector/evidence store without an authorized evidence state.
- Treat memory continuity as document evidence.

### 7.5 `manual_review_required`

When it applies:

- Permission or evidence state is ambiguous.
- Conflicting catalog/memory/evidence labels make automated handling unsafe.

Safe behavior:

- Stop automated answer.
- Produce a sanitized review reason.
- Do not execute repair, write memory, or choose a source as truth.

Safe user wording:

> The current permission or evidence state is ambiguous. Manual review is required before this can be used as verified context.

Forbidden behavior:

- Resolve ambiguity by guessing.
- Convert ambiguous user feedback into long-term memory.
- Execute any data repair or permission update.

## 8. Fixture File

The Phase 2.104b fixture file is:

`eval/phase2_inventory/memory_continuity_permission_examples.json`

Fixture rules:

1. Use fake IDs only, such as `file_demo_101`, `model_demo_101`, `query_demo_101`, `trace_demo_101`.
2. Do not include real project names, real file names, raw paths, raw rows, asset UIDs, source IDs, secrets, tokens, or customer-sensitive content.
3. Every case must make these booleans explicit:
   - `should_store_memory`
   - `should_use_as_content_evidence`
   - `should_bypass_permission`
   - `should_expose_raw_path`
   - `should_query_evidence`
4. `should_use_as_content_evidence` and `should_bypass_permission` must always be false for memory continuity references.

## 9. Shared Follow-up

No shared folder files were edited in Phase 2.104b.

Recommended shared follow-up after Codex B review:

1. Mirror the three-layer permission model into shared `integration-contracts`.
2. Add the allowed/forbidden memory field list to shared `feedback_contract.md` or a future memory continuity contract.
3. Keep `related_file_ids` and `related_model_ids` described as low-sensitive references only.

## 10. Phase 2.104b Conclusion

Phase 2.104b provides a docs-only Memory Continuity + Permission Boundary Contract and sanitized fixtures. It is ready for Codex B review after validation, but it does not authorize runtime memory writes, permission changes, evidence search, DB/NAS access, index writes, or production rollout.
