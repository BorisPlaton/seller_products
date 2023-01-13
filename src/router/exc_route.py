from typing import Callable

from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse


class ExceptionRouteHandler(APIRoute):
    """
    Overrides the default APIRoute for logging application internal exceptions.
    """

    def get_route_handler(self) -> Callable:
        handler = super().get_route_handler()

        async def log_decorated_handler(request: Request):
            response = None
            with logger.catch():
                response = await handler(request)
            return response or JSONResponse(
                {'detail': 'Internal error occurred when your request was processing.'},
                status_code=500
            )

        return log_decorated_handler
