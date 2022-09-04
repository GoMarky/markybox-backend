from app.platform.instantiation.disposable import Disposable
from app.base.errors import DBRecordNotFoundError
from app.platform.database.database_service import DatabaseService
from app.platform.router.router_service import RouterService


class SessionService(Disposable):
    def __init__(self, database_service: DatabaseService, router_service: RouterService):
        self.database_service = database_service
        self.router_service = router_service

    async def apply_settings(self, session_id: int, options: dict):
        print(options)

    async def register_user(self, options: dict):
        user_name = options.get('userName')
        user_email = options.get('email')
        user_password = options.get('password')

        normalized_password: str = user_password[::-1]

        async with self.database_service.instance.acquire() as connection:
            register_user_sql: str = '''
            INSERT INTO markybox.users (user_name,email,password) 
            VALUES ('{user_name}','{user_email}','{user_password}')
        '''.format(user_name=user_name, user_email=user_email, user_password=normalized_password)

            await connection.execute(register_user_sql)

            return await self.get_user_by_email_and_password(user_email, normalized_password)

    async def get_user_by_email_and_password(self, email: str, password: str):
        async with self.database_service.instance.acquire() as connection:
            user_sql: str = '''
            select users.user_id, user_name, email
            from markybox.users
            where users.email='{user_email}' AND users.password='{user_password}'
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
            INSERT INTO markybox.sessions (user_id)
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
            FROM markybox.sessions LEFT JOIN markybox.users ON sessions.user_id=users.user_id
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
            SELECT EXISTS (SELECT 1 from markybox.sessions where session_id = '{session_id}');'''.format(
                session_id=session_id)

            has_session_result = await connection.execute(sql)

            if has_session_result:
                return True

            return False

    async def delete_session_by_id(self, session_id: str):
        await self.check_session(session_id)

        sql: str = '''
                DELETE FROM markybox.sessions
                WHERE session_id = '{session_id}';'''.format(session_id=session_id)

        async with self.database_service.instance.acquire() as connection:
            await connection.execute(sql)
