from typing import Callable

from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request


class ExceptionRouteHandler(APIRoute):
    """
    Overrides the default APIRoute for logging application internal exceptions.
    """

    def get_route_handler(self) -> Callable:
        handler = super().get_route_handler()

        async def log_decorated_handler(request: Request):
            with logger.catch(reraise=True):
                response = await handler(request)
                return response

        return log_decorated_handler
