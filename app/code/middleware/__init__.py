from app.code.session.middleware.check_session_id_middleware import SessionIdMiddleware

__all__ = ['all_middlewares']

all_middlewares = [SessionIdMiddleware]
