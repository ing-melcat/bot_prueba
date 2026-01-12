import discord
from discord.ext import commands
import os
import asyncio

# ---------- INTENTS MÍNIMOS ----------
intents = discord.Intents.default()  # Solo lo básico, no pide presencia ni members ni message content

# ---------- BOT ----------
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- CARGAR COGS ----------
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog cargado: {filename}")
            except Exception as e:
                print(f"❌ Error cargando {filename}: {e}")

# ---------- EVENTOS BÁSICOS ----------
@bot.event
async def on_ready():
    print(f"🤖 Bot listo! Conectado como {bot.user} (ID: {bot.user.id})")

# ---------- RUN ----------
async def main():
    await load_cogs()
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("❌ ERROR: No se encontró DISCORD_TOKEN en variables de entorno")
        return
    await bot.start(token)

asyncio.run(main())




