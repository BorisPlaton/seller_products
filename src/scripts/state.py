from dataclasses import dataclass
from functools import wraps

from sqlalchemy.engine import Connection

from database.db import engine_factory


@dataclass
class State:
    """
    Represents some global vars that are accessible from the
    scripts.
    """
    connection: Connection = engine_factory().connect()


state = State()


def transaction(func):
    """
    Wraps the function into the transaction and closes connection
    after the function call.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        res = None
        with state.connection:
            with state.connection.begin():
                res = func(*args, **kwargs)
        return res

    return inner
