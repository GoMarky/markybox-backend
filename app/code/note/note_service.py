from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.code.session.session_service import SessionService


class NoteService(Disposable):
    def __init__(self, database_service: DatabaseService, session_service: SessionService):
        self.database_service = database_service
        self.session_service = session_service

    async def check_session(self, session_id: str):
        await self.session_service.check_session(session_id)

    async def create_note(self, session_id: str, note_title: str, note_data: str):
        print(note_title)
        print(note_data)

        await self.session_service.check_session(session_id)

        async with self.database_service.instance.acquire() as connection:
            note_id = session_id

            return {
                'id': note_id,
            }

    async def update_note(self, session_id: str, note_id: str, note_data: str):
        await self.session_service.check_session(session_id)

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            UPDATE notes 
            SET note_data = '{note_data}' 
            WHERE note_id = '{note_id}';'''.format(note_id=note_id, note_data=note_data)

            await connection.execute(sql)

    async def delete_note(self, session_id: str, note_id: str):
        await self.session_service.check_session(session_id)

        async with self.database_service.instance.acquire() as connection:
            print(note_id)
            return
