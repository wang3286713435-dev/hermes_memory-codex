# Phase 2.46b Mac Mini Evidence Attachment Plan

## 1. Goal

Phase 2.46b plans how human-run Mac mini Day-0 / MVP setup evidence should be attached, archived, referenced, and reviewed.

This is docs-only planning. It does not generate real evidence, run health checks, run API / CLI smoke, execute setup, or approve rollout.

The goal is to make future evidence useful without leaking secrets or confusing local records with deployment approval.

## 2. Non-goals

Phase 2.46b does not:

1. execute Mac mini setup.
2. run Phase 2.45c health-check runner.
3. run API / CLI smoke.
4. start Postgres, OpenSearch, Qdrant, Hermes_memory API, or Hermes CLI.
5. read or generate real `.env` values or secrets.
6. write DB, facts, document_versions, audit_logs, OpenSearch, or Qdrant.
7. run repair, backfill, reindex, cleanup, delete, or migration.
8. create deployment scripts, cron, scheduler, or rollout automation.
9. approve production rollout.
10. implement Data Steward / BIM.
11. change retrieval contract or memory kernel architecture.

## 3. Evidence Types

| evidence type | purpose | recommended ignored local path | generated in this phase |
|---|---|---|---|
| Day-0 setup checklist filled copy | operator-completed setup checklist | `reports/deployment_records/day0_checklist_<timestamp>.md` | no |
| Phase 2.45c health-check dry-run JSON | read-only environment / service readiness summary | `reports/deployment_records/health_check_<timestamp>.json` | no |
| Mac mini env key-name inventory | key-name presence only, no values | `reports/deployment_records/env_inventory_<timestamp>.json|md` | no |
| storage / NAS / SSD mount evidence | mount readiness and storage policy evidence | `reports/deployment_records/storage_mount_<timestamp>.json|md` | no |
| MVP smoke result | future explicitly authorized Codex C / human smoke result | `reports/deployment_records/mvp_smoke_<timestamp>.json|md` | no |
| deployment record | operator sign-off and Go / Pause / No-Go record | `reports/deployment_records/deployment_record_<timestamp>.json|md` | no |

All real files listed above are local operational artifacts and must remain ignored by Git by default.

## 4. Sanitized Summary Fields

Future evidence summaries should record only metadata needed for review.

Allowed summary fields:

| field | meaning |
|---|---|
| `evidence_type` | one of the evidence types above |
| `status` | `pass`, `warn`, `fail`, `not_run`, or `not_evaluated` |
| `path_label` | sanitized local path label or relative ignored path |
| `sha256` | hash of the local artifact if approved by operator |
| `recorded_at` | timestamp |
| `operator` | human operator |
| `reviewer` | reviewer if present |
| `git_commit` | selected repo commit if relevant |
| `git_tag` | selected repo tag if relevant |
| `go_pause_no_go` | human decision if relevant |
| `stop_conditions_triggered` | sanitized list of stop condition names |

Forbidden summary fields:

1. secret values.
2. raw `.env` values.
3. passwords, tokens, API keys, session tokens, cookies.
4. raw terminal logs that may contain secrets.
5. sensitive business file contents.
6. raw absolute paths if they expose private user or company structure.
7. true business document IDs unless a later phase explicitly authorizes sanitized reference.

## 5. Git Policy

Real evidence JSON / Markdown must not be committed.

Allowed in Git:

1. templates.
2. README files.
3. `.gitignore` rules.
4. sanitized empty examples with placeholder values only, if a later phase explicitly adds them.

Not allowed in Git:

1. real machine status.
2. real `.env` inventory with values.
3. real deployment record JSON / Markdown.
4. real health-check report JSON.
5. real MVP smoke result.
6. raw logs.
7. local `latest.*` pointers.
8. secrets or sensitive business identifiers.

Existing `reports/deployment_records/` policy should continue to ignore real JSON / Markdown / logs by default.

## 6. Evidence Attachment Workflow

Future safe workflow:

1. Human operator performs the allowed setup or check in a separately authorized phase.
2. Human operator saves raw output in an ignored local path.
3. Human operator or reviewer checks whether the artifact contains secrets or sensitive fields.
4. Reviewer creates or approves a sanitized summary containing only allowed fields.
5. Codex reads only the sanitized summary, or narrowly reads fields explicitly authorized by the human operator.
6. Codex may help compare status, missing evidence, hashes, and stop conditions.
7. Codex must not treat evidence path existence as proof of successful deployment without reviewer sign-off.

Codex must stop if it is asked to read raw secret-bearing files, run repair, run reindex, write DB / index, or approve rollout.

## 7. Review Roles

| role | responsibility |
|---|---|
| human operator | performs real setup / dry-run / smoke when explicitly authorized |
| reviewer | checks sensitive content and Go / Pause / No-Go decision |
| Codex A | may create templates / planning docs / sanitized summary logic in authorized phases |
| Codex B | reviews boundaries and writes next bounded prompt |
| Codex C | may run explicitly authorized local MVP smoke in a later phase |

## 8. Go / Pause / No-Go

| decision | meaning |
|---|---|
| Go | Evidence is sanitized enough to support the next planning step, such as Codex C smoke prompt planning. It is not deployment approval. |
| Pause | Evidence is missing, incomplete, or not yet sanitized. |
| No-Go | Secret exposure, wrong Git ref, wrong `QDRANT_COLLECTION`, DB / index mutation, repair request, rollout request, or evidence boundary P0 is present. |

`Go` in this phase only means the evidence attachment package can be used for the next review/planning step. It does not mean production rollout or successful deployment.

## 9. Relationship to Existing Artifacts

### Phase 2.45c Health-check Runner

The runner may be manually executed in a later explicitly authorized phase.

Phase 2.46b only defines where its JSON may be referenced and what sanitized summary fields may be used.

### Phase 2.45e Deployment Record Template

The template defines a future operator-filled deployment record.

Phase 2.46b defines how that record or its sanitized summary should be attached and reviewed.

### Phase 2.46a Day-0 Setup Checklist

The checklist is a human-fillable setup artifact.

Phase 2.46b defines how a filled copy should be referenced and sanitized, not how to execute setup.

## 10. Stop Conditions

Stop immediately if any of the following occurs:

1. secret value appears in evidence, summary, docs, chat, or Git.
2. raw `.env` values are requested or exposed.
3. wrong Git commit / tag is detected.
4. `QDRANT_COLLECTION` is not the expected collection.
5. evidence includes DB / index mutation not explicitly authorized.
6. request asks Codex to repair, reindex, backfill, cleanup, delete, migrate, or run rollout.
7. request asks Codex to run health-check runner or API / CLI smoke without explicit later authorization.
8. raw deployment records are staged.
9. real reports / logs are staged.

## 11. Next Phase Candidate

### Phase 2.46c: Codex C Local MVP Smoke Prompt Planning

Candidate scope after Codex B review:

1. write a bounded Codex C prompt for local MVP smoke.
2. require explicit authorization before running anything.
3. specify allowed smoke queries and P0 stop conditions.
4. still prohibit upload / ingestion / repair / reindex / DB / index writes unless separately authorized.
5. treat smoke results as internal MVP evidence, not production rollout approval.

## 12. Current Conclusion

Phase 2.46b is ready for Codex B review as a planning artifact.

No real evidence was generated. No health-check runner was executed. No API / CLI smoke was run. No Mac mini setup was executed. No DB, facts, document_versions, audit logs, OpenSearch, or Qdrant writes occurred.
