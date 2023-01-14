from xlsx.exceptions import XLSXException
from validation.exceptions import ValidationException
from validation.mixin import ValidationMixin


class XLSXValidationMixin(ValidationMixin):
    """
    Overrides a base class validate method for rising an exception
    related to the xlsx exception.
    """

    def validate(self, **kwargs):
        """
        Raises `XLSXException` instead of `ValidationError`.
        """
        try:
            return super().validate(**kwargs)
        except ValidationException as e:
            raise XLSXException(str(e))
