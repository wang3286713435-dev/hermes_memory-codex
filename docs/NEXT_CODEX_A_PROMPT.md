# NEXT_CODEX_A_PROMPT

## Phase 2.115 Runtime Test-candidate Validation Handoff

You are Codex A, the Hermes runtime development agent.

Phase 2.115 local implementation candidate is complete in Hermes main. Do not reimplement it unless Codex B or Codex C returns a concrete blocker.

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

Local candidate implemented:

1. workspace context inference from safe filename / folder labels / query;
2. safe generated alias such as `@C塔人力成本测算表`;
3. workspace metadata stored on session alias bindings and continuity;
4. fuzzy file discovery over safe workspace / alias candidates;
5. import success response shows workspace / alias diagnostics and hides raw path;
6. diagnostics are marked as non-evidence.

Local validation:

```text
git diff --check: pass
py_compile: pass
natural import / runtime / session scope regression: 129 passed
```

Expected runtime candidate:

```text
tag: phase-2.115-workspace-auto-alias-runtime-test-candidate
```

## Next Required Action

Do not implement more functionality. The next action is Codex B review and Codex C / test-machine validation.

Validate the real OpenWebUI / 8642 flow with an authorized small non-sensitive file:

```text
帮我导入这个文件：<AUTHORIZED_FILE_PATH_TO_C塔项目人力配置及成本测算表0506.xlsx>
```

Do not provide `PROJECT_CONTEXT`.
Do not provide an explicit `ALIAS`.

Expected behavior:

1. import succeeds through the authorized natural import pipeline;
2. response includes safe `workspace_context`;
3. response suggests and binds a safe alias, preferably `@C塔人力成本测算表` or equivalent safe normalized alias;
4. raw path is not printed;
5. follow-up by generated alias returns retrieval evidence and citation;
6. fuzzy query such as `帮我找 C塔项目的人力成本表` returns the imported file as a safe candidate or resolves it without third-file contamination;
7. workspace / alias diagnostics are not treated as retrieval evidence.

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

## Validation Required Before Handoff

If Codex C returns Pause, capture:

1. API / 8642 / CLI status;
2. generated alias;
3. workspace_context;
4. document_id / version_id;
5. follow-up retrieval evidence ids and citations;
6. fuzzy discovery trace;
7. any raw-path leak or third-document contamination.

Do not patch code until a concrete blocker is documented.

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
