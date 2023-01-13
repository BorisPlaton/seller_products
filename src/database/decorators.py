from functools import wraps

from database.db import SessionFactory


def session_transaction(func):
    """
    Wraps a function call into transaction.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        with SessionFactory() as session:
            with session.begin():
                res = func(*args, **kwargs)
                return res

    return inner
