from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.platform.database.database_service import DatabaseService


class NoteService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_note(self, request: web.Request, body: dict):
        session_id = body.get('sessionId')

        print(session_id)

        async with request.app['db'].acquire() as connection:
            id = session_id

            return {
                'id': id,
            }

    async def update_note(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return

    async def delete_note(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return
