from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.code.session.session_service import SessionService
from uuid import UUID


class NoteService(Disposable):
    def __init__(self, database_service: DatabaseService, session_service: SessionService):
        self.database_service = database_service
        self.session_service = session_service

    async def get_note_by_id(self, note_id: str):
        return

    async def get_notes_by_session_id(self, session_id: str):
        user = await self.session_service.get_session_by_id(session_id)
        user_id = user.get('user_id')

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            SELECT users.user_id, notes.note_id, notes.title, notes.note_data, notes.created_at, notes.updated_at
            FROM users LEFT JOIN notes ON users.user_id=notes.user_id
            WHERE users.user_id='{user_id}' AND notes.note_data IS NOT NULL
            ORDER BY notes.updated_at DESC;'''.format(user_id=user_id)

            notes_result = await connection.execute(sql)

            note_body = [dict(row) for row in notes_result].pop()

            print(note_body)

    async def create_note(self, session_id: str, note_title: str = 'unnamed', note_data: str = ''):
        user = await self.session_service.get_session_by_id(session_id)

        user_id = user.get('user_id')

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            insert into notes (user_id, title, note_data)
            values ('{user_id}', '{note_title}','{note_data}')
            RETURNING NOTE_ID;'''.format(user_id=user_id, note_title=note_title,
                                         note_data=note_data)

            create_note_result = await connection.execute(sql)
            note_body = [dict(row) for row in create_note_result].pop()
            note_uuid: UUID = note_body.get('note_id')

            note_id = note_uuid.hex

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
            sql: str = '''
            delete from notes
            where note_id='{note_id}';'''.format(note_id=note_id)

            await connection.execute(sql)
