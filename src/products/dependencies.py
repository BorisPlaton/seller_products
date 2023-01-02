from sqlalchemy.orm import Session
from starlette.requests import Request


def get_db_session(request: Request) -> Session:
    """
    Returns a SQLAlchemy Session object.
    """
    return request.state.session
