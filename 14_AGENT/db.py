import sqlite3

from pathlib import Path
from datetime import datetime, timezone
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "meetings.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            create table if not exists meetings (
                id integer primary key autoincrement,
                title varchar(1000) not null,
                people varchar(1000) not null,
                notes text not null,
                summary text not null,
                actions text not null,
                result text not null,
                created_at varchar(1000) not null
            )        
            """
        )
        conn.commit()
        
def save_meeting(title: str, people: str, notes: str, summary: str, actions: str, result: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_connection() as conn:
        cursor = conn.execute(
            """
            insert into meetings (title, people, notes, summary, actions, result, created_at) values (?, ?, ?, ?, ?, ?, ?)        
            """, (title, people, notes, summary, actions ,result, created_at)
        )
        conn.commit()
        return int(cursor.lastrowid)

# Any는 import 필요
def list_meetings(limit: int = 20) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            select id, title, people, summary, created_at from meetings
            order by id desc
            limit ?        
            """, (limit,)
        ).fetchall()
    return [dict(row) for row in rows]

def format_meetings_markdown(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "저장된 회의가 없습니다."
    lines = ["### 저장된 회의 목록", ""]
    for row in rows:
        lines.append(
            f"- #{row['id']} {row['title']}"
            f"({row['people'] or '참가자 없음'}) - {row['created_at']}"
        )
        lines.append(f" -요약: {row['summary']}")
    return "\n".join(lines)

def get_meeting(meeting_id: int) -> list[dict[str, Any]] | None:
    with get_connection() as conn:
        row = conn.execute(
            "select * from meetings where id = ?", (meeting_id,)
        ).fetchone()
    return [dict(row)] if row else None