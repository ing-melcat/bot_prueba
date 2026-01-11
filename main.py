import os
import threading
import discord
from discord.ext import commands

# Health check
from health import start_health_server

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Cargar cog manualmente
async def load_cogs():
    await bot.load_extension("cogs.moodle_calendar")

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# Arrancar health check en otro hilo
threading.Thread(target=start_health_server, daemon=True).start()

# Main
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())  # carga el cog
    bot.run(os.environ["DISCORD_TOKEN"])


