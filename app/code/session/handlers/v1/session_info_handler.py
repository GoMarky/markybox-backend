from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_success_response, send_unexpected_error_response, send_not_found_response

from app.db import sessions, users
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService


class SessionInfoHandler(RouteHandler):
    path = '/session/info/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = SessionInfoHandler.path
        self.request_type = hdrs.METH_POST

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.session.info'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        session_id = body['sessionId']

        async with request.app['db'].acquire() as connection:
            try:
                session = await connection.execute(
                    sessions.select().where(sessions.c.session_id == session_id)
                )

                if session.rowcount == 0:
                    return send_not_found_response(self.name, 'Session was not found.')
                else:
                    return await self.do_handle(session, connection)
            except Exception:
                return send_unexpected_error_response(self.name)

    async def do_handle(self, session_result, conn) -> web.Response:
        for session in session_result:
            session = dict(session)

            client_id = session['client_id']

            user_result = await conn.execute(users.select().where(users.c.client_id == client_id))

            for user in user_result:
                user = dict(user)

                transformed_session = self.session_service.transform_session(session, user)

                return self.router_service.send_success_response(self.name, transformed_session)
