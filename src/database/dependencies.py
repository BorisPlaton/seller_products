from sqlalchemy.orm import Session

from database.db import SessionFactory


def get_db_session() -> Session:
    """
    Returns a SQLAlchemy Session object.
    """
    with SessionFactory() as session:
        with session.begin():
            yield session
