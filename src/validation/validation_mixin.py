import inspect
from typing import Callable

from loguru import logger

from validation.exceptions import ValidationException


class ValidationMixin:
    """
    Additional validation that executes during parsing a *.xlsx file.
    """

    def __init__(self):
        """
        The descendant must redefine this list with validators that
        must be executed.
        """
        self.validators = []

    def validate(self):
        """
        Runs all validators that are specified in the validators attribute. Logs
        an exception if it was risen and reraise it.
        """
        for validator in self.validators:
            try:
                return validator(**self._get_validator_kwargs(validator))
            except ValidationException as e:
                logger.warning(str(e))
                raise e

    @property
    def common_validators_kwargs(self) -> dict:
        """
        Returns dictionary with arguments to be passed to the validators.
        """
        return {}

    def _get_validator_kwargs(self, validator: Callable) -> dict:
        """
        Returns dictionary with keyword arguments for the specific
        validator.
        """
        validator_params = inspect.signature(validator).parameters
        return {param: self.common_validators_kwargs[param] for param in validator_params}
