from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService
from app.base.errors import DBRecordNotFoundError
from app.code.session.validation.session import REGISTER_USER_SCHEMA
from jsonschema import validate, ValidationError


class SessionRegisterUserHandler(RouteHandler):
    path = '/session/register/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = SessionRegisterUserHandler.path
        self.request_type = hdrs.METH_POST

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.session.register.user'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body: dict = await request.json()

            validate(body, REGISTER_USER_SCHEMA)

            return await self.do_handle(body)
        except DBRecordNotFoundError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict) -> web.Response:
        try:
            result = await self.session_service.register_user(body)

            return self.router_service.send_success_response(self.name, result)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)
