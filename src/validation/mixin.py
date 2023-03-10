import inspect
from typing import Callable, Any

from validation.utils import get_validator_name


class ValidationMixin:
    """
    Additional validation that executes during parsing a *.xlsx file.
    """

    def __init__(self):
        """
        The descendant must redefine this list with validators that
        must be executed.
        """
        self.validators: list[Callable] = []
        self.validators_returns: dict[str, Any] = {}

    def validate(self, **kwargs):
        """
        Runs all validators that are specified in the validators attribute. If kwargs
        are passed, they update a dictionary from the `get_validators_kwargs` method.
        """
        general_kwargs = self.get_validators_kwargs()
        general_kwargs.update(kwargs)
        for validator in self.validators:
            validator_name = get_validator_name(validator)
            self.validators_returns[validator_name] = validator(
                **self._get_kwargs_for_specific_validator(validator, general_kwargs)
            )

    def get_validators_kwargs(self) -> dict:
        """
        Returns dictionary with arguments to be passed to the validators.
        """
        return {}

    @staticmethod
    def _get_kwargs_for_specific_validator(validator: Callable, general_kwargs: dict) -> dict:
        """
        Returns dictionary with keyword arguments for the specific
        validator.
        """
        validator_params = inspect.signature(validator).parameters
        return {param: general_kwargs[param] for param in validator_params}
