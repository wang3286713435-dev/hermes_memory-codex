#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

export RALPH_ACTIVE=1
export RALPH_MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-10}"

STATE_FILE=".claude/context/runtime/ralph-state.json"
mkdir -p "$(dirname "$STATE_FILE")"
rm -f "$STATE_FILE"

now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
printf '{\n  "iteration": 0,\n  "startedAt": "%s",\n  "lastRunAt": "%s",\n  "lastFindingsCount": null,\n  "maxIterations": %s\n}\n' \
  "$now" "$now" "$RALPH_MAX_ITERATIONS" > "$STATE_FILE"

claude --print-output-format text < .claude/ralph/PROMPT.md
