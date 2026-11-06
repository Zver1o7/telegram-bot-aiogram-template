from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with self._lock:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_seen TEXT NOT NULL DEFAULT (datetime('now')),
                        created_at TEXT NOT NULL DEFAULT (datetime('now'))
                    )
                    """
                )
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        username TEXT,
                        text TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT (datetime('now'))
                    )
                    """
                )
                await db.execute(
                    "CREATE INDEX IF NOT EXISTS idx_users_last_seen ON users(last_seen)"
                )
                await db.execute(
                    "CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at)"
                )
                await db.commit()

    async def upsert_user(
        self, user_id: int, username: str | None, first_name: str | None
    ) -> None:
        async with self._lock:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, first_name, last_seen)
                    VALUES (?, ?, ?, datetime('now'))
                    ON CONFLICT(user_id) DO UPDATE SET
                        username=excluded.username,
                        first_name=excluded.first_name,
                        last_seen=datetime('now')
                    """,
                    (user_id, username, first_name),
                )
                await db.commit()

    async def save_feedback(self, user_id: int, username: str | None, text: str) -> int:
        async with self._lock:
            async with aiosqlite.connect(self.path) as db:
                cur = await db.execute(
                    "INSERT INTO feedback (user_id, username, text) VALUES (?, ?, ?)",
                    (user_id, username, text),
                )
                await db.commit()
                return int(cur.lastrowid)

    async def counts(self) -> dict[str, Any]:
        async with self._lock:
            async with aiosqlite.connect(self.path) as db:
                users = await (await db.execute("SELECT COUNT(*) FROM users")).fetchone()
                feedback = await (await db.execute("SELECT COUNT(*) FROM feedback")).fetchone()
        return {
            "users": int(users[0]) if users else 0,
            "feedback": int(feedback[0]) if feedback else 0,
        }

    async def get_user_ids(self, limit: int = 1000) -> list[int]:
        limit = max(1, min(int(limit), 5000))
        async with self._lock:
            async with aiosqlite.connect(self.path) as db:
                cur = await db.execute(
                    "SELECT user_id FROM users ORDER BY last_seen DESC LIMIT ?",
                    (limit,),
                )
                rows = await cur.fetchall()
        return [int(r[0]) for r in rows]
