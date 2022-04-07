from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService
from jsonschema import validate, ValidationError as JSONValidationError
from app.code.session.validation.session import CREATE_SESSION_SCHEMA


class SessionLoginHandler(RouteHandler):
    path = '/session/login/'

    def __init__(self, log_service: LogService, router_service: RouterService, session_service: SessionService):
        super().__init__(log_service)

        self.path = SessionLoginHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.log_service = log_service
        self.session_service = session_service

        self.name = 'client.session.login'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        try:
            validate(body, CREATE_SESSION_SCHEMA)

            session = await self.session_service.create_session(request, body)

            self.router_service.send_success_response(self.name, session)

        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

        return self.router_service.send_not_found_response(self.name, 'Session not found')
