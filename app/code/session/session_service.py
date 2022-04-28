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
            user_sql: str = '''
            select users.user_id, user_name, email, array_agg(ARRAY[
            notes.note_id::text, 
            notes.title, 
            notes.note_data, 
            notes.created_at::text,
            notes.updated_at::text]) AS user_notes
            from users, notes 
            where users.user_id=notes.user_id AND users.email='{user_email}' AND users.password='{user_password}'
            group by users.email, users.user_name, users.user_id;
            '''.format(user_email=email, user_password=password)

            user_result = await connection.execute(user_sql)

            if user_result.rowcount == 0:
                raise DBRecordNotFoundError("User with specified email not found")

            arr = [dict(row) for row in user_result]
            body: dict = arr.pop()

            return body

    async def create_session(self, body: dict):
        email: str = body.get('email')
        hashed_password: str = body.get('password')
        normalized_password: str = hashed_password[::-1]

        user = await self.get_user_by_email_and_password(email, normalized_password)

        user_id = user.get('user_id')

        async with self.database_service.instance.acquire() as connection:
            session_sql: str = '''
            INSERT INTO session (user_id)
            VALUES ('{user_id}') RETURNING session_id::text;
            '''.format(user_id=user_id)

            session_result = await connection.execute(session_sql)

            arr = [dict(row) for row in session_result]
            session: dict = arr.pop()
            session_id = session.get('session_id')

            user['session_id'] = session_id

            return await self.get_session_by_id(session_id)

    async def get_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            SELECT session_id, users.user_id, user_name, email
            FROM session LEFT JOIN users ON session.user_id=users.user_id
            WHERE session_id='{session_id}';
                                    '''.format(session_id=session_id)

            get_session_result = await connection.execute(sql)

            if get_session_result.rowcount == 0:
                raise DBRecordNotFoundError("session_id with " + session_id + " not found")

            arr = [dict(row) for row in get_session_result]
            body: dict = arr.pop()

            session_uuid = body.pop('session_id')
            session_uuid = str(session_uuid)
            user_name = body.pop('user_name')

            body['session_id'] = session_uuid
            body['user'] = user_name

            return body

    async def check_session(self, session_id: str) -> bool:
        async with self.database_service.instance.acquire() as connection:
            sql: str = '''
            SELECT EXISTS (SELECT 1 from session where session_id = '{session_id}');'''.format(session_id=session_id)

            has_session_result = await connection.execute(sql)

            if has_session_result:
                return True

            return False

    async def delete_session_by_id(self, session_id: str):
        await self.check_session(session_id)

        sql: str = '''
                DELETE FROM session
                WHERE session_id = '{session_id}';'''.format(session_id=session_id)

        async with self.database_service.instance.acquire() as connection:
            await connection.execute(sql)
