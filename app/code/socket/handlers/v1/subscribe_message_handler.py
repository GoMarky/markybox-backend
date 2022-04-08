from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs, WSMsgType
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService


class SubscribeMessageHandler(RouteHandler):
    path = '/subscribe/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = SubscribeMessageHandler.path
        self.request_type = hdrs.METH_GET

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.socket.subscribe'

    async def handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await self.do_handle(ws, msg)
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')

        return ws

    async def do_handle(self, ws: web.WebSocketResponse, msg):
        response: dict = dict()
        response['ok'] = True

        print(msg.data)

        await ws.send_json(response)
