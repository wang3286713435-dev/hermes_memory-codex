# Phase 2.45 Mac Mini MVP Server Deployment Plan

## 1. Goal

Phase 2.45 plans how to package Hermes as an internal controlled MVP server on the new Mac mini:

```text
Mac mini M4 / 24GB memory / 512GB SSD / 10GbE
```

The target is a company-internal Hermes MVP node that can run the current Hermes_memory stack, accept controlled Pilot usage, receive hot updates from Git, and keep enough logs / reports / backups for review.

This is deployment planning only. It does not execute deployment, write scripts, approve production rollout, or implement Data Steward / BIM.

## 2. Non-goals

Phase 2.45 does not:

1. perform production rollout.
2. expose Hermes as a production service.
3. implement automatic bid review, automatic tender submission, or final business decision automation.
4. implement repair executor, cleanup, backfill, reindex, or destructive tools.
5. implement Data Steward / BIM asset catalog, graph, spatial index, scheduler, or monitoring agents.
6. implement MDM, full IT operations platform, SSO, or complete RBAC / ABAC.
7. change retrieval contract or memory kernel main architecture.
8. write DB / facts / document_versions / OpenSearch / Qdrant data.
9. create production cron or scheduler.

## 3. Hardware and Network Assumptions

### 3.1 Hardware

| item | target |
|---|---|
| machine | Mac mini M4 |
| memory | 24GB |
| local SSD | 512GB |
| network | 10GbE |
| role | internal MVP server node |

### 3.2 Network

Recommended setup:

1. assign fixed LAN IP and stable hostname, for example `hermes-mini.local` or an internal DNS name.
2. enable SSH for controlled operator access.
3. prefer wired 10GbE for NAS / large file access.
4. restrict inbound access to internal network or VPN.
5. do not expose ports directly to public internet.

### 3.3 Storage Boundary

| storage | usage |
|---|---|
| Mac mini internal SSD | code, service config, hot indexes, Docker volumes, local logs, small reports |
| NAS | original enterprise files, large document pool, future BIM raw files, long-term archive |
| external SSD | optional ingestion cache, local backup staging, temporary processing workspace |

Original enterprise files and future BIM large files should live on NAS first. The Mac mini should not become the long-term raw-file warehouse.

## 4. Service Topology

Minimum internal MVP services:

1. Postgres: document metadata, chunks, versions, facts, audit logs.
2. OpenSearch: sparse / BM25 index.
3. Qdrant: dense vector index.
4. Hermes_memory API: ingestion, retrieval, facts, eval, audit endpoints.
5. Hermes main repository / CLI: agent interaction layer and operator CLI.
6. reports / logs / backups: local ignored runtime artifacts and backup outputs.

Recommended dependency order:

```text
Postgres -> OpenSearch -> Qdrant -> Hermes_memory API -> Hermes CLI smoke
```

Do not start Pilot usage until `/health`, index reachability, and minimum CLI smoke pass.

## 5. Directory Strategy

Recommended local layout:

```text
/Users/hermes/
  code/
    Hermes_memory/
    hermes-agent/
  env/
    hermes_memory.env
    hermes_agent.env
  data/
    postgres/
    opensearch/
    qdrant/
  reports/
    agent_runs/
    pilot_issues/
    pilot_triage/
    mvp_pilot_reviews/
  logs/
    hermes_memory/
    hermes_agent/
  backups/
    postgres/
    qdrant/
    opensearch/
    reports/
  tmp/
    ingestion/
    uploads/
```

Recommended NAS mount shape:

```text
/Volumes/HermesNAS/
  enterprise_files/
  tender_files/
  meeting_records/
  bim_raw/
  archived_reports/
```

Recommended external SSD shape:

```text
/Volumes/HermesScratch/
  ingestion_cache/
  backup_staging/
  temp_extract/
```

Notes:

1. real `reports/**/*.json`, `reviews/**/*.json`, and `agent_runs/latest.json` remain local artifacts by default.
2. raw Pilot reports, issue records, and review records should not be committed to Git.
3. `.env` files must stay outside Git.
4. NAS path availability is a deployment pre-flight condition.

## 6. Environment Variables and Secrets

Checklist only; do not commit real secrets.

Required categories:

1. `DATABASE_URL`
2. `OPENSEARCH_URL`
3. `QDRANT_URL`
4. `QDRANT_COLLECTION`
5. `ALIYUN_EMBEDDING_API_KEY`
6. optional `ALIYUN_RERANK_API_KEY`
7. API host / port
8. logging level
9. reports / backup paths
10. NAS mount path

Important constraints:

1. `.env` must not enter Git.
2. Mac mini `.env` should not accidentally point to Docker-only hostnames such as `postgres` when local host ports are expected.
3. `QDRANT_COLLECTION` should match the active collection used by eval and retrieval; historical false failures occurred when pointing at the wrong collection.
4. keys should be stored in a local operator-managed secret file or system keychain, not in docs.

