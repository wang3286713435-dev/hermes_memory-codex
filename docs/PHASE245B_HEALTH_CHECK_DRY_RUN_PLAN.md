# Phase 2.45b Health-check / Deploy-smoke Dry-run Plan

## 1. Goal and Non-goals

Phase 2.45b plans a future read-only health-check / deploy-smoke dry-run for the Mac mini internal MVP server.

The goal is to define what a bounded operator or future script may check after the Mac mini environment is prepared.

This phase does not implement or run the checks.

Non-goals:

1. no real Mac mini deployment.
2. no health-check script implementation.
3. no deployment script.
4. no automatic service restart.
5. no migration execution.
6. no repair, cleanup, backfill, reindex, or delete.
7. no DB / facts / document_versions / OpenSearch / Qdrant writes.
8. no production rollout.
9. no Data Steward / BIM implementation.
10. no retrieval contract or memory kernel architecture changes.

## 2. Read-only Scope

Future health-check / deploy-smoke dry-run must be read-only by default.

Allowed future checks:

1. inspect local files and directories.
2. inspect Git branch / tag / clean worktree.
3. check required `.env` key names without printing secret values.
4. check local network reachability.
5. call health endpoints with GET requests.
6. run bounded CLI help commands.
7. read ignored local report / agent state paths.

Forbidden future actions:

1. write business DB rows.
2. mutate facts, document_versions, audit_logs, OpenSearch, or Qdrant.
3. upload or ingest files.
4. run repair / backfill / reindex.
5. start production cron or scheduler.
6. restart services automatically.
7. approve rollout.

## 3. Candidate Checks

### 3.1 Git / Code State

| check | read-only method | expected result | stop on fail |
|---|---|---|---|
| selected branch / tag | inspect `git status` / `git rev-parse` | selected ref recorded | no |
| clean worktree | inspect `git status --short` | only approved dirty, if any | yes if unknown dirty |
| latest baseline tag | inspect tags | expected tag exists | no |

### 3.2 Environment File Presence

Check only whether key names are present. Do not print values.

Required key names:

1. `DATABASE_URL`
2. `OPENSEARCH_URL`
3. `QDRANT_URL`
4. `QDRANT_COLLECTION`
5. `ALIYUN_EMBEDDING_API_KEY` if embedding is enabled
6. `ALIYUN_RERANK_API_KEY` if rerank smoke is enabled
7. local report path / runtime path settings if configured

High-risk checks:

1. `DATABASE_URL` must not point at an unreachable Docker-only hostname from the current execution context.
2. `QDRANT_COLLECTION` must match the active collection, expected currently as `hermes_chunks` unless a later phase changes it.
3. `.env` must remain outside Git.

### 3.3 Storage / Mounts

| check | expected result | stop on fail |
|---|---|---|
| NAS mount exists if required | path exists and is readable | yes for large-file deployment |
| external SSD mount exists if configured | path exists and is readable | no unless configured as required |
| reports path exists | local ignored path reachable | no |
| logs path exists | path reachable | no |
| backup path exists | path reachable or operator records gap | no |

### 3.4 Service Reachability

| service | candidate check | expected result | stop on fail |
|---|---|---|---|
| Postgres | read-only connection check | reachable | yes |
| OpenSearch | GET health / info endpoint | reachable | yes |
| Qdrant | GET health / collections endpoint | reachable | yes |
| Hermes_memory API | GET `/health` | status OK | yes |
| Hermes CLI | `hermes chat --help` | help prints | yes |

These checks are candidates for a later bounded dry-run implementation. Phase 2.45b does not execute them.

### 3.5 Git Ignore / Runtime Path Checks

Candidate checks:

1. `reports/agent_runs/latest.json` is ignored.
2. real reports JSON are ignored.
3. real review records are ignored.
4. no secret-bearing `.env` files are staged.
5. no deployment output artifacts are tracked.

## 4. MVP Smoke Candidates

These are future smoke candidates only. Phase 2.45b does not run them.

