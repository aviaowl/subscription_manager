class MissingFieldsException(Exception):
    """Raises when some fields in subscription are missed"""


class WrongFrequencyException(Exception):
    """Raised when the input value is too small"""


class SubsNotFoundException(Exception):
    """Raises when the input subscription was not found"""


class InvalidSubsFieldException(Exception):
    """Raises when taken subscription is invalid"""
