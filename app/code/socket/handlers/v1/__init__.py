from app.code.socket.handlers.v1.subscribe_message_handler import SubscribeMessageHandler

__all__ = ['socket_routes']

socket_routes = [SubscribeMessageHandler]

for route in socket_routes:
    route.path = '/v1' + route.path
