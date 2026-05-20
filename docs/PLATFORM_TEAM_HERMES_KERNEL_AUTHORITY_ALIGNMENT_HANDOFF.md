# Platform Team Handoff: Hermes Kernel Authority Alignment

## One-line Positioning

```text
Hermes is the enterprise agent kernel; Platform is the UI + Gateway + permission/data surface.
```

Data Steward / Catalog is one Hermes capability module. It is not the whole Hermes identity.

## Why This Handoff Exists

The current Gateway design is safe and should be preserved. The risk is product coupling: if Platform treats Hermes as a stateless single-turn chat endpoint, Hermes loses the session continuity, reasoning state, tool orchestration, evidence policy, and memory boundary that make it an enterprise kernel.

This handoff does not request runtime changes in this phase. It defines the alignment Platform should follow in future implementation planning.

## Keep These Gateway Authorities

Platform Gateway must continue to own:

1. login and requester identity;
2. project / tenant / role switch handling;
3. server-validated `project_scope`;
4. permission proof and permission refresh;
5. path redaction;
6. forbidden-field scan;
7. platform audit;
8. safe mapping from platform records to Hermes-safe refs.

Hermes must not replace these authorities.

## Give Hermes These Kernel Responsibilities

Hermes owns:

1. agent session continuity;
2. reasoning state;
3. tool orchestration;
4. evidence / Missing Evidence policy;
5. memory continuity boundary;
6. response trace semantics;
7. cross-tool answer synthesis;
8. safe memory candidate generation.

Frontend may display the assistant thread, but frontend should not become the reasoning-state owner.

## Future Request / Response Expectations

Future Platform -> Hermes calls should carry safe continuity refs:

1. `session_id`;
2. `thread_id`;
3. current `query`;
4. server-validated `project_scope`;
5. `permission_proof_ref`;
6. sanitized context refs;
7. optional `previous_response_id`.

Future Hermes -> Platform responses should carry kernel trace refs:

1. `response_id`;
2. `query_id`;
3. `trace_id`;
4. `context_refs`;
5. `tool_plan_summary`;
6. `missing_evidence`;
7. `safe_memory_candidates`;
8. authority / coupling health fields where useful.

## Go / Pause / No-Go

### Go

Go when:

1. Platform treats Hermes as kernel/session/orchestration owner.
2. Gateway remains permission and redaction owner.
3. Data Steward is presented as one Hermes tool/capability module.
4. Session / thread / context refs are planned as safe references, not raw history dumps.

### Pause

Pause when:

1. Platform only sends current user message and a prompt.
2. Platform discards session continuity.
3. Platform calls Hermes a generic chat plugin.
4. Platform expects catalog metadata to answer content questions.

### No-Go

No-Go when:

1. Hermes is asked to naked-connect to DB.
2. Hermes is asked to generate SQL.
3. Raw NAS paths, raw DB rows, raw file content, secrets, tokens, or credentials are sent to Hermes prompts.
4. Raw assistant history is stored as memory evidence.
5. Data Steward is treated as the whole Hermes product.

## Safe Platform Message

Recommended internal wording:

> Platform owns UI, Gateway, permission proof, redaction, and audit. Hermes owns the enterprise agent kernel: session continuity, reasoning state, tool orchestration, evidence policy, Missing Evidence, memory boundary, and response trace semantics.

## Current Runtime Status

Current status remains conservative:

1. Gateway catalog-only safety is valid and useful.
2. Hermes should still return Missing Evidence for content questions when only catalog metadata exists.
3. No runtime session/Gateway change is implemented by Phase 2.105.
4. No platform repo file was modified by Phase 2.105.
5. Any future implementation should be planned as a separate bounded phase.

## Phase 2.105 Handoff Conclusion

Use this handoff to keep Platform integration safe without turning Hermes into a stateless plugin. The next implementation decision should preserve both sides:

```text
Gateway safety authority remains with Platform.
Agent kernel authority remains with Hermes.
```
