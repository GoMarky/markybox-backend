from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.db import sessions
from app.base.errors import DBRecordNotFoundError
from app.base.uuid import generate_id
from app.platform.database.database_service import DatabaseService


class SessionService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_session(self, request: web.Request, options: dict):
        author: str = options.get('author')
        removeable: bool = options.get('removeable')

        async with request.app['db'].acquire() as conn:
            has_session_result = await conn.execute(sessions.select().where(sessions.c.client_id == uuid))

            session_id = generate_id(20)

            await conn.execute(sessions.insert().values({
                'session_id': session_id,
            }))

    async def get_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            session = await connection.execute(
                sessions.select().where(sessions.c.session_id == session_id)
            )

            if session.rowcount == 0:
                raise DBRecordNotFoundError('Session with id ' + session_id + ' was not found.')

            return dict(await session.fetchone())

    async def delete_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            result = await connection.execute(sessions.delete().where(sessions.c.session_id == session_id))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Session with id ' + session_id + ' was not found.')

    def transform_session(self, session, user):
        new_session = dict()

        return new_session
