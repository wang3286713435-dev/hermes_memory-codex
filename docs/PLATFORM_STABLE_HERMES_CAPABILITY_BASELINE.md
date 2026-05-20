# Platform Stable Hermes Capability Baseline

## 1. Baseline Name

```text
Phase 2 Stable Hermes for Platform Integration
```

This is a platform-facing capability baseline, not a production rollout and not full Phase 2 closeout.

## 2. What Platform Can Depend On

1. Product identity: Hermes is the enterprise agent kernel.
2. Platform responsibility: UI, Gateway, login, project switch, permission proof, path redaction, forbidden-field scan, platform audit.
3. Hermes responsibility: session continuity, reasoning state, tool orchestration, evidence / Missing Evidence policy, memory continuity boundary, response trace semantics, cross-tool answer synthesis.
4. Current runtime-facing capability: read-only `asset_catalog_search` / catalog-only asset query.
5. Current evidence boundary: catalog metadata is not file正文, DWG/RVT internals, or BIM component evidence.
6. Current safe refs: `file_id`, `model_id`, `source_view`, `query_id`, `trace_id`, safe display locator.
7. Current safety behavior: permission-aware / fail-closed / path redacted.
8. Current answer behavior: Missing Evidence for content-level questions when governed evidence is unavailable.
9. Current memory boundary: low-sensitive refs only; no raw path, raw row, file content, or permission proof in memory.
10. Current feedback boundary: feedback can become review signal only; it cannot auto-pass metrics, create facts, write memory, or trigger repair.

## 3. Stable User-Facing Capability Wording

Approved internal wording:

> Hermes can help users search authorized asset catalog metadata and identify candidate files or models through the Platform Gateway. When content evidence is unavailable, Hermes returns Missing Evidence rather than guessing.

Approved internal wording:

> Hermes is the enterprise agent kernel. Platform provides UI, Gateway, permission proof, path redaction, and audit.

Forbidden wording:

> Hermes can read all NAS files.

Forbidden wording:

> Hermes can understand DWG / RVT / BIM contents today.

Forbidden wording:

> Hermes is just a platform chat plugin.

Forbidden wording:

> Data Steward is the whole Hermes product.

## 4. Stable Response Expectations

Platform can expect Hermes or the Gateway-facing integration layer to preserve these safe concepts:

1. `query_id`
2. `trace_id`
3. `file_id`
4. `model_id`
5. `source_view`
6. `permission_decision`
7. `missing_evidence_reason`
8. safe display path / locator only
9. no raw path or raw row
10. no unsupported content claim

Future expected kernel fields, still not guaranteed by current runtime:

1. `response_id`
2. `session_id`
3. `thread_id`
4. `context_refs`
5. `tool_plan_summary`
6. `safe_memory_candidates`
7. `authority_health`

## 5. Known Risks For Platform Stable Baseline

| Risk | Status | Platform Handling |
|---|---|---|
| Runtime session/thread/context refs are incomplete | known risk | Treat as next integration phase, not current blocker if product wording stays honest. |
| Evidence layer is not productized | known risk | Keep catalog-only and Missing Evidence wording. |
| Memory continuity is not productized | known risk | Show only low-sensitive contract language, not raw memory claims. |
| PRD/Roadmap metric counts remain incomplete | known risk | Do not claim full Phase 2 closeout or metric targets. |
| Data Steward is catalog-only | accepted boundary | Do not imply BIM/DWG/RVT content understanding. |

## 6. Go / Pause / No-Go For Platform Stable Baseline

### Go

1. Platform uses Hermes as enterprise agent kernel.
2. Gateway remains permission / redaction / audit authority.
3. Platform accepts catalog-only current capability and Missing Evidence for content questions.
4. Shared `hermes_kernel_authority_contract.md` remains aligned.
5. Test-machine update can verify docs / tag / environment key names without runtime smoke.

### Pause

1. Platform still describes Hermes as single-turn plugin.
2. Platform wants runtime session/context refs before freezing baseline.
3. Platform needs natural import or employee trial evidence before stable embed.
4. Test-machine update prompt cannot be run cleanly.

### No-Go

1. Platform expects production rollout.
2. Platform asks Hermes to connect directly to DB/NAS.
3. Platform expects Agent SQL or raw DB rows.
4. Platform sends or displays raw NAS/storage paths.
5. Platform expects DWG/RVT/BIM content evidence from catalog metadata.

## 7. Baseline Conclusion

The stable platform baseline is intentionally narrow:

```text
catalog-only + permission-aware + Missing Evidence + safe refs + Hermes kernel authority contract
```

It is enough for a controlled platform integration target. It is not enough to declare full Phase 2 PRD / Roadmap closeout.
