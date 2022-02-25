from app.code.session.handlers.v1 import session_routes
from app.code.category.handlers.v1 import category_routes
from app.code.tag.handlers.v1 import tag_routes
from app.code.user.handlers.v1 import user_routes
from app.code.post.handlers.v1 import post_routes

__all__ = ['all_routes']

all_routes = \
    [
        *session_routes,
        *category_routes,
        *tag_routes,
        *user_routes,
        *post_routes
    ]
