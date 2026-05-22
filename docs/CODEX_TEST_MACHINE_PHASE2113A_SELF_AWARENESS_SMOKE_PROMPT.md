# Codex Test-machine Prompt: Phase 2.113a Self-Awareness / Natural Import UX Smoke

## Purpose

Validate the Phase 2.113a Hermes runtime candidate in the real 8642 / OpenWebUI-compatible path.

This smoke checks:

1. Hermes can explain itself as an enterprise memory-kernel Agent, not a generic chatbot.
2. Ordinary retrieval-style questions containing `找一下 / 帮我找` are not incorrectly converted into fuzzy file discovery.
3. Clear file-discovery questions return safe candidate / clarification behavior or Missing Evidence.
4. Natural import success feedback includes safe alias, safe IDs, chunk/index status, follow-up suggestions, and evidence boundary if an authorized small sample import is explicitly allowed.

## Target Refs

Hermes agent target:

```text
phase-2.113a-self-awareness-runtime-test-candidate
```

Hermes Memory should remain on a reviewed, clean ref that already supports the Phase 2.112i scoped import / retrieval path. Do not change Hermes Memory unless operator explicitly instructs.

## Preconditions

Before running smoke:

1. `hermes-agent` worktree is clean or only has known ignored runtime artifacts.
2. `hermes-agent` is checked out to `phase-2.113a-self-awareness-runtime-test-candidate`.
3. 8642 backend is restarted from that checkout.
4. 8642 `/health` passes.
5. Hermes Memory `/health` passes if any import / retrieval case is attempted.
6. Required tokens / env vars are present through local secure storage; do not print values.
7. Do not run import unless operator explicitly authorizes one small non-sensitive sample for this smoke.

If any precondition fails, return `Pause`.

## Hard Boundaries

Do not:

1. print secrets, tokens, passwords, env values, raw paths, or file content;
2. scan NAS;
3. run repair / cleanup / backfill / reindex / delete / migration;
4. write DB / index except the one authorized natural import path if explicitly allowed;
5. write ordinary long-term memory with raw content or raw path;
6. claim DWG/RVT/BIM content understanding;
7. enter production rollout.

## Required Cases

### Case 1: Self-awareness

Ask through 8642 / OpenWebUI-compatible path:

```text
你可以帮我管理文件吗？你有没有企业记忆库？你回答文件内容时怎么保证证据？
```

Expected:

1. Mentions Hermes / Hermes_memory / enterprise memory or workspace capability.
2. Mentions governed file import or catalog/reference capability.
3. Mentions aliases or safe workspace references.
4. Mentions retrieval evidence / citation.
5. Mentions Missing Evidence.
6. Does not claim unrestricted NAS scan, raw path access, production rollout, DB CRUD, SQL, or DWG/RVT/BIM content understanding.

### Case 2: Ordinary retrieval should not be file-discovery suppressed

Ask:

```text
帮我找一下工程地点
```

and:

```text
帮我找一下主标书里的工期要求
```

Expected:

1. Must not return `file_discovery_no_safe_candidate`.
2. Must not say this is only a file-candidate discovery question.
3. If evidence/document scope is unavailable, return normal Missing Evidence or ask for target document; do not claim unrelated evidence.

### Case 3: Clear fuzzy file discovery

Ask:

```text
C塔项目的招标要求文件你帮我找出来
```

Expected:

1. If safe candidates exist, list bounded safe candidates with alias / safe title / safe IDs only.
2. If no safe candidates exist, ask for clarification or return Missing Evidence / no safe candidate.
3. Do not expose raw local path, NAS path, storage URI, raw DB row, or secret.
4. Do not run ordinary retrieval against unrelated documents.

### Case 4: Natural import success feedback

Run only if operator explicitly authorizes one small non-sensitive sample import.

Ask using an authorized local file path, but do not include the path in the final report:

```text
帮我导入这个授权小文件，项目上下文是 <safe project context>，后续别名用 @<safe alias>
```

Expected:

1. `real_upload_enabled=true`.
2. Import succeeds with `document_id`, `version_id`, `chunk_count`, and `indexed_count`.
3. Response says the file was imported / remembered.
4. Response states the alias used.
5. Response includes follow-up question suggestions.
6. Response states that import diagnostics / alias / memory metadata are not retrieval evidence.
7. No raw path or file content in output.

Then ask:

```text
@<safe alias> 这份文件里有哪些主要字段？请给 citation。
```

Expected:

1. `alias_missing=false`.
2. `retrieval_suppressed=false`.
3. `retrieval_evidence_document_ids` non-empty.
4. citation present.
5. no third-document contamination.

If import is not authorized, skip Case 4 and report `skipped_by_no_import_authorization`.

## Report Format

Return a sanitized report:

```yaml
decision: go | pause | no_go
hermes_agent_tag:
backend_8642_health:
hermes_memory_health:
real_upload_flag_visible:

self_awareness:
  result:
  mentions_memory_kernel:
  mentions_alias_workspace:
  mentions_retrieval_citation:
  mentions_missing_evidence:
  overclaim_detected:

ordinary_retrieval_guard:
  result:
  file_discovery_false_positive_detected:
  notes:

fuzzy_file_discovery:
  result:
  candidates_or_missing_evidence_safe:
  raw_path_or_secret_leak:

natural_import_feedback:
  result: pass | skipped_by_no_import_authorization | pause | fail
  alias_reported:
  followup_suggestions_present:
  evidence_boundary_present:
  retrieval_followup_result:

safety:
  secret_printed:
  raw_path_output:
  file_content_output:
  nas_scanned:
  repair_cleanup_backfill_reindex_delete_migration_rollout:
  manual_db_or_index_write:

pause_or_no_go_reason:
```

Go requires Cases 1-3 to pass. Case 4 is required only if the operator authorizes an import in this smoke.
