from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from psycopg2 import IntegrityError
from app.base.errors import DBRecordNotFoundError

from app.code.user.validation.user import DELETE_USER_SCHEMA
from jsonschema import validate, ValidationError as JSONValidationError
from app.platform.router.router_service import RouterService
from app.code.user.user_service import UserService


class UserDeleteHandler(RouteHandler):
    path = '/user/'

    def __init__(self, log_service: LogService, router_service: RouterService, user_service: UserService):
        super().__init__(log_service)

        self.path = UserDeleteHandler.path
        self.request_type = hdrs.METH_DELETE

        self.router_service = router_service
        self.user_service = user_service

        self.name = 'resources.user.delete'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        body.pop('sessionId')

        try:
            validate(body, DELETE_USER_SCHEMA)

            return await self.do_handle(body)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict):
        client_id: int = body['id']

        try:
            await self.user_service.delete_user_by_id(client_id)

            return self.router_service.send_success_response(self.name, 'OK')
        except IntegrityError as error:
            return self.router_service.send_bad_request_response(self.name, error.pgerror)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)
