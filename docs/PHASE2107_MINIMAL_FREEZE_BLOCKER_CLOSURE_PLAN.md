# Phase 2.107 Minimal Freeze Blocker Closure Plan

## 1. Purpose

Phase 2.107 narrows the Phase 2.106 freeze readiness work into a minimal closure matrix for the platform-facing stable Hermes baseline.

The target remains:

```text
Phase 2 Stable Hermes for Platform Integration
```

This phase answers one question:

```text
What must be closed before a stable platform baseline tag, and what can safely remain as a documented risk or later-phase item?
```

This is a docs / decision-matrix planning phase only. It does not create a stable tag, modify runtime code, modify tests, connect to runtime services, write business data, or enter Phase 3.

## 2. Sources Reviewed

Hermes repo sources:

- `docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md`
- `docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md`
- `docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`
- `eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`
- `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`
- `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`
- `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`
- `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`
- `docs/PHASE2102B_METRIC_SCORING_PACK.md`
- `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`
- `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`

Shared `DigitalDeliveryProject` sources:

- `integration-contracts/hermes_kernel_authority_contract.md`
- `docs/01_capability_matrix.md`

Shared docs status: available. No shared files were modified in Phase 2.107.

## 2.1 Platform Alignment Report Incorporated

The latest Platform / DB Agent alignment report was reviewed during Codex B review and is treated as a Phase 2.107 input.

Accepted findings:

1. Current Platform-to-Hermes runtime still has plugin-mode risk: the external Hermes path is OpenAI-compatible `system + current user message -> choices[0].message.content`, not native Hermes kernel orchestration.
2. Current `architecture_authority_health` should be treated as `orange`, not green.
3. Gateway safety is close to green: Platform owns `project_scope`, `permission_decision`, path redaction, forbidden-field scan, and catalog-only surface.
4. Stable-tag readiness should be `Go only for 0B Gateway hardening`, not native runtime alignment.
5. High-risk forbidden-field hits should fail closed instead of only sanitizing and continuing with the external answer.
6. Capabilities / health should expose `authority_health.architecture_authority_health=orange` until native session / thread / response lifecycle exists.
7. User-facing wording must not imply full native Hermes kernel alignment while the current path is still catalog-only OpenAI-compatible smoke / Gateway wrapping.

Phase 2.107 therefore tightens the stable-tag blocker set: the stable platform baseline may still freeze without native session/thread runtime, but only if 0B Gateway hardening makes the limitation explicit and safe.

## 3. Decision Taxonomy

| Classification | Meaning |
|---|---|
| `must_close_before_stable_tag` | Must be closed, verified, or explicitly confirmed before a platform stable tag. |
| `freeze_with_known_risk` | Can remain open only if named as a stable-baseline limitation. |
| `phase3_plus_deferred` | Outside the stable platform baseline and should not block the tag. |
| `user_business_decision_required` | Requires user/product decision before the stable tag. |
| `already_satisfied` | Already covered by committed docs, contracts, or current safety baseline. |

## 4. Minimal Stable-tag Blocker Set

The smallest recommended `must_close_before_stable_tag` set is:

1. **Platform identity / wording alignment**
   Platform must not present Hermes as a stateless chat plugin or Data Steward-only tool.
2. **Gateway permission / project scope / path redaction boundary**
   Gateway must remain the permission, project-scope, redaction, forbidden-field, and platform-audit authority.
3. **Catalog-only asset query and safe refs**
   Current stable surface must stay catalog-only with safe `file_id`, `model_id`, `source_view`, `query_id`, and `trace_id`.
4. **Missing Evidence for unsupported or unavailable content evidence**
   DWG/RVT/BIM/content-level questions must not be answered from catalog metadata.
5. **Path redaction / forbidden-field policy**
   Raw paths, raw rows, raw answers, secrets, and unsupported evidence claims must remain forbidden; high-risk hits should fail closed instead of silently passing sanitized external answers.
6. **Shared contract sync**
   The shared Hermes kernel authority contract must stay aligned with platform wording.
7. **Test-machine update to stable tag**
   The test machine must be able to checkout the future stable tag and verify docs / JSON / env key names without runtime smoke.
8. **0B Gateway hardening / observability fields**
   Gateway should expose honest compatibility-mode health, including `responseId`, `safeMemoryCandidates=[]`, `authorityHealth.orange`, and session/thread/context placeholder fields without claiming native Hermes semantics.
9. **Platform user-facing wording fix**
   Platform UI / smoke labels should not say or imply "真实 Hermes 回答" when the path is still external Hermes catalog-only smoke / Gateway wrapping.

