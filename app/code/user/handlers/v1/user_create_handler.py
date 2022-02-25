from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from app.code.user.user_service import UserService

from aiohttp import web, hdrs
from ...validation.user import CREATE_USER_SCHEMA
from jsonschema import validate, ValidationError as JSONValidationError
from psycopg2 import IntegrityError

from app.platform.router.router_service import RouterService

USER_CREATE_HANDLER_NAME = 'resources.user.create'


class UserCreateHandler(RouteHandler):
    path = '/user/'

    def __init__(self, log_service: LogService, user_service: UserService, router_service: RouterService):
        super().__init__(log_service)

        self.user_service = user_service
        self.router_service = router_service

        self.path = UserCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.name = USER_CREATE_HANDLER_NAME

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        try:
            validate(body, CREATE_USER_SCHEMA)

            return await self.do_handle(body)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, user: dict):
        try:
            user_result = await self.user_service.create_user(user)

            return self.router_service.send_success_response(self.name, user_result)
        except IntegrityError as error:
            return self.router_service.send_bad_request_response(self.name, error.pgerror)
        except Exception:
            return self.router_service.send_unexpected_error_response(self.name)
