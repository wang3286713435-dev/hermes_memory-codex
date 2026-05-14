# NAS Evidence Eligibility Reports

This directory is reserved for local Phase 2.82a evidence-write eligibility dry-run reports.

Tracked policy:

1. Real eligibility JSON / Markdown outputs are ignored.
2. Reports must be generated only from sanitized evidence manifests.
3. Reports must not contain raw extracted text, true filenames, true NAS paths, raw DB rows, secrets, or sensitive business data.
4. Reports must not authorize `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB writes.
5. Reports must not connect NAS-derived content to Agent final answers.

