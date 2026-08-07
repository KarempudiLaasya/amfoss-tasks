import discord
import requests
import random
from discord.ext import commands
from config import TOKEN
from database import create_tables, get_balance, claim_daily,transfer_berries,get_shop_items,buy_item,get_inventory,get_leaderboard,raid_user,get_history
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def hello(ctx):
    await ctx.send("Ahoy, pirate! 🏴‍☠️")

@bot.command()
async def bounty(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f"🏴‍☠️ Your bounty is **{balance}** 🍓")
@bot.command()
async def setsail(ctx):

    success, balance = claim_daily(ctx.author.id)

    if success:
        await ctx.send(
            f"🏴‍☠️ You raided a merchant ship!\n"
            f"You earned **250 🍓**\n"
            f"Current Balance: **{balance} 🍓**"
        )
    else:
        await ctx.send(
            f"❌ You've already claimed today's reward!\n"
            f"Current Balance: **{balance} 🍓**"
        )

@bot.command()
async def shop(ctx):

    items = get_shop_items()

    message = "🛒 **Berry Broker Shop**\n\n"

    for name, cost, effect in items:
        message += (
            f"**{name}**\n"
            f"💰 {cost} 🍓\n"
            f"✨ {effect}\n\n"
        )

    await ctx.send(message)
@bot.command()
async def buy(ctx, *, item):

    success, result = buy_item(ctx.author.id, item)

    if success:
        await ctx.send(
            f"✅ You bought **{item}**!\n"
            f"Remaining Balance: **{result} 🍓**"
        )
    else:
        await ctx.send(f"❌ {result}")
@bot.command()
async def inventory(ctx):

    items = get_inventory(ctx.author.id)

    if not items:
        await ctx.send("🎒 Your inventory is empty.")
        return

    message = "🎒 **Your Inventory**\n\n"

    for item, active in items:

        status = "🟢 Active" if active else "🔴 Used"

        message += f"**{item}** - {status}\n"

    await ctx.send(message)
@bot.command()
async def worstgeneration(ctx):

    leaderboard = get_leaderboard()

    if not leaderboard:
        await ctx.send("No pirates have set sail yet!")
        return

    message = "🏴‍☠️ **Worst Generation Leaderboard** 🏴‍☠️\n\n"

    rank = 1

    for user_id, berries in leaderboard:

        user = bot.get_user(user_id)

        if user is None:
            try:
                user = await bot.fetch_user(user_id)
            except:
                username = "Unknown Pirate"
            else:
                username = user.name
        else:
            username = user.name

        message += f"**{rank}. {username}** — {berries} 🍓\n"
        rank += 1

    await ctx.send(message)
@bot.command()
async def raid(ctx, member: discord.Member):

    success, value = raid_user(ctx.author.id, member.id)

    if success:
        await ctx.send(
            f"🏴‍☠️ Raid successful!\n"
            f"You stole **{value} 🍓** from {member.mention}!"
        )
    else:

        if isinstance(value, str):
            await ctx.send(f"❌ {value}")
        else:
            await ctx.send(
                f"💀 Raid failed!\n"
                f"You lost **{value} 🍓**."
            )
@bot.command()
async def logpose(ctx):

    try:

        response = requests.get(
            "https://api.api-onepiece.com/v2/characters/en",
            timeout=5
        )

        data = response.json()

        character = random.choice(data)

        name = character.get("name", "Unknown")
        bounty = character.get("bounty", "Unknown")
        crew = character.get("crew", "Unknown")
        fruit = character.get("fruit", "None")

        await ctx.send(
            f"🧭 **Log Pose points to...**\n\n"
            f"👤 Character: **{name}**\n"
            f"🏴 Crew: **{crew}**\n"
            f"🍓 Bounty: **{bounty}**\n"
            f"🍈 Devil Fruit: **{fruit}**"
        )

    except Exception:
        await ctx.send("❌ Couldn't reach the Grand Line right now.")
@bot.command()
async def history(ctx):

    records = get_history(ctx.author.id)

    if not records:
        await ctx.send("📜 No transaction history found.")
        return

    message = "📜 **Your Transaction History**\n\n"

    for action, amount, time in records:

        if amount >= 0:
            sign = "+"
        else:
            sign = ""

        message += (
            f"**{action}**\n"
            f"{sign}{amount} 🍓\n"
            f"🕒 {time}\n\n"
        )

    await ctx.send(message)
@bot.command()
async def trade(ctx, member: discord.Member, amount: int):

    if member == ctx.author:
        await ctx.send("❌ You can't trade with yourself!")
        return

    success, message = transfer_berries(
        ctx.author.id,
        member.id,
        amount
    )

    if success:
        await ctx.send(
            f"🏴‍☠️ {ctx.author.mention} sent **{amount} 🍓** to {member.mention}!"
        )
    else:
        await ctx.send(f"❌ {message}")
create_tables()
bot.run(TOKEN)