# Phase 2.61 Internal MVP Operator Flow / Issue Intake Plan

## 1. Goal

Phase 2.61 defines the operator flow and issue intake process for internal controlled MVP usage on Mac mini.

This phase is docs-only planning. It does not upload files, run API or CLI smoke, write DB or index state, execute repair, activate Data Steward, or enter production rollout.

The purpose is to make real-use issues observable, triageable, and easy to hand back to Codex A / B / C without relying on long chat transcripts.

## 2. Entry Gate

Before any internal controlled MVP session, the operator should run the Phase 2.60 readiness runner:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py --skip-api-health
```

If API health should be checked and the service is already running:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py \
  --api-url http://127.0.0.1:8000
```

Only `status=go` should allow internal controlled usage to proceed.

`go` means the local internal MVP gate is acceptable for supervised use. It does not mean production rollout, Data Steward readiness, automatic tender review, automatic repair, or authorization to upload arbitrary files.

## 3. Operator Flow

### 3.1 Before Use

1. Confirm the operator, date, machine, and session id.
2. Confirm Hermes_memory API health if the use case requires live retrieval.
3. Confirm Hermes CLI availability.
4. Confirm no cleanup, delete, repair, backfill, reindex, migration, or rollout is authorized.
5. Confirm the target files or aliases to be used.
6. Run Phase 2.60 readiness and record the result.

### 3.2 During Use

For each meaningful query, the operator should record:

1. query text or sanitized query summary.
2. target file / alias / document_id if known.
3. session_id.
4. expected business field or task.
5. returned document_ids.
6. evidence / citation status.
7. Missing Evidence status.
8. safety flags:
   - `facts_as_answer`
   - `snapshot_as_answer`
   - `metadata_as_answer`
   - `transcript_as_fact`
9. third-document contamination status.
10. operator judgement:
    - correct
    - partial
    - wrong
    - needs human review

### 3.3 After Use

1. Summarize issue counts by severity.
2. Save sanitized local issue records under an ignored report path.
3. Escalate P0 immediately.
4. Hand P1/P2/P3 items to Codex B for route decision.
5. Do not run repair, cleanup, delete, backfill, reindex, or rollout as part of issue intake.

## 4. Issue Intake Fields

Recommended local issue record fields:

```json
{
  "issue_id": "",
  "created_at": "",
  "operator": "",
  "session_id": "",
  "severity": "P0|P1|P2|P3",
  "query": "",
  "target_alias": "",
  "target_document_id": "",
  "target_version_id": "",
  "expected_behavior": "",
  "actual_behavior": "",
  "returned_document_ids": [],
  "evidence_chunk_ids": [],
  "citation_present": false,
  "missing_evidence": false,
  "third_document_contamination": false,
  "facts_as_answer": false,
  "snapshot_as_answer": false,
  "metadata_as_answer": false,
  "transcript_as_fact": false,
  "operator_judgement": "",
  "recommended_owner": "Codex A|Codex B|Codex C|Codex D|human",
  "notes": ""
}
```

Issue records may contain sensitive business context, so real records should be ignored by Git by default.

## 5. Severity Rules

### 5.1 P0

Immediate stop and escalation.

Examples:

1. facts replace retrieval evidence.
2. transcript or metadata is treated as confirmed evidence.
3. third-document contamination appears in a scoped answer.
4. wrong citation is presented as source proof.
5. automatic decision, automatic bid, automatic tender judgement, or automatic repair is attempted.
6. DB / facts / versions / OpenSearch / Qdrant write occurs outside authorized phase.
7. cleanup, delete, repair, backfill, reindex, or rollout is attempted without explicit authorization.

### 5.2 P1

Blocks stable internal MVP usage until triaged.

Examples:

1. alias or session state is unstable.
2. key citation is missing for a business-critical answer.
3. deep tender field answer is high-risk wrong or overconfident.
4. document scope is wrong even if no third file appears.
5. version / stale-source diagnostics are missing for a version-sensitive issue.

### 5.3 P2

Usability or quality issue that does not immediately break safety.

Examples:

