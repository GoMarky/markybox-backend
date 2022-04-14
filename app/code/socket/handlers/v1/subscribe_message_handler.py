from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs, WSMsgType
from asyncio import CancelledError
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService
from app.code.socket.socket_service import SocketService


class SubscribeMessageHandler(RouteHandler):
    path = '/subscribe/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService,
                 socket_service: SocketService):
        super().__init__(log_service)

        self.path = SubscribeMessageHandler.path
        self.request_type = hdrs.METH_GET

        self.session_service = session_service
        self.router_service = router_service
        self.socket_service = socket_service

        self.name = 'client.socket.subscribe'

    async def handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self.on_message(ws, msg.json())
                elif msg.type == WSMsgType.ERROR:
                    await self.socket_service.remove_client(ws)
        except CancelledError:
            await self.socket_service.remove_client(ws)
        finally:
            await self.socket_service.remove_client(ws)
            return ws

    async def on_message(self, ws: web.WebSocketResponse, message: dict):
        command_type = message.get('type')
        user_name = message.get('user_name')
        note_id = message.get('note_nanoid')

        if command_type == 'enter_room':
            return await self.socket_service.on_create_or_enter_room(ws, user_name, note_id)
        if command_type == 'leave_room':
            return await self.socket_service.leave_room(ws)

        return await ws.send_json(
            {'type': 'error', 'data': {'message': 'Unrecognized command_type received ' + command_type}})
