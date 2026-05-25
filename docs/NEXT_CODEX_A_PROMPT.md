# NEXT_CODEX_A_PROMPT

## Phase 2.116 Natural Import User-facing Response Polish

You are Codex A, the Hermes runtime development agent.

Phase 2.115 core workflow passed in the real OpenWebUI / 8642 path: natural import inferred workspace, generated alias, follow-up retrieval returned citation, and fuzzy discovery found the imported file.

The remaining blocker is user experience: Hermes still prints large `Natural file import diagnostics` blocks to normal users.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2116_NATURAL_IMPORT_USER_RESPONSE_POLISH_PLAN.md`
5. `docs/PHASE2115_WORKSPACE_CONTEXT_AUTO_ALIAS_PLAN.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Current State

Accepted real behavior:

1. user imports without `PROJECT_CONTEXT` or explicit `ALIAS`;
2. Hermes infers `workspace_context`;
3. Hermes generates `@C塔人力成本测算表`;
4. import succeeds;
5. alias retrieval returns evidence + citation;
6. fuzzy query finds the imported file.

Problem:

Hermes still renders internal diagnostics in the default user answer.

## Required Fix

Change only the default user-facing rendering layer.

For successful import, default response should be concise and product-facing:

```text
文件我已经记下了。

我把它放入了：
- 工作区：C塔项目
- 分类：人力配置 / 成本测算
- 别名：@C塔人力成本测算表

后续你可以直接问：
- @C塔人力成本测算表 这份文件有哪些重点？
- 帮我找 C塔项目的人力成本表

说明：工作区和别名只是定位信息；回答文件内容时我仍会基于 retrieval evidence 和 citation。
```

For file-not-found / source path invisible failure, default response should be human-readable:

```text
我识别到你想导入一份文件，并判断它可能属于：C塔项目 / 人力配置 / 成本测算。

但我现在无法读取到这个文件。通常是因为这个路径对 Hermes 后端不可见。

你可以把文件放到 Hermes 授权导入目录，例如：
/Users/hermes/import_samples/

然后再对我说：
帮我导入这个文件：/Users/hermes/import_samples/文件名.docx。
```

Do not dump the whole diagnostics block by default.

## Diagnostics Requirement

Diagnostics must remain available for tests / Codex validation.

Allowed approaches:

1. keep diagnostics in `response.diagnostics`;
2. add an explicit debug render mode / include diagnostics option;
3. preserve machine-readable fields for test harnesses without printing them in normal user text.

## Fuzzy Discovery Polish

Default fuzzy file discovery response should hide developer fields like:

```text
document_id
version_id
chunk_count
workspace_id
```

unless debug mode or explicit user request asks for technical IDs.

Default should show:

```text
@alias — 工作区：workspace / category
```

## Allowed Write Scope

Prefer minimal changes in `hermes-agent`:

1. natural import response renderer;
2. fuzzy discovery/file candidate renderer if needed;
3. tests for user-facing copy and diagnostics preservation.

## Required Tests

Add or update tests proving:

1. successful import default response does not include `Natural file import diagnostics:`;
2. successful import default response includes workspace, category, alias, and follow-up suggestions;
3. successful import response does not show raw path;
4. diagnostics remain present in `response.diagnostics`;
5. file-not-found response is human-readable and gives authorized import directory hint;
6. file-not-found response does not dump all diagnostics;
7. fuzzy discovery default response hides `document_id`, `version_id`, `chunk_count`, `workspace_id` unless debug mode is requested;
8. evidence boundary copy remains visible;
9. core import / generated alias / retrieval / fuzzy discovery behavior remains unchanged.

## Forbidden Actions

1. Do not change upload adapter behavior.
2. Do not change ingestion/indexing logic.
3. Do not change retrieval contract.
4. Do not change workspace inference logic unless needed only for rendering.
5. Do not change platform Gateway code.
6. Do not scan NAS.
7. Do not parse DWG/RVT/BIM content.
8. Do not write raw path / raw content / secret into memory.
9. Do not remove diagnostics needed by test-machine / Codex validation.
10. Do not run production rollout.
