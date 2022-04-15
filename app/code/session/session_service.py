from app.platform.instantiation.disposable import Disposable
from app.base.errors import DBRecordNotFoundError
from app.platform.database.database_service import DatabaseService
from app.platform.router.router_service import RouterService


class SessionService(Disposable):
    def __init__(self, database_service: DatabaseService, router_service: RouterService):
        self.database_service = database_service
        self.router_service = router_service

    async def get_user_by_email_and_password(self, email: str, password: str):
        async with self.database_service.instance.acquire() as connection:
            return

    async def create_session(self, body: dict):
        email: str = body.get('email')
        hashed_password: str = body.get('password')

        normalized_password: str = hashed_password[::-1]

        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            INSERT INTO session (user_id)
            VALUES ('{user_id}') RETURNING session_id;
            '''.format(user_id='user_id')

            result = await connection.execute(sql)

            arr = [dict(row) for row in result]
            body: dict = arr.pop()

    async def get_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
                        select session_id, user_name, email, 
                        array_agg(ARRAY[notes.note_id::text, notes.title, notes.note_data,notes.created_at::text,notes.updated_at::text]) AS user_notes
                        from session, users, notes 
                        where users.user_id=session.user_id AND users.user_id=notes.user_id AND session_id='{session_id}'
                        group by session.session_id, users.email, users.user_name;
                        '''.format(session_id=session_id)

            result = await connection.execute(sql)

            if result.rowcount == 0:
                raise DBRecordNotFoundError("session_id with " + session_id + " not found")

            arr = [dict(row) for row in result]
            user_notes = []
            body: dict = arr.pop()

            print(body)

            session_uuid = body.pop('session_id')
            session_uuid = str(session_uuid)

            raw_notes = body.get('user_notes')
            user_name = body.pop('user_name')

            for note in raw_notes:
                user_note = dict()

                note_id = note[0]
                title = note[1]
                data = note[2]
                created_at = note[3]
                updated_at = note[4]

                user_note['id'] = note_id
                user_note['title'] = title
                user_note['data'] = data
                user_note['createdAt'] = created_at
                user_note['updatedAt'] = updated_at

                user_notes.append(user_note)

            body['session_id'] = session_uuid
            body['notes'] = user_notes
            body['user'] = user_name
            body.pop('user_notes')

            return body

    async def delete_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return
