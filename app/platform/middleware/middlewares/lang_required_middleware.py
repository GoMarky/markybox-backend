from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from app.platform.router.router_service import RouterService


class LangRequiredMiddleware(MiddlewareHandler):
    def __init__(self, router_service: RouterService):
        super().__init__()

        self.router_service = router_service

        self.routes = [
            'resources.post.get_by_slug',
            'resources.post.get_all'
        ]

    async def call(self, request_name: str, request: web.Request, handler):
        lang = 'ru'

        if request_name in self.routes:
            lang = await self.handle(request)

        request['lang'] = lang

        return await handler(request)

    async def handle(self, request: web.Request) -> str:
        query = dict(request.query)

        lang = query.get('lang')

        if not lang:
            lang = 'ru'

        return lang
