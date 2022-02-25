from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from json import JSONDecodeError
from app.base.errors import ValidationError, DBRecordNotFoundError

from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService


class SessionIdMiddleware(MiddlewareHandler):
    def __init__(self, router_service: RouterService, session_service: SessionService):
        super().__init__()

        self.router_service = router_service
        self.session_service = session_service

        self.routes = []

    async def call(self, request_name: str, request: web.Request, handler):
        if request_name in self.routes:
            try:
                await self.handle(request)
            except ValidationError as error:
                return self.router_service.send_bad_request_response(request_name, error.message)
            except DBRecordNotFoundError as error:
                return self.router_service.send_not_found_response(request_name, error.message)
            except JSONDecodeError as error:
                print(error)

        return await handler(request)

    async def handle(self, request: web.Request):
        body = await request.json()

        if 'sessionId' in body:
            session_id = body['sessionId']

            if isinstance(session_id, str):
                return await self.session_service.get_user_session_by_id(session_id)

            raise ValidationError('Field sessionId must be a string')
        else:
            raise ValidationError('Field sessionId is required')
