# NAS Evidence Manifests

This directory is reserved for local Phase 2.81a sanitized evidence manifest artifacts.

Tracked policy:

1. Real manifest JSON / Markdown outputs are ignored.
2. Manifests must not contain raw extracted text, true filenames, true NAS paths, raw DB rows, secrets, or sensitive business data.
3. Manifests must not be used as Agent final answer evidence.
4. Manifests must not imply `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB writes.

