import sys
from typing import Callable

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from config.settings import settings
from database.db import SessionFactory
from products.views import router as products_router, products_tag


DESCRIPTION = """
The service for receiving products from sellers in the *Excel* format. It
is a solution for the test [task](https://github.com/avito-tech/mx-backend-trainee-assignment).
"""


def create_app():
    """
    The factory function. Returns a FastAPI application instance.
    """
    app = FastAPI(
        title="Seller products",
        description=DESCRIPTION,
        openapi_tags=[
            {
                'name': products_tag,
                'description': "Provides the *CRUD* operations for the sellers products."
            }
        ]
    )
    app.include_router(products_router)

    @app.on_event('startup')
    def initialize_logger():
        """
        Initializes a logger. Defines levels, handlers and a message
        format.
        """
        message_prefix = "[ {time:YYYY:MM:DD HH:mm:ss} | {level} | {name}.{function}:{line} ] "
        logger.remove(0)
        logger.add(
            settings.ERRORS_LOG_FILE, format=message_prefix + "{exception}", level='ERROR',
            filter=lambda x: x['level'].name == 'ERROR'
        )
        logger.add(
            settings.WARNINGS_LOG_FILE, format=message_prefix + "{message}", level='WARNING',
            filter=lambda x: x['level'].name == 'WARNING'
        )
        if settings.DEBUG:
            logger.add(sys.stdout, format=message_prefix + "{message}", level='DEBUG')

    @app.middleware("http")
    def set_db_session(request: Request, call_next: Callable):
        """
        Sets the instance of Session class to the incoming request. Commits
        all changes at the end of request and returns view's response.
        """
        with SessionFactory() as session:
            with session.begin():
                request.state.session = session
                res = call_next(request)
                return res

    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        factory=True
    )
