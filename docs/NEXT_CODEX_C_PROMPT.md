# NEXT_CODEX_C_PROMPT

## Pending Authorization Template: Phase 2.59 Natural Import Second Real Smoke

当前 Codex C 不得执行本测试。必须等待用户明确提供 `<AUTHORIZED_FILE_PATH>` 并授权真实 natural import smoke 后，才可替换占位符并运行。

## 待替换字段

- `<AUTHORIZED_FILE_PATH>`：用户明确授权的小型非敏感文件路径。
- `<ALIAS>`：本次导入后要绑定和检索的 alias。
- `<OPERATOR>`：执行真实终端验收的人。

## 授权后目标

1. 使用 Hermes CLI 自然语言导入 path 上传一个小型非敏感文件。
2. 验证同一 session 内 alias persisted 与 retrieval citation。
3. 记录 document/version/chunk/index 与安全 flags。
4. 保存 ignored sanitized run record。

## 硬边界

1. 不允许 direct API upload 替代 Hermes CLI natural-language import path。
2. 不允许 cleanup / delete / repair / backfill / reindex / migration。
3. 不允许 production rollout。
4. 不允许批量导入、目录扫描、NAS / TB / BIM 文件池。
5. 不允许提交真实 source file、真实 evidence JSON、local latest 指针或 operator 敏感备注。

## 授权后执行步骤

1. 检查 Hermes_memory API `/health`。
2. 检查 Hermes CLI：`hermes chat --help`。
3. 新建 session，并记录 `session_id`。
4. source file preflight：
   - path: `<AUTHORIZED_FILE_PATH>`
   - exists
   - regular file
   - size
   - suffix
5. 生成 dry-run evidence template：

```bash
uv run python scripts/phase257a_natural_import_evidence_template.py \
  --source-path "<AUTHORIZED_FILE_PATH>" \
  --alias "<ALIAS>" \
  --session-id "<SESSION_ID>" \
  --operator "<OPERATOR>"
```

6. 对 dry-run JSON 执行 review：

```bash
uv run python scripts/phase257a_natural_import_evidence_template.py \
  --review-json "<DRY_RUN_EVIDENCE_JSON>"
```

7. 只有 `go_pause_no_go=ReadyForAuthorizedSmoke` 且 `review_status=ready_for_operator_authorization` 时，才继续真实 smoke。
8. 通过 Hermes CLI 自然语言导入 `<AUTHORIZED_FILE_PATH>`，并绑定 `<ALIAS>`。
9. 在同一 session 里围绕 `<ALIAS>` 做 retrieval smoke。
10. 保存 sanitized run record 到 ignored reports path。
11. 输出 Go / Pause / No-Go。

## 授权后验收表

| 项目 | 结果 |
|---|---|
| API `/health` |  |
| Hermes CLI |  |
| session_id |  |
| source exists / size / suffix |  |
| dry-run `go_pause_no_go` |  |
| review-json `review_status` |  |
| natural import path used |  |
| direct API upload used | must be false |
| document_id |  |
| version_id |  |
| chunk_count |  |
| indexed_count |  |
| alias | `<ALIAS>` |
| alias persisted |  |
| same-session returned_document_ids |  |
| returned only new document |  |
| citation visible |  |
| third-document contamination | must be false |
| metadata_as_answer | must be false |
| facts_as_answer | must be false |
| snapshot_as_answer | must be false |
| transcript_as_fact | must be false |
| cleanup / repair / backfill / reindex / rollout attempted | must be false |
| ignored sanitized run record path |  |
| Go / Pause / No-Go |  |

## Stop Conditions

- API or CLI unavailable.
- Source path missing or not a regular file.
- Dry-run template does not return `ReadyForAuthorizedSmoke`.
- Review helper does not return `ready_for_operator_authorization`.
- Natural import parser does not trigger.
- Direct API upload is used as substitute evidence.
- Alias does not persist.
- Retrieval lacks citation.
- Third-document contamination appears.
- Any cleanup, delete, repair, backfill, reindex, migration, or rollout is attempted.

当前状态：未授权，不执行。
