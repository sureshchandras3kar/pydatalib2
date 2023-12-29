from typing import Any


class PatternTypeNotFoundError(Exception):
    """
    Exception raised when a pattern type is not found.
    """

    def __init__(self, message="Pattern type not found."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidPatternTypeError(Exception):
    """
    Exception raised when a pattern type is invalid
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Pattern type is invalid."


class InvalidInputError(TypeError):
    """
    Custom error raised when received object is not a string as expected.
    """

    def __init__(self, input_data: Any) -> None:
        """
        Initialize the InvalidInputError instance.

        :param input_data: Any received object
        """
        if input_data is None:
            msg = 'No input provided'
        else:
            type_name = input_data.__class__.__name__
            msg = f'Expected "str", received "{type_name}"'
        super().__init__(msg)
