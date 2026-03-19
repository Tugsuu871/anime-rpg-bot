# ══════════════════════════════════════
# config.py — Бүх тохиргоо
# ══════════════════════════════════════
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN  = os.getenv("DISCORD_TOKEN", "YOUR_TOKEN_HERE")
PREFIX = "!"

# ── Валют ──────────────────────────────
CURRENCY_NAME   = "Val"
CURRENCY_SYMBOL = "🪙"
# 1 val = 15₮ (лого утга, donate биш)

def fmt(n: int) -> str:
    """1500 → '1.5kv' | 2000000 → '2.0Mv'"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}Mv"
    if n >= 1_000:
        return f"{n/1_000:.1f}kv"
    return f"{n:,} val"

# ── Tier үнэ ──────────────────────────
TIER_PRICES = {
    "F": 0,
    "D": (2_000,    5_000),
    "C": (20_000,   50_000),
    "B": (150_000,  400_000),
    "A": (2_000_000, 3_000_000),
    "S": (8_000_000, 12_000_000),
}

TIER_COLOR = {
    "S": 0xED4245,
    "A": 0xEF9F27,
    "B": 0x3B8BD4,
    "C": 0x1D9E75,
    "D": 0x888780,
    "F": 0x5C5C5A,
}

TIER_EMOJI = {
    "S": "🔴", "A": "🟡", "B": "🔵",
    "C": "🟢", "D": "⚪", "F": "🆓",
}

# ── Dungeon орлого (val) ──────────────
# Тэнцвэр тооцоо (дундаж тоглогч):
#   Easy   20 run/өдөр → ~10k–18k/өдөр  (6 сар → 2.5Mv)
#   Medium  5 run/өдөр → ~30k–60k/өдөр  (6 сар → 8Mv)
#   Hard    4 run/өдөр → ~50k–100k/өдөр (1 жил → 27Mv)
#   Legend  2 run/өдөр → ~100k–200k/өдөр (lv50+ шаардлагатай)
# → S tier (8Mv) авахад нийт ~1.5–2 жил идэвхтэй тоглоход
DUNGEON_REWARDS = {
    "easy":   {"floor": (150,   300),  "boss": (800,    1_500)},
    "medium": {"floor": (500,  1_200), "boss": (4_000,  8_000)},
    "hard":   {"floor": (1_500, 3_500),"boss": (12_000, 25_000)},
    "legend": {"floor": (2_000, 5_000),"boss": (20_000, 40_000)},
}

# ── Cooldown (секунд) ─────────────────
# Easy: 10 мин (өдөрт ~20 run дээд)
# Medium: 2 цаг (өдөрт ~12 run дээд, дундаж 4-5)
# Hard: 6 цаг (өдөрт ~4 run дээд, дундаж 2-3)
# Legend: 24 цаг (өдөрт 1 run — маш ховор)
DUNGEON_COOLDOWNS = {
    "easy":   600,      # 10 мин
    "medium": 7_200,    # 2 цаг
    "hard":   21_600,   # 6 цаг
    "legend": 86_400,   # 24 цаг — өдөрт 1 удаа
}

DUNGEON_MIN_LEVEL = {
    "easy": 1, "medium": 10, "hard": 25, "legend": 50,
}

DUNGEON_ENTRY_FEE = {
    "easy": 0, "medium": 500, "hard": 2_000, "legend": 10_000,
}

# ── Economy механик ───────────────────
DEATH_PENALTY_PCT = 0.10   # wallet-ийн 10%
MARKET_TAX_PCT    = 0.03   # 3%
PAY_TAX_PCT       = 0.01   # 1%
SWITCH_CHAR_FEE   = 1_000  # val

# ── Daily / Work ──────────────────────
DAILY_REWARD      = (200,  500)
DAILY_XP          = 50
WORK_REWARD       = (100,  300)
WORK_XP           = 20
WORK_COOLDOWN     = 1_800  # 30 мин

# ── XP & Level ────────────────────────
XP_PER_FLOOR_KILL = (30, 80)
XP_PER_BOSS_KILL  = (200, 800)
CRAFT_XP          = (20,  100)

LEVEL_XP = {
    1:0, 2:300, 3:700, 4:1_300, 5:2_000,
    10:7_000, 15:15_000, 20:28_000, 25:45_000,
    30:70_000, 35:100_000, 40:140_000, 45:190_000,
    50:250_000, 60:400_000, 70:600_000, 80:900_000,
    90:1_300_000, 99:2_000_000,
}

LEVEL_UNLOCKS = {
    5:  "Skill 1 нээгдэнэ",
    10: "Medium dungeon нээгдэнэ",
    20: "Skill 2 нээгдэнэ + Tier B shop",
    25: "Hard dungeon нээгдэнэ",
    35: "Skill 3 нээгдэнэ",
    50: "Legendary dungeon нээгдэнэ + Tier A shop",
    99: "MAX LEVEL — Legendary title",
}

# ── Admin ─────────────────────────────
# Admin болон Moderator-ын Discord User ID-г энд нэмнэ
# Жишээ: ADMIN_IDS = ["123456789012345678", "987654321098765432"]
ADMIN_IDS = [
    "1390361522274041948",   # Серверийн үндсэн admin
]
MOD_IDS = [
    # "MODERATOR_DISCORD_USER_ID",
]
