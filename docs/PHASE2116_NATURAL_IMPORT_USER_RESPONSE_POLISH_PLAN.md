# Phase 2.116 Natural Import User-facing Response Polish Plan

## 1. Purpose

Phase 2.115 proved the core enterprise-Agent workflow:

```text
natural-language import -> inferred workspace -> generated alias -> retrieval citation -> fuzzy discovery
```

However, the user-facing import response still exposes too much developer diagnostics. That makes Hermes feel like a backend trace tool instead of a company kernel Agent.

Phase 2.116 fixes only the response presentation layer.

## 2. Current Accepted Behavior

The following real OpenWebUI / 8642 flow passed:

1. User asked Hermes to import a file without `PROJECT_CONTEXT` or explicit `ALIAS`.
2. Hermes inferred:
   - workspace: `C塔项目`
   - category: `人力配置 / 成本测算`
   - alias: `@C塔人力成本测算表`
3. Import succeeded and indexed one chunk.
4. Follow-up by alias returned retrieval evidence and citation.
5. Fuzzy query `帮我找 C塔项目的人力成本表` found the imported file.

## 3. Problem

Hermes still prints a large block like:

```text
Natural file import diagnostics:
- natural_import_detected=true
- real_upload_enabled=true
- upload_adapter_status=executed
...
```

This is useful for Codex / test-machine validation, but it is not acceptable as the default user-facing answer.

## 4. Target User-facing Success Response

For a successful import, Hermes should answer like:

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

It may include safe IDs only in debug / test-machine mode, not in default user mode.

## 5. Target User-facing Failure Response

For a file-not-found import failure, Hermes should answer like:

```text
我识别到你想导入一份文件，并判断它可能属于：C塔项目 / 人力配置 / 成本测算。

但我现在无法读取到这个文件。通常是因为这个路径对 Hermes 后端不可见。

你可以把文件放到 Hermes 授权导入目录，例如：
/Users/hermes/import_samples/

然后再对我说：
帮我导入这个文件：/Users/hermes/import_samples/文件名.docx。
```

It must not dump raw diagnostics by default.

## 6. Target Fuzzy Discovery Response

For fuzzy discovery, Hermes should default to a product-facing candidate list:

```text
我找到了一个可能相关的文件：

1. @C塔人力成本测算表 — 工作区：C塔项目 / 人力配置 / 成本测算

你可以直接问：
@C塔人力成本测算表 这份文件有哪些重点？
```

Default user response should hide developer fields such as `document_id`, `version_id`, `chunk_count`, `workspace_id`, unless the user explicitly asks for technical diagnostics.

## 7. Diagnostics Boundary

Diagnostics must remain available for tests / Codex validation, but should not be dumped in normal user mode.

Allowed implementation patterns:

1. add a `debug` / `include_diagnostics` render option;
2. keep diagnostics in `response.diagnostics` while rendering concise `final_response`;
3. expose sanitized diagnostics only when explicitly requested by test harness or environment flag.

Do not remove diagnostics from code paths that tests rely on. Only change default rendering behavior.

## 8. Allowed Write Scope

Prefer minimal changes in `hermes-agent`:

1. natural import response renderer;
2. fuzzy discovery / file candidate response rendering if currently too technical;
3. tests for user-facing copy and diagnostics preservation.

## 9. Forbidden Scope

1. Do not change upload adapter behavior.
2. Do not change ingestion/indexing logic.
3. Do not change retrieval contract.
4. Do not change workspace inference logic unless needed only for rendering.
5. Do not change platform Gateway code.
6. Do not scan NAS.
7. Do not parse DWG/RVT/BIM content.
8. Do not write raw path / raw content / secret into memory.
9. Do not remove diagnostics needed by test-machine / Codex validation.

## 10. Required Tests

Codex A should add or update tests proving:

1. successful import default response does not include `Natural file import diagnostics:`;
2. successful import default response includes workspace, category, alias, and follow-up suggestions;
3. successful import response does not show raw path;
4. diagnostics remain present in `response.diagnostics`;
5. file-not-found response is human-readable and gives the authorized import directory hint;
6. file-not-found response does not dump all diagnostics;
7. fuzzy discovery default response hides `document_id`, `version_id`, `chunk_count`, `workspace_id` unless debug mode is requested;
8. evidence boundary copy remains visible.

## 11. Acceptance

Go requires:

1. core 2.115 import / alias / retrieval / fuzzy discovery behavior unchanged;
2. normal OpenWebUI import success response is concise and product-facing;
3. diagnostics are still available for automated validation;
4. no raw path, raw content, secret, NAS scan, repair/reindex/rollout, or manual DB/index write.