| smoke | expected result | write risk | stop on fail |
|---|---|---|---|
| bind `@主标书` | alias resolves to target document | read-only session state only | yes |
| bind `@会议纪要` | alias resolves to target document | read-only session state only | yes |
| structured citation sample | Excel / PPTX citation fields visible if sample exists | none | no |
| Missing Evidence sample | no fabricated answer | none | yes |
| facts boundary | `facts_as_answer=false` | none | yes |
| transcript boundary | `transcript_as_fact=false` | none | yes |
| compare contamination sample | only target documents in evidence | none | yes |

Candidate smoke must not upload new files, create facts, mutate versions, write index payloads, or repair data.

## 5. Output Schema Draft

Future dry-run output should be JSON-serializable.

```json
{
  "dry_run": true,
  "writes_db": false,
  "repairs": false,
  "rollout_approved": false,
  "generated_at": "",
  "machine": "",
  "git": {
    "branch": "",
    "commit": "",
    "tag": "",
    "clean": false
  },
  "checks_total": 0,
  "passed": 0,
  "warnings": 0,
  "failures": 0,
  "stop_required": false,
  "human_action_required": [],
  "checks": [
    {
      "id": "",
      "category": "",
      "status": "pass|warn|fail|skipped",
      "message": "",
      "stop_required": false,
      "human_action_required": false
    }
  ]
}
```

Invariant fields:

1. `dry_run=true`
2. `writes_db=false`
3. `repairs=false`
4. `rollout_approved=false`

## 6. Stop Conditions

Stop immediately if any of the following appears:

1. API health fails.
2. wrong `.env` host or unreachable DB host.
3. wrong Qdrant collection.
4. NAS missing when NAS is required for the deployment path.
5. evidence boundary P0 appears, including fabrication, `facts_as_answer=true`, `transcript_as_fact=true`, cross-document contamination, or permission leakage.
6. any step asks for DB write, index write, migration, repair, backfill, reindex, cleanup, or delete.
7. any output claims production rollout approval.
8. any secret value is printed or staged.
9. unknown dirty files appear outside the phase whitelist.

## 7. Human vs Future Script Boundary

Human-only checks:

1. physical Mac mini setup.
2. LAN / 10GbE / NAS cable and mount confirmation.
3. secret provisioning.
4. service restart decisions.
5. migration approval.
6. Go / Pause / No-Go sign-off.

Potential future bounded script checks:

1. Git clean / tag inspection.
2. `.env` key-name presence check without values.
3. mount path existence.
4. service health GET requests.
5. CLI help availability.
6. ignored runtime file checks.
7. JSON summary generation.

Future script must not restart services, run migrations, write DB/indexes, or approve rollout.

## 8. Future Phase Candidates

### Phase 2.45c: Read-only Health-check Script Implementation

Possible next step if Codex B review passes:

1. implement a small read-only dry-run script.
2. support `--json`.
3. support explicit config path or env file path.
4. mask secrets.
5. emit stop conditions.
6. do not run smoke unless explicitly requested.

### Phase 2.45d: Mac mini Real-machine Deployment Record

Only after user explicitly authorizes real Mac mini setup:

1. record operator-filled deployment checklist.
2. record Go / Pause / No-Go.
3. do not convert this into production rollout.

### Deferred: Data Steward / BIM

Data Steward / BIM remains deferred.

Do not add DB schema, Neo4j, PostGIS, spatial index, BIM parser, scheduler, or product rollout in Phase 2.45b.

## 9. Review Checklist

| item | expected | reviewed |
|---|---|---|
| read-only scope clear | yes |  |
| no deployment script | yes |  |
| no real smoke execution | yes |  |
| no DB / index writes | yes |  |
| output schema includes invariant false flags | yes |  |
| stop conditions include P0 evidence boundary | yes |  |
| Data Steward remains deferred | yes |  |
| next step limited to Phase 2.45c planning / implementation review | yes |  |
