import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # NECESARIO

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN no existe")

bot.run(TOKEN)

