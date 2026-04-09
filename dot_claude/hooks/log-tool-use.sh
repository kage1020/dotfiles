#!/bin/bash
# PostToolUse hook: log tool usage event with detail
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

# Extract tool-specific detail from tool_input
DETAIL=""
case "$TOOL_NAME" in
  Bash)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' | head -c 500)
    ;;
  Agent)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '(.tool_input.subagent_type // "general") + ": " + (.tool_input.description // empty)' | head -c 500)
    ;;
  Read|Write|Edit)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
    ;;
  Grep)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '(.tool_input.pattern // "") + " in " + (.tool_input.path // ".")' | head -c 500)
    ;;
  Glob)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '.tool_input.pattern // empty')
    ;;
  Skill)
    DETAIL=$(printf '%s' "$INPUT" | jq -r '.tool_input.skill // empty')
    ;;
esac

# Build log entry with jq for safe JSON encoding
printf '%s' "$INPUT" | jq -c \
  --arg type "tool_use" \
  --arg sid "$SESSION_ID" \
  --arg ts "$TIMESTAMP" \
  --arg tool "$TOOL_NAME" \
  --arg detail "$DETAIL" \
  '{
    type: $type,
    session_id: $sid,
    timestamp: $ts,
    tool_name: $tool,
    detail: (if $detail != "" then $detail else null end)
  }' >> "$LOG_DIR/$TODAY.jsonl"

exit 0
