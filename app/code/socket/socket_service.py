from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from aiohttp import web


class SocketService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

        self.rooms = {}

    async def send_all(self, user_name: str, note_id: str, message: dict):
        room_set = self.rooms.get(note_id)

        position = message.get('position')

        response = dict()
        response['type'] = 'editor_action'
        response['data'] = {
            'user_name': user_name,
            'position': position
        }

        for room_client in room_set:
            conn = room_client[1]
            await conn.send_json(response)

    def get_client_by_connection(self, ws: web.WebSocketResponse):
        for room_id, room_set in self.rooms.items():
            for client in room_set:
                connection = client[1]

                if ws == connection:
                    return room_id, client

        return None

    async def remove_client(self, ws: web.WebSocketResponse):
        result = self.get_client_by_connection(ws)

        if result is None:
            return

        room_id, client = result
        user_name = client[0]

        room_set = self.rooms.get(room_id)
        room_set.remove(client)

        response = dict()
        response['type'] = 'leave_room'
        response['data'] = {
            'user_name': user_name,
            'text': 'User ' + user_name + ' left room.'
        }

        for room_client in room_set:
            conn = room_client[1]
            await conn.send_json(response)

    async def on_create_or_enter_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        if self.rooms.get(note_id):
            return await self.enter_room(ws, user_name, note_id)
        else:
            return await self.create_room(ws, user_name, note_id)

    async def enter_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        response = dict()
        response['type'] = 'enter_room'
        response['data'] = {
            'user_name': user_name,
            'text': 'User ' + user_name + ' entered room.'
        }

        for client in self.rooms.get(note_id):
            conn = client[1]

            await conn.send_json(response)

        room_set: set = self.rooms.get(note_id)
        room_set.add((user_name, ws))

        return await ws.send_json({
            'type': 'info',
            'data': {
                'text': 'You entered room ' + note_id + '.'
            }
        })

    async def create_room(self, ws: web.WebSocketResponse, user_name: str, note_id: str):
        response = dict()
        response['type'] = 'create_room'
        response['data'] = {
            'note_id': note_id
        }

        new_set = set()
        new_set.add((user_name, ws))
        self.rooms[note_id] = new_set

        await ws.send_json(response)

    async def leave_room(self, ws: web.WebSocketResponse):
        return await self.remove_client(ws)
