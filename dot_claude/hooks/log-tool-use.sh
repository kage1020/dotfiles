#!/bin/bash
# PostToolUse hook: log tool usage event
INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty')
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty')

if [ -z "$SESSION_ID" ] || [ -z "$TOOL_NAME" ]; then
  exit 0
fi

# Normalize Windows backslashes to forward slashes
TRANSCRIPT_PATH=$(echo "$TRANSCRIPT_PATH" | tr '\\' '/')

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TODAY=$(date -u +%Y-%m-%d)

PROJECT_SLUG=$(echo "$TRANSCRIPT_PATH" | sed -n 's|.*/\.claude/projects/\([^/]*\)/.*|\1|p')
PROJECT_SLUG="${PROJECT_SLUG:-_unknown}"

LOG_DIR="$HOME/.claude/logs/$PROJECT_SLUG"
mkdir -p "$LOG_DIR"

printf '{"type":"tool_use","session_id":"%s","timestamp":"%s","tool_name":"%s"}\n' \
  "$SESSION_ID" "$TIMESTAMP" "$TOOL_NAME" >> "$LOG_DIR/$TODAY.jsonl"

exit 0
