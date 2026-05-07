# Phase 2.45d Mac mini Real-machine Deployment Record Plan

## 1. Goal and Non-goals

Phase 2.45d plans a future Mac mini real-machine deployment record and operator sign-off workflow.

The goal is to define how a human operator records the real-machine deployment process, attached evidence, stop conditions, and Go / Pause / No-Go result after the Mac mini environment is physically available.

This phase does not execute deployment.

Non-goals:

1. no real Mac mini deployment.
2. no automatic deployment script.
3. no service restart.
4. no migration execution.
5. no repair, cleanup, backfill, reindex, or delete.
6. no DB / facts / document_versions / audit_logs / OpenSearch / Qdrant writes.
7. no API / CLI smoke execution.
8. no production rollout approval.
9. no Data Steward / BIM implementation.
10. no retrieval contract or memory kernel architecture changes.

## 2. Record Inputs

Future deployment record input should be filled by a human operator.

Required input fields:

1. selected Hermes_memory commit and tag.
2. selected Hermes main commit and tag.
3. Mac mini hostname.
4. Mac mini LAN IP.
5. operator name.
6. operation timestamp.
7. NAS mount path, if used.
8. external SSD path, if configured.
9. `.env` key-name checklist without values.
10. Phase 2.45c health-check dry-run JSON path, if manually run.
11. MVP smoke result path, only if a later phase explicitly authorizes human-run smoke.
12. known dirty files, if any.
13. stop conditions triggered, if any.

Secret values must not be copied into the record.

## 3. Record Output Schema

Future sanitized record output should be JSON or Markdown and local ignored by default.

Suggested JSON fields:

```json
{
  "record_type": "mac_mini_deployment_record",
  "deployment_executed_by_human": true,
  "codex_executed_deployment": false,
  "production_rollout_approved": false,
  "hermes_memory_commit": "",
  "hermes_memory_tag": "",
  "hermes_main_commit": "",
  "hermes_main_tag": "",
  "hostname": "",
  "lan_ip": "",
  "operator": "",
  "recorded_at": "",
  "dry_run_evidence_path": "",
  "mvp_smoke_result_path": "",
  "go_pause_no_go": "go|pause|no_go|not_evaluated",
  "operator_signoff": {
    "signed_by": "",
    "signed_at": "",
    "decision": "",
    "notes": ""
  },
  "stop_conditions_triggered": [],
  "human_actions_required": []
}
```

The record must keep `codex_executed_deployment=false` unless a later explicitly authorized phase changes the process.

## 4. Operator Checklist

Human operator checklist:

1. confirm physical Mac mini setup.
2. confirm selected Hermes_memory Git ref.
3. confirm selected Hermes main Git ref.
4. confirm `.env` file exists without exposing secret values.
5. confirm NAS mount is reachable if required.
6. confirm external SSD is reachable if configured.
7. confirm Postgres is reachable by a human-run read-only check.
8. confirm OpenSearch is reachable by a human-run read-only check.
9. confirm Qdrant is reachable by a human-run read-only check.
10. confirm `QDRANT_COLLECTION` matches the expected collection.
11. optionally attach Phase 2.45c health-check dry-run JSON.
12. run MVP smoke only if a later phase explicitly authorizes it.
13. record Go / Pause / No-Go.
14. record operator sign-off.

Codex must not perform these operator actions in this phase.

## 5. Stop Conditions

Future real-machine deployment record must stop or mark `Pause` / `No-Go` if any of the following appears:

1. health-check fails.
2. `QDRANT_COLLECTION` is wrong.
3. env host points to an unreachable or wrong target.
4. secret value is exposed in logs, terminal output, record, or Git.
5. unknown dirty files appear outside the approved deployment scope.
6. evidence boundary P0 appears, including fabrication, cross-document contamination, facts as answer, transcript as fact, or permission leakage.
7. any step asks Codex to repair, reindex, backfill, write DB, or approve rollout.
8. any migration is required without explicit separate approval.
9. any real API / CLI smoke is requested without explicit later authorization.
10. NAS / external storage required for the deployment path is unavailable.

Stop condition handling must be conservative. `Pause` is acceptable; silent continuation is not.

## 6. Storage Policy

Real deployment records are local operational artifacts.

Storage rules:

1. real deployment record JSON / Markdown must be ignored by Git by default.
2. committed docs may contain only sanitized planning documents or templates.
3. records must not contain secrets, raw tokens, passwords, or copied `.env` values.
4. records must not include raw logs that contain tokens or sensitive local paths unless sanitized.
5. record paths should be attached by reference, not pasted as full raw log content.
6. future record directories should use `.gitignore`, README, or `.gitkeep` strategy before real records are created.

## 7. Phase 2.45c Runner Relationship

Phase 2.45c provides a read-only health-check dry-run runner.

Allowed future usage:

1. human operator may run the runner manually.
2. operator may attach the resulting ignored JSON path to the deployment record.
3. the record may summarize runner status as `pass`, `warn`, or `fail`.

Not allowed in Phase 2.45d:

1. Codex does not run the runner.
2. Codex does not convert runner warnings into automatic repair.
3. Codex does not treat a runner pass as production rollout approval.

## 8. Future Phase Candidates

### Phase 2.45e: Sanitized Deployment Record Template Artifact

Candidate scope:

1. create a sanitized JSON / Markdown template.
2. add ignored local storage rules for real deployment records.
3. include operator fill-in guidance.
4. still do not execute deployment.

### Phase 2.45f: Explicit Real-machine Deployment Record Dry-run

Candidate scope only after user authorization:

1. read a user-provided sanitized deployment record draft.
2. validate required fields.
3. produce a dry-run summary.
4. do not execute deployment or smoke.

### Deferred: Data Steward / BIM

Data Steward / BIM remains a later product line and does not enter Phase 2.45d.

## 9. Current Phase 2.45d Conclusion

Phase 2.45d is a docs-only planning phase.

It defines how future real-machine deployment records should be structured and reviewed, while explicitly preserving the boundary that Codex does not execute deployment, smoke, repair, rollout, or data mutation in this phase.
