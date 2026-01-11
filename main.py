import os
import asyncio
import discord
from discord.ext import commands

# ---------- VARIABLES DESDE ENVIRON ----------
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))
MOODLE_ICS_URL = os.environ.get("MOODLE_ICS_URL")
CHECK_INTERVAL_MIN = int(os.environ.get("CHECK_INTERVAL_MIN", 15))
TIMEZONE = os.environ.get("TIMEZONE", "America/Mexico_City")

# ---------- BOT SIN INTENTS PRIVILEGIADOS ----------
intents = discord.Intents.default()  # nada de all(), sin miembros ni mensajes
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- CARGAR COGS ----------
async def load_cogs():
    await bot.load_extension("cogs.moodle_calendar")

asyncio.run(load_cogs())

# ---------- CORRER BOT ----------
bot.run(TOKEN)



