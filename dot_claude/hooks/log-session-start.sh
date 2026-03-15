#!/bin/bash
# SessionStart hook: log session start event
INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty')
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty')
SOURCE=$(printf '%s' "$INPUT" | jq -r '.source // empty')
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty')

if [ -z "$SESSION_ID" ]; then
  exit 0
fi

# Normalize Windows backslashes to forward slashes
TRANSCRIPT_PATH=$(echo "$TRANSCRIPT_PATH" | tr '\\' '/')

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TODAY=$(date -u +%Y-%m-%d)

# Derive project slug from transcript_path
PROJECT_SLUG=$(echo "$TRANSCRIPT_PATH" | sed -n 's|.*/\.claude/projects/\([^/]*\)/.*|\1|p')
PROJECT_SLUG="${PROJECT_SLUG:-_unknown}"

LOG_DIR="$HOME/.claude/logs/$PROJECT_SLUG"
mkdir -p "$LOG_DIR"

# Write session start event
printf '{"type":"session_start","session_id":"%s","timestamp":"%s","cwd":"%s","source":"%s"}\n' \
  "$SESSION_ID" "$TIMESTAMP" "$CWD" "$SOURCE" >> "$LOG_DIR/$TODAY.jsonl"

# Save start timestamp for duration calculation
echo "$TIMESTAMP" > "$HOME/.claude/logs/.session-$SESSION_ID"

exit 0
