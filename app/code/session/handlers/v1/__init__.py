from app.code.session.handlers.v1.session_info_handler import SessionInfoHandler
from app.code.session.handlers.v1.session_login_handler import SessionLoginHandler
from app.code.session.handlers.v1.session_logout_handler import SessionLogoutHandler
from app.code.session.handlers.v1.get_all_users_handler import GetAllUsersHandler

__all__ = ['session_routes']

session_routes = [SessionLoginHandler, SessionInfoHandler, SessionLogoutHandler, GetAllUsersHandler]

for route in session_routes:
    print(route.path)

    route.path = '/v1' + route.path
