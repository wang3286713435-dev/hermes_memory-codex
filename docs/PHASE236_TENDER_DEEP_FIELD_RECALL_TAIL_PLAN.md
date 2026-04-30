# Phase 2.36 Tender Deep-field Recall Tail Plan

## 1. Goal

Phase 2.36 is a planning-only phase after the Phase 2.35c baseline.

Phase 2.35c closed the alias/session blocker: `@主标书` can now be bound and reused in real Hermes CLI Q1/Q2 without `alias_missing` or `retrieval_suppressed`.

Phase 2.35c did not close all tender deep-field recall gaps. This phase classifies the remaining gaps and proposes a bounded Phase 2.36a implementation path.

This phase does not write feature code, mutate DB data, update OpenSearch/Qdrant, run repair/backfill/reindex, enter rollout, or create automatic tender-review conclusions.

## 2. Source Evidence

Phase 2.35c Codex C validation:

1. Session: `20260429_165301_e3c312`.
2. `@主标书` resolved document: `869d4684-0a98-4825-bc72-ada65c15cfc9`.
3. `@主标书` resolved version: `43558ba9-2813-42ff-b11b-3fbb4448a5bb`.
4. Formal Q1 / Q2: `alias_resolved`, `alias_missing=false`, `retrieval_suppressed=false`.
5. Evidence scope: only the main tender document.
6. Safety flags: `snapshot_as_answer=false`, `facts_as_answer=false`, `transcript_as_fact=false`.

Q1 result:

1. 工程名称: pass.
2. 工程地点: pass.
3. 建设单位: pass.
4. 代建单位: pass.
5. 工期: pass.
6. 最高投标限价 / 招标控制价 / 投标报价上限: Missing Evidence.

Q2 result:

1. 联合体: pass.
2. 项目经理 / 注册建造师 / B 证: partial.
3. 投标资质等级 / 类别: Missing Evidence.
4. 类似业绩: Missing Evidence.
5. 人员要求: Missing Evidence.

Trace result:

1. `metadata_snapshot_used=true`.
2. `metadata_snapshot_status=full_match`.
3. `metadata_guided_query_profile` contains expected pricing / qualification hints.
4. `metadata_deep_field_profile=null`.
5. `deep_field_profile=single_pass`.
6. `deep_field_section_hints=null`.

## 3. Gap Classification

Classification keys:

1. A: the real file may not contain the field, or the current sample has not exposed it; keep Missing Evidence.
2. B: section targeting / retrieval profile may be insufficient; plan section-targeted recall diagnostics.
3. C: trace mapping / display is insufficient; plan trace polish.
4. D: needs real terminal sampling or human confirmation before code changes.

| Field | Current result | Classification | Planning note |
| --- | --- | --- | --- |
| 最高投标限价 / 招标控制价 / 投标报价上限 | Missing Evidence; no fabricated amount | A + B + D | Keep Missing Evidence unless a concrete amount chunk is retrieved. Add diagnostics to prove whether 招标公告 / 投标人须知前附表 / 最高投标限价 sections were searched. |
| 投标资质等级 / 类别 | Missing Evidence for concrete level/category | A + B + D | Certificate-list chunks are not enough. Retrieval should target qualification review / bidder qualification / 投标人资格要求 sections, but no model should infer a level without evidence. |
| 项目经理等级 / B 证 | B 证 and registered constructor evidence found; level incomplete | B + D | Keep partial. Add diagnostics to distinguish 注册建造师证 / B 证 evidence from explicit level evidence. |
| 联合体 | Pass | D | Keep as validated. Future changes must not regress current pass. |
| 类似业绩 | Missing Evidence for amount / scale / year | A + B + D | Existing evidence appears to be form/ranking rules, not concrete requirement. Target 资格审查 / 评分办法 / 业绩要求 sections if present. |
| 人员数量 / 专业 / 证书 | Missing Evidence for concrete personnel details | A + B + D | Target 项目管理机构 / 人员配备 / 拟派人员 / 资格审查 sections. Keep Missing Evidence if only generic forms are found. |
| `metadata_deep_field_profile` | `null` in terminal trace | C | Retrieval layer has profile concepts, but terminal-visible trace does not reliably surface them. Needs trace/display polish before more recall changes are judged. |
| `deep_field_profile` | `single_pass` in terminal trace | C | This may be adapter/context flattening or route-level default display. Do not interpret it as retrieval quality failure without trace audit. |
| `deep_field_section_hints` | `null` | C | Terminal trace should show which section hints were applied or why none were applied. |

## 4. Phase 2.36a Minimum Boundary

Recommended Phase 2.36a: section-targeted retrieval diagnostics + trace polish.

Minimum implementation candidates:

1. Expose terminal-visible trace fields for:
   - `metadata_deep_field_profile`
   - `deep_field_profile`
   - `deep_field_section_hints`
   - `deep_field_query_aliases`
   - `deep_field_missing_reason`
