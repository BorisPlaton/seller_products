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
        Runs all validators that are specified in the validators attribute.
        """
        for validator in self.validators:
            validator()
