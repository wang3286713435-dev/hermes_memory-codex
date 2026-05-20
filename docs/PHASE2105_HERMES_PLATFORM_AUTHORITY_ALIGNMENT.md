# Phase 2.105 Hermes Kernel Authority / Platform Alignment

## 1. Purpose

Phase 2.105 aligns the product and architecture boundary between Hermes and the digital delivery platform.

The current platform integration is safe, but it can accidentally compress Hermes into a platform-embedded single-turn Q&A plugin. That is not the intended architecture.

Target architecture:

```text
Hermes = enterprise agent kernel
Platform = UI + Gateway + permission/data surface
Data Steward / Catalog = one Hermes capability module, not the whole Hermes identity
```

This phase is docs / contract / fixture planning only. It does not implement runtime session changes, Gateway changes, platform code, DB access, NAS access, evidence search, memory writes, facts writes, repair, or rollout.

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`
- `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`
- `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md`
- `docs/PHASE2104D_FEEDBACK_SCORING_LINKAGE_CONTRACT.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
- `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`

Shared `DigitalDeliveryProject` sources:

- `README.md`
- `PROJECT_CHARTER.md`
- `RISK_RED_LINES.md`
- `docs/01_capability_matrix.md`
- `integration-contracts/platform_to_hermes_contract.md`
- `integration-contracts/catalog_tool_contract.md`
- `integration-contracts/missing_evidence_policy.md`
- `agent-briefings/hermes_agent_bootstrap.md`

Shared docs status: available. No shared files were edited.

## 3. Authority Split

| Owner | Authority | Must Not Own |
|---|---|---|
| Platform UI | User surface, project page context display, front-end interaction, assistant thread display | Reasoning state, permission bypass, raw path exposure, final evidence policy |
| Platform Gateway | Login, project switch, permission proof, `project_scope`, path redaction, forbidden-field scan, platform audit | Hermes reasoning state, tool orchestration, long-term memory, answer synthesis |
| Hermes Kernel | Agent session continuity, reasoning state, tool orchestration, evidence / Missing Evidence policy, memory continuity boundary, response trace semantics, cross-tool answer synthesis | Platform login, raw DB access, raw NAS access, permission proof minting, path redaction authority |
| Data Steward / Catalog | Hermes capability/tool module for asset governance, catalog search, safe file/model IDs, evidence availability signals | The whole Hermes identity, reasoning owner, final assistant product shell |

Operational principle:

```text
Gateway owns permission and redaction.
Hermes owns agent kernel continuity and answer governance.
Catalog is one Hermes tool surface, not Hermes itself.
```

## 4. Minimum Repair Without Architecture Reversal

Preserve the current safe Gateway architecture:

1. Gateway remains the permission and path-redaction authority.
2. Hermes must not naked-connect to DB.
3. Hermes must not generate SQL.
4. Hermes must not expose raw NAS path or raw storage path.
5. Hermes must not write catalog rows, NAS content, raw paths, raw rows, or file contents into long-term memory.

Fix the product boundary:

1. Platform must not treat Hermes as a stateless endpoint receiving only one user message.
2. Platform should pass `session_id`, `thread_id`, or equivalent conversation reference.
3. Platform should pass sanitized recent conversation context or a safe `previous_response_id` equivalent when available.
4. Hermes should return `response_id`, `query_id`, `trace_id`, `context_refs`, `tool_plan_summary`, `missing_evidence`, and `safe_memory_candidates` where applicable.
5. On project / tenant / role switch, Platform must revalidate or invalidate prior context.
6. Frontend may display the assistant thread, but should not become the reasoning-state owner.

## 5. Coupling Health Definition

