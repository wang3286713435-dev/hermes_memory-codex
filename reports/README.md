# Reports

This directory is reserved for local Phase 2.26b audit report archives.

Runtime JSON files are intentionally ignored:

- `reports/readiness/*.json`
- `reports/repair_plan/*.json`
- `reports/manifest.json`
- `reports/latest.json`

Do not commit real readiness or repair-plan reports by default. They may contain local service status, document ids, fact ids, and other environment-specific diagnostics.

