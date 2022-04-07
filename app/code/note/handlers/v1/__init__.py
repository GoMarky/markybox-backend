from app.code.session.handlers.v1.session_info_handler import SessionInfoHandler
from app.code.session.handlers.v1.session_login_handler import SessionLoginHandler
from app.code.session.handlers.v1.session_logout_handler import SessionLogoutHandler

__all__ = ['session_routes']

session_routes = [SessionLoginHandler, SessionInfoHandler, SessionLogoutHandler]

for route in session_routes:
    route.path = '/v1' + route.path
