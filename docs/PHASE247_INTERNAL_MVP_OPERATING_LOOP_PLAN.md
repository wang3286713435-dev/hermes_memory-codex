# Phase 2.47 Internal Controlled MVP Operating Loop Plan

## 1. Phase Goal

Phase 2.47 defines how Hermes may start an internal controlled MVP operating loop after the Mac mini local MVP smoke returned `Go`.

This is an operating plan only. It does not approve production rollout, customer delivery, automatic tender review, automatic bidding, automatic business decisions, repair execution, cleanup, backfill, reindex, Data Steward implementation, BIM schema work, or scheduler work.

## 2. Landing Judgment

| Area | Judgment | Boundary |
|---|---|---|
| Internal controlled MVP | Allowed to start | Only internal users, fixed query set, human review required |
| Production rollout | Not allowed | No production SLA, customer-facing delivery, or broad deployment |
| Customer delivery | Not allowed | External customer output remains human-owned and manually reviewed |
| Automatic tender / bid / business decisions | Not allowed | Hermes output is evidence assistance only |
| Repair / cleanup / backfill / reindex | Not allowed | Requires separate phase, explicit human approval, and dry-run first |
| Data Steward / BIM implementation | Not allowed | Remains a later product line, not part of this MVP loop |

Current Mac mini smoke status supports a controlled internal trial, not a production launch.

## 3. First-Week Operating Rhythm

### Day 0: Operator Startup

The Operator starts the local services, confirms `/health`, checks CLI availability, confirms the four key aliases, and records stop conditions before any internal user trial.

Minimum Day-0 checks:

1. API `/health` returns OK.
2. Hermes CLI opens help and can run the fixed smoke commands.
3. Required aliases can bind and resolve:
   - `@主标书`
   - `@硬件清单`
   - `@C塔方案`
   - `@会议纪要`
4. No secrets, `.env` values, raw logs, or real reports are committed to Git.
5. Stop conditions are visible to Operator / Recorder / Reviewer.

### Day 1-2: Narrow Internal Use

Only 1-2 internal owners may use Hermes with a fixed query set. All answers must be treated as assisted retrieval output and manually reviewed.

Rules:

1. Use the predefined query set from the pilot / smoke artifacts.
2. Do not ask Hermes to make tender, bidding, contract, procurement, customer communication, or company-direction decisions.
3. Recorder captures issues with severity, evidence ids, citation status, and Missing Evidence behavior.
4. Reviewer decides Go / Pause / No-Go at the end of each day.

### Day 3-5: Small Internal Expansion

If Day 1-2 has no P0 / P1, the trial can expand to a small number of internal colleagues. Outputs still require human review.

Expansion is paused if:

1. Any P0 appears.
2. Any P1 appears without a clear manual workaround.
3. Evidence policy becomes unclear.
4. Facts / transcript / metadata snapshots are presented as final answer sources.
5. Cross-document contamination appears.

### Week 2: Internal Service Evaluation

Week 2 is for deciding whether the Mac mini node can become a more stable internal company service. It is still not production rollout.

Week-2 decision inputs:

1. First-week P0 / P1 / P2 / P3 counts.
2. Health and CLI availability record.
3. Alias stability record.
4. Citation and Missing Evidence behavior.
5. Manual review burden.
6. Update / rollback experience.

## 4. Daily Fixed Checks

Every internal MVP operating day should record:

1. API `/health` status.
2. Hermes CLI availability.
3. Four key alias bind / resolve status.
4. P0 / P1 / P2 / P3 issue counts.
5. Citation presence and quality.
6. Missing Evidence behavior.
7. `facts_as_answer` must remain `false`.
8. `transcript_as_fact` must remain `false`.
9. `snapshot_as_answer` must remain `false` when metadata snapshot is used.
10. Cross-document contamination / third-document mixing status.
11. Whether all business decisions were manually reviewed by the Business owner.

## 5. Human Roles

