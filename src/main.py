from typing import Callable

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.requests import Request

from config.settings import settings
from database.db import Base


DESCRIPTION = """
The service for receiving products from sellers in the excel format. It
is a solution for the test [task](https://github.com/avito-tech/mx-backend-trainee-assignment).
"""


def create_app():
    """
    The factory function. Returns a FastAPI application instance.
    """
    app = FastAPI(
        title="Text Searcher",
        description=DESCRIPTION,
        openapi_tags=[
            {
                "name": "Text documents",
                "description": "You can receive or delete them.",
            },
        ]
    )

    @app.middleware("http")
    def set_db_session(request: Request, call_next: Callable):
        """
        Sets the instance of Session class to the incoming request.
        """
        with Session() as session:
            request.state.session = session
            return call_next(request)

    @app.on_event('startup')
    def initialization():
        """
        Creates all necessary tables.
        """
        Base.metadata.create_all()

    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        factory=True
    )
