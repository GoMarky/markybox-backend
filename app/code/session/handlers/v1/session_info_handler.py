from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_unexpected_error_response, send_not_found_response

from app.db import users
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
        try:
            body: dict = await request.json()

            sessionId = body.get('sessionId')

            return self.router_service.send_not_found_response(self.name,
                                                               "Session with id" + sessionId + " was not found")
        except RuntimeError as error:
            return self.router_service.send_unexpected_error_response(self.name, "")

    async def do_handle(self, session_result, conn) -> web.Response:
        for session in session_result:
            session = dict(session)

            return self.router_service.send_success_response(self.name, session)
