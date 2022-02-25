from .user_update_handler import UserUpdateHandler
from .user_create_handler import UserCreateHandler
from .user_get_all_handler import UserGetAllHandler
from .user_delete_handler import UserDeleteHandler

__all__ = ['user_routes']

user_routes = [UserGetAllHandler, UserDeleteHandler, UserCreateHandler, UserUpdateHandler]

for route in user_routes:
    route.path = '/v1' + route.path
