# Mac Mini MVP Deployment Runbook

## 1. Purpose and Boundary

This runbook is for setting up the Mac mini as an internal controlled Hermes MVP server.

Target hardware:

```text
Mac mini M4 / 24GB memory / 512GB SSD / 10GbE
```

The runbook is designed for a human operator. It is a checklist and sign-off artifact, not an automated deployment script.

This runbook is not:

1. production rollout approval.
2. automatic bid review / automatic tender submission.
3. automatic business decision workflow.
4. repair / cleanup / backfill / reindex authorization.
5. Data Steward / BIM implementation.
6. complete IT operations / MDM / scheduler setup.

## 2. Operator Rules

1. A human owner must execute and sign off each step.
2. Codex may help read logs or suggest next checks only when explicitly asked.
3. Codex must not execute real deployment, migration, DB writes, index writes, repair, backfill, reindex, cleanup, delete, or production cron creation from this runbook.
4. Any failed P0 evidence boundary stops the deployment flow.
5. MVP server success does not mean production rollout readiness.

## 3. Day-0 Preparation Checklist

| item | required result | actual result | owner | status |
|---|---|---|---|---|
| macOS initial setup completed | user account created |  |  |  |
| machine name set | e.g. `hermes-mini` |  |  |  |
| fixed IP reserved | LAN IP documented |  |  |  |
| hostname / DNS set | hostname reachable |  |  |  |
| SSH enabled | operator can SSH |  |  |  |
| 10GbE connected | link speed confirmed |  |  |  |
| NAS reachable | mount path reachable |  |  |  |
| external SSD reachable if used | mount path reachable |  |  |  |
| Git available | version recorded |  |  |  |
| Homebrew available if used | version recorded |  |  |  |
| `uv` available | version recorded |  |  |  |
| Docker / container runtime available | version recorded |  |  |  |
| Python available | version recorded |  |  |  |

Notes:

1. Do not expose Hermes services to the public internet.
2. Use internal LAN / VPN only.
3. If NAS is unavailable, do not ingest large enterprise files.

## 4. Directory Creation Checklist

Recommended base:

```text
/Users/hermes/
```

| directory | purpose | created | owner | notes |
|---|---|---|---|---|
| `/Users/hermes/code/Hermes_memory` | Hermes_memory repo |  |  |  |
| `/Users/hermes/code/hermes-agent` | Hermes main repo |  |  |  |
| `/Users/hermes/env` | local `.env` files, not Git |  |  |  |
| `/Users/hermes/data/postgres` | Postgres volume |  |  |  |
| `/Users/hermes/data/opensearch` | OpenSearch volume |  |  |  |
| `/Users/hermes/data/qdrant` | Qdrant volume |  |  |  |
| `/Users/hermes/reports` | local runtime reports |  |  |  |
| `/Users/hermes/logs/hermes_memory` | API logs |  |  |  |
| `/Users/hermes/logs/hermes_agent` | CLI / agent logs |  |  |  |
| `/Users/hermes/backups/postgres` | DB backups |  |  |  |
| `/Users/hermes/backups/opensearch` | index backup plan |  |  |  |
| `/Users/hermes/backups/qdrant` | vector backup plan |  |  |  |
| `/Users/hermes/tmp/ingestion` | temporary processing |  |  |  |

Recommended NAS mount:

```text
/Volumes/HermesNAS/
```

| NAS path | purpose | reachable | owner | notes |
|---|---|---|---|---|
| `/Volumes/HermesNAS/enterprise_files` | original enterprise files |  |  |  |
| `/Volumes/HermesNAS/tender_files` | tender source files |  |  |  |
| `/Volumes/HermesNAS/meeting_records` | meeting source files |  |  |  |
| `/Volumes/HermesNAS/bim_raw` | future BIM raw files |  |  |  |
| `/Volumes/HermesNAS/archived_reports` | report archive if approved |  |  |  |

Optional external SSD:

```text
/Volumes/HermesScratch/
```

| SSD path | purpose | reachable | owner | notes |
|---|---|---|---|---|
| `/Volumes/HermesScratch/ingestion_cache` | large extraction cache |  |  |  |
| `/Volumes/HermesScratch/backup_staging` | backup staging |  |  |  |
| `/Volumes/HermesScratch/temp_extract` | temporary extraction |  |  |  |

