# Local PR Proposal: Alias Binding UX Follow-up

## Status

This is a local PR-style proposal only.

It is meant to inform later mainline Hermes agent work without changing current mainline behavior today.

It is not:

1. a production rollout request
2. an authorization to change retrieval contract
3. an authorization to change memory kernel main architecture
4. an instruction to bypass current MVP evidence boundaries

## Context

During the first controlled MVP validation on the Mac mini test machine, the operator experience exposed a usability tail:

1. file alias binding works
2. session memory and alias persistence work
3. but the human wording needed to bind files is still not intuitive enough

In particular, a natural instruction like:

```text
把当前主标书设为 @主标书
```

may fail in practice when the current session does not already have a stable active document, even though the underlying feature itself exists.

## Observed Problem

Current behavior is technically correct but operationally awkward:

1. users do not naturally know whether they are in a session with an active document already locked
2. users do not know whether they should say:
   - `把《主标书》设为 @主标书`
   - `把当前主标书设为 @主标书`
   - `请把上一轮已锁定的当前文件设为 @主标书`
3. when binding fails, the failure message can feel like “file not found”, even though the real issue is often session scope or missing active document state

This creates unnecessary friction in live human use.

## Current Safe Guidance

For the current MVP stage, the recommended human wording should be:

1. prefer explicit title binding:
   - `把《主标书》设为 @主标书`
   - `把《会议纪要》设为 @会议纪要`
2. use current-file phrasing only after a document has already been clearly locked in the same session
3. if needed, first ask one scoped question against the target file, then bind alias

This is a usage workaround, not the ideal long-term UX.

## Requested Follow-up For Mainline Agent

Later mainline Hermes agent work should improve alias binding UX in a bounded way.

Priority goals:

1. reduce implicit dependence on active document state for natural phrases like `把当前主标书设为 @主标书`
2. make title-based binding the obvious happy path
3. improve failure diagnostics so the user sees:
   - whether no active document exists
   - whether the session was not resumed
   - whether the title did not uniquely resolve
4. provide a clearer next-step hint when binding fails

Examples of better UX:

1. if current document is missing:
   - explain that no active file is locked in this session
   - suggest `把《主标书》设为 @主标书`
2. if retrieval fallback is ambiguous:
   - explain that multiple candidate files matched
   - suggest explicit title binding
3. if resume context is missing:
   - explain that the session may not have been resumed

## Non-goals

This follow-up should not silently expand into:

1. project-level alias system redesign
2. retrieval contract rewrite
3. memory kernel architecture rewrite
4. automatic business decision logic
5. evidence boundary relaxation

## Why This Matters

The current MVP is already usable, but this issue directly affects operator confidence.

The gap is not core retrieval correctness; it is human-facing ergonomics.

Improving this will make the CLI feel more like “it remembers what I mean” instead of “I need to remember the exact magic words”.
