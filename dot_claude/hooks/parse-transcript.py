#!/usr/bin/env python3
"""Parse a Claude Code transcript JSONL file and output usage summary as JSON."""

import json
import sys
from collections import defaultdict


def parse_transcript(path: str) -> dict:
    tokens = {
        "input": 0,
        "output": 0,
        "cache_creation": 0,
        "cache_read": 0,
    }
    tools: dict[str, int] = defaultdict(int)
    turn_count = 0
    user_prompt_count = 0
    model = ""

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")

            if entry_type == "user":
                if not entry.get("isMeta", False):
                    user_prompt_count += 1

            elif entry_type == "assistant":
                msg = entry.get("message", {})
                if not model and msg.get("model"):
                    model = msg["model"]

                usage = msg.get("usage", {})
                if usage:
                    turn_count += 1
                    tokens["input"] += usage.get("input_tokens", 0)
                    tokens["output"] += usage.get("output_tokens", 0)
                    tokens["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
                    tokens["cache_read"] += usage.get("cache_read_input_tokens", 0)

                for block in msg.get("content", []):
                    if block.get("type") == "tool_use":
                        tool_name = block.get("name", "unknown")
                        tools[tool_name] += 1

    return {
        "tokens": tokens,
        "tools": dict(tools),
        "turn_count": turn_count,
        "user_prompt_count": user_prompt_count,
        "model": model,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse-transcript.py <transcript_path>", file=sys.stderr)
        sys.exit(1)
    result = parse_transcript(sys.argv[1])
    json.dump(result, sys.stdout, ensure_ascii=False)
