from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.base.errors import DBRecordNotFoundError
from app.db import users
from sqlalchemy import sql


class UserService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_user(self, user: dict):
        async with self.database_service.instance.acquire() as conn:
            formatted_user = {
                'client_name': user['name'],
                'client_email': user['email'],
                'password': user['password']
            }

            await conn.execute(users.insert().values(formatted_user))

            result = await conn.execute(
                sql.select([sql.func.max(users.c.client_id).label('client_id')])
            )

            user = await result.fetchone()

            return dict(user)

    async def update_user(self):
        pass

    async def delete_user_by_id(self, client_id: int):
        async with self.database_service.instance.acquire() as conn:
            result = await conn.execute(users.delete().where(users.c.client_id == client_id))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Client with client_id ' + str(client_id) + ' was not found')

    async def delete_user_by_email(self, email: str):
        async with self.database_service.instance.acquire() as conn:
            result = await conn.execute(users.delete().where(users.c.client_email == email))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Client with email ' + str(email) + ' was not found')

    async def get_user(self):
        pass
