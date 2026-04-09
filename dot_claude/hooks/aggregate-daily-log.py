#!/usr/bin/env python3
"""Aggregate daily logs from all projects into a structured summary for daily report generation.

Usage: aggregate-daily-log.py [--date YYYY-MM-DD] [--project PROJECT_SLUG]
  --date      Target date (default: today in UTC)
  --project   Filter to a specific project slug (default: all projects)

Output: JSON object with aggregated session data, tool usage, memos, and timeline.
"""

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def parse_jsonl(path: Path) -> list[dict]:
    """Parse a JSONL file, skipping malformed lines."""
    entries = []
    if not path.exists():
        return entries
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def get_git_activity(date_str: str) -> list[dict]:
    """Get git commits from all repos for the given date."""
    commits = []
    # Search common project directories
    search_dirs = [
        Path.home() / "projects",
        Path.home() / "work",
        Path.home() / "dev",
    ]
    seen_repos: set[str] = set()

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for repo_dir in search_dir.iterdir():
            git_dir = repo_dir / ".git"
            if not git_dir.exists():
                continue
            repo_path = str(repo_dir.resolve())
            if repo_path in seen_repos:
                continue
            seen_repos.add(repo_path)

            try:
                result = subprocess.run(
                    [
                        "git",
                        "-C",
                        repo_path,
                        "log",
                        "--all",
                        f"--after={date_str}T00:00:00",
                        f"--before={date_str}T23:59:59",
                        "--format=%H|%s|%aI|%an",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                for line in result.stdout.strip().split("\n"):
                    if not line:
                        continue
                    parts = line.split("|", 3)
                    if len(parts) == 4:
                        commits.append(
                            {
                                "repo": repo_dir.name,
                                "hash": parts[0][:8],
                                "message": parts[1],
                                "date": parts[2],
                                "author": parts[3],
                            }
                        )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

    return commits


def aggregate(date_str: str, project_filter: str | None = None) -> dict:
    """Aggregate all daily log data into a structured summary."""
    log_root = Path.home() / ".claude" / "logs"
    if not log_root.exists():
        return {"date": date_str, "projects": [], "summary": "No logs found"}

    projects = []
    total_sessions = 0
    total_duration_ms = 0
    total_tokens = {"input": 0, "output": 0, "cache_creation": 0, "cache_read": 0}
    all_tool_counts: dict[str, int] = defaultdict(int)
    all_memos: list[dict] = []
    timeline: list[dict] = []

    for project_dir in sorted(log_root.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("."):
            continue
        slug = project_dir.name
        if project_filter and slug != project_filter:
            continue

        log_file = project_dir / f"{date_str}.jsonl"
        memo_file = project_dir / f"{date_str}-memo.jsonl"

        entries = parse_jsonl(log_file)
        memos = parse_jsonl(memo_file)

        if not entries and not memos:
            continue

        # Process entries by session
        sessions: dict[str, dict] = {}
        tool_counts: dict[str, int] = defaultdict(int)
        tool_details: list[dict] = []

        for entry in entries:
            entry_type = entry.get("type")
            sid = entry.get("session_id", "unknown")
            ts = entry.get("timestamp", "")

            if entry_type == "session_start":
                sessions[sid] = {
                    "session_id": sid,
                    "start": ts,
                    "end": None,
                    "duration_ms": 0,
                    "cwd": entry.get("cwd", ""),
                    "source": entry.get("source", ""),
                    "tokens": None,
                    "turn_count": 0,
                    "user_prompt_count": 0,
                }
                timeline.append(
                    {
                        "timestamp": ts,
                        "type": "session_start",
                        "project": slug,
                        "detail": f"Session started in {entry.get('cwd', '')}",
                    }
                )

            elif entry_type == "session_end":
                if sid in sessions:
                    sessions[sid]["end"] = ts
                    sessions[sid]["duration_ms"] = entry.get("duration_ms", 0)
                    sessions[sid]["tokens"] = entry.get("tokens")
                    sessions[sid]["turn_count"] = entry.get("turn_count", 0)
                    sessions[sid]["user_prompt_count"] = entry.get(
                        "user_prompt_count", 0
                    )
                    total_duration_ms += entry.get("duration_ms", 0)

                    if entry.get("tokens"):
                        for k in total_tokens:
                            total_tokens[k] += entry["tokens"].get(k, 0)

                    if entry.get("tools"):
                        for tool, count in entry["tools"].items():
                            tool_counts[tool] += count
                            all_tool_counts[tool] += count

                timeline.append(
                    {
                        "timestamp": ts,
                        "type": "session_end",
                        "project": slug,
                        "detail": f"Session ended ({entry.get('reason', 'unknown')})",
                    }
                )

            elif entry_type == "tool_use":
                tool_name = entry.get("tool_name", "unknown")
                detail = entry.get("detail")
                tool_details.append(
                    {
                        "timestamp": ts,
                        "tool": tool_name,
                        "detail": detail,
                    }
                )
                timeline.append(
                    {
                        "timestamp": ts,
                        "type": "tool_use",
                        "project": slug,
                        "detail": f"{tool_name}"
                        + (f": {detail[:100]}" if detail else ""),
                    }
                )

            elif entry_type == "stop":
                timeline.append(
                    {
                        "timestamp": ts,
                        "type": "stop",
                        "project": slug,
                        "detail": "Task completed",
                    }
                )

        # Process memos
        for memo in memos:
            memo_entry = {
                "timestamp": memo.get("timestamp", ""),
                "content": memo.get("content", ""),
                "project": slug,
            }
            all_memos.append(memo_entry)
            timeline.append(
                {
                    "timestamp": memo.get("timestamp", ""),
                    "type": "memo",
                    "project": slug,
                    "detail": memo.get("content", ""),
                }
            )

        session_list = sorted(sessions.values(), key=lambda s: s.get("start", ""))
        total_sessions += len(session_list)

        projects.append(
            {
                "slug": slug,
                "sessions": session_list,
                "session_count": len(session_list),
                "tool_usage": dict(tool_counts),
                "tool_details": tool_details,
                "memo_count": len(memos),
            }
        )

    # Sort timeline chronologically
    timeline.sort(key=lambda e: e.get("timestamp", ""))

    # Format duration
    total_minutes = total_duration_ms // 60000
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Git activity
    git_commits = get_git_activity(date_str)

    return {
        "date": date_str,
        "summary": {
            "total_sessions": total_sessions,
            "total_duration": f"{hours}h {minutes}m",
            "total_duration_ms": total_duration_ms,
            "total_tokens": total_tokens,
            "tool_usage_total": dict(all_tool_counts),
            "memo_count": len(all_memos),
            "git_commit_count": len(git_commits),
        },
        "projects": projects,
        "memos": all_memos,
        "git_commits": git_commits,
        "timeline": timeline,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate daily Claude Code logs")
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Target date (YYYY-MM-DD, default: today UTC)",
    )
    parser.add_argument("--project", default=None, help="Filter to a specific project")
    args = parser.parse_args()

    result = aggregate(args.date, args.project)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