2. Add diagnostics showing which section targets were attempted for pricing and qualification queries:
   - 招标公告
   - 投标人须知前附表
   - 投标人资格要求
   - 资格审查
   - 评分办法
   - 项目管理机构 / 人员配备
   - 最高投标限价 / 招标控制价
3. Add regression tests for trace surfacing, not answer generation.
4. Add targeted retrieval tests with fixture chunks that contain:
   - concrete price ceiling amount
   - concrete qualification level/category
   - project manager level + B cert
   - performance amount/scale/year
   - personnel quantity/specialty/certificate
5. Preserve Missing Evidence behavior when fixture chunks do not contain concrete values.

Implementation should be bounded to Hermes_memory retrieval trace / diagnostics unless investigation proves the missing fields are only blocked by Hermes main trace display.

## 5. Non-goals

Phase 2.36a must not:

1. Implement full automatic tender review.
2. Produce final bid qualification judgments without evidence.
3. Infer price ceiling, qualification levels, performance requirements, or personnel counts from nearby chunks.
4. Hide Missing Evidence.
5. Modify retrieval contract.
6. Modify memory kernel main architecture.
7. Write business DB / facts / document_versions.
8. Modify OpenSearch / Qdrant data.
9. Run repair / backfill / reindex / cleanup / delete.
10. Enter production rollout.

## 6. Validation Plan

Planning-level validation:

1. No code test required for this phase.
2. Review that this document keeps Phase 2.35c alias/session closure separate from deep-field recall status.
3. Review that each missing field remains Missing Evidence unless concrete source evidence exists.

Future Phase 2.36a validation:

1. Targeted unit tests for section-targeted trace fields.
2. Retrieval fixture tests for concrete vs non-concrete deep fields.
3. No real API / CLI smoke until Codex B approves implementation.
4. If implementation affects terminal-visible output, Codex C should rerun Q1/Q2.

## 7. Recommendation

Proceed to Phase 2.36a only after Codex B review.

Recommended Phase 2.36a scope:

1. Trace polish first.
2. Section-targeted retrieval diagnostics second.
3. Fixture-based concrete field tests third.

Do not expand into automatic tender review or production rollout.

## 8. Phase 2.36a Implementation Update

Phase 2.36a has now added retrieval-layer trace diagnostics in Hermes_memory only.

Implemented:

1. `snapshot_trace` keeps `metadata_intent_fields` even when no concrete snapshot field is matched.
2. `price_ceiling` and `qualification_requirement` now emit Missing Evidence reasons when concrete evidence gates are not satisfied:
   - `missing_concrete_price_amount`
   - `missing_concrete_qualification_level_or_category`
3. `RetrievalService.search()` top-level trace now stabilizes:
   - `metadata_deep_field_profile`
   - `deep_field_profile`
   - `deep_field_section_hints`
   - `deep_field_query_aliases`
   - `deep_field_missing_reason`
   - `deep_field_diagnostics`
4. `deep_field_diagnostics` includes:
   - `section_targets_attempted`
   - `query_aliases_used`
   - `boosted_phrases_used`
   - `concrete_evidence_required`
   - `concrete_evidence_required_fields`
   - `concrete_evidence_matched_fields`
   - `concrete_evidence_missing_fields`
   - `missing_reason`
5. Fixture tests cover:
   - concrete price ceiling amount.
   - placeholder price ceiling text that must remain Missing Evidence.
   - concrete qualification level + category.
   - generic certificate list that must remain Missing Evidence.

Validation:

```bash
uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py
uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py -q
```

Result:

```text
17 passed
```

No real API / CLI smoke was run in this implementation turn. If terminal output still shows `metadata_deep_field_profile=null` or `deep_field_profile=single_pass`, the next diagnosis should check Hermes main adapter / context rendering with Codex B authorization.

## 9. Phase 2.36b Main Trace Display Follow-up

Codex C terminal sampling after Phase 2.36a showed that Hermes_memory retrieval trace was correct at the API layer, but Hermes CLI output still did not expose the new deep-field diagnostics:

1. `metadata_deep_field_profile=null`.
2. `deep_field_profile=null`.
3. `deep_field_diagnostics=null`.
4. Q1 / Q2 `query_aliases` still displayed only the file alias, not pricing / qualification aliases.

Phase 2.36b therefore made a bounded Hermes main consumer-layer fix:

1. `HermesMemoryAdapter` now flattens deep-field trace fields from Hermes_memory retrieval trace:
   - `metadata_snapshot_status`
   - `metadata_guided_query_profile`
   - `metadata_deep_field_profile`
   - `deep_field_profile`
   - `deep_field_section_hints`
   - `deep_field_query_aliases`
   - `deep_field_missing_reason`
   - `deep_field_diagnostics`
