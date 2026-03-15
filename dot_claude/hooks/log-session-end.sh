#!/bin/bash
# SessionEnd hook: log session end with transcript summary
INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty')
REASON=$(printf '%s' "$INPUT" | jq -r '.reason // empty')
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty')

if [ -z "$SESSION_ID" ]; then
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

# Calculate duration
DURATION_MS=0
SESSION_FILE="$HOME/.claude/logs/.session-$SESSION_ID"
if [ -f "$SESSION_FILE" ]; then
  START_TS=$(cat "$SESSION_FILE")
  START_EPOCH=$(date -d "$START_TS" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%SZ" "$START_TS" +%s 2>/dev/null || echo 0)
  END_EPOCH=$(date -d "$TIMESTAMP" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%SZ" "$TIMESTAMP" +%s 2>/dev/null || echo 0)
  if [ "$START_EPOCH" -gt 0 ] && [ "$END_EPOCH" -gt 0 ]; then
    DURATION_MS=$(( (END_EPOCH - START_EPOCH) * 1000 ))
  fi
  rm -f "$SESSION_FILE"
fi

# Parse transcript for usage summary
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SUMMARY="{}"
if [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
  SUMMARY=$(python3 "$SCRIPT_DIR/parse-transcript.py" "$TRANSCRIPT_PATH" 2>/dev/null || echo '{}')
fi

# Build session_end event using jq
echo "$SUMMARY" | jq -c \
  --arg type "session_end" \
  --arg sid "$SESSION_ID" \
  --arg ts "$TIMESTAMP" \
  --arg reason "$REASON" \
  --argjson dur "$DURATION_MS" \
  '{
    type: $type,
    session_id: $sid,
    timestamp: $ts,
    reason: $reason,
    duration_ms: $dur,
    tokens: .tokens,
    tools: .tools,
    turn_count: .turn_count,
    user_prompt_count: .user_prompt_count,
    model: .model
  }' >> "$LOG_DIR/$TODAY.jsonl"

exit 0
