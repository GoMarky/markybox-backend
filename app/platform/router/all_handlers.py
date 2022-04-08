from app.code.session.handlers.v1 import session_routes
from app.code.socket.handlers.v1 import socket_routes

__all__ = ['all_routes']

all_routes = \
    [
        *session_routes,
        *socket_routes
    ]
