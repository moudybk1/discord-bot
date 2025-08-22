import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")           # your bot token
ROLE_ID = os.getenv("1408534362215022592", "")     # role to ping (as an integer string)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def is_nansen_alert(message: discord.Message) -> bool:
    """Only act on Nansen-style embed alerts from bots."""
    if not message.author.bot:
        return False
    if not message.embeds:
        return False
    title = (message.embeds[0].title or "").lower()
    return "smart alert" in title  # simple, safe filter

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    # never react to itself
    if message.author == bot.user:
        return

    if is_nansen_alert(message):
        try:
            embed = message.embeds[0]
            ping = (f"<@&{int(ROLE_ID)}>" if ROLE_ID else "@everyone")
            await message.channel.send(
                content=f"{ping} 🚨 New Nansen Smart Alert!",
                embed=embed,
                allowed_mentions=discord.AllowedMentions(everyone=True, roles=True)
            )
            await message.delete()  # remove the original
            print("✅ Relayed & deleted original.")
        except discord.Forbidden:
            print("❌ Missing permissions (Manage Messages / Mention Everyone).")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    
bot.run(TOKEN)
