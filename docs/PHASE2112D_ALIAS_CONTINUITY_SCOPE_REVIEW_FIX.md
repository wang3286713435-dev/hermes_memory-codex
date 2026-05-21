# Phase 2.112d Alias Continuity Scope Review Fix

## 1. Review Result

Phase 2.112c implementation direction is correct, but Codex B review found one blocker before runtime baseline.

Current implementation stores alias-continuity candidates keyed only by alias. That fixes the immediate OpenWebUI follow-up symptom, but the boundary is too wide for an enterprise agent.

Observed risky shape in Hermes agent:

```text
_alias_continuity: dict[alias, list[FileAliasBinding]]
_continuity_candidates(alias)
_resolve_alias_continuity_reference(... alias ...)
```

Risk:

1. User/session A imports `@建筑类数据样表`.
2. User/session B later asks for `@建筑类数据样表`.
3. If that alias has only one continuity candidate globally, Hermes can restore B's query to A's document.

Even if the candidate is unique, this is not safe enough for the Phase 2 security boundary.

## 2. Required Fix

Codex A should keep the Phase 2.112c feature but narrow the continuity boundary.

Required behavior:

1. Alias continuity must be scoped by a safe continuity owner key, not alias alone.
2. The owner key should prefer stable explicit session / conversation identifiers when available.
3. If no stable key exists, fallback must be short-lived, process-local, and fail-closed on any ambiguity.
4. Persisted continuity records must not create cross-user or cross-project alias recovery.
5. Add TTL / expiration or equivalent stale cleanup for continuity records.
6. Diagnostics must expose only sanitized scope labels, never raw session tokens, paths, secrets, or user-private values.

## 3. Acceptable Scope Key Sources

Preferred:

1. Explicit `X-Hermes-Session-Id` when accepted by the gateway.
2. OpenWebUI / OpenAI-compatible stable conversation id if present and sanitized.
3. A sanitized platform/user/project scope key only if already available and safe.

Fallback:

1. If no stable owner key is available, use a very short-lived process-local recent-import scope.
2. Do not persist unscoped fallback continuity across restarts.
3. If more than one candidate exists for an alias in fallback scope, suppress retrieval and ask for clarification.

Forbidden:

1. Do not persist alias continuity as a global alias-only map.
2. Do not use ordinary long-term memory for alias persistence.
3. Do not treat alias continuity as retrieval evidence.
4. Do not expose raw path, secret, token, raw row, or raw content.

## 4. Required Tests

Codex A should add or update tests proving:

1. Same safe continuity owner can restore `@alias` after API-derived session drift.
2. Different continuity owner cannot restore another owner’s imported alias.
3. Persisted storage does not restore unscoped fallback aliases across a new store load.
4. Fallback continuity expires or is ignored after TTL/stale condition.
5. Conflict candidates still suppress retrieval and require clarification.
6. Import diagnostics and continuity records remain non-evidence.

## 5. Baseline Gate

Do not create a runtime test-candidate tag until:

1. Codex B accepts the scope/TTL fix.
2. Targeted natural import / session scope / gateway tests pass.
3. Unrelated dirty files are excluded from staging.

After that, the test machine can rerun real OpenWebUI / 8642 alias + retrieval + citation validation.
