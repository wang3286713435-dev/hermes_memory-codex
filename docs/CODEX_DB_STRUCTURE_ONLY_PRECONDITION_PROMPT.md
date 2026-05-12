# Codex Test-machine DB Structure-only Precondition Prompt

## Purpose

This prompt is for the test-machine Codex/operator to check whether the machine is ready to rerun `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`.

This is a precondition check only. It must not connect to the database, execute SQL, read rows, install tools, or print secrets.

## Context

The previous test-machine `structure_only` smoke returned `Pause` safely:

1. Hermes_memory install / version was not confirmed.
2. DB host / port / database / readonly credential key names were not found in checked secure environment keys.
3. Direct mysql client was unavailable.
4. No DB connection was attempted.
5. No SQL was executed.
6. No real rows were read.
7. No secret or true business data was printed.
8. No writes were performed.

## Allowed Checks

Check only:

1. Hermes_memory install directory exists.
2. Hermes_memory current branch / HEAD / tag / dirty state.
3. Required secure env key names exist, without printing values.
4. DB host key name exists, without printing value.
5. DB port key name exists, without printing value.
6. DB database key name exists, without printing value.
7. Readonly username / API key identifier exists, without printing secret.
8. Readonly credential secret key exists, without printing value.
9. Contract version key or operator confirmation exists for `delivery_platform.asset_views.v1`.
10. `mysql --version` or equivalent MySQL client is available.
11. Hermes_memory readonly structure tooling exists.

If a tool is missing, report `Pause` and list the missing tool. Do not install it.

## Forbidden Actions

Do not:

1. Connect to MySQL.
2. Execute SQL.
3. Read real rows.
4. Print `.env` values or credential values.
5. Print secret, token, password, API key, or connection string.
6. Print true project names, file names, NAS paths, `asset_uid`, `source_id`, raw rows, or SQL stderr.
7. Scan NAS.
8. Write platform DB.
9. Write Hermes Memory DB.
10. Write OpenSearch / Qdrant / MinIO.
11. Enable Data Steward runtime feature flags.
12. Install tools.
13. Modify business code.
14. Run migration / repair / backfill / reindex / cleanup / delete.
15. Execute DB CRUD.
16. Enter production rollout.

## Suggested Safe Commands

Use only commands equivalent to:

```bash
pwd
git status --short
git branch --show-current
git rev-parse --short HEAD
git tag --points-at HEAD
test -d /path/to/Hermes_memory && echo hermes_memory_dir_present
command -v mysql >/dev/null && mysql --version
python - <<'PY'
import os
for key in [
    "PLATFORM_ASSET_READONLY_DB_HOST",
    "PLATFORM_ASSET_READONLY_DB_PORT",
    "PLATFORM_ASSET_READONLY_DB_DATABASE",
    "PLATFORM_ASSET_READONLY_DB_USER",
    "PLATFORM_ASSET_READONLY_DB_PASSWORD",
    "PLATFORM_ASSET_READONLY_DB_CONTRACT_VERSION",
]:
    print(f"{key}: {'present' if os.environ.get(key) else 'missing'}")
PY
```

Do not print environment values.

## Report Fields

Return a sanitized report:

1. `status`: `go` / `pause` / `no_go`.
2. `hermes_memory_path_checked`: boolean.
3. `hermes_memory_head`: short commit only.
4. `hermes_memory_tag`: tag name only, if present.
5. `hermes_memory_dirty`: boolean.
6. `secure_env_keys_present`: list of key names only.
7. `secure_env_keys_missing`: list of key names only.
8. `mysql_client_available`: boolean.
9. `hermes_readonly_tooling_available`: boolean.
10. `contract_version_expected`: `delivery_platform.asset_views.v1`.
11. `secret_printed`: must be `false`.
12. `db_connected`: must be `false`.
13. `sql_executed`: must be `false`.
14. `real_rows_read`: must be `false`.
15. `writes_performed`: must be `false`.
16. `next_recommendation`.

## Go / Pause / No-Go

Go:

1. Hermes_memory install / version is confirmed.
2. Required DB key names are present.
3. Readonly credential key name is present.
4. Credential values were not printed.
5. MySQL client or Hermes readonly tooling is available.
6. Operator can rerun `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`.

Pause:

1. Hermes_memory path / version is unclear.
2. Any required key name is missing.
3. Credential is not injected.
4. MySQL client and Hermes readonly tooling are both unavailable.

No-Go:

1. Secret value was printed.
2. SQL was executed.
3. DB connection was attempted.
4. Real rows or business data were read or printed.
5. Any write / migration / repair / rollout was attempted.

## Final Instruction

If status is `Go`, do not automatically run DB smoke. Return the report and wait for the user to explicitly rerun `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`.