This set is intentionally narrow. It is enough for a stable platform integration target, not for full Phase 2 PRD / Roadmap closeout.

## 5. Known Risks Allowed For Freeze

The following can remain open only as explicit `freeze_with_known_risk` items:

1. Runtime `session_id` / `thread_id` / `previous_response_id` support, but only after the 0B Gateway hardening above makes the current limitation explicit.
2. Evidence Layer / future `document_evidence_search` not productized.
3. Low-sensitive memory continuity runtime not productized.
4. Feedback / scoring linkage remains contract / review-signal oriented.
5. Eval inventory remains 19 accepted starter cases, below PRD 100+ and Roadmap 300+.
6. Top5 / citation metrics are not measured at target scale.

These risks must stay visible in the baseline notes. They cannot be used to claim full Phase 2 closeout.

## 6. Phase 3+ Deferred Items

The following should not block the stable platform tag:

1. Production rollout.
2. Full Data Steward productization.
3. DWG/RVT/BIM content understanding.
4. NAS semantic collection.
5. Agent DB CRUD / SQL.
6. Repair executor / destructive cleanup / reindex automation.
7. Graph, spatial, ontology, or model-internal understanding productization.

These are outside the current stable platform integration baseline.

## 7. User Business Decisions Needed

The main user decision before a stable tag is:

```text
Does natural-language import / file governance usability need to be proven before the stable platform baseline tag?
```

Recommended default:

```text
Do not block the platform stable tag on natural import usability unless the user explicitly wants this as part of the stable embed.
```

Reason:

1. Stable platform baseline is catalog-only / permission-aware / Missing-Evidence-first.
2. Natural import is a user-flow and governance usability concern.
3. It can be documented as post-freeze or Phase 3+ if not required for platform embed.

## 8. Closure Matrix Summary

| Area | Classification | Decision |
|---|---|---|
| Platform plugin wording risk | `must_close_before_stable_tag` | Close through shared wording plus 0B Gateway hardening; current architecture health is `orange`. |
| Runtime session/thread refs | `freeze_with_known_risk` | Do not block only if 0B Gateway hardening exposes honest `authority_health.orange` and placeholder fields without claiming native semantics. |
| Gateway permission / project scope | `must_close_before_stable_tag` | Must remain explicit and accepted. |
| Catalog-only safe refs | `must_close_before_stable_tag` | Must remain current stable surface. |
| Missing Evidence | `must_close_before_stable_tag` | Must remain active answer boundary. |
| Path redaction / forbidden-field fail-closed | `must_close_before_stable_tag` | Must remain current safety boundary; high-risk forbidden-field hits should fail closed. |
| 0B Gateway hardening | `must_close_before_stable_tag` | Must expose response / memory-candidate / authority-health fields honestly before stable tag. |
| Platform wording for smoke / compatibility path | `must_close_before_stable_tag` | Must not imply full native Hermes kernel alignment. |
| Evidence Layer | `freeze_with_known_risk` | Contract exists; runtime productization deferred. |
| Memory runtime | `freeze_with_known_risk` | Contract exists; runtime productization deferred. |
| Eval counts and target metrics | `freeze_with_known_risk` | Blocks full closeout, not narrow platform baseline. |
| Natural import | `user_business_decision_required` | User decides whether this blocks stable tag. |
| Test-machine update | `must_close_before_stable_tag` | Must run after future stable tag exists. |
| Production rollout / Data Steward productization / Agent DB CRUD / NAS semantic collection | `phase3_plus_deferred` | Not part of stable platform tag. |

## 9. Recommended Stable-tag Gate

Before creating a future stable Hermes tag:

1. Codex B reviews this plan and `eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json`.
2. User confirms whether natural import usability blocks the stable tag.
3. Platform wording remains aligned with Hermes kernel authority.
4. Test-machine update prompt is run against the future stable tag.
5. No runtime code, shared files, or unrelated `docs/digital-delivery-standards/` files are mixed into the baseline.
6. The baseline is described as platform stable integration, not production rollout or Phase 2 full closeout.

## 10. Phase 2.107 Conclusion

Phase 2.107 recommends a narrow stable-tag blocker set: identity / authority alignment, Gateway safety, catalog-only safe refs, Missing Evidence, path redaction, shared contract sync, and test-machine update.

Evidence Layer, Memory runtime, target-scale metrics, and session/thread runtime refs can be frozen with known risk if the platform accepts the limitations.

Production rollout, full Data Steward, DB CRUD / SQL, NAS semantic collection, and DWG/RVT/BIM content understanding remain Phase 3+ or later.