2. `MemoryKernel._with_context_governance_trace` now promotes the same fields when they are nested under `retrieval_trace`.
3. `ContextBuilder` now renders a dedicated deep-field diagnostics block in the enterprise context.
4. The diagnostics block explicitly states that routing diagnostics do not replace retrieval evidence or Missing Evidence.
5. `SessionDocumentScopeStore` now recognizes:
   - `绑定为 @alias`
   - `绑定成 @alias`
   - Chinese curly quoted title syntax such as `锁定“标题”，并绑定为 @主标书`.

Validation:

```bash
./.venv/bin/python -m py_compile agent/memory_kernel/adapters/hermes_memory_adapter.py agent/memory_kernel/kernel.py agent/memory_kernel/context_builder.py agent/memory_kernel/session_document_scope.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py -q
```

Result:

```text
59 passed
```

No real API / CLI smoke was run in this implementation turn. Codex C should rerun the one-step binding prompt plus Q1 / Q2 terminal trace sampling before Phase 2.36b baseline.

## 10. Phase 2.36c Diagnostics / Answer Boundary Consistency

Codex C terminal sampling after Phase 2.36b confirmed that one-step alias binding and terminal-visible deep-field trace were visible, but found two semantic consistency issues:

1. Q1 pricing diagnostics could show concrete evidence found while the final answer still correctly returned Missing Evidence for the price ceiling amount.
2. Q2 could over-read an "一级注册建造师电子证书" material / format clause as if it were an explicit project manager level requirement.

Phase 2.36c keeps the implementation bounded to Hermes_memory retrieval diagnostics and tests.

Implemented:

1. Price ceiling concrete evidence now requires a price-field clause that contains a numeric amount with currency / unit.
2. Placeholder or reference-only clauses such as "详见附件", "按招标控制价执行", "不得超过招标控制价" without an amount remain Missing Evidence.
3. Deep-field diagnostics are rechecked against final retrieval evidence before the response trace is returned.
4. If metadata snapshot matches but final retrieval evidence does not contain concrete evidence, diagnostics now report:
   - `deep_field_missing_reason=missing_concrete_price_amount`
   - `concrete_evidence_present=false`
   - `diagnostic_consistency=metadata_anchor_without_final_concrete_evidence`
5. Project manager concrete evidence now requires an explicit role-level requirement such as "项目经理须具备一级注册建造师".
6. Electronic certificate / certificate material / format clauses do not count as explicit project manager level evidence.
7. Diagnostics can emit:
   - `project_manager_level_explicit=false`
   - `project_manager_level_missing_reason=electronic_certificate_format_is_not_role_level_requirement`

Validation:

```bash
UV_CACHE_DIR=.uv-cache uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py
UV_CACHE_DIR=.uv-cache uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q
```

Result:

```text
33 passed
```

The default `uv run ...` command could not use the user-level uv cache inside the current sandbox, so validation used `UV_CACHE_DIR=.uv-cache`. A direct `.venv/bin/python` fallback also produced the same target pytest result: `33 passed`.

No real API / CLI smoke was run in this implementation turn. Codex B should review Phase 2.36c before Codex C reruns Step 1 / Q1 / Q2 terminal sampling.

## 11. Phase 2.36c Review / Terminal Validation / Baseline

Phase 2.36c has passed Codex B review and Codex C real Hermes terminal validation.

Codex C validation evidence:

1. Session: `20260430_123308_6660a8`.
2. Step 1 one-turn alias binding passed:
   - `alias_resolution.status=alias_bound`
   - `resolved_document_id=869d4684-0a98-4825-bc72-ada65c15cfc9`
   - `resolved_version_id=43558ba9-2813-42ff-b11b-3fbb4448a5bb`
   - `alias_missing=false`
   - `retrieval_suppressed=false`
3. Q1 price-ceiling diagnostics and answer boundary are consistent:
   - final answer keeps Missing Evidence for highest bid limit / control price amount.
   - `deep_field_missing_reason=missing_concrete_price_amount`
   - `concrete_evidence_present=false`
   - `concrete_evidence_missing_fields=["price_ceiling"]`
4. Q2 project-manager level boundary passed:
   - `project_manager_level_explicit=false`
   - electronic certificate / certificate material / format clauses are not treated as explicit project manager level requirements.
5. Safety flags stayed stable:
   - `snapshot_as_answer=false`
   - `facts_as_answer=false`
   - `transcript_as_fact=false`
   - retrieval evidence stayed within the main tender document.

Remaining non-blocking tail items:

1. Deep-field recall is still partial.
2. Real price-ceiling amount, concrete qualification level / category, performance requirements, and personnel quantity still require further evidence or manual review.
3. Phase 2.36c must not be described as full automatic tender-review closure.
4. No rollout, repair, DB mutation, OpenSearch mutation, or Qdrant mutation is included in this baseline.
