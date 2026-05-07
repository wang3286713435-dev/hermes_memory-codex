# Mac Mini Deployment Record Template

This is a sanitized template for a future human-filled Mac mini deployment record.

It is not proof that deployment was executed. It is not a deployment script. It is not production rollout approval.

Real deployment records must be stored in ignored local paths such as `reports/deployment_records/` and must not be committed to Git.

## 1. Fixed Boundary Fields

```text
record_type=mac_mini_deployment_record
deployment_executed_by_human=true
codex_executed_deployment=false
production_rollout_approved=false
```

These fields are required for every real record unless a future phase explicitly changes the operating protocol.

## 2. Selected Git Baselines

| field | value |
|---|---|
| Hermes_memory commit | `<commit>` |
| Hermes_memory tag | `<tag>` |
| Hermes main commit | `<commit>` |
| Hermes main tag | `<tag>` |
| selected by | `<operator>` |
| selected at | `<timestamp>` |

## 3. Machine / Operator Metadata

| field | value |
|---|---|
| Mac mini hostname | `<hostname>` |
| LAN IP | `<lan-ip>` |
| operator | `<operator-name>` |
| recorded_at | `<timestamp>` |
| signoff reviewer | `<reviewer-name>` |

Use sanitized values where possible. Do not paste secrets, tokens, raw `.env` values, or sensitive local logs.

## 4. Environment Key-name Checklist

Do not fill secret values. Mark only whether the key name exists and where it is managed.

| key name | present | location / owner | notes |
|---|---|---|---|
| `DATABASE_URL` | `<yes/no>` | `<outside-git-env-location>` | no value |
| `OPENSEARCH_URL` | `<yes/no>` | `<outside-git-env-location>` | no value |
| `QDRANT_URL` | `<yes/no>` | `<outside-git-env-location>` | no value |
| `QDRANT_COLLECTION` | `<yes/no>` | `<outside-git-env-location>` | expected `hermes_chunks` unless changed by later phase |
| `ALIYUN_EMBEDDING_API_KEY` | `<yes/no/not-used>` | `<secret-store-owner>` | no value |
| `ALIYUN_RERANK_API_KEY` | `<yes/no/not-used>` | `<secret-store-owner>` | no value |

## 5. Storage / Mount Checklist

Use sanitized path labels when the exact path is sensitive.

| item | expected | actual / sanitized label | status |
|---|---|---|---|
| NAS mount | readable if configured | `<nas-label-or-path>` | `<pass/warn/fail>` |
| external SSD | readable if configured | `<ssd-label-or-path>` | `<pass/warn/fail/not-used>` |
| local report directory | ignored by Git | `reports/deployment_records/` or operator path | `<pass/warn/fail>` |
| logs directory | no secret exposure | `<log-label-or-path>` | `<pass/warn/fail>` |

## 6. Optional Evidence Paths

These are path references only. Do not paste raw logs or JSON bodies that contain secrets.

| evidence | path | status | notes |
|---|---|---|---|
| Phase 2.45c health-check dry-run JSON | `<ignored-local-json-path>` | `<pass/warn/fail/not-run>` | optional, human-run only |
| MVP smoke result | `<ignored-local-json-or-md-path>` | `<pass/warn/fail/not-run>` | fill only if later explicitly authorized |
| operator notes | `<ignored-local-md-path>` | `<attached/not-attached>` | no secrets |

## 7. Stop Conditions

Mark every triggered stop condition. If any P0 stop condition appears, the deployment record should be `Pause` or `No-Go`.

| stop condition | triggered | evidence / notes |
|---|---|---|
| health-check failed | `<yes/no>` | `<sanitized-reference>` |
| wrong `QDRANT_COLLECTION` | `<yes/no>` | `<sanitized-reference>` |
| wrong env host | `<yes/no>` | `<sanitized-reference>` |
| secret exposure | `<yes/no>` | `<sanitized-reference>` |
| unknown dirty files | `<yes/no>` | `<sanitized-reference>` |
| evidence boundary P0 | `<yes/no>` | fabrication / contamination / facts-as-answer / transcript-as-fact / permission leakage |
| repair / reindex / DB write requested | `<yes/no>` | `<sanitized-reference>` |
| rollout approval requested | `<yes/no>` | `<sanitized-reference>` |
| NAS / external storage unavailable | `<yes/no/not-required>` | `<sanitized-reference>` |

## 8. Go / Pause / No-Go

| field | value |
|---|---|
| go_pause_no_go | `<go/pause/no_go/not_evaluated>` |
| decision owner | `<operator-or-reviewer>` |
| decision time | `<timestamp>` |
| human_actions_required | `<summary>` |

`Go` means only that the internal Mac mini MVP node record has no blocking stop condition for the reviewed scope. It does not mean production rollout approval.

## 9. Operator Signoff

| field | value |
|---|---|
| signed_by | `<operator>` |
| signed_at | `<timestamp>` |
| decision | `<go/pause/no_go/not_evaluated>` |
| notes | `<sanitized-notes-no-secrets>` |

## 10. JSON Shape Reference

```json
{
  "record_type": "mac_mini_deployment_record",
  "deployment_executed_by_human": true,
  "codex_executed_deployment": false,
  "production_rollout_approved": false,
  "hermes_memory_commit": "<commit>",
  "hermes_memory_tag": "<tag>",
  "hermes_main_commit": "<commit>",
  "hermes_main_tag": "<tag>",
  "hostname": "<hostname>",
  "lan_ip": "<lan-ip>",
  "operator": "<operator>",
  "recorded_at": "<timestamp>",
  "env_key_names_present": {
    "DATABASE_URL": true,
    "OPENSEARCH_URL": true,
    "QDRANT_URL": true,
    "QDRANT_COLLECTION": true
  },
  "nas_mount": "<sanitized-label-or-path>",
  "external_ssd": "<sanitized-label-or-path-or-not-used>",
  "dry_run_evidence_path": "<ignored-local-json-path>",
  "mvp_smoke_result_path": "<ignored-local-json-or-md-path-or-not-run>",
  "go_pause_no_go": "<go|pause|no_go|not_evaluated>",
  "operator_signoff": {
    "signed_by": "<operator>",
    "signed_at": "<timestamp>",
    "decision": "<go|pause|no_go|not_evaluated>",
    "notes": "<sanitized-notes-no-secrets>"
  },
  "stop_conditions_triggered": [],
  "human_actions_required": []
}
```

## 11. Not-production-rollout Statement

This template does not authorize production rollout.

This template does not authorize Codex to run deployment, restart services, run migrations, run API / CLI smoke, write DB or indexes, repair data, backfill, reindex, cleanup, delete, or create production schedulers.

Any real deployment action must be separately authorized in a later phase and executed by a human operator.
