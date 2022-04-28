from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService
from app.base.errors import DBRecordNotFoundError


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
            session_id: str = body.get('sessionId')

            return await self.do_handle(session_id)
        except Exception as error:
            print(error)
            return self.router_service.send_unexpected_error_response(self.name, "")

    async def do_handle(self, session_id: str) -> web.Response:
        try:
            result = await self.session_service.get_session_by_id(session_id)

            return self.router_service.send_success_response(self.name, result)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)
