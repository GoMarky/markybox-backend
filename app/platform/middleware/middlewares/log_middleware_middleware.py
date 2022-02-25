from app.platform.middleware.middleware_handler import MiddlewareHandler
from app.platform.log.log_service import LogService
from aiohttp import web


class LogMiddleware(MiddlewareHandler):
    def __init__(self, log_service: LogService):
        super().__init__()

        self.log_service = log_service
        self.routes = []

    async def call(self, request_name: str, request: web.Request, handler):
        self.log_service.info('LogMiddleware - request ' + request_name + ' called.')

        return await handler(request)
