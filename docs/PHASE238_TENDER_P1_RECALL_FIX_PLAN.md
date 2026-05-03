# Phase 2.38 Tender P1 Recall Fix Plan

## 1. Goal

Phase 2.38 starts from MVP Pilot P1 quality issues in the main tender document.

The first step, Phase 2.38a, is a read-only source availability audit. It determines whether the fields that failed during terminal validation are present in parsed chunks, only present as anchors/placeholders, absent from visible chunks, or ambiguous.

This phase does not fix retrieval ranking and does not change business data.

## 2. Target Scope

Target document:

- `document_id`: `869d4684-0a98-4825-bc72-ada65c15cfc9`
- `version_id`: `43558ba9-2813-42ff-b11b-3fbb4448a5bb`
- alias: `@主标书`

Fields:

1. `price_ceiling`: 最高投标限价 / 招标控制价 / 投标报价上限。
2. `qualification_grade_category`: 投标资质具体等级 + 类别。
3. `project_manager_level`: 项目经理等级；电子证书格式要求不得误判为等级要求。
4. `performance_requirement`: 类似业绩数量 / 金额 / 年限 / 规模门槛。
5. `personnel_requirement`: 人员数量 / 专业 / 资质。

## 3. Audit Status Semantics

Each field returns one of:

1. `concrete_source_found`: parsed chunks contain hard evidence such as amount, level/category, count, year, scale, or explicit qualification.
2. `anchor_only`: only headings, placeholders, material requirements, or generic anchors were found.
3. `not_found`: no related source evidence was found in visible chunks.
4. `ambiguous`: related text exists but is insufficient for a safe field conclusion.
5. `skipped_live_unavailable`: local DB/OpenSearch was unavailable, so live read-only diagnosis was skipped.

## 4. Phase 2.38a Implementation

Implemented runner:

```bash
uv run python scripts/phase238a_tender_p1_source_audit.py \
  --document-id 869d4684-0a98-4825-bc72-ada65c15cfc9 \
  --version-id 43558ba9-2813-42ff-b11b-3fbb4448a5bb \
  --field all \
  --dry-run-preview
```

The runner:

1. Keeps `dry_run=true`, `read_only=true`, `destructive_actions=[]`, `writes_db=false`, `mutates_index=false`, `repairs_issue=false`, and `rollout_approved=false`.
2. Reads local DB chunks only when live audit is available.
3. Supports `--skip-live` for fixture/static validation without DB/OpenSearch.
4. Writes local reports only under ignored `reports/tender_p1_audit/` when not in preview mode.

Validation:

1. `uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py`
2. `uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q`
3. `git diff --check`

Phase 2.38a baseline result:

1. `uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py` passed.
2. `uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q` passed with `10 passed`.
3. Git baseline completed with commit `456b32d` and tag `phase-2.38a-tender-p1-source-audit-baseline`.
4. The first live read-only dry-run was attempted with the target document/version and `--dry-run-preview`.
5. The first local `.env` run pointed to host `postgres`, which was not resolvable on this machine, so all fields returned `skipped_live_unavailable`.
6. Codex B later reran read-only live audit with localhost host overrides. No report file was written and no DB / OpenSearch / Qdrant mutation occurred.
7. The localhost read-only audit found:
   - `price_ceiling`: `anchor_only`
   - `qualification_grade_category`: `concrete_source_found`
   - `project_manager_level`: `ambiguous`
   - `performance_requirement`: `concrete_source_found`
   - `personnel_requirement`: `concrete_source_found`

## 5. Non-goals

Phase 2.38a does not:

1. Modify retrieval logic or ranking.
2. Modify ingestion, indexing, facts, document versions, OpenSearch, or Qdrant.
3. Execute repair, backfill, reindex, cleanup, or delete.
4. Run Hermes CLI answer smoke.
5. Create external issues.
6. Produce automatic tender-review conclusions.
7. Enter production rollout.
8. Modify retrieval contract or memory kernel main architecture.

## 6. Phase 2.38b Direction

Phase 2.38b should not directly fix retrieval ranking. It should first diagnose whether known concrete source candidate chunks are visible to current retrieval.

Field policy:

1. `price_ceiling`: preserve Missing Evidence; Phase 2.38a only found anchors/placeholders, not a concrete amount.
2. `project_manager_level`: require human review; Phase 2.38a found ambiguous related text and must not infer a level from electronic certificate format clauses.
3. `qualification_grade_category`, `performance_requirement`, and `personnel_requirement`: run read-only retrieval candidate visibility diagnostics.

Allowed next diagnostic statuses:

1. `candidate_in_top_k`
2. `candidate_present_but_low_rank`
3. `candidate_absent_from_retrieval`
4. `field_should_remain_missing_evidence`
5. `field_requires_human_review`
6. `skipped_live_unavailable`

## 7. Phase 2.38b Implementation

Implemented runner:

```bash
uv run python scripts/phase238b_tender_concrete_recall_diagnostics.py \
  --document-id 869d4684-0a98-4825-bc72-ada65c15cfc9 \
  --version-id 43558ba9-2813-42ff-b11b-3fbb4448a5bb \
  --dry-run-preview
```

The runner:

1. Keeps `dry_run=true`, `read_only=true`, `destructive_actions=[]`, `writes_db=false`, `mutates_index=false`, `repairs_issue=false`, and `rollout_approved=false`.
2. Does not modify retrieval ranking or query profile.
3. Does not write DB, facts, document versions, OpenSearch, or Qdrant.
4. Writes local reports only under ignored `reports/tender_recall_diagnostics/` when not in preview mode.

Validation:

1. `uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py` passed.
2. `uv run pytest tests/test_phase238b_tender_concrete_recall_diagnostics.py -q` passed with `9 passed`.
3. `git diff --check` passed.

Read-only live preview with localhost service overrides:

1. `price_ceiling`: `field_should_remain_missing_evidence`; Phase 2.38a found only anchor-only source availability.
2. `qualification_grade_category`: `candidate_in_top_k`; candidate chunk `b5a34baa-2b01-44c3-aa44-3dbcefd6cde4` ranked 2.
3. `project_manager_level`: `field_requires_human_review`; ambiguous source must not be converted into inferred grade.
4. `performance_requirement`: `candidate_in_top_k`; candidate chunk `03ce871a-e1b6-4bab-9a1d-266711827146` ranked 1.
5. `personnel_requirement`: `candidate_present_but_low_rank`; candidate chunks appeared at ranks 17, 19, and 41.

Phase 2.38b conclusion:

1. Qualification and performance candidate sources are already visible in top-k.
2. Personnel requirement candidate sources are retrievable but low-ranked.
3. Price ceiling remains Missing Evidence / source supplementation territory.
4. Project manager level remains human-review territory.
5. The next bounded fix, if approved, should focus on personnel requirement query/profile diagnostics rather than broad retrieval tuning.
