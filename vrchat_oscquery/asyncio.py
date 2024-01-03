import asyncio
from aiohttp import web
from zeroconf.asyncio import AsyncZeroconf
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from .common import _unused_port,  _oscjson_response, _create_service_info


async def vrc_osc(name: str, dispatcher: Dispatcher, foreground=False):
    port = _unused_port()

    await AsyncZeroconf().async_register_service(_create_service_info(name, port))

    await AsyncIOOSCUDPServer(
        ("127.0.0.1", port), dispatcher, asyncio.get_event_loop()
    ).create_serve_endpoint()

    app = web.Application()

    def req_handler(req):
        return web.Response(body=_oscjson_response(req.path_qs, port))

    app.add_routes([web.get("/", req_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "127.0.0.1", port).start()

    if foreground:
        await asyncio.gather(*asyncio.all_tasks())
