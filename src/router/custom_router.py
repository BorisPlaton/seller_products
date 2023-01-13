from fastapi import APIRouter

from router.exc_route import ExceptionRouteHandler


class CustomAPIRouter(APIRouter):
    """
    Overrides default API router to set a custom API route
    class.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('route_class', ExceptionRouteHandler)
        super().__init__(*args, **kwargs)