## 5. Environment and Secrets Checklist

Do not write real secret values into this document.

| item | expected | checked | owner | notes |
|---|---|---|---|---|
| `.env` stored outside Git | yes |  |  |  |
| `DATABASE_URL` set | points to Mac mini Postgres |  |  |  |
| `OPENSEARCH_URL` set | points to Mac mini OpenSearch |  |  |  |
| `QDRANT_URL` set | points to Mac mini Qdrant |  |  |  |
| `QDRANT_COLLECTION` set | expected active collection |  |  |  |
| `ALIYUN_EMBEDDING_API_KEY` set if needed | secret available |  |  |  |
| `ALIYUN_RERANK_API_KEY` set if used | secret available or documented fallback |  |  |  |
| API host / port configured | internal only |  |  |  |
| report path configured | local ignored path |  |  |  |
| NAS mount path configured | path reachable |  |  |  |

High-risk checks:

1. `DATABASE_URL` must not point at a stale Docker hostname unless running inside that Docker network.
2. `QDRANT_COLLECTION` must match the active collection used by retrieval and eval.
3. `.env` must not be committed.
4. secret values must not be pasted into docs, reports, or chat.

## 6. Repository Checkout Checklist

| step | expected result | actual result | owner | status |
|---|---|---|---|---|
| clone / pull `Hermes_memory` | repo available |  |  |  |
| clone / pull Hermes main repo | repo available |  |  |  |
| verify branch / tag | selected baseline recorded |  |  |  |
| verify clean worktree | no unapproved dirty |  |  |  |
| verify ignored runtime files | `latest.json` / reports ignored |  |  |  |

Selected baseline:

| field | value |
|---|---|
| Hermes_memory branch |  |
| Hermes_memory commit / tag |  |
| Hermes main branch |  |
| Hermes main commit / tag |  |
| operator |  |
| timestamp |  |

## 7. Service Startup Order

Start services in this order:

1. Postgres.
2. OpenSearch.
3. Qdrant.
4. Hermes_memory API.
5. Hermes CLI smoke.

Manual checklist:

| service | command / method | health check | result | owner | status |
|---|---|---|---|---|---|
| Postgres | human-run command | connection OK |  |  |  |
| OpenSearch | human-run command | HTTP OK |  |  |  |
| Qdrant | human-run command | HTTP OK |  |  |  |
| Hermes_memory API | human-run command | `/health` OK |  |  |  |
| Hermes CLI | human-run command | `hermes chat --help` OK |  |  |  |

Codex must not start these services automatically from this runbook unless a later phase explicitly authorizes a bounded smoke task.

## 8. Deployment / Hot Update Flow

Human-run flow:

1. Finish development and validation on developer machine.
2. Commit and tag bounded phase changes.
3. Push to Git remote.
4. SSH into Mac mini.
5. Pull selected branch or tag.
6. Verify worktree status.
7. Sync dependencies.
8. Check migrations.
9. Restart services in order.
10. Run health checks.
11. Run minimal MVP smoke.
12. Record result in this runbook or an ignored local deployment record.

Checklist:

| step | required result | actual result | owner | status |
|---|---|---|---|---|
| developer push completed | branch / tag visible remotely |  |  |  |
| Mac mini pulled selected ref | commit matches expected |  |  |  |
| dependencies synced | no error |  |  |  |
| migration check completed | no unexpected migration |  |  |  |
| services restarted | no fatal error |  |  |  |
| health check passed | all required services reachable |  |  |  |
| smoke passed | minimum smoke pass / partial / fail recorded |  |  |  |

Migration rule:

1. Do not run new migrations unless the phase baseline explicitly requires them.
2. Do not run destructive migrations during MVP deployment.
3. If migration is unclear, stop and ask for Codex B review.

## 9. Minimal Smoke Checklist

This smoke is internal MVP readiness only.

