# Phase 2.38d Personnel Requirement Recall Implementation

## 1. Scope

Phase 2.38d is a bounded implementation for one field only: `personnel_requirement`.

The goal is to improve visibility for known personnel requirement candidate chunks that were previously retrievable but low-ranked.

This phase does not fix price ceiling, project manager level, broad retrieval ranking, automatic tender review, repair, reindex, or rollout.

## 2. Changes

Implemented personnel-only recall improvements:

1. Added `personnel_scope` for personnel-focused queries.
2. Added stronger personnel-specific aliases and section hints:
   - `项目管理机构`
   - `人员配备`
   - `人员要求`
   - `主要人员`
   - `主要管理人员`
   - `项目班子`
   - `技术负责人`
   - `专职安全员`
   - `安全员`
   - `质量员`
   - `施工员`
   - `人员数量`
   - `人员专业`
   - `人员资质`
3. Kept broad qualification queries in `qualification_scope`.
4. Added diagnostics query expansion for `personnel_requirement`.
5. Added tests proving:
   - personnel-focused queries use `personnel_scope`;
   - personnel-focused queries do not retain broad qualification aliases / sections;
   - broad qualification queries are not hijacked by personnel scope;
   - personnel boosts are present;
   - price ceiling and project manager level fixed policies remain unchanged.

## 2.1 Review Fix

Codex B review found that the first implementation still allowed personnel-focused queries to merge broad `qualification_scope` aliases / sections.

Fixed:

1. `人员要求是什么？` stays in `personnel_scope`.
2. `项目人员数量、专业、职称或资质要求是什么？` stays in `personnel_scope`.
3. The above queries no longer include broad aliases such as `项目经理`、`项目负责人`、`注册建造师`、`安全考核证`、`联合体投标`、`类似工程业绩`.
4. The above queries no longer include broad sections such as `资信标`、`联合体投标`、`类似工程业绩`.
5. Broad mixed query `投标资质、项目经理、联合体、业绩、人员要求分别是什么？` remains `qualification_scope`.

## 2.2 Q1 Exclusion Intent Fix

Codex C terminal validation found one additional intent parsing edge case:

`项目人员数量、专业、职称或资质要求是什么？请只回答人员要求，不要回答投标资质、项目经理、联合体、业绩。`

The query asks for personnel only, but the negative / exclusion sentence contains broad qualification terms.

Fixed:

1. Negative / exclusion spans such as `不要回答...`、`不回答...`、`不要包含...`、`排除...` are ignored for personnel intent classification.
2. The Q1 query now remains `personnel_scope`.
3. Metadata field inference now returns only `personnel_requirement` for that Q1 query.
4. Broad mixed query remains `qualification_scope`.

## 2.3 Answer Boundary Fix

Codex C terminal validation showed that retrieval / trace were correct, but final answers still overreached:

1. Q1 still mentioned project manager / constructor content despite personnel-only scope.
2. Q2 inferred counts such as `每类1人` while also saying count evidence was missing.
3. Q3 mentioned `一级建造师` while also preserving Missing Evidence language.

Fixed in Hermes main repository context rendering:

1. `personnel_scope` now injects a `personnel_answer_boundary`.
2. The context block says personnel-only answers must not include project manager / project lead / registered constructor / B-certificate content unless explicitly requested.
3. The context block says not to infer counts such as each role/personnel category equals one person unless cited evidence explicitly states the count.
4. If count, profession, title, or qualification is not explicit, the answer should say Missing Evidence for that subfield.

## 2.4 Stronger Final Answer Guard

Codex C second terminal validation showed the first answer-boundary wording was still too soft:

1. Q1 personnel-only answer still listed `项目经理`.
2. Q2 still mentioned `项目经理`, `每个项目只能1个`, and `类似工程业绩`.
3. Q3 broad query was mostly correct, but the personnel subsection still overreached with implicit count wording.

Fixed in Hermes main repository context rendering:

1. `personnel_answer_boundary` is now a `STRICT PERSONNEL-ONLY FINAL ANSWER GUARD`.
2. Personnel-only answers explicitly forbid project manager / project lead / registered constructor / first-class constructor / B-certificate / safety assessment certificate / tender qualification / consortium / similar project performance.
3. The guard includes the Chinese forbidden terms: `项目经理 / 项目负责人 / 注册建造师 / 一级建造师 / B证 / 安全考核证 / 投标资质 / 联合体 / 类似工程业绩`.
4. If cited chunks mix personnel staffing with forbidden fields, the answer must extract only the personnel staffing part.
5. Role names must not be converted into implicit counts such as `每个项目只能1个`、`每类1人`、`至少各1名`.
6. Broad `qualification_scope` queries must not receive this personnel-only boundary.

## 2.5 Structured Answer Guard Lines

Codex C latest terminal validation still failed because the final answer included forbidden wording such as `项目经理` and `每个项目限1人`.

Fixed in Hermes main repository context rendering:

1. `personnel_scope` now renders `personnel_forbidden_answer_terms=[...]`.
2. `personnel_scope` now renders `personnel_count_inference_forbidden=true`.
3. `personnel_scope` now renders `ignore_non_personnel_content_in_mixed_chunks=true`.
4. Forbidden terms explicitly include `项目经理`、`项目负责人`、`注册建造师`、`一级建造师`、`B证`、`安全考核证`、`投标资质`、`联合体`、`类似工程业绩`.
5. Forbidden count inference examples explicitly include `每个项目限1人`、`每个项目只能1个`、`每类1人`、`至少各1名`.
6. Broad `qualification_scope` context must not render these personnel-only structured guard lines.

## 2.6 Safe Fallback Contract

