from aiohttp import web
import config

async def health(request):
    return web.Response(text="OK")

def start_health_server():
    app = web.Application()
    app.router.add_get("/health", health)
    web.run_app(app, port=config.HEALTH_PORT)
