from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService


class SocketService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def on_message_handler(self):
        return
