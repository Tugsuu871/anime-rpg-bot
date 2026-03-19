# ══════════════════════════════════════
# database.py
# ══════════════════════════════════════
import aiosqlite
import os

DB_PATH = "data/rpg.db"

async def init_db():
    os.makedirs("data", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id      TEXT PRIMARY KEY,
                username     TEXT,
                wallet       INTEGER DEFAULT 0,
                bank         INTEGER DEFAULT 0,
                active_char  TEXT DEFAULT NULL,
                profession   TEXT DEFAULT NULL,
                level        INTEGER DEFAULT 1,
                xp           INTEGER DEFAULT 0,
                wins         INTEGER DEFAULT 0,
                losses       INTEGER DEFAULT 0,
                last_daily   TEXT DEFAULT NULL,
                last_work    TEXT DEFAULT NULL,
                created_at   TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_characters (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT NOT NULL,
                char_name   TEXT NOT NULL,
                obtained_at TEXT DEFAULT (datetime('now')),
                UNIQUE(user_id, char_name)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT NOT NULL,
                item_name   TEXT NOT NULL,
                quantity    INTEGER DEFAULT 1,
                obtained_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id   TEXT,
                receiver_id TEXT,
                amount      INTEGER,
                reason      TEXT,
                ts          TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dungeon_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT,
                dungeon     TEXT,
                floors      INTEGER,
                reward      INTEGER,
                ts          TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.commit()

# ── Хэрэглэгч авах / үүсгэх ──────────
async def get_or_create(user_id: str, username: str) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, wallet) VALUES (?,?,?)",
            (user_id, username, 500)   # эхлэх 500 val
        )
        await db.commit()
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cur:
            return dict(await cur.fetchone())

# ── Wallet шинэчлэх ───────────────────
async def add_wallet(user_id: str, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET wallet = wallet + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

async def set_wallet(user_id: str, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET wallet = ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

# ── XP & Level ────────────────────────
async def add_xp(user_id: str, xp: int) -> tuple[int, int, bool]:
    """XP нэмж, level ахисан эсэхийг буцаана (old_level, new_level, leveled_up)"""
    from config import LEVEL_XP
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT xp, level FROM users WHERE user_id=?", (user_id,)
        ) as cur:
            row = dict(await cur.fetchone())

        new_xp  = row["xp"] + xp
        old_lvl = row["level"]
        new_lvl = old_lvl

        thresholds = sorted(LEVEL_XP.items())
        for lvl, req in thresholds:
            if new_xp >= req:
                new_lvl = lvl

        await db.execute(
            "UPDATE users SET xp=?, level=? WHERE user_id=?",
            (new_xp, new_lvl, user_id)
        )
        await db.commit()
        return old_lvl, new_lvl, new_lvl > old_lvl

# ── Дүр эзэмшиж байгаа эсэх ──────────
async def owns_character(user_id: str, char_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM user_characters WHERE user_id=? AND char_name=?",
            (user_id, char_name)
        ) as cur:
            return await cur.fetchone() is not None

async def add_character(user_id: str, char_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO user_characters (user_id, char_name) VALUES (?,?)",
            (user_id, char_name)
        )
        await db.commit()

async def get_user_characters(user_id: str) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT char_name FROM user_characters WHERE user_id=? ORDER BY obtained_at",
            (user_id,)
        ) as cur:
            return [r[0] for r in await cur.fetchall()]

# ── Inventory ─────────────────────────
async def add_item(user_id: str, item_name: str, qty: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, quantity FROM inventory WHERE user_id=? AND item_name=?",
            (user_id, item_name)
        ) as cur:
            row = await cur.fetchone()
        if row:
            await db.execute(
                "UPDATE inventory SET quantity=quantity+? WHERE id=?",
                (qty, row[0])
            )
        else:
            await db.execute(
                "INSERT INTO inventory (user_id, item_name, quantity) VALUES (?,?,?)",
                (user_id, item_name, qty)
            )
        await db.commit()

async def get_inventory(user_id: str) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT item_name, quantity FROM inventory WHERE user_id=? AND quantity>0 ORDER BY item_name",
            (user_id,)
        ) as cur:
            return await cur.fetchall()

# ── Leaderboard ───────────────────────
async def get_top_wallet(limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT username, wallet+bank as total, level FROM users ORDER BY total DESC LIMIT ?",
            (limit,)
        ) as cur:
            return await cur.fetchall()

async def get_top_level(limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT username, level, xp FROM users ORDER BY xp DESC LIMIT ?",
            (limit,)
        ) as cur:
            return await cur.fetchall()