| smoke item | expected | actual | pass / partial / fail | notes |
|---|---|---|---|---|
| API `/health` | 200 OK |  |  |  |
| Hermes CLI help | `hermes chat --help` works |  |  |  |
| `@主标书` alias | binds and resolves |  |  |  |
| `@会议纪要` alias | binds and resolves |  |  |  |
| Excel structured citation if available | sheet / cell visible |  |  |  |
| PPTX structured citation if available | slide number / title visible |  |  |  |
| Missing Evidence query | no fabrication |  |  |  |
| facts boundary | `facts_as_answer=false` |  |  |  |
| transcript boundary | `transcript_as_fact=false` |  |  |  |
| compare / contamination sample | no third-file pollution |  |  |  |

Stop if:

1. `facts_as_answer=true`.
2. `transcript_as_fact=true`.
3. unsupported answer fabricates missing evidence.
4. cross-document contamination appears.
5. permission / tenant leakage appears.

## 10. Backup Checklist

| target | required policy | result | owner | status |
|---|---|---|---|---|
| Git tag | selected deployment tag recorded |  |  |  |
| `.env` inventory | keys listed without values |  |  |  |
| Postgres | backup plan / dump path recorded |  |  |  |
| OpenSearch | snapshot or volume backup plan recorded |  |  |  |
| Qdrant | snapshot or volume backup plan recorded |  |  |  |
| reports / pilot issue artifacts | local-only backup policy recorded |  |  |  |
| NAS source files | NAS backup handled outside Hermes |  |  |  |

Do not paste secret values into backup notes.

## 11. Rollback Checklist

Rollback trigger examples:

1. API health fails after deployment.
2. CLI cannot start.
3. retrieval evidence boundary fails.
4. index collection mismatch appears.
5. unexpected migration is detected.

Rollback steps:

| step | expected result | actual result | owner | status |
|---|---|---|---|---|
| stop Hermes API | API stopped |  |  |  |
| checkout previous known-good tag | code restored |  |  |  |
| restore compatible `.env` | env restored |  |  |  |
| restart dependent services if needed | services healthy |  |  |  |
| run `/health` | 200 OK |  |  |  |
| run minimum smoke | pass / partial / fail recorded |  |  |  |
| record rollback reason | reason documented |  |  |  |

Rollback must not run repair / backfill / reindex / cleanup / delete unless a later phase explicitly authorizes it.

## 12. Stop Conditions

Stop immediately if:

1. service health fails.
2. NAS is missing when large source files are required.
3. `.env` points to wrong host or stale container DNS.
4. `QDRANT_COLLECTION` points to an unexpected collection.
5. Postgres / OpenSearch / Qdrant data appears inconsistent.
6. any P0 evidence boundary appears.
7. any step requires unplanned DB / index writes.
8. any step asks for repair / backfill / reindex / cleanup / delete.
9. anyone describes this MVP server as production rollout.
10. Data Steward / BIM implementation is requested inside this deployment runbook.
11. production scheduler / cron is requested.

## 13. Operator Sign-off

| field | value |
|---|---|
| machine name |  |
| fixed IP |  |
| hostname |  |
| NAS mount path |  |
| external SSD path |  |
| Hermes_memory branch / tag |  |
| Hermes_memory commit |  |
| Hermes main branch / tag |  |
| Hermes main commit |  |
| `.env` checklist completed | yes / no |
| health result | pass / partial / fail |
| smoke result | pass / partial / fail |
| decision | Go / Pause / No-Go |
| human owner |  |
| timestamp |  |
| notes |  |

Decision meaning:

1. Go: internal MVP server flow may continue under controlled Pilot boundaries.
2. Pause: stop and review blocker.
3. No-Go: do not use this server for MVP Pilot until blocker is resolved.

Go is not production rollout approval.

## 14. What Codex Must Not Execute From This Runbook

Codex must not automatically:

1. run deployment commands.
2. start or stop production services.
3. apply migrations.
4. write DB / facts / document_versions.
5. modify OpenSearch / Qdrant.
6. run repair / backfill / reindex / cleanup / delete.
7. create deployment scripts.
8. create scheduler / cron.
9. upload real enterprise files.
10. make production rollout decisions.

Codex may help only with explicitly bounded planning, review, log reading, command explanation, and later user-authorized smoke tasks.

## 15. Next Recommendation

Wait for Codex B review.

If approved, the next step should be Phase 2.45a docs-only Git baseline or Phase 2.45b health-check / deploy-smoke dry-run planning. Do not execute real Mac mini deployment from this artifact.
