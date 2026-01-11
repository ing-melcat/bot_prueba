import discord
from discord.ext import commands
import config
import threading

from health import start_health_server


class DashboardBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.moodle_calendar")


intents = discord.Intents.default()
bot = DashboardBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


if __name__ == "__main__":
    # 🔍 Health check (MISMO BOT, MISMO PROCESO)
    threading.Thread(
        target=start_health_server,
        daemon=True
    ).start()

    bot.run(config.DISCORD_TOKEN)
