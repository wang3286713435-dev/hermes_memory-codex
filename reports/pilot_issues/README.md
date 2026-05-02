# Pilot Issue Records

This directory is for local MVP Pilot issue records.

Real issue JSON / Markdown records are sensitive local trial artifacts and are ignored by Git by default.

Use the dry-run intake tool to validate and summarize records:

```bash
uv run python scripts/phase237a_pilot_issue_intake.py --input-dir reports/pilot_issues --strict
```

Do not treat this directory as a repair queue, rollout approval, or automatic tender-review backlog.
