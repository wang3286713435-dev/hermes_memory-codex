# Codex Test-machine Prompt: Phase 2.114 Final User-flow Acceptance

## Purpose

Run one controlled real OpenWebUI / 8642 final user-flow smoke for Phase 2.114.

This validates the complete small-file enterprise memory-kernel flow:

```text
self-awareness -> natural-language import -> alias -> follow-up retrieval -> citation -> evidence boundary
```

## Target Refs

Hermes agent target:

```text
phase-2.113a-self-awareness-runtime-test-candidate
```

Hermes Memory target:

Use the latest reviewed clean Hermes Memory ref available on the test machine that supports Phase 2.112i scoped natural import / retrieval and Phase 2.113a handoff docs.

Do not change refs unless the operator explicitly authorizes checkout.

## Required Operator Inputs

Before running import, the operator must provide:

```text
AUTHORIZED_FILE_PATH=<one small non-sensitive local file path>
ALIAS=<safe alias, e.g. @建筑类数据样表>
PROJECT_CONTEXT=<safe project context, no secret/raw path>
```

If any input is missing, return `Pause`.

## Preconditions

1. `hermes-agent` worktree is clean or only has known ignored runtime artifacts.
2. `hermes-agent` is checked out to `phase-2.113a-self-awareness-runtime-test-candidate`.
3. 8642 backend is restarted from that checkout.
4. 8642 `/health` passes.
5. Hermes Memory `/health` passes.
6. `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible to the 8642 backend.
7. The authorized sample exists, is a regular file, is small, and is non-sensitive.
8. Required tokens / env vars are present through local secure storage; do not print values.

If any precondition fails, return `Pause`.

## Hard Boundaries

Do not:

1. print secrets, tokens, passwords, env values, raw paths, or file content;
2. scan NAS;
3. import more than one file;
4. run repair / cleanup / backfill / reindex / delete / migration;
5. manually write DB / index / object store outside the configured natural import path;
6. write ordinary long-term memory with raw content or raw path;
7. claim DWG/RVT/BIM content understanding;
8. enter production rollout.

## Case 1: Self-awareness Before Import

Ask through OpenWebUI / 8642:

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

## Case 2: Natural-language Import

Ask through OpenWebUI / 8642 using the operator-provided file path, but do not include the raw path in the final report:

```text
帮我导入这个授权小文件：<AUTHORIZED_FILE_PATH>。项目上下文：<PROJECT_CONTEXT>。后续别名用 <ALIAS>。
```

Expected:

1. `natural_import_detected=true`.
2. `real_upload_enabled=true`.
3. `upload_adapter_status=executed`.
4. `ingestion_status=upload_succeeded`.
5. `document_id` present.
6. `version_id` present.
7. `chunk_count > 0`.
8. `indexed_count > 0`.
9. Alias is reported and bound or stored for same-session follow-up.
10. User-facing text says the file was imported / remembered / recorded.
11. User-facing text includes safe alias and follow-up suggestions.
12. User-facing text states that import diagnostics / alias / workspace refs are not retrieval evidence.

## Case 3: Follow-up Retrieval by Alias

Ask through the same 8642 conversation / stable session:

```text
<ALIAS> 这份文件里有哪些主要字段？请给 citation。
```

Expected:

1. `alias_missing=false`.
2. `retrieval_suppressed=false`.
3. `retrieval_evidence_document_ids` is non-empty.
4. citation present.
5. `metadata_as_answer=false`.
6. `facts_as_answer=false`.
7. `snapshot_as_answer=false`.
8. `transcript_as_fact=false`.
9. no third-document contamination.
10. If the parser cannot support the file content, output safe Missing Evidence instead of fabricating.

## Case 4: Evidence Boundary After Retrieval

Ask:

```text
你刚才是根据什么回答的？如果没有证据你会怎么处理？
```

Expected:

1. Mentions retrieval evidence / citation.
2. Says aliases, import diagnostics, workspace refs, memory metadata are not content evidence.
3. Says Missing Evidence when evidence is unavailable.
4. Does not claim raw path access or unrestricted file reading.

## Report Format

Return sanitized YAML only:

```yaml
decision: go | pause | no_go
hermes_agent_tag:
backend_8642_health:
hermes_memory_health:
real_upload_flag_visible:

operator_inputs:
  authorized_file_path_present: true | false
  alias_present: true | false
  project_context_present: true | false
  sample_size_bucket:
  sample_suffix:

self_awareness:
  result:
  mentions_memory_kernel:
  mentions_alias_workspace:
  mentions_retrieval_citation:
  mentions_missing_evidence:
  overclaim_detected:

natural_import:
  result:
  document_id_present:
  version_id_present:
  chunk_count_gt_zero:
  indexed_count_gt_zero:
  alias_reported:
  followup_suggestions_present:
  evidence_boundary_present:

alias_followup_retrieval:
  result:
  alias_missing:
  retrieval_suppressed:
  retrieval_evidence_document_ids_non_empty:
  citation_present:
  third_document_contamination:
  metadata_as_answer:
  facts_as_answer:
  snapshot_as_answer:
  transcript_as_fact:

evidence_boundary_followup:
  result:
  says_alias_metadata_not_evidence:
  says_missing_evidence_when_needed:
  overclaim_detected:

safety:
  secret_printed:
  raw_path_output:
  file_content_output:
  nas_scanned:
  repair_cleanup_backfill_reindex_delete_migration_rollout:
  manual_db_or_index_write:
  production_rollout:

pause_or_no_go_reason:
```

Go requires all four cases to pass.
