from exceptions.base_exc import AppException


class ValidationException(AppException):
    """
    The exception is risen during validation process.
    """
