from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.base.errors import DBRecordNotFoundError

from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService


class SessionLogoutHandler(RouteHandler):
    path = '/session/logout/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = SessionLogoutHandler.path
        self.request_type = hdrs.METH_POST

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.session.logout'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        session_id = body.get('sessionId')

        try:
            await self.session_service.delete_session_by_id(session_id)

            return self.router_service.send_success_response(self.name, 'OK')
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)
