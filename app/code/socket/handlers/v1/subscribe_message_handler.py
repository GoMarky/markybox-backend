from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs, WSMsgType, WSMessage
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService
import json


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
                    await self.on_message(ws, msg.json())

        return ws

    async def on_message(self, ws: web.WebSocketResponse, message: dict):
        command_type = message.get('type')
        user_name = message.get('user_name')
        note_id = message.get('note_nanoid')

        if command_type == 'enter_room':
            return await self.on_enter_room(ws, user_name, note_id)

    async def on_enter_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        response = dict()

        response['type'] = 'enter_room'
        response['data'] = {
            'user_name': user_name
        }

        print('User ' + user_name + 'entered room ' + note_id)

        await ws.send_json(response)
