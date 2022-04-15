from app.code.session.handlers.v1 import session_routes
from app.code.socket.handlers.v1 import socket_routes
from app.code.note.handlers.v1 import note_routes

__all__ = ['all_routes']

all_routes = \
    [
        *session_routes,
        *socket_routes,
        *note_routes
    ]
