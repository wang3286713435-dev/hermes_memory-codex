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

Current validation result:

1. `uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py` passed.
2. `uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q` passed with `10 passed`.
3. Live read-only dry-run was attempted with the target document/version and `--dry-run-preview`.
4. Local `.env` currently points to host `postgres`, which is not resolvable on this machine, so all fields returned `skipped_live_unavailable`.
5. No report file was written and no DB / OpenSearch / Qdrant mutation occurred.

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

## 6. Next Step

After Codex B review, use the audit result to decide the next bounded task:

1. If `concrete_source_found`: plan targeted retrieval recall diagnostics/fix for the field.
2. If `anchor_only` or `ambiguous`: keep Missing Evidence or require human review before any fix.
3. If `not_found`: treat as source/parse/index availability issue, not a ranking-only problem.
4. If `skipped_live_unavailable`: rerun read-only audit when local services are available.
