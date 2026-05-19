# DB / Platform Team Handoff: Hermes Capability Maximization

## One-line Positioning

```text
Hermes = Evidence-first enterprise memory kernel + permission-aware catalog agent.
```

Official slogan:

```text
Hermes：证据先行，权限闭环；让企业数据可问、可信、可控。
```

Engineering motto:

```text
先目录，后正文；先证据，后智能；先受控，后自动化。
```

## What Hermes Is

Hermes is an evidence-first enterprise memory kernel.

It is designed to:

1. answer with citations when evidence exists
2. say Missing Evidence when evidence is unavailable
3. preserve permission and audit boundaries
4. remember only safe, low-sensitive context
5. work with platform-owned Gateway controls
6. help users ask enterprise data questions without bypassing governance

## What Hermes Is Not

Hermes is not:

1. a generic chatbot
2. a raw DB agent
3. an SQL generator
4. a NAS file reader
5. a DWG/RVT/BIM content-understanding agent
6. a production rollout system
7. a replacement for platform auth, permission, audit, or path-redaction logic

## Current Safe Integration Pattern

The platform should maximize current Hermes value through read-only catalog integration.

Recommended current flow:

1. User asks through frontend "Ask Hermes".
2. Platform Gateway authenticates the user and project context.
3. Gateway applies permission and project scope.
4. Gateway calls safe catalog / Hermes endpoints.
5. Gateway redacts paths and scans forbidden fields.
6. Hermes answers catalog questions from safe catalog metadata.
7. Hermes may use only low-sensitive memory references, such as `related_file_ids`, `query_id`, and user feedback labels, for continuity.
8. Content-level answers require separately governed retrieval, full-text, parser, or component evidence.
9. Catalog metadata and low-sensitive memory references must not be treated as file正文 evidence.
10. Hermes returns Missing Evidence when content evidence is not available.
8. Platform records `query_id` / `trace_id` for audit and feedback loops.

## Gateway Must Own

Gateway must own:

1. auth
2. project scope
3. permission decision
4. path redaction
5. forbidden-field scan
6. query trace / audit trace
7. any mapping from platform identity to Hermes-safe request context

Hermes should not trust frontend-provided project scope or raw path fields.

## Safe Memory Fields

Hermes may remember low-sensitive context such as:

1. `related_file_ids`
2. `related_model_ids`
3. `query_id`
4. `trace_id`
5. user feedback labels
6. low-sensitive preferences

These fields help Hermes maintain continuity without storing sensitive file contents or raw platform rows.

Low-sensitive memory references are not content evidence. A `related_file_id` means only that a file was referenced in a governed interaction; it does not mean Hermes has read, parsed, indexed, or remembered that file's contents.

## Forbidden Memory Fields

Hermes must not store:

1. raw `storage_path`
2. raw DB row
3. NAS raw path
4. DWG/RVT content
5. PDF / Office正文
6. customer-sensitive content
7. secrets, tokens, credentials, passwords, bearer values, or `.env` values

## What To Maximize Now

The platform / DB team can maximize:

1. catalog search
2. safe file/model IDs
3. Missing Evidence answers
4. permission-aware deny behavior
5. feedback loop
6. related-file memory references for continuity, not as content evidence
7. frontend "Ask Hermes" entry
8. query / trace identifiers
9. response shapes that separate catalog metadata from content evidence

## Current Safe Answer Modes

Hermes can safely support:

1. "Which catalog files/models are related to this query?"
2. "What safe metadata does the catalog know?"
3. "Which file IDs should be reviewed next?"
4. "What evidence is missing before Hermes can answer content-level questions?"
5. "What related file IDs did the user previously discuss?"

These answer modes remain catalog-only unless a later phase explicitly enables governed evidence retrieval. Catalog metadata and `related_file_ids` must not be presented as proof that Hermes has access to file正文.

Hermes should return Missing Evidence for:

1. DWG/RVT/BIM content questions
2. NAS file text questions
3. PDF/Office正文 questions when content was not ingested as evidence
4. raw DB row questions
5. storage path questions

## Future Capabilities

The following remain future and must not be presented as current:

1. DWG/RVT content understanding
2. BIM component search
3. NAS semantic index
4. Agent DB CRUD
5. Agent-generated SQL
6. production rollout
7. Data Steward productization
8. automatic repair / reindex / migration flows

## Practical Team Guidance

When explaining Hermes to platform users:

1. Say Hermes is evidence-first and permission-aware.
2. Say Hermes can help find safe catalog references.
3. Say Hermes will clearly state Missing Evidence for unsupported content-level questions.
4. Do not say Hermes has read raw NAS files unless that evidence has been explicitly ingested and governed.
5. Do not say Hermes can understand DWG/RVT/BIM content today.
6. Do not expose raw paths or DB rows to Hermes or users through Hermes responses.
7. Do not treat low-sensitive memory references as retrieval evidence.
