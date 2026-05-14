# NAS Evidence Payload Plans

This directory is reserved for local Phase 2.83a evidence-write payload dry-run artifacts.

Tracked policy:

1. Real payload JSON / Markdown outputs are ignored.
2. Payload plans must be generated only from sanitized eligibility reports.
3. Payload plans must not contain raw extracted text, true filenames, true NAS paths, raw DB rows, secrets, or sensitive business data.
4. Payload plans must not authorize `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB writes.
5. Payload plans must not connect NAS-derived content to Agent final answers.

