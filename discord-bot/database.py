"""
database.py — SQLite helpers for enabled/disabled channels and settings.
"""

import aiosqlite
from config import DATABASE_PATH


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                guild_id   INTEGER NOT NULL,
                enabled    INTEGER NOT NULL DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                guild_id         INTEGER PRIMARY KEY,
                user_cooldown    REAL NOT NULL DEFAULT 5.0,
                channel_cooldown REAL NOT NULL DEFAULT 3.0
            )
        """)
        await db.commit()


async def set_channel_enabled(guild_id: int, channel_id: int, enabled: bool):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO channels (channel_id, guild_id, enabled)
            VALUES (?, ?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET enabled=excluded.enabled
        """, (channel_id, guild_id, int(enabled)))
        await db.commit()


async def is_channel_enabled(channel_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT enabled FROM channels WHERE channel_id = ?", (channel_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return bool(row and row[0])


async def get_enabled_channels(guild_id: int) -> list[int]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT channel_id FROM channels WHERE guild_id = ? AND enabled = 1",
            (guild_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]


async def get_guild_settings(guild_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT user_cooldown, channel_cooldown FROM settings WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"user_cooldown": row[0], "channel_cooldown": row[1]}
            return {"user_cooldown": 5.0, "channel_cooldown": 3.0}


async def set_cooldown(guild_id: int, user_cooldown: float, channel_cooldown: float):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO settings (guild_id, user_cooldown, channel_cooldown)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                user_cooldown=excluded.user_cooldown,
                channel_cooldown=excluded.channel_cooldown
        """, (guild_id, user_cooldown, channel_cooldown))
        await db.commit()
