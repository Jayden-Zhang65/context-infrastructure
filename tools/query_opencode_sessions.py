#!/usr/bin/env python3
"""Query OpenCode session DB for cross-project conversation history.

Usage:
    python query_opencode_sessions.py                    # today's sessions
    python query_opencode_sessions.py --days 3            # last 3 days
    python query_opencode_sessions.py --date 2026-07-24   # specific date
    python query_opencode_sessions.py --project LIMS      # filter by project dir
    python query_opencode_sessions.py --full              # include message content
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from argparse import ArgumentParser

DB_PATH = Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def get_sessions(cursor: sqlite3.Cursor, start_ms: int, end_ms: int | None = None,
                 project_filter: str | None = None) -> list[tuple]:
    query = """
        SELECT s.id, s.title, s.directory, s.time_created, s.time_updated,
               (SELECT COUNT(*) FROM message WHERE session_id = s.id) as msg_count
        FROM session s
        WHERE s.time_updated > ?
    """
    params: list = [start_ms]
    if end_ms is not None:
        query += " AND s.time_updated < ?"
        params.append(end_ms)

    query += " ORDER BY s.time_updated DESC"

    rows = cursor.execute(query, params).fetchall()

    if project_filter:
        rows = [r for r in rows if project_filter.lower() in (Path(r[2]).name or "").lower()]

    return rows


def get_user_prompts(cursor: sqlite3.Cursor, session_id: str, limit: int = 20) -> list[str]:
    cursor.execute("""
        SELECT data FROM message
        WHERE session_id = ? AND data LIKE '%"role":"user"%'
        ORDER BY time_created ASC
        LIMIT ?
    """, (session_id, limit))
    prompts: list[str] = []
    for (raw,) in cursor.fetchall():
        try:
            d = json.loads(raw)
            content = d.get("content", "")
            if isinstance(content, list):
                parts = []
                for p in content:
                    if isinstance(p, dict) and p.get("type") == "text":
                        parts.append(p.get("text", ""))
                content = " | ".join(parts) if parts else ""
            content = str(content).strip()
            if content:
                prompts.append(content)
        except Exception:
            pass
    return prompts


def main():
    parser = ArgumentParser(description="Query OpenCode session history")
    parser.add_argument("--days", type=int, default=1, help="Look back N days (default: 1)")
    parser.add_argument("--date", type=str, help="Specific date YYYY-MM-DD (overrides --days)")
    parser.add_argument("--project", type=str, help="Filter by project directory name")
    parser.add_argument("--full", action="store_true", help="Show user message content")
    parser.add_argument("--max-prompts", type=int, default=10, help="Max prompts per session (default: 10)")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    if args.date:
        day = datetime.strptime(args.date, "%Y-%m-%d")
        start = day.replace(hour=0, minute=0, second=0)
        end = day.replace(hour=23, minute=59, second=59)
    else:
        end = datetime.now()
        start = end - timedelta(days=args.days)
        start = start.replace(hour=0, minute=0, second=0)

    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)

    sessions = get_sessions(cursor, start_ms, end_ms, args.project)

    if not sessions:
        print(f"No sessions found for {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        conn.close()
        return

    print(f"Sessions: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}  ({len(sessions)} found)")
    print("=" * 65)

    for sid, title, directory, created, updated, msg_count in sessions:
        dir_name = Path(directory).name if directory else "?"
        upd = datetime.fromtimestamp(updated / 1000).strftime("%m-%d %H:%M")
        print(f"\n[{dir_name}] {title}")
        print(f"  Updated: {upd}  |  Messages: {msg_count}")

        if args.full:
            prompts = get_user_prompts(cursor, sid, args.max_prompts)
            if prompts:
                for i, p in enumerate(prompts):
                    display = p[:200] + "..." if len(p) > 200 else p
                    print(f"  [{i + 1}] {display}")

    conn.close()


if __name__ == "__main__":
    main()
