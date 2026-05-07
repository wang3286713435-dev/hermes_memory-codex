# Internal MVP Run Records

This directory is for local Hermes internal controlled MVP run records.

Real run records are sensitive local artifacts and are ignored by Git by default.

Do not commit:

1. Real run JSON or Markdown.
2. Raw transcript or raw model output.
3. Secrets, `.env` values, tokens, passwords, or local credentials.
4. Customer-sensitive content or business-sensitive evidence.
5. Production deployment records.

If a sample is needed, create a separate sanitized fake template and ask Codex B to review it before committing.

A run record is not production rollout approval, customer delivery approval, repair approval, or automatic business decision evidence.

