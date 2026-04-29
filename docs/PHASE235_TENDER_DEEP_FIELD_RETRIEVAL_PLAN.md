# Phase 2.35 Tender Deep Field Retrieval

## 1. Goal

Phase 2.35 is a diagnostic-first internal MVP recall improvement for Day-1 Pilot Q1/Q2.

It focuses on large tender deep-field evidence retrieval for:

1. 最高投标限价 / 招标控制价 / 投标报价上限.
2. 投标资质 / 资质等级.
3. 项目经理 / 注册建造师 / 安全生产考核 B 证.
4. 联合体.
5. 类似工程业绩.
6. 人员要求 / 人员配备.

This phase does not implement automatic bid review, automatic conclusions, production rollout, facts extraction, DB mutation, reindex, or repair.

## 2. Diagnosis

Before this phase, tender basic metadata covered engineering name, location, construction unit, delegate unit, duration, project number, and section info.

The weak spots were:

1. Price ceiling aliases were too narrow. Queries that said 招标控制价, 投标报价上限, 报价上限, or 控制价 could miss metadata guidance.
2. Qualification-style Day-1 Q2 fields had section boosts, but metadata snapshot did not provide explicit anchors for 联合体、业绩、人员要求.
3. Metadata-guided scope always collapsed to `tender_basic_info`, which could under-describe deep-field profiles in trace.
4. Retrieval diagnostics did not expose a stable `deep_field_profile` / section-hint view for Codex B or Codex C review.

## 3. Implementation

Implemented minimal retrieval-layer improvements in Hermes_memory only:

1. Extended tender metadata snapshot rules for:
   - `price_ceiling`
   - `qualification_requirement`
   - `project_manager_requirement`
   - `consortium_requirement`
   - `performance_requirement`
   - `personnel_requirement`
2. Added metadata-guided query profile selection:
   - `pricing_scope`
   - `qualification_scope`
   - `schedule_scope`
   - `tender_basic_info`
3. Extended section scope triggers and section hints for:
   - 招标控制价 / 最高投标限价 / 投标报价上限.
   - 联合体 / 业绩 / 人员要求 / 人员配备.
4. Added stronger sparse phrase boosts for price ceiling and qualification queries.
5. Added additive trace fields:
   - `deep_field_profile`
   - `deep_field_section_hints`
   - `deep_field_query_aliases`
   - `metadata_deep_field_profile`

Snapshot remains navigation-only:

1. `snapshot_as_answer=false`.
2. `evidence_required=true`.
3. Final answer must still use retrieval evidence.
4. Missing evidence must remain visible when no supporting chunk is retrieved.

## 4. Validation

Executed:

```bash
uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py
uv run pytest tests/test_tender_metadata_retrieval.py tests/test_retrieval_contract.py tests/test_phase235_tender_deep_field_retrieval.py -q
```

Result:

```text
22 passed
```

No API / live retrieval smoke was executed because `RetrievalService.search()` writes retrieval / audit logs, and Phase 2.35 explicitly avoids business DB writes.

## 4.1 Phase 2.35b Follow-up

Codex C terminal validation showed that the original Phase 2.35 implementation remained safe but partial:

1. Price ceiling remained Missing Evidence when no concrete amount was retrieved.
2. Qualification requirement did not surface a concrete qualification level / category.
3. Terminal trace displayed `deep_field_profile=single_pass`, so Codex B/C needed more direct retrieval-layer profile fields.
4. One first-session alias bind issue was observed once, but a second terminal session was stable.

Phase 2.35b made only bounded retrieval-layer adjustments:

1. Added top-level trace fields to `SearchResponse.trace`:
   - `metadata_snapshot_status`
   - `metadata_guided_query_profile`
   - `metadata_deep_field_profile`
2. Tightened `price_ceiling` metadata anchoring:
   - Strong metadata match now requires a concrete numeric amount with currency / unit evidence such as `人民币`, `元`, `万元`, `¥`, or `￥`.
   - Placeholder language such as “最高投标限价详见另行公示” no longer becomes a strong metadata match.
3. Tightened `qualification_requirement` metadata anchoring:
   - Strong metadata match now requires qualification level plus category evidence, such as `建筑工程施工总承包一级及以上资质`.
   - Certificate-list chunks without concrete level / category remain non-strong matches.
4. Alias first-bind instability was checked through Hermes main direct assertion diagnostics. Existing alias binding, persistence, same-turn retrieval fallback, and cross-store resolution paths passed; no main-repo code was changed.

Phase 2.35b validation:

