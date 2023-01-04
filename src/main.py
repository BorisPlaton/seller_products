from typing import Callable

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from config.settings import settings
from database.db import SessionLocal
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
                'description': "Represents the *CRUD* operations for the sellers products."
            }
        ]
    )
    app.include_router(products_router)

    @app.middleware("http")
    def set_db_session(request: Request, call_next: Callable):
        """
        Sets the instance of Session class to the incoming request. Commits
        all changes at the end of request and returns view's response.
        """
        with SessionLocal() as session:
            request.state.session = session
            res = call_next(request)
            session.commit()
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
