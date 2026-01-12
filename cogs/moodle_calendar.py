import discord
from discord.ext import commands, tasks
import aiohttp
from icalendar import Calendar
from datetime import datetime, timedelta
import pytz
import os

class MoodleCalendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ======= VARIABLES =======
        self.tz = pytz.timezone(os.environ.get("TIMEZONE", "America/Mexico_City"))
        self.channel_id = int(os.environ.get("CHANNEL_ID", 0))
        self.moodle_ics_url = os.environ.get("MOODLE_ICS_URL", "")
        self.check_interval_min = int(os.environ.get("CHECK_INTERVAL_MIN", 10))

        # ======= ESTADO =======
        self.dashboard_id = None
        self.log_id = None
        self.known_tasks = {}

        # ======= INICIAR LOOP =======
        self.loop.change_interval(minutes=self.check_interval_min)
        self.loop.start()

    # ---------- UTILIDADES ----------
    async def fetch_calendar(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.moodle_ics_url) as r:
                    if r.status != 200:
                        print(f"❌ Error descargando calendario: {r.status}")
                        return None
                    data = await r.text()
                    return Calendar.from_ical(data)
        except Exception as e:
            print(f"❌ Error fetch_calendar: {e}")
            return None

    def classify(self, hours):
        if hours <= 10:
            return "🔴 PRIORIDAD"
        elif hours <= 24:
            return "🟠 ATENTO"
        elif hours <= 48:
            return "🟡 ALERTA"
        return None

    # ---------- LOOP PRINCIPAL ----------
    @tasks.loop(minutes=10)  # Intervalo inicial, se ajusta en __init__
    async def loop(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print("❌ No se encontró el canal. Verifica CHANNEL_ID y permisos")
            return

        cal = await self.fetch_calendar()
        if cal is None:
            print("❌ No se pudo cargar el calendario")
            return

        now = datetime.now(self.tz)

        dashboard = discord.Embed(
            title="📊 Dashboard de Tareas Moodle",
            description="Estado actualizado automáticamente",
            color=discord.Color.blurple()
        )

        cambios = {"nuevas": [], "urgentes": [], "vencidas": []}
        active_tasks = {}

        for e in cal.walk("VEVENT"):
            title = str(e.get("summary"))
            due = e.get("dtend").dt

            if not isinstance(due, datetime):
                continue

            due = due.astimezone(self.tz)
            hours = (due - now).total_seconds() / 3600
            active_tasks[title] = due

            # ---- VENCIDAS ----
            if hours <= 0:
                if title not in self.known_tasks:
                    cambios["vencidas"].append(title)
                continue

            estado = self.classify(hours)
            if not estado:
                continue

            dashboard.add_field(
                name=f"{estado} — {title}",
                value=f"⏰ {due.strftime('%d/%m %H:%M')} | ⌛ {int(hours)}h",
                inline=False
            )

            # ---- NUEVAS ----
            if title not in self.known_tasks:
                cambios["nuevas"].append((title, int(hours)))
                if hours <= 24:
                    cambios["urgentes"].append(title)

        # ---------- DASHBOARD ----------
        dashboard.set_footer(text="Sistema automático • Sin comandos")
        try:
            if not self.dashboard_id:
                msg = await channel.send(embed=dashboard)
                self.dashboard_id = msg.id
            else:
                msg = await channel.fetch_message(self.dashboard_id)
                await msg.edit(embed=dashboard)
        except Exception as e:
            print(f"❌ Error enviando dashboard: {e}")

        # ---------- LOG UNIFICADO ----------
        if any(cambios.values()):
            try:
                if self.log_id:
                    old = await channel.fetch_message(self.log_id)
                    await old.delete()
            except:
                pass

            log = discord.Embed(
                title="📝 Registro de Cambios Detectados",
                color=discord.Color.orange(),
                timestamp=now
            )

            if cambios["nuevas"]:
                log.add_field(
                    name="🆕 Tareas agregadas",
                    value="\n".join(f"• {t} ({h}h)" for t, h in cambios["nuevas"]),
                    inline=False
                )
            if cambios["urgentes"]:
                log.add_field(
                    name="🚨 Avisos importantes",
                    value="\n".join(f"• {t}" for t in cambios["urgentes"]),
                    inline=False
                )
            if cambios["vencidas"]:
                log.add_field(
                    name="⛔ Tareas vencidas",
                    value="\n".join(f"• {t}" for t in cambios["vencidas"]),
                    inline=False
                )

            try:
                log_msg = await channel.send(content="@everyone", embed=log)
                self.log_id = log_msg.id
            except Exception as e:
                print(f"❌ Error enviando log: {e}")

        # ---------- GUARDAR ESTADO ----------
        self.known_tasks = active_tasks

    # ---------- LIMPIEZA AL INICIAR ----------
    @loop.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            # Borrar mensajes anteriores del bot
            async for msg in channel.history(limit=50):
                if msg.author == self.bot.user:
                    try:
                        await msg.delete()
                    except:
                        pass

        # Resetear estado
        self.dashboard_id = None
        self.log_id = None
        self.known_tasks = {}
        print("✅ MoodleCalendar cog listo y loop iniciado")

# ---------- SETUP ----------
async def setup(bot):
    await bot.add_cog(MoodleCalendar(bot))


