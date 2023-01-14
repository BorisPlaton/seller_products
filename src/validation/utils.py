from typing import Callable


def get_validator_name(validator: Callable):
    """
    Returns a validator's name. If it is wrapped by validator decorator,
    returns the value of '__validator_name__' attribute. Otherwise,
    '__name__' is returned.
    """
    validator_name = getattr(validator, '__validator_name__', None) or validator.__name__
    return str(validator_name)
