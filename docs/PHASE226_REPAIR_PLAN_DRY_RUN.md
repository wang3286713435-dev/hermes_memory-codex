# Phase 2.26 Repair Plan Dry-run

## 1. 本轮目标

Phase 2.26 先规划并实现 stale facts / 数据一致性修复工具 dry-run。

该工具只输出结构化 repair plan，不执行 repair，不修改 facts、document_versions、OpenSearch、Qdrant 或任何业务数据。

## 2. 当前背景

Phase 2.25a readiness audit 已收口：

1. commit：`5734e5dded5963e208fcf16c2c3bd3a9e9f456ad`。
2. tag：`phase-2.25a-readiness-audit-baseline`。
3. readiness audit runner 已能发现当前 warning：stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`。
4. 当前 readiness audit 仍是 dry-run，只诊断不修复。

用户裁决：

1. 下一阶段优先做 stale facts / 数据一致性修复工具 dry-run。
2. readiness audit 定期 smoke / 报告归档后置到 Phase 2.26b 或更后续阶段。

## 3. Phase 2.26a 推荐方向

推荐进入：

**Phase 2.26a：Repair Plan Dry-run。**

核心目标不是修复数据，而是生成结构化 repair plan，供人工审核。

该阶段必须回答：

1. 哪些实体存在 stale / missing / inconsistency。
2. 每个问题建议什么保守动作。
3. 该动作是否可执行。
4. 执行前需要哪些人工确认或后续工具。

## 4. Repair Plan 覆盖项

### 4.1 stale confirmed facts

检测：

1. confirmed fact 的 `source_version_id` 是否仍为 latest。
2. 若不是 latest，查找 `latest_version_id`。
3. 保留 source document / version / chunk 信息。

建议动作：

1. `keep_with_warning`：保留事实，但在展示和 Agent context 中继续提示 stale。
2. `revalidate_against_latest`：后续人工或工具对照 latest chunk 重新验证事实。
3. `mark_needs_review`：标记需要人工复核。
4. `reject_if_source_missing`：仅当 source document / version / chunk 缺失时作为候选动作。

默认策略：

1. `recommended_action` 偏保守。
2. 不自动迁移到 latest version。
3. 不自动确认新版本事实。
4. 不自动 reject 仍有来源的 stale fact。

### 4.2 source missing facts

检测：

1. fact 引用的 `source_document_id` 不存在。
2. fact 引用的 `source_version_id` 不存在。
3. fact 引用的 `source_chunk_id` 不存在。

建议动作：

1. `mark_needs_review`。
2. `reject_if_source_missing`。

默认策略：

1. 不自动删除 fact。
2. 不自动补 source。
3. 不自动 reject；只生成计划项。

### 4.3 version index inconsistency

检测：

1. DB 中 latest / superseded 与 OpenSearch payload 不一致。
2. DB 中 latest / superseded 与 Qdrant payload 不一致。
3. OpenSearch 或 Qdrant 缺失目标 version / chunk。

建议动作：

1. `reindex_version_payload`。
2. `rerun_dense_backfill`。

默认策略：

1. 只输出计划，不执行 reindex。
2. 不默认全库扫描。
3. 若后续实现执行型工具，必须要求显式 `document_id` / `version_id`。

### 4.4 duplicate / near-duplicate documents

本阶段只规划可检测方向，不要求 Phase 2.26a 实现复杂相似判断。

候选检测：

1. 同 title / source_type / document_type 的多个 document。
2. title normalized 后高度相似的 document。
3. file_hash / content_hash 重复但 document_id 不同。

建议动作：

1. `report_duplicate_candidates`。
2. `manual_merge_review`。

默认策略：

1. 不自动合并。
2. 不自动删除。
3. 不自动迁移 alias / facts。

### 4.5 audit gap

要求：

1. repair plan 若涉及 facts，必须声明未来执行时需要写 audit。
2. 本阶段 dry-run 不写 fact mutation audit。
3. 是否写 read-only audit 作为后续评审项，不在 Phase 2.26a 强制实现。

## 5. Phase 2.26a 最小实现边界

建议新增只读脚本：

`scripts/phase226_repair_plan_dry_run.py`

建议新增测试：

`tests/test_phase226_repair_plan_dry_run.py`

CLI 最小参数：

1. `--json`。
2. `--document-id` 可重复，用于限定 version / index 诊断范围。
3. `--fact-id` 可重复，用于限定 facts 诊断范围。
4. `--include-index-checks`，默认关闭，只做 OpenSearch / Qdrant 只读检查。
5. `--fail-on-critical`，若存在 critical plan item 则非零退出。
6. `--limit-facts` / `--limit-documents`，限制默认扫描范围。

默认行为：

1. 只读。
2. 不执行任何修复。
3. 不写 audit。
4. 不生成 migration。
5. 不默认全库 index 修复。

## 6. JSON 输出结构

Phase 2.26a runner 应输出：

```json
{
  "dry_run": true,
  "destructive_actions": [],
  "repair_plan_id": "phase226-...",
  "generated_at": "...",
  "summary": {
    "stale_facts": 0,
    "missing_sources": 0,
    "index_inconsistencies": 0,
    "warnings": 0,
    "failures": 0
  },
  "items": [
    {
      "item_type": "stale_fact",
      "severity": "warning",
      "entity_type": "fact",
      "entity_id": "...",
      "source_document_id": "...",
      "source_version_id": "...",
      "latest_version_id": "...",
      "issue": "source_version_is_not_latest",
      "recommended_action": "revalidate_against_latest",
      "reason": "confirmed fact points to superseded source version",
      "executable": false
    }
  ],
  "next_steps": []
}
```

硬性要求：

1. `dry_run` 必须恒为 `true`。
2. `destructive_actions` 必须恒为空数组。
3. 所有 `items[].executable` 在 Phase 2.26a 必须为 `false`。

## 7. 推荐判定策略

### 7.1 severity

建议分级：

1. `info`：仅提示，例如 duplicate candidate。
2. `warning`：需要人工复核，例如 stale confirmed fact。
3. `critical`：source missing、版本状态异常或 index latest 泄露，有潜在错误召回风险。

### 7.2 recommended_action

允许值建议：

1. `keep_with_warning`。
2. `revalidate_against_latest`。
3. `mark_needs_review`。
4. `reject_if_source_missing`。
5. `reindex_version_payload`。
6. `rerun_dense_backfill`。
7. `report_duplicate_candidates`。
8. `manual_merge_review`。

默认推荐：

1. stale confirmed fact：`revalidate_against_latest` 或 `keep_with_warning`。
2. source missing fact：`mark_needs_review`，严重时建议 `reject_if_source_missing`。
3. OpenSearch old latest leak：`reindex_version_payload`。
4. Qdrant missing dense payload：`rerun_dense_backfill`。
5. duplicate candidate：`manual_merge_review`。

## 8. 测试规划

Phase 2.26a 应至少测试：

1. stale confirmed fact 生成 plan item。
2. missing source document / version / chunk 生成 high severity item。
3. OpenSearch / Qdrant inconsistency 只生成 plan，不执行。
4. `destructive_actions=[]`。
5. `dry_run=true`。
6. `items[].executable=false`。
7. recommended_action 采用保守值。
8. `--fact-id` / `--document-id` 能限定范围。

测试应优先使用 fake repository / fake result，不依赖真实 DB。

## 9. 硬边界

Phase 2.26a 不做：

1. 修改 facts。
2. 修改 document_versions。
3. 修改 OpenSearch。
4. 修改 Qdrant。
5. 删除任何数据。
6. 自动确认 facts。
7. 执行 repair。
8. rollout。
9. retrieval contract 修改。
10. memory kernel 主架构修改。

## 10. 后置 TODO

后置到 Phase 2.26b 或更后续：

1. readiness audit 定期 smoke / 报告归档。
2. repair plan 人工审核工作流。
3. repair plan 执行型工具设计。
4. read-only audit 是否记录 repair plan generation。
5. duplicate / near-duplicate document 更复杂相似判断。

自动 repair 只有在 repair plan dry-run 稳定，并经过人工确认后才允许规划；当前不得进入。

## 11. 当前结论

Phase 2.26a 最小实现已完成。

Phase 2.26a 的唯一目标是生成可审阅、不可执行、无破坏动作的 repair plan dry-run。

当前不建议进入自动 repair、生产 rollout、facts 自动抽取或更深 Agent reasoning。

## 12. Phase 2.26a 实现结果

新增：

1. `scripts/phase226_repair_plan_dry_run.py`。
2. `tests/test_phase226_repair_plan_dry_run.py`。

已实现诊断项：

1. stale confirmed facts：confirmed fact 指向 superseded source version 时生成 `stale_fact` plan item。
2. source missing facts：source document / version / chunk 缺失时生成 `missing_source` plan item。
3. version governance inconsistency：0 个 latest、多个 latest、superseded 仍 active/latest 时生成 `version_inconsistency` plan item。
4. index consistency plan：在显式 `--include-index-checks` 下只读检查 OpenSearch / Qdrant，生成 `index_inconsistency` 或 `service_warning`。

JSON invariant：

1. `dry_run=true`。
2. `destructive_actions=[]`。
3. `executable=false`。
4. 所有 `items[].executable=false`。

验证结果：

1. `uv run python -m py_compile scripts/phase226_repair_plan_dry_run.py`：通过。
2. `uv run pytest tests/test_phase226_repair_plan_dry_run.py -q`：`6 passed`。
3. 127.0.0.1 覆写环境 live dry-run：`status=warn`，`items_total=1`，`warnings=1`，`critical=0`，`failures=0`。
4. 已检出 stale fact `9f98384b-5053-4a8f-9b83-35983b28b38e`，`latest_version_id=76ca95a1-393f-4278-b254-ab66295bb14f`。

当前唯一 warning 是已知 stale confirmed fact；本轮未执行任何 repair / backfill / reindex。