| Role | Responsibility | Not Allowed |
|---|---|---|
| Operator | Starts / stops services, checks machine, network, health, CLI, storage, and update state | Does not edit code on Mac mini ad hoc |
| Recorder | Records issues, evidence, citations, Missing Evidence, and daily status | Does not write business DB or repair data |
| Reviewer | Decides Go / Pause / No-Go from evidence and issue severity | Does not waive P0 / P1 without explicit record |
| Business owner | Owns tender, bid, contract, procurement, customer communication, and company-direction decisions | Does not delegate final decisions to Hermes |

## 6. Issue Intake

| Severity | Definition | Required Action |
|---|---|---|
| P0 | Security, wrong document used as evidence, facts/transcript replacing evidence, destructive behavior, production boundary breach | Immediate Pause / No-Go |
| P1 | Core workflow blocker, persistent alias failure, wrong document evidence, important field incorrectly answered without Missing Evidence | Pause expansion; fix or manual workaround required |
| P2 | Display, citation precision, trace visibility, latency, or partial recall issue that is human-reviewable | Continue internal trial but record and triage |
| P3 | Low-risk wording, UX, copy, or minor operator friction | Record as backlog |

Known current P2 tails:

1. Excel citation may show a broad range plus row hint instead of an exact single-row cell range.
2. Meeting transcript answer may not always explicitly print `transcript_as_fact=false`, although transcript content was not treated as confirmed facts in the latest smoke.

## 7. Hot Update Principles

Hot updates must follow dev-machine to baseline to Mac mini discipline.

Rules:

1. Development happens on the development machine.
2. Tests and review happen before baseline.
3. Mac mini only pulls reviewed commit / tag.
4. No ad-hoc code edits on Mac mini.
5. Run health + smoke before update.
6. Pull reviewed commit / tag.
7. Run health + smoke after update.
8. If post-update smoke regresses P0 / P1, roll back by reviewed Git ref and record the incident.

## 8. Git / Report / Evidence Strategy

1. Real run reports, raw evidence, and local status JSON remain ignored unless separately sanitized.
2. Small wording changes, ignored `latest.json` updates, and single review conclusions do not require separate baseline.
3. Docs-only planning may remain dirty until grouped with checklist, template, or validated artifact work.
4. Baseline should happen when a reusable artifact or phase switch needs durable Git state.
5. Codex B should approve baseline for phase switches, scope expansion, reusable artifacts, or Yellow Lane work.

## 9. Nightly / Low-Manual-Intervention Policy

1. Nightly or automated work may only execute one bounded item at a time.
2. It must not cross multiple large phases automatically.
3. It must not tag / push unless `NEXT_CODEX_A_PROMPT.md` explicitly authorizes baseline.
4. It must stop on hard boundaries, dirty-file mismatch, test failure beyond the allowed retry budget, or need for human samples / secrets / terminal evidence.
5. Codex A output must always state whether Codex B review, Codex C validation, or human operator action is required.

## 10. Non-Goals

Phase 2.47 does not authorize:

1. Production rollout.
2. External customer delivery.
3. Automatic tender review.
4. Automatic bidding.
5. Automatic business / company-direction decisions.
6. Repair / cleanup / backfill / reindex / delete.
7. Direct DB / facts / document_versions / audit_logs / OpenSearch / Qdrant mutation.
8. Data Steward implementation.
9. BIM schema / Neo4j / PostGIS / spatial index implementation.
10. Production cron / scheduler.
11. Retrieval contract changes.
12. Memory kernel main architecture changes.

## 11. Next Phase Candidates

| Candidate | Purpose | Baseline Need |
|---|---|---|
| Phase 2.47a | Internal MVP daily operator checklist artifact | Yes, if it becomes reusable |
| Phase 2.47b | Local ignored pilot run record template | Yes, if template / ignore policy is added |
| Phase 2.47c | P2 display tails triage plan | Maybe; docs-only planning can wait for grouped baseline |

## 12. Current Recommendation

Internal controlled MVP can start with Day-0 / Day-1 discipline, fixed query set, issue intake, and human review.

Do not start production rollout. Do not use Hermes as an autonomous tender, bid, contract, procurement, customer communication, or business-decision system.

