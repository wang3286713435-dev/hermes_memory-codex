# NEXT_CODEX_A_PROMPT

## Phase 2.115 Workspace Context Inference / Auto Alias / Fuzzy File Discovery

You are Codex A, the Hermes runtime development agent.

Phase 2.114a final user-flow acceptance returned Go. The remaining user-experience gap is that real natural-language import still feels like a test harness because users must provide `PROJECT_CONTEXT` and often explicit alias text.

Implement Phase 2.115 so Hermes can infer workspace context, generate a safe alias, store the imported file in its workspace/alias registry, and later find it through fuzzy file discovery.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2115_WORKSPACE_CONTEXT_AUTO_ALIAS_PLAN.md`
5. `docs/PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PLAN.md`
6. `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`
7. `docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`
8. `eval/phase2_inventory/phase2_final_freeze_checklist.json`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

## Current State

Phase 2.114a passed in the real OpenWebUI / 8642 path:

```text
path extraction -> natural import -> alias -> same-session retrieval -> evidence IDs -> citation
```

However, the accepted test flow still relies on operator-style fields:

```text
AUTHORIZED_FILE_PATH=...
ALIAS=...
PROJECT_CONTEXT=...
```

This is not the final enterprise-agent experience.

## Required Product Behavior

Hermes should support this user prompt without manual alias or project context:

```text
帮我导入这个文件：/Users/hermes/import_samples/C塔项目人力配置及成本测算表0506.xlsx。
```

Expected Hermes behavior:

1. infer a safe `workspace_context` from the filename, folder labels, current conversation, and existing workspace/alias registry;
2. generate a safe alias, for example `@C塔人力成本测算表`;
3. import the file through the existing authorized natural import pipeline;
4. bind the generated alias to the imported `document_id/version_id`;
5. report the workspace and alias to the user;
6. explain that workspace/alias/import diagnostics are not retrieval evidence;
7. support same-session follow-up retrieval by the generated alias;
8. support fuzzy file discovery such as `帮我找 C塔项目的人力成本表`.

## Required Output Shape

Import success should include safe diagnostics similar to:

```yaml
workspace_context:
  workspace_id: safe-id
  workspace_name: C塔项目
  workspace_type: project
  document_category: 人力配置 / 成本测算
  confidence: high | medium | low
  needs_user_confirmation: true | false
suggested_alias: "@C塔人力成本测算表"
alias_status: alias_bound | alias_suggested | needs_confirmation
```

Do not print raw path. Do not treat workspace metadata as content evidence.

## Fuzzy File Discovery Behavior

For a query like:

```text
C塔项目的招标要求文件你帮我找出来。
```

Hermes should:

1. search safe workspace / alias / imported document candidates;
2. list safe candidate aliases and safe workspace labels;
3. ask the user to choose when multiple candidates match;
4. avoid answering file content until a selected candidate has retrieval evidence;
5. avoid raw path, raw file content, and secret output.

## Allowed Write Scope

Prefer minimal changes in `hermes-agent`:

1. natural import parsing / response assembly;
2. workspace-context inference helper;
3. alias suggestion / normalization helper;
4. session/workspace alias registry integration;
5. fuzzy file discovery over safe workspace / alias registry;
6. focused tests and diagnostics.

Do not modify platform Gateway code. Do not modify Hermes Memory ingestion/retrieval contract unless you first prove the agent-side workspace/alias layer cannot solve the problem.

## Required Tests

Add or update focused tests covering:

1. import prompt with only an authorized absolute path, no alias and no project context;
2. workspace context inferred from safe filename/folder labels;
3. generated alias is safe and bound to imported document/version;
4. explicit alias still overrides generated alias;
5. ambiguous workspace context requests confirmation instead of overclaiming;
6. same-session follow-up by generated alias returns retrieval evidence + citation;
7. fuzzy file discovery returns safe candidates and asks clarification for multiple matches;
8. ordinary retrieval prompts are not misclassified as fuzzy file discovery;
9. workspace metadata / import diagnostics are never treated as retrieval evidence;
10. final answer does not print raw path.

## Validation Required Before Handoff

Run:

1. py_compile for touched files;
2. targeted natural import / workspace / fuzzy discovery tests;
3. relevant regression tests that protected ordinary retrieval and alias continuity.

Then publish a runtime test-candidate tag for test-machine validation.

## Forbidden Actions

1. Do not run production rollout.
2. Do not scan NAS.
3. Do not import more than one file in smoke paths.
4. Do not write DB / facts / document_versions / OpenSearch / Qdrant outside the configured authorized import pipeline.
5. Do not repair / cleanup / backfill / reindex / delete / migrate.
6. Do not modify memory kernel main architecture.
7. Do not treat diagnostics, aliases, workspace refs, or memory metadata as retrieval evidence.
8. Do not claim DWG/RVT/BIM content understanding.
9. Do not write raw path / raw content / secret / customer-sensitive material into memory.
10. Do not stage unrelated `uv.lock`, adapter reload, repo-hygiene, shared-doc import, or runtime artifact files.
