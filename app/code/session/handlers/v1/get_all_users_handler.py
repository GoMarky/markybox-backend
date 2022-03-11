from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_unexpected_error_response, send_not_found_response

from app.db import users
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService


class GetAllUsersHandler(RouteHandler):
    path = '/users/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = GetAllUsersHandler.path
        self.request_type = hdrs.METH_GET

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.users.all'

    async def handler(self, request: web.Request) -> web.Response:
        async with request.app['db'].acquire() as connection:
            all_users = []

            users_result = await connection.execute(
                '''SELECT users.id, users.email FROM users ORDER BY id;''')

            for user in users_result:
                all_users.append(dict(user))

        return self.router_service.send_success_response(self.name, all_users)

    async def do_handle(self, session_result, conn) -> web.Response:
        return
