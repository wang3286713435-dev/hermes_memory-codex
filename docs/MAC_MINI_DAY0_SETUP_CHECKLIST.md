# Mac Mini Day-0 Setup Checklist

This checklist is a sanitized, human-fillable Day-0 setup artifact for the internal Hermes MVP Mac mini.

It is not a deployment script, not deployment proof, and not production rollout approval.

Target machine:

```text
Mac mini M4 / 24GB memory / 512GB SSD / 10GbE
```

## 1. Record Metadata

| field | value |
|---|---|
| checklist_type | `mac_mini_day0_setup_checklist` |
| operator | `<operator-name>` |
| reviewer | `<reviewer-name>` |
| date | `<YYYY-MM-DD>` |
| machine name | `<hostname-or-device-name>` |
| serial / asset tag | `<sanitized-asset-id>` |
| LAN IP | `<lan-ip-or-pending>` |
| current decision | `<go|pause|no_go|not_evaluated>` |

Rules:

1. Do not record secrets, passwords, tokens, or raw `.env` values.
2. Do not paste raw logs that may contain secrets.
3. Use sanitized path labels when exact local paths are sensitive.

## 2. Boundary Confirmation

| boundary | expected | confirmed |
|---|---|---|
| This checklist is human-operated | yes | `<yes/no>` |
| Codex executes real setup | no | `<yes/no>` |
| Production rollout approved | no | `<yes/no>` |
| DB / index writes authorized | no | `<yes/no>` |
| repair / reindex / backfill authorized | no | `<yes/no>` |
| API / CLI smoke authorized in this checklist | no | `<yes/no>` |

If any answer conflicts with the expected value, stop and mark `Pause` or `No-Go`.

## 3. Physical Inspection and macOS Initial Setup

| item | expected result | actual / note | owner | status |
|---|---|---|---|---|
| Unbox Mac mini | no visible damage |  |  | `<pending/pass/warn/fail>` |
| Power adapter / cable checked | all required accessories present |  |  | `<pending/pass/warn/fail>` |
| First boot completed | macOS setup assistant completed |  |  | `<pending/pass/warn/fail>` |
| Local admin / operator account | account created and secured |  |  | `<pending/pass/warn/fail>` |
| Device name set | stable name, e.g. `hermes-mini` |  |  | `<pending/pass/warn/fail>` |
| macOS update checked | approved patch level recorded |  |  | `<pending/pass/warn/fail>` |
| Timezone / locale checked | expected company setting |  |  | `<pending/pass/warn/fail>` |

## 4. Remote Access and Exposure Policy

| item | expected result | actual / note | owner | status |
|---|---|---|---|---|
| SSH policy decided | enabled only if operator-approved |  |  | `<pending/pass/warn/fail>` |
| Screen sharing policy decided | internal-only if enabled |  |  | `<pending/pass/warn/fail>` |
| Firewall / inbound policy | internal LAN / VPN only |  |  | `<pending/pass/warn/fail>` |
| Public internet exposure | not exposed |  |  | `<pending/pass/warn/fail>` |
| Operator access owner | named person/team recorded |  |  | `<pending/pass/warn/fail>` |

## 5. Workspace Directory Checklist

Recommended base:

```text
/Users/hermes/
```

| directory | purpose | actual path / sanitized label | status |
|---|---|---|---|
| `code/` | Git checkouts |  | `<pending/pass/warn/fail>` |
| `code/Hermes_memory/` | Hermes_memory repo |  | `<pending/pass/warn/fail>` |
| `code/hermes-agent/` | Hermes main repo |  | `<pending/pass/warn/fail>` |
| `env/` | `.env` files outside Git |  | `<pending/pass/warn/fail>` |
| `data/` | service data roots |  | `<pending/pass/warn/fail>` |
| `reports/` | ignored local reports |  | `<pending/pass/warn/fail>` |
| `logs/` | service logs |  | `<pending/pass/warn/fail>` |
| `backups/` | backup staging |  | `<pending/pass/warn/fail>` |
| `tmp/` | temporary processing |  | `<pending/pass/warn/fail>` |

Notes:

1. `env/` must remain outside Git.
2. real `reports/**/*.json` and deployment records should remain ignored local artifacts.
3. logs must not be copied into Git without sanitization.

## 6. Git Checkout Information

| item | expected | actual | status |
|---|---|---|---|
| Hermes_memory checkout path | selected local path |  | `<pending/pass/warn/fail>` |
| Hermes_memory remote | approved remote |  | `<pending/pass/warn/fail>` |
| Hermes_memory branch | selected branch |  | `<pending/pass/warn/fail>` |
| Hermes_memory commit | selected commit |  | `<pending/pass/warn/fail>` |
| Hermes_memory tag | selected tag if used |  | `<pending/pass/warn/fail>` |
| Hermes main checkout path | selected local path |  | `<pending/pass/warn/fail>` |
| Hermes main remote | approved remote |  | `<pending/pass/warn/fail>` |
| Hermes main branch | selected branch |  | `<pending/pass/warn/fail>` |
| Hermes main commit | selected commit |  | `<pending/pass/warn/fail>` |
| Hermes main tag | selected tag if used |  | `<pending/pass/warn/fail>` |
| Dirty policy | stop on unknown dirty |  | `<pending/pass/warn/fail>` |

Current known Hermes_memory planning baseline:

```text
commit=13e2206
tag=phase-2.46-mac-mini-day0-setup-plan-baseline
```

Do not guess a production ref. Record the selected ref explicitly before any later setup step.

## 7. Environment Key-name Inventory

Do not record values. Record only key names, ownership, and whether present.

| key name | present | owner / storage location | notes |
|---|---|---|---|
| `DATABASE_URL` | `<yes/no>` | `<outside-git-location>` | no value |
| `OPENSEARCH_URL` | `<yes/no>` | `<outside-git-location>` | no value |
| `QDRANT_URL` | `<yes/no>` | `<outside-git-location>` | no value |
| `QDRANT_COLLECTION` | `<yes/no>` | `<outside-git-location>` | expected `hermes_chunks` |
| `ALIYUN_EMBEDDING_API_KEY` | `<yes/no/not-used>` | `<secret-owner>` | no value |
| `ALIYUN_RERANK_API_KEY` | `<yes/no/not-used>` | `<secret-owner>` | no value |
| API host / port | `<yes/no>` | `<outside-git-location>` | internal only |
| reports path | `<yes/no>` | `<outside-git-location>` | ignored local path |
| NAS mount path | `<yes/no/not-used>` | `<outside-git-location>` | no secret |

High-risk environment checks:

| check | expected | status |
|---|---|---|
| `.env` outside Git | yes | `<pending/pass/warn/fail>` |
| no secret copied into docs / chat / report | yes | `<pending/pass/warn/fail>` |
| `QDRANT_COLLECTION=hermes_chunks` unless later changed | yes | `<pending/pass/warn/fail>` |
| `DATABASE_URL` not pointing to wrong Docker-only hostname | yes | `<pending/pass/warn/fail>` |
| `.env` file not staged | yes | `<pending/pass/warn/fail>` |

## 8. Storage, NAS, External SSD

| item | expected result | actual / sanitized label | status |
|---|---|---|---|
| NAS decision | required / optional / not used |  | `<pending/pass/warn/fail>` |
| NAS mount | readable if required |  | `<pending/pass/warn/fail>` |
| NAS raw file policy | no accidental source mutation |  | `<pending/pass/warn/fail>` |
| external SSD decision | required / optional / not used |  | `<pending/pass/warn/fail>` |
| external SSD mount | readable if required |  | `<pending/pass/warn/fail>` |
| external SSD role | scratch / backup staging only |  | `<pending/pass/warn/fail>` |
| local backup path | exists or planned |  | `<pending/pass/warn/fail>` |

Stop if required storage is unavailable.

## 9. Network Checklist

| item | expected result | actual | status |
|---|---|---|---|
| 10GbE link | confirmed by operator |  | `<pending/pass/warn/fail>` |
| LAN IP | reserved / recorded |  | `<pending/pass/warn/fail>` |
| hostname | stable local hostname / DNS |  | `<pending/pass/warn/fail>` |
| access scope | internal LAN / VPN only |  | `<pending/pass/warn/fail>` |
| public exposure | none |  | `<pending/pass/warn/fail>` |

