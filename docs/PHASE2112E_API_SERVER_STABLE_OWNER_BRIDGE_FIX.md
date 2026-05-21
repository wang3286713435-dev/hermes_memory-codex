# Phase 2.112e API Server Stable Owner Bridge Fix

## 1. Review Result

Codex B reviewed Phase 2.112d and found one remaining blocker before runtime baseline.

Phase 2.112d correctly removed alias-global continuity restore and introduced owner-scoped continuity, TTL, stale cleanup, and conflict fail-closed behavior. That closes the cross-user / cross-project safety risk.

However, the OpenAI-compatible API server path still does not pass a stable continuity owner into `AIAgent`.

Observed code shape:

```text
gateway/platforms/api_server.py::_create_agent(...)
  AIAgent(..., session_id=session_id, platform="api_server", ...)
```

It does not pass `gateway_session_key`.

When OpenWebUI sends only the latest user message, `_derive_chat_session_id(...)` may derive a different `api-*` session id per turn. Without a stable owner key, `AIAgent._alias_continuity_owner()` falls back to `process_local_fallback`, which is keyed by the drifting session id. The follow-up therefore still cannot restore `@alias`.

Minimal reproduction result:

```text
scope_resolution_status=alias_missing
alias_continuity_status=not_found
alias_continuity_owner_source=process_local_fallback
suppress_retrieval=True
filters={}
```

## 2. Required Fix

Codex A should preserve the Phase 2.112d safety model and add a bounded stable-owner bridge for the API server path.

Required behavior:

1. API server must pass a safe stable continuity owner into `AIAgent` when one is available.
2. Preferred source: authenticated `X-Hermes-Session-Id` / explicit stable conversation header already accepted by the API server.
3. If adding support for additional OpenWebUI-compatible conversation headers, use only sanitized stable identifiers and document the accepted header names.
4. Do not use volatile request ids, timestamps, raw tokens, raw paths, body text, or aliases as owner keys.
5. If no stable owner is available, keep fail-closed behavior and output a sanitized diagnostic such as `stable_owner_missing`.
6. Do not reintroduce alias-global restore.
7. Do not store alias continuity in ordinary long-term memory.

## 3. Required Tests

Codex A should add or update tests proving:

1. API server passes an explicit stable owner key to `AIAgent`.
2. Same explicit owner can restore `@alias` after `api-*` session drift.
3. Different explicit owners cannot restore each other’s alias.
4. Without a stable owner, follow-up remains fail-closed and diagnostics explain stable owner missing.
5. No raw owner value, token, path, secret, raw row, or content appears in diagnostics.
6. Phase 2.112d TTL / cross-owner / conflict tests still pass.

## 4. Baseline Gate

Do not create a runtime test-candidate tag until:

1. API server stable owner bridge passes targeted tests.
2. Phase 2.112d owner-scope safety tests still pass.
3. Codex B accepts the final diff.
4. Unrelated dirty files are excluded from staging.

After that, test machine can rerun real OpenWebUI / 8642 natural import -> `@alias` retrieval + citation validation.
