# Internal MVP Daily Operator Checklist

This checklist is for Hermes internal controlled MVP daily operation.

It is not a production rollout checklist. It does not authorize customer delivery, automatic tender review, automatic bidding, automatic business decisions, repair, cleanup, backfill, reindex, Data Steward implementation, or direct DB / index mutation.

## 1. Daily Basic Information

| Field | Value |
|---|---|
| Date |  |
| Operator |  |
| Recorder |  |
| Reviewer |  |
| Business owner |  |
| Mac mini hostname |  |
| Mac mini LAN IP, sanitized if shared |  |
| Hermes_memory Git commit |  |
| Hermes_memory Git tag |  |
| Hermes agent Git commit |  |
| Hermes agent Git tag |  |
| Operator decision window | Day 0 / Day 1-2 / Day 3-5 / Week 2 |

Rules:

1. Do not paste secrets, `.env` values, tokens, passwords, raw logs, or customer-sensitive content into this checklist.
2. Record commit / tag only after the Operator confirms the Mac mini pulled the reviewed Git ref.
3. If the machine is not on the reviewed commit / tag, mark the day as `Pause` before trial use.

## 2. Startup Checks

| Check | Expected | Result | Notes |
|---|---|---|---|
| API `/health` | OK | pass / warn / fail |  |
| Hermes CLI help | Available | pass / warn / fail |  |
| Postgres reachability | Reachable | pass / warn / fail | No repair here |
| OpenSearch reachability | Reachable | pass / warn / fail | No reindex here |
| Qdrant reachability | Reachable | pass / warn / fail | No backfill here |
| MinIO reachability | Reachable if used | pass / warn / fail |  |
| Redis reachability | Reachable if used | pass / warn / fail |  |
| Required env key names present | Present, values not recorded | pass / warn / fail | Do not paste values |
| `QDRANT_COLLECTION` | `hermes_chunks` | pass / warn / fail | Record deviation only |
| Worktree cleanliness | Only approved dirty files | pass / warn / fail | No ad-hoc Mac mini edits |
| Reports / records ignored | Real local outputs not tracked | pass / warn / fail |  |

Stop immediately if:

1. API or CLI is unavailable and cannot be clearly classified as an operator startup issue.
2. The Mac mini worktree contains unreviewed code changes.
3. Runtime checks imply repair / backfill / reindex / migration is needed.
4. Secrets or `.env` values were copied into a record.

## 3. Fixed Alias Checks

| Alias | Expected document | alias_resolution.status | document_id | version_id | alias_missing | retrieval_suppressed | Result |
|---|---|---|---|---|---|---|---|
| `@主标书` | Main tender |  |  |  | false | false | pass / warn / fail |
| `@会议纪要` | Meeting minutes |  |  |  | false | false | pass / warn / fail |
| `@硬件清单` | Hardware Excel |  |  |  | false | false | pass / warn / fail |
| `@C塔方案` | C tower PPTX |  |  |  | false | false | pass / warn / fail |

Alias severity rules:

1. Any `alias_missing=true` on a fixed alias is at least P1.
2. Any `retrieval_suppressed=true` on a fixed alias without an intentional missing-alias test is P1.
3. Wrong document_id / version_id is P0 if it affects answer evidence.
4. Stale version warnings are not automatically P0, but must be reviewed before business use.

## 4. Fixed Daily Query Checks

| Query Area | Expected Behavior | Result | Evidence / Citation Notes |
|---|---|---|---|
| Main tender basic fields | Answer from `@主标书`; Missing Evidence if concrete amount / requirement not found | pass / partial / fail |  |
| Main tender Missing Evidence behavior | No fabricated amount, qualification, personnel count, or project manager level | pass / partial / fail |  |
| Excel structured citation | Uses `@硬件清单`; shows sheet and cell/range; row fallback recorded as P2 | pass / partial / fail |  |
| PPTX structured citation | Uses `@C塔方案`; shows slide number / title | pass / partial / fail |  |
| Meeting action / decision / risk | Uses `@会议纪要`; transcript not treated as fact | pass / partial / fail |  |
| Optional company-direction analysis | Recommendations are suggestions only; Business owner decides | pass / partial / fail |  |

Minimum daily prompts should remain within the fixed query set unless Reviewer approves a small variation.

## 5. Evidence Boundary Checks

| Boundary | Required Value | Observed | Result |
|---|---|---|---|
| `facts_as_answer` | `false` |  | pass / fail |
| `transcript_as_fact` | `false` |  | pass / fail |
| `snapshot_as_answer` | `false` |  | pass / fail |
| Third-document contamination | none |  | pass / fail |
| Wrong document evidence | none |  | pass / fail |
| Fabricated amount | none |  | pass / fail |
| Fabricated qualification / personnel count | none |  | pass / fail |
| Business conclusion without human decision | none |  | pass / fail |
| Missing Evidence used when evidence absent | yes |  | pass / fail |

If any fact, transcript, or metadata snapshot replaces retrieval evidence, classify as P0.

## 6. Issue Intake

| Field | Value |
|---|---|
| issue_id |  |
| severity | P0 / P1 / P2 / P3 |
| issue_type | retrieval_recall / citation_display / trace_ux / alias_session / latency / contamination / answer_boundary / operator_env / other |
| affected_alias |  |
| source_document_id |  |
| source_version_id |  |
| evidence_chunk_id / citation |  |
| observed_behavior |  |
| expected_behavior |  |
| manual_workaround |  |
| owner |  |
| next_action |  |
| reviewer_decision | Go / Pause / No-Go |

Severity handling:

1. P0: immediate Pause / No-Go.
2. P1: pause expansion; fix or manual workaround required.
3. P2: continue internal trial only if human-reviewable and recorded.
4. P3: record as backlog.

## 7. Go / Pause / No-Go Decision

| Decision | Criteria |
|---|---|
| Go | P0=0, P1=0, citations are human-checkable, evidence boundaries normal |
| Pause | Alias/session unstable, core citation not checkable, P1 without workaround, unclear operator state |
| No-Go | Any P0, wrong document evidence, facts/transcript replacing evidence, production boundary breach |

Daily decision:

| Field | Value |
|---|---|
| P0 count |  |
| P1 count |  |
| P2 count |  |
| P3 count |  |
| Decision | Go / Pause / No-Go |
| Reviewer |  |
| Business owner acknowledgement |  |
| Notes |  |

## 8. Daily Closeout

| Closeout Item | Result | Notes |
|---|---|---|
| Sanitized issue record saved if needed | yes / no / n/a |  |
| Raw logs avoided in Git | yes / no |  |
| Secrets avoided in Git | yes / no |  |
| Need Codex A fix | yes / no |  |
| Need Codex B review | yes / no |  |
| Need Codex C smoke | yes / no |  |
| Allow next operating day | yes / no |  |
| Next-day scope | same users / small expansion / pause |  |

Do not baseline, tag, push, repair, cleanup, backfill, reindex, migrate, or change production operations from this checklist alone.

## 9. Permanent Non-Goals

This checklist does not authorize:

1. Production rollout.
2. Customer delivery.
3. Automatic tender review.
4. Automatic bidding.
5. Automatic business decisions.
6. Repair / cleanup / backfill / reindex / delete.
7. Direct mutation of DB / facts / document_versions / audit_logs / OpenSearch / Qdrant.
8. Data Steward / BIM schema / Neo4j / PostGIS / spatial index / scheduler implementation.
9. Retrieval contract changes.
10. Memory kernel main architecture changes.