## 10. Runtime Readiness

This checklist records readiness only. It does not start services.

| runtime | expected result | actual / version / note | status |
|---|---|---|---|
| Docker / container runtime | installed or alternative selected |  | `<pending/pass/warn/fail>` |
| Python | version recorded |  | `<pending/pass/warn/fail>` |
| `uv` | version recorded |  | `<pending/pass/warn/fail>` |
| Git | version recorded |  | `<pending/pass/warn/fail>` |
| Homebrew if used | version recorded |  | `<pending/pass/warn/fail>` |
| Postgres | runtime method selected |  | `<pending/pass/warn/fail>` |
| OpenSearch | runtime method selected |  | `<pending/pass/warn/fail>` |
| Qdrant | runtime method selected |  | `<pending/pass/warn/fail>` |
| Hermes_memory API | runtime method selected; not started here |  | `<pending/pass/warn/fail>` |
| Hermes CLI | runtime method selected; not run here |  | `<pending/pass/warn/fail>` |

## 11. Evidence Placeholders

These are references only. Do not generate real evidence as part of this checklist artifact.

| evidence | local ignored path placeholder | status |
|---|---|---|
| Day-0 operator notes | `<ignored-local-path>/day0_notes.md` | `<pending/not-generated>` |
| Phase 2.45c health-check dry-run JSON | `<ignored-local-path>/health_check_dry_run.json` | `<pending/not-generated>` |
| deployment record | `reports/deployment_records/<timestamp>_record.md|json` | `<pending/not-generated>` |
| MVP smoke result | `<ignored-local-path>/mvp_smoke_result.json|md` | `<pending/not-generated>` |
| env key-name inventory | `<ignored-local-path>/env_key_inventory.md|json` | `<pending/not-generated>` |
| storage / mount evidence | `<ignored-local-path>/storage_mount_check.md|json` | `<pending/not-generated>` |

## 12. Stop Conditions

Mark any triggered stop condition.

| stop condition | triggered | notes / evidence reference |
|---|---|---|
| secret value exposed | `<yes/no>` |  |
| wrong Git ref | `<yes/no>` |  |
| unknown dirty files | `<yes/no>` |  |
| wrong `QDRANT_COLLECTION` | `<yes/no>` |  |
| required NAS unavailable | `<yes/no/not-required>` |  |
| required external SSD unavailable | `<yes/no/not-required>` |  |
| Docker / runtime unavailable | `<yes/no>` |  |
| request for DB / index write | `<yes/no>` |  |
| request for repair / backfill / reindex | `<yes/no>` |  |
| request for cleanup / delete / migration | `<yes/no>` |  |
| request for API / CLI smoke without authorization | `<yes/no>` |  |
| request for production rollout | `<yes/no>` |  |

Any `yes` should normally produce `Pause` or `No-Go`.

## 13. Go / Pause / No-Go Sign-off

| decision | meaning | selected |
|---|---|---|
| Go | Checklist is complete enough to proceed to the next separately authorized planning / setup step. Not rollout. | `<yes/no>` |
| Pause | Missing information or non-P0 uncertainty requires review. | `<yes/no>` |
| No-Go | Stop condition triggered or unsafe request detected. | `<yes/no>` |

| sign-off field | value |
|---|---|
| operator | `<operator-name>` |
| reviewer | `<reviewer-name>` |
| signed_at | `<timestamp>` |
| decision | `<go|pause|no_go|not_evaluated>` |
| required next action | `<summary>` |
| notes | `<sanitized-notes-no-secrets>` |

## 14. Not-production-rollout Statement

This checklist does not authorize production rollout.

This checklist does not authorize Codex to run deployment, start services, run migrations, run API / CLI smoke, write DB or indexes, repair data, backfill, reindex, cleanup, delete, or create production schedulers.

Any real setup, smoke, health-check execution, or deployment record generation must be separately authorized in a later phase and executed by a human operator unless that later phase explicitly says otherwise.