Codex C third terminal validation showed the structured guard still did not reliably prevent personnel-only answers from outputting forbidden terms or inferred counts.

Fixed in Hermes main repository context rendering:

1. `personnel_scope` now renders `personnel_violation_if_answer_contains_forbidden_term=true`.
2. `personnel_scope` now renders `personnel_violation_if_answer_contains_inferred_count=true`.
3. `personnel_scope` now renders `personnel_safe_fallback_required_on_violation=true`.
4. `personnel_scope` now renders a fixed safe fallback template:
   - 数量: `Missing Evidence / 人工复核`
   - 专业: `Missing Evidence / 人工复核`
   - 职称: `Missing Evidence / 人工复核`
   - 资质: `Missing Evidence / 人工复核`
   - 证明材料: `Missing Evidence / 人工复核`
5. Forbidden count inference examples now also include `每个项目各1人`、`每项目1人`、`每项目各1人`、`每个岗位1人`、`各1人`.
6. If a draft answer contains forbidden terms or inferred counts, the context contract instructs the model to discard the draft and output only the safe fallback template.

Limitation:

1. The current Phase 2.38d whitelist did not allow editing `run_agent.py`.
2. In the current Hermes CLI flow, `MemoryKernel.finish_turn()` runs after the response is delivered and cannot replace the already streamed answer.
3. Therefore this round did not implement a true post-answer retry / replacement hook.
4. Real terminal validation is still required before baseline.

## 3. Guardrails

Unchanged:

1. Retrieval contract.
2. Memory kernel main architecture.
3. Global top-k.
4. Broad ranking weights.
5. DB / facts / document_versions.
6. OpenSearch / Qdrant data.
7. Repair / backfill / reindex / cleanup / delete.
8. Rollout.

`price_ceiling` remains Missing Evidence / source supplementation.

`project_manager_level` remains human-review-only.

## 4. Tests

Executed:

1. `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`
2. `uv run pytest tests/test_phase238d_personnel_recall_tail.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`
3. `uv run pytest tests/test_phase238d_personnel_recall_tail.py -q`
4. `git diff --check`

Results:

1. Targeted combined tests: `30 passed`.
2. New Phase 2.38d tests: `8 passed`.
3. `git diff --check`: passed.
4. Review-fix scope check: personnel-only queries no longer mix broad qualification aliases / sections.
5. Q1 exclusion intent check: negative broad terms no longer force `qualification_scope`.
6. Hermes main context builder targeted tests after structured guard: `12 passed`.
7. Hermes main context builder targeted tests after safe fallback contract: `12 passed`.

## 5. Live Preview

No DB-backed live preview was run.

Reason:

1. The existing diagnostics path calls `RetrievalService.search()`.
2. That path can write retrieval logs.
3. Phase 2.38d execution boundary disallows DB writes.

Instead, a `--skip-live --dry-run-preview` smoke was run for `personnel_requirement` to verify the expanded diagnostic payload shape without DB writes.

The smoke confirmed:

1. `personnel_expanded_query=true`.
2. Personnel aliases and section hints are surfaced.
3. `dry_run=true`.
4. `writes_db=false`.
5. `mutates_index=false`.
6. `destructive_actions=[]`.

## 6. Current Judgment

Implementation status: implemented; awaiting Codex B review of the structured answer guard.

Expected improvement:

1. Personnel-focused queries should now produce `personnel_scope`.
2. Personnel aliases / section hints should be visible in trace and diagnostics.
3. Known personnel candidate chunks have a more targeted path into the evidence window.

Still not proven:

1. Real terminal answer improvement.
2. Live DB/OpenSearch candidate rank improvement.
3. Whether the final model answer fully stops mixing project manager / registered constructor / qualification / consortium / performance / inferred count wording in personnel-only turns.

Codex C targeted terminal validation is recommended before baseline if Codex B approves the structured answer guard.

Additional caveat:

1. The current answer-boundary fix is still a context / prompt contract, not a runtime post-answer validator.
2. A true retry / replacement path would require a separately authorized main-repo answer pipeline change.

## 7. Next Step

Recommended next step:

1. Codex B review of the structured answer guard.
2. If approved, Codex C targeted Q1/Q2/Q3 terminal check, with attention to personnel-only answer wording.
3. Git baseline only after review / validation decision.

## 8. Runtime Post-answer Guard

Status: implemented; pending Codex B review and Codex C terminal validation.

Scope:

1. Hermes main repo only.
2. No Hermes_memory retrieval changes.
3. No retrieval contract changes.
4. No DB / OpenSearch / Qdrant / facts / document_versions mutation.

Implementation:

1. `run_agent.py` now calls `MemoryKernel.apply_personnel_answer_guard()` before final response persistence and return.
2. The guard only applies when the trace profile is `personnel_scope`, the user query is personnel-only, and the profile is not broad `qualification_scope`.
3. Forbidden personnel-only answer terms include project manager / constructor / B-certificate / qualification / consortium / performance wording.
4. Forbidden count inference includes phrases such as `每项目各1人`, `每类1人`, `各1人`, and equivalent regex-detected forms.
5. If the final answer violates the guard, Hermes replaces it with a conservative safe fallback that reports each personnel subfield as `Missing Evidence / 人工复核` and explicitly keeps `facts_as_answer=false` and `transcript_as_fact=false`.

Tests:

1. `.venv/bin/python -m py_compile run_agent.py agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py` passed.
2. `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py -q` passed: `65 passed`.

Current judgment:

1. Runtime guard is implemented and unit-covered.
2. Phase 2.38d is not baseline-ready until Codex B review and Codex C Q1/Q2/Q3 real terminal validation pass.
3. `price_ceiling`, `project_manager_level`, and broad retrieval tuning remain out of scope.
