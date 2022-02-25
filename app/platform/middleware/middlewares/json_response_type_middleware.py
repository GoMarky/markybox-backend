from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from app.base.errors import NetworkError
from app.platform.router.router_service import RouterService


class JSONResponseTypeMiddleware(MiddlewareHandler):
    def __init__(self, router_service: RouterService):
        super().__init__()

        self.router_service = router_service

        self.routes = map(lambda route: route.name, router_service.routes)

    async def call(self, request_name: str, request: web.Request, handler):
        if request_name in self.routes:
            try:
                await self.handle(request_name, request)
            except NetworkError as error:
                return self.router_service.send_bad_request_response(request_name, error.message)

        return await handler(request)

    async def handle(self, request_name: str, request: web.Request):
        if request.content_type != 'application/json':
            raise NetworkError('Request ' + request_name + ' must bet application/json type')
