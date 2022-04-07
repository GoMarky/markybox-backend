from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.db import users
from app.base.errors import DBRecordNotFoundError
from app.base.uuid import generate_id
from app.platform.database.database_service import DatabaseService


class SessionService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_session(self, request: web.Request, options: dict):
        email: str = options.get('email')
        hashed_password: str = options.get('password')

        normalized_password: str = hashed_password[::-1]

        print(email)
        print(normalized_password)

        async with request.app['db'].acquire() as conn:
            return

    async def get_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return

    async def delete_session_by_id(self, session_id: str):
        async with self.database_service.instance.acquire() as connection:
            return

    def transform_session(self, session):
        new_session = dict()

        return new_session
