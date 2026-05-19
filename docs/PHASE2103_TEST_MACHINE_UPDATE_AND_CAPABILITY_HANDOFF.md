# Phase 2.103 Test Machine Update + Hermes Capability Maximization Handoff

## Purpose

Phase 2.103 provides a docs-only operational handoff after the Phase 2.102b metric scoring pack baseline.

It has two goals:

1. Give test-machine Codex a safe prompt to update Hermes Memory to `phase-2.102b-metric-scoring-pack-baseline`.
2. Give the database / platform team a clear explanation of Hermes' current capability boundary.

This phase does not modify runtime behavior.

## Current Baseline

Phase 2.102b baseline:

1. commit: `5c37661`
2. tag: `phase-2.102b-metric-scoring-pack-baseline`
3. pushed: true

Phase 2.102b adds offline metric scoring machinery:

1. `scripts/phase2102b_metric_scoring_pack.py`
2. `tests/test_phase2102b_metric_scoring_pack.py`
3. `docs/PHASE2102B_METRIC_SCORING_PACK.md`

The scorer is local/offline only. It does not run Hermes runtime, Gateway, DB, NAS, parser, writer, repair, or rollout paths.

## Why Test Machine Update Is Safe

The test machine can update from Phase 2.102a to Phase 2.102b because this baseline adds documentation, eval inventory scoring machinery, and target tests only.

Safe validation is limited to:

1. checkout/tag verification
2. required file existence checks
3. `py_compile` for the scorer script
4. target pytest for the scorer test
5. manifest JSON parse

The update prompt explicitly forbids:

1. service restart unless separately authorized
2. API / CLI / Gateway / DB / NAS smoke
3. DB / NAS / OpenSearch / Qdrant / MinIO connections
4. secret output
5. parser / scratch copy / writer / repair / backfill / reindex / rollout

## Hermes Capability Positioning

Hermes should be described as:

```text
Hermes = Evidence-first enterprise memory kernel + permission-aware catalog agent.
```

Hermes should not be described as:

```text
generic chatbot
raw DB agent
SQL generator
NAS file reader
DWG/RVT/BIM content-understanding agent
production rollout system
```

## Official Slogan

```text
Hermes：证据先行，权限闭环；让企业数据可问、可信、可控。
```

Engineering motto:

```text
先目录，后正文；先证据，后智能；先受控，后自动化。
```

## What Platform Can Safely Rely On Today

Current read-only platform integration may safely rely on:

1. read-only catalog search through Gateway / Catalog Tool
2. safe file and model identifiers
3. `query_id` / `trace_id`
4. permission-aware responses controlled by Gateway
5. Missing Evidence answers when content evidence is unavailable
6. low-sensitive related-file memory references for continuity, not as content evidence
7. user feedback labels for later controlled review
8. frontend "Ask Hermes" entry points that call safe Gateway endpoints

Gateway must own:

1. auth
2. project scope
3. permission decision
4. path redaction
5. forbidden-field scan
6. query trace / audit trace

## Current Memory Boundary

Hermes may remember only low-sensitive context such as:

1. `related_file_ids`
2. `related_model_ids`
3. `query_id`
4. `trace_id`
5. user feedback labels
6. low-sensitive preferences

Low-sensitive memory references are not content evidence. `related_file_ids` do not mean Hermes has read, parsed, indexed, or remembered file contents.

Content-level answers require separately governed retrieval, full-text, parser, or component evidence. Current platform integration remains catalog-only unless a later phase explicitly enables governed evidence retrieval.

Hermes must not store:

1. raw `storage_path`
2. raw DB rows
3. NAS raw paths
4. DWG/RVT content
5. PDF / Office正文
6. customer-sensitive content
7. secrets, tokens, credentials, or `.env` values

## Remaining Phase 2 Blockers

Phase 2 closeout readiness remains false.

Still blocked:

1. PRD 100+ eval cases
2. Roadmap 300+ eval cases
3. reviewed result JSON for the inventory
4. Top5 / citation scoring using real reviewed results
5. structured fact manual spot-check

Phase 2.102b provides scoring machinery, not final score evidence.

## Why Phase 3 / Production Rollout Remains Blocked

The following capabilities remain future or separately gated:

1. DWG/RVT content understanding
2. BIM component search
3. NAS semantic index
4. Agent DB CRUD
5. Agent-generated SQL
6. Data Steward productization
7. production rollout
8. repair / reindex / migration flows

Phase 2.103 does not authorize any of those items.
