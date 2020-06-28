class SubscriptionException(Exception):
    """Parent exception for Subscription creation"""


class MissingFieldsException(SubscriptionException):
    """Raises when some fields in subscription are missed"""


class InvalidValueException(SubscriptionException):
    """Raises when taken subscription fields are invalid"""


class WrongTypeException(SubscriptionException):
    """Raises when wrong type of fields was found"""


class SubsNotFoundException(Exception):
    """Raises when the input subscription was not found"""
