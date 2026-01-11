import discord
from discord.ext import commands
import threading
import os

class DashboardBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.moodle_calendar")


intents = discord.Intents.default()
bot = DashboardBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

def run_bot():
    bot.run(os.environ["DISCORD_TOKEN"])



