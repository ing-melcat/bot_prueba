import os
import asyncio
import discord
from discord.ext import commands

# Intents necesarios
intents = discord.Intents.default()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento on_ready
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# Función para cargar cogs
async def load_cogs():
    await bot.load_extension("cogs.moodle_calendar")

# Main
if __name__ == "__main__":
    # Carga cogs antes de correr el bot
    asyncio.run(load_cogs())
    
    # Ejecuta bot
    bot.run(os.environ["DISCORD_TOKEN"])


