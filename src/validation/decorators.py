from functools import wraps


def validator(*, name: str = None):
    """
    Marks a decorated function as a validator. It sets additional
    information about it.
    """

    def wrapper(func):
        func.__validator_name__ = name

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper
