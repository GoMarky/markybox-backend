from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
import socketio


class SocketService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

        self.sio = self.sio = socketio.AsyncServer(async_mode='aiohttp')

    async def create_room(self):
        return
