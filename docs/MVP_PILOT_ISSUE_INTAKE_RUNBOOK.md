# MVP Pilot Issue Intake Runbook

## 1. Purpose

This runbook defines how internal MVP Pilot findings, Codex C terminal validation results, and user trial feedback are captured as local structured issue records.

The goal is to make feedback reviewable and repeatable before any fix is planned.

This runbook uses the Phase 2.37a dry-run tool:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --help
```

## 2. Non-goals

This runbook does not:

1. Fix issues.
2. Create Linear or GitHub issues automatically.
3. Write business DB records.
4. Modify facts, document_versions, OpenSearch, or Qdrant.
5. Execute repair, backfill, reindex, cleanup, or delete.
6. Enter rollout.
7. Produce automatic tender-review conclusions.
8. Change retrieval contract or memory kernel architecture.

## 3. Storage Convention

Save local Pilot issue records under:

```text
reports/pilot_issues/*.json
```

These files are local sensitive trial records and are ignored by Git by default.

Do not commit real Pilot issue JSON or Markdown records. Only commit the directory README and ignore policy.

## 4. Issue Record Template

Use this sanitized example as a starting point. Replace values with the actual finding, but do not add secrets or unrelated personal data.

```json
{
  "issue_id": "pilot-issue-YYYYMMDD-001",
  "source": "codex_c_terminal_validation",
  "source_phase": "Phase 2.37b",
  "reported_at": "2026-05-02T21:55:00+08:00",
  "reporter": "codex-c",
  "query": "围绕 @主标书 提取最高投标限价",
  "aliases": [
    "@主标书"
  ],
  "expected_behavior": "Return cited evidence for the requested field, or return Missing Evidence when the field is absent from retrieved evidence.",
  "actual_behavior": "Missing Evidence was returned because no concrete amount citation was found.",
  "document_ids": [
    "example-document-id"
  ],
  "version_ids": [
    "example-version-id"
  ],
  "citations": [],
  "trace_flags": {
    "snapshot_as_answer": false,
    "facts_as_answer": false,
    "transcript_as_fact": false,
    "retrieval_evidence_document_ids": [
      "example-document-id"
    ]
  },
  "issue_type": "retrieval_recall",
  "priority": "P1",
  "safety_boundary": [
    "missing_evidence",
    "evidence_required"
  ],
  "human_review_required": true,
  "suggested_next_action": "Keep as Missing Evidence and route to manual triage before any retrieval fix.",
  "status": "new",
  "notes": "Sanitized local sample. Do not treat this issue record as a repair request or rollout approval."
}
```

## 5. Commands

Print a template:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --print-template
```

Validate one issue record:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input reports/pilot_issues/example.json --strict
```

Validate and summarize all local issue records:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

## 6. Priority Rules

P0:

1. Fabricated answer presented as evidence-backed.
2. Facts or transcript replacing retrieval evidence.
3. Cross-document contamination in final evidence.
4. Permission or tenant leakage.
5. Automatic business, tender, legal, or repair decision beyond boundary.

P1:

1. Key field recall failure that blocks pilot use.
2. Trace contradicts answer boundary.
3. Alias / session failure that blocks retrieval.
4. Citation missing for a core answer.

P2:

1. Latency or long output that slows pilot use but does not corrupt evidence.
2. Display is confusing but trace / evidence remain safe.
3. Non-critical field remains partial.

P3:

1. Copy, prompt, or documentation polish.
2. Low-risk formatting issue.
3. Nice-to-have runbook enhancement.

## 7. Go / Pause Interpretation

The dry-run summary returns `go_pause_recommendation`:

1. `pause`: at least one P0 exists.
2. `continue_with_manual_review`: P0 is zero and at least one P1 exists.
3. `continue`: only P2 / P3 findings exist.

These are triage recommendations, not rollout approval.

## 8. PRD Alignment

Every issue record must preserve evidence and safety boundaries:

1. Keep document_id, version_id, citation, and trace flags when available.
2. Use Missing Evidence instead of inventing unsupported fields.
3. Mark human review when the issue affects business interpretation.
4. Never treat issue intake as automatic repair.
5. Never treat issue intake as automatic tender review.

## 9. BIM Relationship

BIM Data Steward is now recorded as a later PRD planning direction.

This runbook does not handle BIM asset catalog, BIM file governance, model parsing, online viewing, clash detection, or automatic quantity takeoff.

MVP Pilot issue intake remains focused on current Hermes_memory trial feedback and evidence-bound triage.
