# Phase 2.112h Explicit Natural Import Alias Preservation Fix

## 1. Background

Phase 2.112g fixed header-only `X-Hermes-Session-Id` stable-owner restore at the development-machine level, but test-machine OpenWebUI / 8642 validation still returned Pause.

Latest test-machine evidence:

```text
hermes-agent HEAD: 20d9fb561bf680cfbf8d1a786b2e504358f9ca7d
tag: phase-2.112g-header-owner-restore-runtime-test-candidate
worktree clean: true
8642 backend: pass
real upload flag visible: true

explicit alias import: partial
chunk_count: 6
indexed_count: 6
import_alias_status: alias_bound
import_alias_continuity_status: stored
import_alias_continuity_owner_source: gateway_session_key
import_alias_continuity_persistent: true

requested alias: @建筑类数据样表
follow-up alias_resolution.status: alias_missing
alias_missing: true
retrieval_suppressed: true
retrieval_evidence_document_ids: []
citation_present: false
```

Key finding:

```text
Import succeeded and bound an alias, but not the user-requested @建筑类数据样表.
```

## 2. Codex B Diagnosis

Phase 2.112g appears to have fixed the stable-owner path, but the natural import parser / runtime did not preserve the explicit user-requested alias.

Likely root cause:

1. `agent/memory_kernel/natural_file_import.py::_ALIAS_RE` only supports a narrow form such as `绑定为 @alias`, `命名为 @alias`, `叫 @alias`.
2. Real OpenWebUI user phrasing can be more natural, for example `别名 @建筑类数据样表`, `别名为 @建筑类数据样表`, `别名设为 @建筑类数据样表`, `后续别名叫 @建筑类数据样表`, or `我想叫它 @建筑类数据样表`.
3. When explicit alias parsing misses, `natural_file_import_flow.py` generates a safe alias from title/file name.
4. The follow-up asks for the user-requested alias, not the generated alias, so alias continuity restore correctly misses.

This is an explicit alias parsing / alias preservation bug, not another stable-owner bug.

## 3. Required Fix

Codex A should implement the smallest safe fix so natural import preserves user-requested aliases across common natural-language phrasings.

Required behavior:

1. Parse explicit aliases from common Chinese phrases, including at least:
   - `绑定为 @建筑类数据样表`
   - `绑定成 @建筑类数据样表`
   - `命名为 @建筑类数据样表`
   - `取名为 @建筑类数据样表`
   - `别名 @建筑类数据样表`
   - `别名为 @建筑类数据样表`
   - `别名叫 @建筑类数据样表`
   - `别名设为 @建筑类数据样表`
   - `设定别名为 @建筑类数据样表`
   - `我想叫它 @建筑类数据样表`
2. Preserve the exact normalized requested alias without the leading `@`.
3. When explicit alias is present, do not replace it with generated alias.
4. Import diagnostics must show the requested alias in `alias_resolution.alias`.
5. Follow-up `@建筑类数据样表` must restore to the imported `document_id/version_id` in tests.

## 4. Safety Rules

Keep all previous safety boundaries:

1. No alias-global restore.
2. No ordinary long-term memory alias persistence.
3. No raw path / owner / token / file content in diagnostics.
4. No fuzzy global file search for alias binding.
5. No DB / index / NAS writes beyond the already authorized upload path in real test-machine validation.
6. Import diagnostics remain non-evidence.
7. Facts / metadata / snapshot / transcript cannot replace retrieval evidence.

## 5. Expected Code Areas

Likely files:

1. `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/natural_file_import.py`
2. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import.py`
3. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_flow.py`
4. `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_natural_file_import_runtime.py`
5. `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
6. `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

If other runtime files are touched, Codex A must explain why.

## 6. Required Tests

Run:

```bash
cd /Users/Weishengsu/.hermes/hermes-agent
./.venv/bin/python -m py_compile agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/session_document_scope.py run_agent.py gateway/platforms/api_server.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_session_document_scope.py tests/agent/test_natural_file_upload_adapter.py tests/agent/test_hermes_memory_upload_client.py -q
```

Add/update tests for:

1. each accepted alias phrase listed above;
2. requested alias wins over generated alias;
3. diagnostics show requested alias;
4. import alias persistence uses requested alias;
5. follow-up `@建筑类数据样表` resolves after import with requested alias;
6. malformed aliases remain fail-closed / not requested.

## 7. Stop Condition

Stop after the bounded fix and local tests.

Do not tag or push unless Codex B explicitly approves after review.

Phase 2 natural import closeout remains blocked until the test machine proves:

```text
OpenWebUI / 8642 import with requested @建筑类数据样表 -> follow-up @建筑类数据样表 retrieval -> retrieval_evidence_document_ids non-empty -> citation present
```
