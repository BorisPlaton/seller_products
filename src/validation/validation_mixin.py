import inspect
from typing import Callable

from loguru import logger


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

    @logger.catch(ValueError)
    def validate(self):
        """
        Runs all validators that are specified in the validators attribute.
        """
        for validator in self.validators:
            validator(**self._get_validator_kwargs(validator))

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
