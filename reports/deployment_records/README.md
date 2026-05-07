# Deployment Records

This directory is for local Mac mini deployment records created by a human operator.

Real deployment records are operational artifacts and are ignored by Git by default.

Do not commit:

1. real deployment record JSON.
2. real deployment record Markdown.
3. raw logs.
4. `latest.*` pointers.
5. secrets, tokens, passwords, `.env` values, or raw sensitive logs.

Committed files in this directory are limited to this README and `.gitignore`.

Codex must not treat a template or a local record path as proof that deployment was executed. A deployment record only documents human operator activity and sign-off after a separately authorized phase.