1. display is incomplete but evidence is correct.
2. trace field is not explicit enough.
3. latency is acceptable but slow.
4. answer is cautious but too verbose.
5. Missing Evidence wording is unclear.

### 5.4 P3

Small polish item.

Examples:

1. formatting issue.
2. minor wording problem.
3. ordering or layout issue.
4. optional operator convenience improvement.

## 6. Codex Roles

### 6.1 Codex A

Codex A implements bounded fixes, dry-run runners, templates, and docs after Codex B route decision.

Codex A must not auto-expand from issue intake into repair, rollout, DB/NAS/Data Steward, or automatic business decision features.

### 6.2 Codex B

Codex B reviews issue records, classifies route, writes the next bounded prompt, and decides whether Codex C validation is required.

Codex B should identify whether an issue is:

1. implementation bug.
2. retrieval quality tail.
3. display / trace tail.
4. operator misuse.
5. out-of-scope request.

### 6.3 Codex C

Codex C performs explicitly authorized real terminal rechecks.

Codex C should not repair data or implement features unless separately instructed.

### 6.4 Codex D

Codex D may perform drift audit and cross-file consistency review.

Codex D should not block mainline unless it finds a blocker such as safety regression, untracked data mutation, or phase-boundary drift.

## 7. Phase 2.61a Candidate

Recommended next implementation candidate:

Phase 2.61a: local issue intake runner / template.

Minimum boundary:

1. generate an ignored issue template.
2. validate local issue JSON.
3. summarize P0/P1/P2/P3 counts.
4. flag unsafe fields.
5. produce dry-run output only.

Non-goals for 2.61a:

1. no DB write.
2. no external issue creation.
3. no Linear automation.
4. no repair executor.
5. no production rollout.
6. no automatic business conclusion.

## 8. Phase 2.61a Implementation

Phase 2.61a adds a read-only local issue intake helper:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py --new-template
```

To write a template to an explicit local path:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --new-template \
  --output-json /tmp/hermes_issue_template.json
```

To validate and summarize an issue record:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --input-json /tmp/hermes_issue.json
```

The helper accepts either a single issue object or an object with `issues: []`.

The summary always includes:

1. `dry_run=true`.
2. `read_only=true`.
3. `destructive_actions=[]`.
4. `db_or_index_written=false`.
5. `external_issue_created=false`.
6. `repair_attempted=false`.
7. `production_rollout=false`.
8. `status=ready|pause|no_go`.
9. P0/P1/P2/P3 counts.
10. validation errors and operator next steps.

Status mapping:

1. P0 or any dangerous field is `no_go`.
2. P1 is `pause`.
3. Invalid severity or missing `operator_judgement` is `pause`.
4. Valid P2/P3-only records are `ready`.

Dangerous fields include:

1. `facts_as_answer=true`.
2. `snapshot_as_answer=true`.
3. `metadata_as_answer=true`.
4. `transcript_as_fact=true`.
5. `third_document_contamination=true`.
6. `repair_attempted=true`.
7. `db_or_index_written=true`.
8. `production_rollout=true`.

The helper does not write DB, create external issues, repair data, upload files, run API/CLI smoke, or choose a persistent report path unless the operator explicitly supplies `--output-json`.

## 9. Non-Goals

Phase 2.61 does not implement:

1. production rollout.
2. automatic tender review.
3. automatic bid or business decision.
4. DB / NAS / Data Steward / BIM / TB file pool.
5. repair, cleanup, delete, backfill, reindex, or migration.
6. real upload.
7. API / CLI smoke.
8. facts auto-extraction.
9. facts replacing retrieval evidence.
10. retrieval contract changes.
11. memory kernel architecture changes.

## 10. Current Recommendation

Phase 2.61 should not block internal controlled MVP usage if Phase 2.60 readiness is `go`.

It should improve how issues from internal use are recorded, triaged, and returned to Codex A/B/C for bounded follow-up.

Current Phase 2.61a implementation is complete and awaiting Codex B review. If accepted, the next step is a selective Git baseline prompt or a follow-up planning prompt for local issue storage policy.
