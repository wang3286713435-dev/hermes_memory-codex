# Phase 2.38c Personnel Requirement Recall Tail Plan

## 1. Background

Phase 2.38b confirmed that `personnel_requirement` is not a source-missing problem.

The read-only diagnostics showed:

1. `personnel_requirement`: `candidate_present_but_low_rank`.
2. Known candidate chunks were retrievable, but ranked around 17, 19, and 41.
3. No retrieval ranking, retrieval contract, DB, OpenSearch, Qdrant, facts, or document version changes were made.

Phase 2.38c is planning-only. It turns this low-rank finding into a bounded implementation candidate.

## 2. Goal

Plan the personnel requirement recall tail without changing code.

The goal is to answer:

1. Whether current query wording is too broad.
2. Whether personnel-specific aliases are insufficient.
3. Whether section hints need to target personnel-related tender sections more directly.
4. Whether candidate pool diagnostics should be expanded before any ranking change.
5. Whether the next phase can be a personnel-only bounded implementation.

## 3. Diagnostic Conclusion

The current evidence suggests:

1. Personnel candidate chunks exist in the parsed/indexed corpus.
2. Current retrieval can find them, but not high enough for reliable answer use.
3. The likely issue is query/profile/candidate-pool behavior, not source availability.
4. This should not be treated as broad retrieval failure.

Known live preview result:

1. `personnel_requirement`: `candidate_present_but_low_rank`.
2. Candidate ranks observed: `17 / 19 / 41`.
3. This is below the current top-k answer window.

## 4. Candidate Implementation Boundary

If Codex B approves a follow-up implementation, Phase 2.38d should stay personnel-only.

Allowed candidate work:

1. Add personnel-specific query aliases such as:
   - `项目管理机构`
   - `人员配备`
   - `技术负责人`
   - `专职安全员`
   - `项目班子`
   - `主要管理人员`
   - `人员资格`
   - `人员要求`
2. Add personnel-specific section hints for:
   - `资格审查`
   - `投标人资格要求`
   - `项目管理机构`
   - `人员配备`
   - `主要人员`
   - `技术负责人`
   - `专职安全员`
3. Add diagnostics that compare:
   - baseline personnel query
   - personnel-expanded query aliases
   - section-hinted query profile
   - top-k and diagnostic-limit visibility
4. Keep the implementation bounded to `personnel_requirement`.
5. Preserve Missing Evidence and human-review semantics.

## 5. Non-goals

Phase 2.38c does not:

1. Fix `price_ceiling`.
2. Infer or fix `project_manager_level`.
3. Perform broad retrieval tuning.
4. Change ranking weights globally.
5. Change retrieval contract.
6. Change memory kernel main architecture.
7. Write DB, facts, document versions, OpenSearch, or Qdrant.
8. Execute repair, backfill, reindex, cleanup, or delete.
9. Produce automatic tender-review conclusions.
10. Enter rollout.

## 6. Go / No-Go

Go to Phase 2.38d only if the implementation stays bounded to personnel requirement recall.

Go conditions:

1. Personnel-specific aliases / section hints can be added without changing retrieval contract.
2. Candidate source visibility can be measured before and after the change.
3. The next phase keeps live preview and tests read-only except for code changes.
4. Codex C terminal validation is planned only after retrieval output changes.

No-Go conditions:

1. The fix requires broad ranking changes.
2. The fix requires index rebuild, DB mutation, repair, backfill, or reindex.
3. The fix requires source supplementation or manual business interpretation.
4. The fix tries to solve `price_ceiling` or `project_manager_level` in the same phase.
5. The fix claims full automatic tender-review capability.

## 7. Codex C Validation

Codex C validation is not needed for Phase 2.38c because this is planning-only.

If Phase 2.38d changes retrieval behavior, Codex C should re-run a targeted Q2 personnel requirement terminal check:

1. Bind `@主标书`.
2. Ask for personnel quantity / specialty / qualification requirements.
3. Confirm returned evidence is only from the main tender document.
4. Confirm personnel-specific candidate chunks appear in answer evidence.
5. Confirm no price ceiling or project manager level inference regression.

## 8. Recommendation

Recommend Phase 2.38d: personnel-only bounded recall implementation.

Do not proceed to broad retrieval tuning, repair, rollout, or automatic tender review.