```bash
uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py
uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py -q
uv run pytest tests/test_tender_metadata_retrieval.py tests/test_retrieval_contract.py tests/test_phase235_tender_deep_field_retrieval.py -q
git diff --check
```

Result:

```text
13 passed
26 passed
git diff --check passed
```

Hermes main `.venv` does not include pytest, so alias diagnostics used direct assertion calls against selected alias tests:

```text
alias direct assertion diagnostics passed: 10
```

## 4.2 Phase 2.35c Alias / Session Follow-up

Codex C later reproduced the alias blocker in real Hermes CLI:

1. Session `20260429_024717_785309` printed a successful `@主标书` bind result.
2. Formal Q1 / Q2 in the same session then returned `alias_missing=true` and `retrieval_suppressed=true`.
3. The target session had no `@主标书` entry in `get_hermes_home()/state/session_document_scope.json`.
4. The bind response referenced an older session id, indicating the model surfaced historical context instead of current session state.

Phase 2.35c made a bounded Hermes main fix:

1. Expanded current-document alias binding recognition for phrases such as `上一轮已锁定的当前文件`.
2. Such prompts now use active document binding when active state exists.
3. If no active state exists, they use current retrieval fallback and persist the alias from unique retrieval evidence.
4. Added direct assertions for cross-store resume and run_agent pre-resolved scope paths.

Validation:

```text
Hermes main py_compile: passed
Hermes main direct assertion tests: 6 passed
Hermes main pytest with addopts disabled: 48 passed
Hermes_memory Phase 2.35 targeted tests: 13 passed
```

This does not prove the real terminal flow yet. Codex C must re-run `@主标书` binding and Day-1 Q1 / Q2 before Phase 2.35c can baseline.

## 4.3 Phase 2.35c Codex C Validation

Codex C re-ran the real Hermes terminal validation in session `20260429_165301_e3c312`.

Alias / session result:

1. `@主标书` bind succeeded and persisted.
2. Formal Q1 / Q2 both returned `alias_resolved`.
3. `alias_missing=false` and `retrieval_suppressed=false` for both formal queries.
4. `retrieval_evidence_document_ids` contained only the main tender document `869d4684-0a98-4825-bc72-ada65c15cfc9`.

Q1 result:

1. 工程名称、工程地点、建设单位、代建单位、工期: pass.
2. 最高投标限价 / 招标控制价 / 投标报价上限: fail as Missing Evidence.
3. No fabricated amount was produced.

Q2 result:

1. 联合体: pass.
2. 项目经理 / 注册建造师 / B证: partial; certificate requirement was found but level remains incomplete.
3. 投标资质等级 / 类别: fail as Missing Evidence for concrete main tender level / category.
4. 类似业绩: fail as Missing Evidence for amount / scale / year requirements.
5. 人员要求: fail as Missing Evidence for count / specialty / qualification details.

Trace result:

1. `metadata_snapshot_used=true`.
2. `metadata_snapshot_status=full_match`.
3. `metadata_guided_query_profile` includes the expected pricing / qualification related fields.
4. `metadata_deep_field_profile=null` remains a trace / display tail item.
5. `deep_field_profile=single_pass` remains a trace / display tail item.
6. `snapshot_as_answer=false`, `facts_as_answer=false`, and `transcript_as_fact=false`.

Phase judgment:

1. Phase 2.35c alias/session fix is validated and may baseline.
2. Deep-field recall is not fully closed.
3. Missing Evidence behavior is correct and must not be hidden.
4. Follow-up should treat price ceiling amount, concrete qualification level / category, performance requirements, personnel requirements, and trace profile surfacing as separate tail items.

Baseline validation:

```text
Hermes_memory targeted regression: 26 passed
Hermes main session scope regression: 48 passed
git diff --check: passed in both repos
```

## 5. Expected Impact

Expected improvement:

1. Q1 should have stronger evidence anchoring for 最高投标限价 / 招标控制价 / 投标报价上限 if those chunks exist in the indexed tender.
2. Q2 should have stronger evidence anchoring for 投标资质、项目经理、联合体、业绩、人员要求.
3. Trace should make it easier to distinguish pricing / qualification deep-field routing from generic tender basic info.

Still not guaranteed:

1. If the target chunks do not contain recognizable source terms, Hermes must still output Missing Evidence.
2. If OCR / parsing omitted relevant text, this phase does not repair ingestion.
3. If query evidence is partial, business users must still perform manual review.

## 6. Next Step

Recommended next step:

1. Execute Phase 2.35c Git baseline for the bounded alias/session fix and Phase 2.35 retrieval work.
2. Baseline wording must state that deep-field recall remains partial.
3. Do not claim production rollout, automatic tender review, or full deep-field closure.
