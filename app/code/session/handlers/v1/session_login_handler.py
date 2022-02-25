from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService
from app.base.errors import AuthenticatedError, AuthErrorCode


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

        if 'email' in body and 'password' in body:
            user = await self.session_service.get_user_by_email(request, body['email'])

            if user:
                try:
                    session = await self.session_service.login_user(request, user)

                    transformed_session = self.session_service.transform_session(session, user)

                    return self.router_service.send_success_response(self.name, transformed_session)
                except AuthenticatedError as error:
                    if error.type is AuthErrorCode.InvalidPassword:
                        return self.router_service.send_not_found_response(self.name,
                                                                           'Email or password are incorrect')
            else:
                return self.router_service.send_not_found_response(self.name, 'User not found')

        return self.router_service.send_bad_request_response(self.name, 'Fields email, password are require.')
