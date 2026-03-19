# ══════════════════════════════════════
# bot.py — Anime RPG Bot Entry Point
# ══════════════════════════════════════
import discord, asyncio, traceback
from discord.ext import commands
from config import TOKEN, PREFIX
from database import init_db

intents = discord.Intents.default()
intents.message_content = True   # Portal: MESSAGE CONTENT INTENT → ON
# intents.members = True          # Хэрэв "Server Members Intent" нээгдсэн бол comment-г авна

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None   # Custom help
)

COGS = ["cogs.economy", "cogs.character", "cogs.dungeon", "cogs.admin"]

# ── Events ────────────────────────────
@bot.event
async def on_ready():
    await init_db()
    print(f"✅ {bot.user} нэвтэрлээ!")
    print(f"   Сервер тоо: {len(bot.guilds)}")
    await bot.change_presence(
        activity=discord.Game(name="!start | Anime RPG 🎭")
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Аргумент дутуу! `!help {ctx.command.name if ctx.command else ''}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Буруу аргумент! Тоо эсвэл @mention шаардлагатай.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(str(error))
    else:
        print(f"Алдаа [{ctx.command}]: {error}")
        traceback.print_exc()

# ── Custom help ───────────────────────
@bot.command(name="help", aliases=["туслах","?"])
async def help_cmd(ctx, *, section: str = None):
    from data.characters import CHARACTERS
    tier_count = {}
    for c in CHARACTERS.values():
        tier_count[c["tier"]] = tier_count.get(c["tier"], 0) + 1

    if section and section.lower() in ("admin","а","админ"):
        em = discord.Embed(
            title="🔧 Admin командууд",
            description="Зөвхөн `ADMIN_IDS`-д буй User ID-д ажиллана.",
            color=0xED4245
        )
        em.add_field(name="Үндсэн", value="`!admin` — бүх жагсаалт\n`!admin whoami` — өөрийн ID", inline=False)
        em.add_field(name="Мөнгө",
            value=("`!admin give val @user [дүн]`\n"
                   "`!admin take val @user [дүн]`\n"
                   "`!admin set val @user [дүн]`"), inline=False)
        em.add_field(name="Дүр / Item / XP",
            value=("`!admin give char @user [дүр]`\n"
                   "`!admin give item @user [item] [тоо]`\n"
                   "`!admin give xp @user [дүн]`"), inline=False)
        em.add_field(name="Хэрэглэгч удирдах",
            value=("`!admin info @user`\n"
                   "`!admin level @user [1-99]`\n"
                   "`!admin reset @user`\n"
                   "`!admin confirm [user_id]`"), inline=False)
        em.add_field(name="Сервер",
            value=("`!admin stats`\n"
                   "`!admin announce [текст]`\n"
                   "`!admin addadmin [user_id]`"), inline=False)
        em.set_footer(text="!help — үндсэн туслах цэс рүү буцах")
        return await ctx.send(embed=em)

    if section and section.lower() in ("char","дүр","characters"):
        em = discord.Embed(
            title="🎭 Дүрийн командууд",
            description=(
                f"Нийт **{len(CHARACTERS)} дүр** — "
                f"🆓 F:{tier_count.get('F',0)} "
                f"⚪ D:{tier_count.get('D',0)} "
                f"🟢 C:{tier_count.get('C',0)} "
                f"🔵 B:{tier_count.get('B',0)} "
                f"🟡 A:{tier_count.get('A',0)} "
                f"🔴 S:{tier_count.get('S',0)}"
            ),
            color=0x5865F2
        )
        em.add_field(name="Харах",
            value=("`!chars` — бүх дүр\n"
                   "`!chars [F/D/C/B/A/S]` — tier-ээр харах\n"
                   "`!char [нэр]` — дэлгэрэнгүй\n"
                   "`!mychars` — миний дүрүүд\n"
                   "`!shop` — дэлгүүр"), inline=False)
        em.add_field(name="Авах / Солих",
            value=("`!choose [нэр]` — F tier үнэгүй авах\n"
                   "`!buy char [нэр]` — мөнгөөр авах\n"
                   "`!switch [нэр]` — дүр солих"), inline=False)
        em.add_field(name="Tier үнэ",
            value=("🆓 F: Үнэгүй\n"
                   "⚪ D: 2k–5k val\n"
                   "🟢 C: 20k–50k val\n"
                   "🔵 B: 150k–400k val *(Lv20+)*\n"
                   "🟡 A: 2M–3M val *(Lv50+)*\n"
                   "🔴 S: 8M–12M val *(Lv50+)*"), inline=False)
        em.set_footer(text="!help — үндсэн цэс")
        return await ctx.send(embed=em)

    if section and section.lower() in ("dungeon","агуй","d"):
        em = discord.Embed(
            title="⚔️ Dungeon командууд",
            color=0xE24B4A
        )
        em.add_field(name="Командууд",
            value=("`!dungeons` — бүх dungeon жагсаалт\n"
                   "`!enter [dungeon]` — орох"), inline=False)
        em.add_field(name="Dungeon-ууд",
            value=("🟢 `konoha` — Easy Lv1+ 10мин\n"
                   "🟢 `soul_society` — Easy Lv1+ 10мин\n"
                   "🟡 `demon_mountains` — Medium Lv10+ 2цаг\n"
                   "🟡 `jjk_tokyo` — Medium Lv10+ 2цаг\n"
                   "🟠 `marineford` — Hard Lv25+ 6цаг\n"
                   "🟠 `dragon_world` — Hard Lv25+ 6цаг\n"
                   "🔴 `legendary` — Legend Lv50+ 24цаг"), inline=False)
        em.add_field(name="Анхааруулга",
            value=("⚠️ Нас барвал wallet-ийн **10%** алдана\n"
                   "💡 Орохоосоо өмнө `!deposit all` хийгээрэй\n"
                   "🔒 Medium+ орох төлбөртэй"), inline=False)
        em.set_footer(text="!help — үндсэн цэс")
        return await ctx.send(embed=em)

    # ── Үндсэн help ───────────────────
    total_chars = len(CHARACTERS)
    em = discord.Embed(
        title="📖 Anime RPG Bot — Туслах цэс",
        description=(
            f"**{total_chars} anime дүр** | F→S tier | 7 dungeon | 4 мэргэжил\n"
            f"1 val = 15₮ | S tier = 8,000,000 val\n\n"
            f"`!help [хэсэг]` — дэлгэрэнгүй харах"
        ),
        color=0x5865F2
    )
    em.add_field(
        name="🚀 Эхлэх",
        value=("`!start` — бүртгүүлэх (+500 val)\n"
               "`!profile [@user]` — профайл\n"
               "`!balance [@user]` — данс харах"),
        inline=False
    )
    em.add_field(
        name=f"🎭 Дүр — нийт {total_chars} дүр  (`!help char`)",
        value=(f"🆓×{tier_count.get('F',0)} ⚪×{tier_count.get('D',0)} "
               f"🟢×{tier_count.get('C',0)} 🔵×{tier_count.get('B',0)} "
               f"🟡×{tier_count.get('A',0)} 🔴×{tier_count.get('S',0)}\n"
               "`!chars` `!char [нэр]` `!choose [нэр]` `!buy char [нэр]`"),
        inline=False
    )
    em.add_field(
        name="⚔️ Dungeon  (`!help dungeon`)",
        value=("`!dungeons` — жагсаалт\n"
               "`!enter konoha` — Easy (Lv1+)\n"
               "`!enter demon_mountains` — Medium (Lv10+)\n"
               "`!enter marineford` — Hard (Lv25+)\n"
               "`!enter legendary` — Legend (Lv50+)"),
        inline=False
    )
    em.add_field(
        name="💰 Economy",
        value=("`!daily` — өдрийн 200–500 val\n"
               "`!work` — 100–300 val (30мин CD)\n"
               "`!pay @user [дүн]` — шилжүүлэх\n"
               "`!deposit [дүн/all]` · `!withdraw [дүн/all]`\n"
               "`!leaderboard` — топ 10"),
        inline=False
    )
    em.add_field(
        name="🔧 Admin  (`!help admin`)",
        value="`!admin` — бүх admin командын жагсаалт",
        inline=False
    )
    em.set_footer(text="!help char | !help dungeon | !help admin — дэлгэрэнгүй")
    await ctx.send(embed=em)

# ── Main ──────────────────────────────
async def main():
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"  ✅ {cog} ачааллагдлаа")
            except Exception as e:
                print(f"  ❌ {cog} алдаа: {e}")
                traceback.print_exc()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
