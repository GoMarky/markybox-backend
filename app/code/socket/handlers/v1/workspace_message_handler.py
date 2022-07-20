from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs, WSMsgType
from asyncio import CancelledError
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService
from app.code.socket.socket_service import SocketService


class WorkspaceMessageHandler(RouteHandler):
    path = '/workspace/{id}/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = WorkspaceMessageHandler.path
        self.request_type = hdrs.METH_GET

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.workspace.message'

    async def handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self.on_message(ws, msg.json())
                elif msg.type == WSMsgType.ERROR:
                    pass
        except CancelledError:
            print(f"the websocket({ws}) cancelled")
        finally:
            return ws

    async def on_message(self, ws: web.WebSocketResponse, message: dict):
        command_type = message.get('type')

        return await ws.send_json(
            {'type': 'error', 'data': {'message': 'Unrecognized command_type received ' + command_type}})
