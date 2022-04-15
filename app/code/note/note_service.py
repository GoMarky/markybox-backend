from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService


class NoteService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_note(self, body: dict):
        session_id = body.get('sessionId')

        async with self.database_service.instance.acquire() as connection:
            note_id = session_id

            return {
                'id': note_id,
            }

    async def update_note(self):
        async with self.database_service.instance.acquire() as connection:
            return

    async def delete_note(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return
