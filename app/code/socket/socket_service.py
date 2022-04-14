from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from aiohttp import web


class SocketService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

        self.rooms = {}
        self.clients = set()

    def remove_client(self, ws: web.WebSocketResponse):
        print("Remove client with reason " + ws.reason)
        self.clients.remove(ws)

    async def on_create_or_enter_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        if self.rooms.get(note_id):
            return await self.enter_room(ws, user_name, note_id)
        else:
            return await self.create_room(ws, user_name, note_id)

    async def enter_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        response = dict()

        response['type'] = 'enter_room'
        response['data'] = {
            'user_name': user_name
        }

        room_set: set = self.rooms.get(note_id)
        room_set.add(user_name)

        for client in self.clients:
            await client.send_json(response)

        await ws.send_json(response)

    async def create_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        response = dict()

        response['type'] = 'create_room'
        response['data'] = {
            'note_id': note_id
        }

        new_set = set()

        self.clients.add(ws)
        new_set.add(user_name)
        self.rooms[note_id] = new_set

        await ws.send_json(response)

    async def leave_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        room_set: set = self.rooms.get(note_id)

        room_set.remove(user_name)
        self.clients.remove(ws)
