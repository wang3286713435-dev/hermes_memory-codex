# Phase 2.115 Workspace Context Inference / Auto Alias / Fuzzy File Discovery Plan

## 1. Purpose

Phase 2.115 turns natural-language import from a test-style flow into a real enterprise-agent user flow.

Current Phase 2.114 acceptance still allows this operator-style input:

```text
AUTHORIZED_FILE_PATH=...
ALIAS=...
PROJECT_CONTEXT=...
```

That is acceptable for smoke testing, but not for the final Hermes user experience. In real use, the user should be able to say:

```text
帮我导入这个文件：/Users/hermes/import_samples/C塔项目人力配置及成本测算表0506.xlsx。
```

Hermes should infer a safe workspace context, suggest or assign a safe alias, store the file in its workspace registry, and support later fuzzy discovery.

## 2. Product Requirement

`PROJECT_CONTEXT` must become an optional hint, not a required user input.

Hermes should derive `workspace_context` from safe signals:

1. file name / display name;
2. parent folder labels when available, without exposing raw path;
3. current conversation hints;
4. existing session/workspace aliases;
5. platform-provided project/file context when available;
6. optional user wording such as “这是 C塔项目资料”.

If confidence is high enough, Hermes can auto-assign a safe workspace and alias. If confidence is ambiguous, Hermes should ask for confirmation or list candidate workspaces.

## 3. Target User Flow

### 3.1 Import Without Manual Project Context

User:

```text
帮我导入这个文件：/Users/hermes/import_samples/C塔项目人力配置及成本测算表0506.xlsx。
```

Expected Hermes behavior:

```text
文件已导入并记入工作区。

我判断它属于：C塔项目 / 人力配置 / 成本测算。
我为它设置的别名是：@C塔人力成本测算表。

后续你可以这样问：
- @C塔人力成本测算表 这份表有哪些字段？
- 帮我找 C塔项目的人力成本表。

说明：工作区、别名和导入诊断不是正文证据；回答文件内容时仍需要 retrieval evidence 和 citation。
```

Hermes response must include safe diagnostics:

```yaml
workspace_context:
  workspace_id: safe-id
  workspace_name: safe display name
  workspace_type: project | folder | session | unknown
  document_category: safe inferred category or unknown
  confidence: high | medium | low
  needs_user_confirmation: true | false
suggested_alias: "@..."
alias_status: alias_bound | alias_suggested | needs_confirmation
```

### 3.2 Fuzzy File Discovery

User:

```text
C塔项目的招标要求文件你帮我找出来。
```

Expected Hermes behavior:

1. Search safe workspace / alias / imported document registry.
2. Return safe candidates, not raw paths.
3. If multiple candidates exist, ask which one the user means.
4. Do not answer file content until a candidate is selected and retrieval evidence is available.

Example:

```text
我找到几个可能相关的文件：

1. @C塔主标书 — 工作区：C塔项目 / 招标资料
2. @C塔招标答疑 — 工作区：C塔项目 / 招标资料
3. @C塔人力成本测算表 — 工作区：C塔项目 / 成本测算

你说的是哪一个？确认后我再基于 retrieval evidence 回答内容问题。
```

## 4. Data Boundary

Allowed low-sensitive workspace metadata:

1. `workspace_id`
2. `workspace_name`
3. `workspace_type`
4. `document_category`
5. `discipline` when safe
6. `alias`
7. `document_id`
8. `version_id`
9. `related_file_ids` / `related_document_ids`
10. `query_id` / `trace_id`
11. user confirmation flags

Forbidden workspace / memory content:

1. raw storage path;
2. raw NAS path;
3. raw file content;
4. secrets / tokens;
5. raw catalog rows;
6. customer-sensitive material;
7. DWG/RVT/BIM parsed content claims;
8. import diagnostics treated as retrieval evidence.

## 5. Implementation Boundary

Allowed Codex A write scope:

1. `hermes-agent` natural import parsing and response assembly;
2. safe workspace-context inference helper;
3. safe alias suggestion / normalization helper;
4. session/workspace alias registry integration;
5. fuzzy file discovery over safe workspace / alias registry;
6. focused tests and diagnostics.

Forbidden in Phase 2.115:

1. no platform Gateway code changes;
2. no Hermes Memory ingestion/retrieval contract change unless parser-only fix is proven insufficient;
3. no DB schema change;
4. no OpenSearch/Qdrant contract change;
5. no NAS scan;
6. no DWG/RVT/BIM content parsing;
7. no production rollout;
8. no long-term memory write of raw path or file content.

## 6. Required Tests

Codex A must add or update tests for:

1. import prompt with only path, no alias, no project context;
2. safe workspace context inferred from file name;
3. safe alias generated and bound;
4. optional explicit alias still overrides generated alias;
5. ambiguous workspace context returns confirmation instead of overclaim;
6. same-session follow-up by generated alias returns retrieval evidence + citation;
7. fuzzy file discovery returns safe candidates and asks clarification for multiple matches;
8. ordinary content retrieval is not misclassified as file discovery;
9. diagnostics / workspace metadata are not treated as retrieval evidence;
10. raw path is not printed in final answer.

## 7. Test-machine Acceptance

A later test-machine smoke should use only:

```text
AUTHORIZED_FILE_PATH=/Users/hermes/import_samples/<safe-small-file>
```

The user-facing OpenWebUI prompt should omit `ALIAS` and `PROJECT_CONTEXT`:

```text
帮我导入这个文件：/Users/hermes/import_samples/C塔项目人力配置及成本测算表0506.xlsx。
```

Go requires:

1. import succeeds;
2. Hermes reports generated safe alias;
3. Hermes reports inferred `workspace_context`;
4. follow-up retrieval by generated alias succeeds with evidence + citation;
5. fuzzy query can find the imported file as a candidate;
6. no raw path / file content / secret / NAS scan / forbidden write.

## 8. Phase Interpretation

Phase 2.115 is still part of Phase 2 stable closeout because it closes a user-experience gap exposed by real OpenWebUI usage.

It does not make Hermes production-ready and does not claim unrestricted enterprise NAS governance. It makes the current MVP feel like an enterprise Agent instead of a test harness.
