from app.code.socket.handlers.v1.subscribe_message_handler import SubscribeMessageHandler
from app.code.socket.handlers.v1.workspace_message_handler import WorkspaceMessageHandler

__all__ = ['socket_routes']

socket_routes = [SubscribeMessageHandler, WorkspaceMessageHandler]

for route in socket_routes:
    route.path = '/v1' + route.path