## 7. Deployment and Hot-update Flow

Recommended controlled flow:

1. develop and test on developer machine.
2. commit and tag bounded phase changes.
3. push to Git remote.
4. SSH to Mac mini.
5. pull the selected branch / tag.
6. verify `git status` is clean except approved local ignored artifacts.
7. sync dependencies.
8. check migrations without blindly applying destructive changes.
9. restart services in dependency order.
10. run health checks.
11. run minimum MVP smoke.
12. record deployment notes in an ignored local report or a sanitized committed runbook if needed.

Hot-update guardrails:

1. no direct unreviewed code editing on Mac mini.
2. update from Git only.
3. deployment should be reversible to previous tag.
4. before migration, confirm it is expected by the phase baseline.
5. if service health fails, stop Pilot use and roll back.

## 8. Health Check and MVP Smoke

Minimum health checks:

1. Postgres connection.
2. OpenSearch reachable.
3. Qdrant reachable.
4. Hermes_memory API `/health`.
5. Hermes CLI `hermes chat --help`.

Minimum internal MVP smoke:

1. bind `@主标书`.
2. bind `@会议纪要`.
3. bind one Excel / structured file alias if available.
4. bind one PPTX / slide file alias if available.
5. ask one main tender Missing Evidence query.
6. ask one meeting transcript action / decision / risk query.
7. ask one structured citation query.
8. verify `facts_as_answer=false`.
9. verify `transcript_as_fact=false`.
10. verify Missing Evidence stays explicit when evidence is absent.

This smoke is not production certification. It is an internal MVP readiness check.

## 9. Backup and Rollback Strategy

### 9.1 Backup Targets

Back up:

1. Postgres database.
2. Qdrant collection or volume snapshot.
3. OpenSearch index / volume snapshot.
4. `.env` checksum / inventory, without exposing secret values.
5. reports / issue intake / triage / review local artifacts if approved by operator.
6. Git commit and tag used by Mac mini.

### 9.2 Rollback Flow

Recommended rollback:

1. stop Hermes API.
2. roll code back to previous known-good tag.
3. restore compatible `.env`.
4. restart Postgres / OpenSearch / Qdrant if required.
5. run `/health`.
6. run minimum smoke.
7. record rollback reason.

Do not run repair / cleanup / reindex automatically during rollback unless a later phase explicitly authorizes it.

## 10. Mac Mini / NAS / External SSD Boundary

The Mac mini should be treated as the internal MVP compute and hot-index node.

| responsibility | Mac mini | NAS | external SSD |
|---|---|---|---|
| code checkout | yes | no | optional mirror |
| API / CLI runtime | yes | no | no |
| Postgres / OpenSearch / Qdrant hot volumes | yes | no | optional backup staging |
| original enterprise files | no, except temporary uploads | yes | optional temp |
| future BIM raw files | no | yes | optional temp |
| reports / logs | yes, local | optional archive | optional archive |
| ingestion scratch | limited | no | yes if large |

If NAS is not mounted, ingestion of large enterprise files should stop. Do not silently copy large raw corpora to the Mac mini internal SSD.

## 11. Stop Conditions

Stop deployment or Pilot use if:

1. `/health` fails.
2. Postgres / OpenSearch / Qdrant is unreachable.
3. `.env` points to wrong host / collection.
4. NAS mount is missing for workflows requiring raw files.
5. OpenSearch / Qdrant collection appears inconsistent with expected active data.
6. P0 evidence boundary appears: hallucination, facts as answer, transcript as fact, cross-document contamination, permission leakage, or automatic business decision.
7. any step requires DB / index mutation outside the planned deployment boundary.
8. any step asks to repair / backfill / reindex / cleanup / delete.
9. anyone interprets internal MVP server as production rollout.
10. Data Steward / BIM implementation is requested without a separate phase.

## 12. Recommended Phase Sequence

1. Phase 2.45: docs-only planning. Current phase.
2. Phase 2.45a: deployment runbook artifact / checklist.
3. Phase 2.45b: local deploy smoke script dry-run or health-check script planning / implementation.
4. Phase 2.45c: Mac mini real-machine deployment record, only after explicit user authorization.
5. Later: controlled MVP server smoke and evidence capture.

Data Steward / BIM remains a separate product line and should not be folded into the Mac mini MVP deployment phase.

## 13. Review Questions for Codex B

Codex B should review:

1. whether the plan is still internal controlled MVP, not production rollout.
2. whether NAS / external SSD boundaries are clear enough.
3. whether hot-update and rollback are conservative.
4. whether health and smoke checks cover the current MVP Pilot risk points.
5. whether Phase 2.45a should produce a human runbook only or include a dry-run health script plan.

## 14. Next Recommendation

Wait for Codex B review.

If approved, proceed only to Phase 2.45 docs-only Git baseline or a Phase 2.45a deployment runbook artifact. Do not execute real Mac mini deployment from this planning phase.