| Health Area | Green | Yellow / Orange | Red |
|---|---|---|---|
| Safety health | Permission proof, path redaction, catalog-only boundary, forbidden-field scan, and Missing Evidence are enforced | Some fields are ambiguous but fail closed | Raw paths, raw rows, permission bypass, or unsupported evidence claims leak |
| Capability health | Catalog, evidence, memory, feedback, and orchestration capabilities are clearly staged | Hermes only answers catalog questions and cannot show future staged path clearly | Platform or users believe unsupported content understanding is current |
| Architecture authority health | Hermes owns session / reasoning / tool orchestration while Platform owns UI / Gateway / permission | Platform passes single-turn prompts and some session refs inconsistently | Platform owns session/reasoning and Hermes becomes a stateless plugin |

Target:

```text
safety green + capability staged + authority aligned
```

Current risk:

```text
safety green + capability narrow + authority orange/red if Platform owns reasoning continuity
```

## 6. Current Status

1. Current Gateway catalog-only safety is useful and should be preserved.
2. Current platform integration appears too close to single-turn plugin mode if it only sends a current user message plus a system prompt.
3. Single-turn plugin mode blocks Hermes from acting as the enterprise kernel.
4. Data Steward / Catalog integration is a valuable capability module, but it is not the whole Hermes product.
5. Phase 2.105 is docs-only alignment. Runtime session implementation remains future work.

## 7. Go / Pause / No-Go

### Go

Proceed with future design or implementation planning when:

1. Platform acknowledges Hermes as kernel/session/orchestration owner.
2. Gateway keeps permission and path-redaction authority.
3. Data Steward is treated as a Hermes capability module.
4. Future implementation will carry session/thread/context refs safely.
5. Permission, project scope, and redaction remain server-side / Gateway controlled.

### Pause

Pause for design correction when:

1. Platform only sends current user message plus system prompt and discards session continuity.
2. Platform calls Hermes a generic chat plugin.
3. Platform expects Hermes to answer content questions from catalog-only data.
4. Platform stores assistant thread history but does not provide safe context refs back to Hermes.
5. Project / tenant / role switches do not invalidate or revalidate prior context.

### No-Go

Reject the integration direction when:

1. Platform asks Hermes to naked-connect to DB or generate SQL.
2. Platform sends raw NAS paths, raw rows, secrets, or raw file content in prompt context.
3. Platform stores unsafe raw assistant history as memory evidence.
4. Platform treats Data Steward as the whole Hermes product.
5. Frontend or Platform becomes the reasoning-state owner while Hermes is only a stateless text endpoint.

## 8. Response / Request Alignment Contract

Minimum future Platform -> Hermes request shape:

```json
{
  "session_id": "safe_session_ref",
  "thread_id": "safe_thread_ref",
  "query": "user message",
  "project_scope": "gateway_validated_scope_ref",
  "permission_proof_ref": "gateway_validated_permission_ref",
  "sanitized_context_refs": [],
  "previous_response_id": "optional_safe_response_ref"
}
```

Minimum future Hermes -> Platform response shape:

```json
{
  "response_id": "safe_response_ref",
  "query_id": "safe_query_ref",
  "trace_id": "safe_trace_ref",
  "context_refs": [],
  "tool_plan_summary": [],
  "missing_evidence": [],
  "safe_memory_candidates": [],
  "authority_health": {
    "safety_health": "green",
    "capability_health": "staged",
    "architecture_authority_health": "aligned"
  }
}
```

This is a planning contract only. It does not add runtime fields today.

## 9. User-Facing Product Language

Safe wording:

> Hermes is the enterprise agent kernel. The platform provides the UI, Gateway, permission proof, and safe data surface. Catalog / Data Steward is one Hermes capability for asset governance.

Unsafe wording:

> Hermes is a chat plugin inside the platform.

Unsafe wording:

> Data Steward is Hermes.

Unsafe wording:

> Hermes can answer document contents from catalog metadata.

## 10. Phase 2.105 Conclusion

Phase 2.105 documents the authority alignment needed before deeper platform integration.

It preserves Gateway safety while correcting the product boundary: Hermes must remain the enterprise agent kernel, not a single-turn platform plugin. Runtime implementation, session propagation, Gateway contracts, and Platform UI changes remain future work.
