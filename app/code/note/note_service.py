from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.code.session.session_service import SessionService
from uuid import UUID
from app.base.date import dt_converter


class NoteService(Disposable):
    def __init__(self, database_service: DatabaseService, session_service: SessionService):
        self.database_service = database_service
        self.session_service = session_service

    def transform_note(self, note: dict) -> dict:
        user_note = dict()

        note_id = note.get('note_id')
        title = note.get('note_title')
        data = note.get('note_data')
        created_at = note.get('created_at')
        updated_at = note.get('updated_at')
        note_lang = note.get('note_lang')

        user_note['id'] = note_id.__str__()
        user_note['title'] = title
        user_note['data'] = data
        user_note['createdAt'] = dt_converter(created_at)
        user_note['updatedAt'] = dt_converter(updated_at)
        user_note['lang'] = note_lang

        return user_note

    async def apply_settings(self, session_id: str, note_id: str, options: dict):
        print(options)

    async def get_note_by_id(self, session_id: str, note_id: str):
        if session_id:
            await self.session_service.get_session_by_id(session_id)

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
                SELECT note_id, note_data, note_lang from markybox.notes
                WHERE note_id='{note_id}';
                '''.format(note_id=note_id)

            note_result = await connection.execute(sql)

            if note_result.rowcount == 0:
                return None

            note = [dict(row) for row in note_result].pop()

            return self.transform_note(note)

    async def get_notes_by_session_id(self, session_id: str):
        user = await self.session_service.get_session_by_id(session_id)
        user_id = user.get('user_id')

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            SELECT 
            notes.user_id, 
            notes.note_id, 
            notes.note_title, 
            notes.note_data, 
            notes.created_at, 
            notes.updated_at, 
            notes.note_lang
            FROM markybox.notes
            WHERE notes.user_id='{user_id}' 
            ORDER BY notes.updated_at DESC'''.format(user_id=user_id)

            notes_result = await connection.execute(sql)

            if notes_result.rowcount == 0:
                return None

            raw_notes = [dict(row) for row in notes_result]
            notes = []

            for note in raw_notes:
                notes.append(self.transform_note(note))

            return notes

    async def create_note(self, session_id: str, note_title: str = 'unnamed', note_data: str = ''):
        user_id = None

        if session_id:
            user = await self.session_service.get_session_by_id(session_id)

            user_id = user.get('user_id')

        async with self.database_service.instance.acquire() as connection:
            if user_id:
                sql = '''
            insert into markybox.notes (user_id, note_title, note_data)
            values ('{user_id}', '{note_title}','{note_data}')
            RETURNING NOTE_ID;'''.format(user_id=user_id, note_title=note_title,
                                         note_data=note_data)
            else:
                sql = '''
            insert into markybox.notes (note_title, note_data)
            values ('{note_title}','{note_data}')
            RETURNING NOTE_ID;'''.format(note_title=note_title,
                                         note_data=note_data)

            create_note_result = await connection.execute(sql)
            note_body = [dict(row) for row in create_note_result].pop()
            note_uuid: UUID = note_body.get('note_id')

            note_id = note_uuid.hex

            return {
                'id': note_id,
            }

    async def update_note(self, session_id: str, note_id: str, note_data: str, note_lang: str):
        if session_id:
            await self.session_service.check_session(session_id)

        async with self.database_service.instance.acquire() as connection:
            note_data_sql: str = '''
            UPDATE markybox.notes 
            SET note_data = $${note_data}$$ 
            WHERE note_id = $${note_id}$$;'''.format(note_id=note_id, note_data=note_data)

            await connection.execute(note_data_sql)

            if note_lang:
                note_lang_sql: str = '''
                UPDATE markybox.notes 
                SET note_lang = $${note_lang}$$ 
                WHERE note_id = $${note_id}$$;'''.format(note_id=note_id, note_lang=note_lang)

                await connection.execute(note_lang_sql)

    async def delete_note(self, session_id: str, note_id: str):
        await self.session_service.check_session(session_id)

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            delete from markybox.notes
            where note_id='{note_id}';'''.format(note_id=note_id)

            await connection.execute(sql)
