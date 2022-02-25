from app.code.session.handlers.v1 import session_routes

__all__ = ['all_routes']

all_routes = \
    [
        *session_routes,
    ]
