# Phase 2.46 Mac Mini Day-0 Real-machine Setup Plan

## 1. Goal

Phase 2.46 defines the Day-0 real-machine setup plan for the Mac mini after arrival.

Target machine:

```text
Mac mini M4 / 24GB memory / 512GB SSD / 10GbE
```

The goal is to prepare a conservative human-operator checklist before any internal MVP application setup, dry-run evidence attachment, or later smoke authorization.

This is planning only. It is not a deployment run, not a deployment proof, and not production rollout approval.

## 2. Non-goals

Phase 2.46 does not:

1. execute real Mac mini deployment.
2. start Postgres, OpenSearch, Qdrant, Hermes_memory API, or Hermes CLI.
3. run Phase 2.45c health-check runner.
4. run API / CLI smoke.
5. write DB, facts, document_versions, audit_logs, OpenSearch, or Qdrant.
6. run repair, backfill, reindex, cleanup, delete, or migration.
7. create deployment scripts, production cron, scheduler, or rollout automation.
8. implement Data Steward / BIM, RBAC expansion, retrieval contract changes, or memory kernel architecture changes.

## 3. Day-0 Human Operator Actions

All actions in this section are human-run. Codex may help inspect sanitized outputs only when explicitly asked.

### 3.1 Physical and System Setup

| item | expected result | owner | evidence placeholder | status |
|---|---|---|---|---|
| Unbox and inspect Mac mini | no visible damage | human operator | `<photo-or-note-path-if-approved>` | pending |
| Complete macOS initial setup | local admin/operator account created | human operator | `<operator-note>` | pending |
| Set device name | stable name such as `hermes-mini` | human operator | `<system-settings-note>` | pending |
| Apply macOS updates | latest approved macOS patch level | human operator | `<update-note>` | pending |
| Enable controlled remote access if needed | SSH / screen sharing policy decided | human operator | `<access-note>` | pending |

### 3.2 Workspace and Directory Preparation

Recommended local workspace:

```text
/Users/hermes/
  code/
    Hermes_memory/
    hermes-agent/
  env/
  data/
  reports/
  logs/
  backups/
  tmp/
```

Day-0 checklist:

| item | expected result | status |
|---|---|---|
| Create local base directory | `/Users/hermes/` or approved equivalent exists | pending |
| Create code directory | Git checkout target exists | pending |
| Create env directory | outside Git; secret-bearing files stored here | pending |
| Create reports directory | local runtime reports; real JSON ignored | pending |
| Create logs directory | local logs; no secrets pasted into docs | pending |
| Create backups directory | backup staging path exists | pending |
| Create tmp directory | temporary ingestion / extraction workspace exists | pending |

## 4. Git Checkout Preparation

Day-0 does not pull or deploy automatically. The operator prepares the checkout target and records intended refs.

| item | expected result | status |
|---|---|---|
| Hermes_memory checkout path selected | e.g. `/Users/hermes/code/Hermes_memory` | pending |
| Hermes main checkout path selected | e.g. `/Users/hermes/code/hermes-agent` | pending |
| Remote URL policy confirmed | approved Git remote only | pending |
| Selected Hermes_memory ref recorded | branch / commit / tag, not guessed | pending |
| Selected Hermes main ref recorded | branch / commit / tag, not guessed | pending |
| Unknown dirty policy confirmed | stop on unknown dirty files | pending |

Reference baseline available before Day-0:

| repo | current known baseline |
|---|---|
| Hermes_memory | `8bd7616`, `phase-2.45e-deployment-record-template-baseline` |
| Hermes main | use latest approved Pilot baseline from runbook / Codex B review |

## 5. Environment Key-name Checklist

Do not record secret values. Record only key names, storage owner, and whether the key is present.

| key name | expected | value recorded? | status |
|---|---|---|---|
| `DATABASE_URL` | points to intended Mac mini Postgres context | no | pending |
| `OPENSEARCH_URL` | points to intended OpenSearch context | no | pending |
| `QDRANT_URL` | points to intended Qdrant context | no | pending |
| `QDRANT_COLLECTION` | expected `hermes_chunks` unless later changed | no | pending |
| `ALIYUN_EMBEDDING_API_KEY` | present if embedding is enabled | no | pending |
| `ALIYUN_RERANK_API_KEY` | optional; fallback policy recorded if absent | no | pending |
| API host / port | internal-only target | no | pending |
| reports / runtime paths | local ignored paths | no | pending |
| NAS mount path | configured only if NAS is ready | no | pending |

High-risk checks:

1. `.env` must remain outside Git.
2. Do not paste keys, tokens, passwords, or raw `.env` values into docs, chat, reports, or screenshots.
3. `DATABASE_URL` must not accidentally point to an unreachable Docker-only hostname from the actual runtime context.
4. `QDRANT_COLLECTION` must not point to stale collections such as historical `hermes_gate_chunks`.

## 6. Storage and Network Preparation

### 6.1 NAS / External SSD

