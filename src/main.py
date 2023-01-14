import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger

from config.settings import settings
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
            settings.DEBUG_LOG_FILE, format=message_prefix + "{message}", level='DEBUG',
            filter=lambda x: x['level'].name == 'DEBUG'
        )
        if settings.DEBUG:
            logger.add(sys.stdout, format=message_prefix + "{message}", level='DEBUG')

    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        factory=True
    )