| item | expected result | stop if unavailable |
|---|---|---|
| NAS mount path selected | approved mount label or path recorded | yes if large-file source depends on NAS |
| NAS read permission | operator can list approved source directories | yes |
| NAS write policy | no accidental writes to raw enterprise source directory | yes |
| external SSD selected if used | mount label or path recorded | no unless configured as required |
| external SSD scratch path | available for cache / backup staging only | no |

### 6.2 Network

| item | expected result | status |
|---|---|---|
| 10GbE link | link speed confirmed by operator | pending |
| fixed LAN IP | reserved / documented | pending |
| hostname | stable local hostname or internal DNS name | pending |
| inbound exposure policy | internal LAN / VPN only | pending |
| public internet exposure | not allowed for MVP node | pending |

## 7. Runtime Readiness Checklist

No runtime command is executed in this phase. This section defines what a human operator should later check.

| runtime | expected Day-0 check | status |
|---|---|---|
| Docker / container runtime | installed or selected alternative documented | pending |
| Python | version recorded | pending |
| `uv` | version recorded | pending |
| Git | version recorded | pending |
| Homebrew if used | version recorded | pending |
| Postgres runtime | installation / container path decided | pending |
| OpenSearch runtime | installation / container path decided | pending |
| Qdrant runtime | installation / container path decided | pending |
| Hermes_memory API runtime | execution method decided, not started by this plan | pending |
| Hermes CLI runtime | execution method decided, not run by this plan | pending |

## 8. Evidence Artifact Placeholders

These are path placeholders only. Do not generate real evidence in Phase 2.46.

| evidence type | placeholder path | generated in this phase? |
|---|---|---|
| Day-0 operator notes | `<ignored-local-path>/day0_notes.md` | no |
| Phase 2.45c health-check dry-run JSON | `<ignored-local-path>/health_check_dry_run.json` | no |
| deployment record | `reports/deployment_records/<timestamp>_record.md|json` | no |
| MVP smoke result | `<ignored-local-path>/mvp_smoke_result.json|md` | no |
| Mac mini env key-name checklist | `<ignored-local-path>/env_key_inventory.md|json` | no |
| NAS / SSD mount evidence | `<ignored-local-path>/storage_mount_check.md|json` | no |

Real evidence artifacts remain local ignored by default unless a later phase explicitly defines a sanitized committed artifact.

## 9. Stop Conditions

Stop and request Codex B / human review if any condition appears:

1. secret value is exposed in docs, terminal, report, screenshot, or Git.
2. selected Git ref is unknown, wrong, unpushed, or dirty beyond approved scope.
3. `QDRANT_COLLECTION` is wrong or points to stale collection.
4. NAS is required but unavailable.
5. external SSD is configured as required but unavailable.
6. Docker / runtime dependency is unavailable and no approved alternative exists.
7. any step asks Codex to write DB, index, facts, document_versions, or audit_logs.
8. any step asks for repair, backfill, reindex, cleanup, delete, migration, or rollout.
9. unknown dirty files appear in either repo.
10. any request treats MVP server setup as production rollout approval.

## 10. Go / Pause / No-Go Rules

| decision | meaning |
|---|---|
| Go | Day-0 preparation plan is clear enough for the next human-run setup checklist or dry-run planning step. It is not production rollout. |
| Pause | required operator detail is missing, such as Git ref, storage path, env key-name inventory, or runtime choice. |
| No-Go | a stop condition is triggered: secret exposure, wrong collection, unavailable required storage, unknown dirty files, or request for data mutation / repair / rollout. |

Phase 2.46 planning can only recommend whether the next planning / checklist phase is ready. It cannot approve real deployment.

## 11. Next Phase Candidates

### Phase 2.46a: Day-0 Setup Checklist Artifact

Create a fillable operator checklist artifact based on this plan.

Boundary:

1. docs-only or template-only.
2. no real setup execution.
3. no API / CLI smoke.
4. no DB / index writes.

### Phase 2.46b: Human-run Health-check Evidence Attachment Plan

Plan how a human operator may attach Phase 2.45c dry-run JSON and other sanitized evidence paths.

Boundary:

1. path references only.
2. real evidence remains ignored.
3. no automatic runner execution.

### Phase 2.46c: Explicitly Authorized Local MVP Smoke Prompt for Codex C

Only after separate explicit authorization, write a Codex C prompt for local MVP smoke on Mac mini or equivalent real-machine environment.

Boundary:

1. smoke only, not rollout.
2. no upload / ingestion unless explicitly authorized.
3. no repair / reindex / DB mutation.
4. facts_as_answer / transcript_as_fact / contamination boundaries remain P0 stop conditions.

## 12. Current Conclusion

Phase 2.46 is ready for Codex B review as a planning artifact.

No real Mac mini setup was executed. No health-check runner was executed. No API / CLI smoke was run. No DB, facts, versions, audit logs, OpenSearch, or Qdrant writes occurred.

Recommended next step: Codex B reviews this plan and, if acceptable, writes a docs-only Git baseline prompt. Do not enter Phase 2.46a automatically.
